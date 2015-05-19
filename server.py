__author__ = 'Tymoteusz Paul'

from bottle import post, request, get, run, HTTPError
import settings
from service import GraphService

@get('/nodes')
def get_nodes():
    return GraphService().get_nodes()

@get('/nodes_from_graph/<dimension>')
def get_nodes_from_graph(dimension):
    return GraphService().get_nodes_from_graph(dimension)

@get('/graph_printout')
def get_grph_printout():
    return GraphService().get_graph_printout()

@post('/nodes')
def post_nodes():
    if 'uid' in request.forms and 'kind' in request.forms:
        if GraphService().update_node(**request.forms):
            return {'success': True}
    raise HTTPError(400)

@post('/connections')
def post_connections():
    if 'result' in request.forms and 'assumption' in request.forms:
        if GraphService().connect_nodes(**request.forms):
            return {'success': True}
    raise HTTPError(400)

if __name__ == '__main__':
    run(**settings.bottle_server)
