__author__ = 'Tymoteusz Paul'
from graph import Graph, Node, SimpleDimensions

from thrift.transport import TSocket, TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

import logging

import settings

service_logger = logging.getLogger('service_logger')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(settings.logging_format)
service_logger.addHandler(stream_handler)


class GraphService:
    def __init__(self, hypothesis_kind=SimpleDimensions.HYPOTHESIS,
                 observation_kind=SimpleDimensions.OBSERVATION):
        self.graph = Graph(hypothesis_kind, observation_kind)
        self.nodes = {}

    def update_node(self, uid, kind, **kwargs) -> bool:
        try:
            self.nodes[uid] = Node(uid, kind, **kwargs)
            return True
        except AttributeError:
            return False

    def connect_nodes(self, result, assumption, relationship=None) -> bool:
        raise NotImplementedError

    def get_nodes(self) -> dict:
        return self.nodes

    def get_nodes_from_graph(self, dimension) -> set:
        raise NotImplementedError

    def get_graph_printout(self) -> str:
        return str(self.graph)

if __name__ == '__main__':
    pass
