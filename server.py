__author__ = 'Tymoteusz Paul'

from bottle import post, request, get, run, HTTPError
import settings
import pickle
from base64 import b64encode
from service import GraphService

@get('/nodes')
def get_nodes():
    return {'nodes': b64encode(pickle.dumps(GraphService().get_nodes.delay().get())).decode('utf-8')}

@get('/nodes_from_graph/<dimension>')
def get_nodes_from_graph(dimension):
    return {'nodes':  b64encode(pickle.dumps(GraphService().get_nodes_from_graph.delay(dimension).get())).decode('utf-8')}

@get('/graph_printout')
def get_grph_printout():
    return {'printout': GraphService().get_graph_printout.delay().get()}

@post('/nodes')
def post_nodes():
    if 'uid' in request.forms and 'kind' in request.forms:
        if GraphService().update_node.delay(**request.forms).get():
            return {'success': True}
    raise HTTPError(400)

@post('/connections')
def post_connections():
    if 'result' in request.forms and 'assumption' in request.forms:
        if GraphService().connect_nodes.delay(**request.forms).get():
            return {'success': True}
    raise HTTPError(400)

if __name__ == '__main__':
    run(**settings.bottle_server)
