__author__ = 'Tymoteusz Paul'
from graph import Graph, Node, SimpleDimensions

import logging

import settings

from celery import Celery
from celery.contrib.methods import task

service_logger = logging.getLogger('service_logger')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(settings.logging_format)
service_logger.addHandler(stream_handler)

app = Celery(broker='amqp://guest@localhost//',
             backend='redis://localhost')

class GraphService:
    def __init__(self, hypothesis_kind=SimpleDimensions.HYPOTHESIS,
                 observation_kind=SimpleDimensions.OBSERVATION):
        self.graph = Graph(hypothesis_kind, observation_kind)
        self.nodes = {}

    @task()
    def update_node(self, uid, kind, **kwargs) -> bool:
        if kind is not str:
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
        raise NotImplementedError

    @task()
    def get_nodes(self) -> dict:
        return self.nodes

    @task()
    def get_nodes_from_graph(self, dimension) -> set:
        raise NotImplementedError

    @task()
    def get_graph_printout(self) -> str:
        return str(self.graph)

if __name__ == '__main__':
    pass
