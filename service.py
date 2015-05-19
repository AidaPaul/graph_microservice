__author__ = 'Tymoteusz Paul'
from graph import Graph, Node, SimpleDimensions

import logging
import pickle
import settings
import redis

from celery import Celery
from celery.contrib.methods import task

service_logger = logging.getLogger('service_logger')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(settings.logging_format)
service_logger.addHandler(stream_handler)

app = Celery(broker='amqp://guest@localhost//',
             backend='redis://localhost')


class GraphService:
    def __init__(self):
        redis_connection = redis.StrictRedis(**settings.redis_server)
        if 'graph' in redis_connection:
            self.graph = pickle.loads(redis_connection.get('graph'))
        else:
            self.graph = self.get_new_graph()
        if 'nodes' in redis_connection:
            self.nodes = pickle.loads(redis_connection.get('graph'))
        else:
            self.nodes = self.get_new_nodes()

    def __del__(self):
        redis_connection = redis.StrictRedis(**settings.redis_server)
        redis_connection.set('graph', pickle.dumps(self.graph))
        redis_connection.set('nodes', pickle.dumps(self.nodes))

    @staticmethod
    def get_new_graph() -> Graph:
        return Graph(SimpleDimensions.HYPOTHESIS, SimpleDimensions.OBSERVATION)

    @staticmethod
    def get_new_nodes() -> dict:
        return {}

    @task()
    def update_node(self, uid, kind, **kwargs) -> bool:
        if type(kind) is not str:
            return False
        elif kind == 'hypothesis':
            kind = SimpleDimensions.HYPOTHESIS
        elif kind == 'observation':
            kind = SimpleDimensions.OBSERVATION
        else:
            return False

        try:
            self.nodes[uid] = Node(uid, kind, **kwargs)
            return True
        except AttributeError:
            return False

    @task()
    def connect_nodes(self, result, assumption, relationship=None) -> bool:
        try:
            self.graph.connect(self.nodes[result], self.nodes[assumption],
                               relationship)
            return True
        except NameError:
            return False

    @task()
    def get_nodes(self) -> dict:
        return self.nodes

    @task()
    def get_nodes_from_graph(self, dimension) -> set:
        return self.graph.nodes(dimension)

    @task()
    def get_graph_printout(self) -> str:
        return str(self.graph)

if __name__ == '__main__':
    pass
