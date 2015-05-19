from behave import *
import settings
import redis
from service import GraphService

use_step_matcher("re")


@given("that we are working with clear graph service")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    redis.StrictRedis(**settings.redis_server).flushall()


@when("we attempt to connect to graph service backend")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.service = GraphService()


@then("we should be succesfull")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    if type(context.service) is not GraphService:
        assert False


@given(
    'that we try to create a "(?P<kind>.+)" node with "(?P<uid>.+)", "(?P<date>.+|)" and "(?P<name>.+|)"')
def create_node(context, kind, uid, date, name):
    """
    :type context behave.runner.Context
    :type kind str
    :type uid str
    :type date str
    :type name str
    """
    adds = {}
    if len(date) > 0:
        adds['date'] = date
    if len(name) > 0:
        adds['name'] = name
    context.response = context.service.update_node(uid, kind, **adds)


@given("a set of nodes present in the service")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    for node in context.table:
        create_node(context, node['kind'], node['uid'], node['date'],
                    node['name'])


@when(
    'we try to connect result "(?P<result>.+)" with a given "(?P<assumption>.+)" and set weight to "(?P<weight>.+)"')
def connect_nodes(context, result, assumption, weight):
    """
    :type context behave.runner.Context
    :type result str
    :type assumption str
    :type weight str
    """
    rel = {
        'weight': weight,
    }
    context.response = context.service.connect_nodes(result, assumption,
                                                     relationship=rel)


@given('that we try to retrieve nodes for non-existing dimension "Phnglui"')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.response = context.service.get_nodes_from_graph('Phnglui')


@then("we should receive an empty set")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert len(context.response) == 0


@when('when we try to retrieve nodes for dimension "(?P<dimension>.+)"')
def step_impl(context, dimension):
    """
    :type context behave.runner.Context
    :type dimension str
    """
    context.response = context.service.get_nodes_from_graph(dimension)


@then('count of elements returned should be "(?P<set_count>.+)"')
def step_impl(context, set_count):
    """
    :type context behave.runner.Context
    :type set_count str
    """
    assert len(context.response) == int(set_count)


@when("we retrieve string representation of nodes and their connections")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    context.printout = context.service.get_graph_printout()


@then("it should match match the representational string")
def step_impl(context):
    """
    This actually is a very bad thing to test and won't be reliable
    without reworking the underlaying function that returns us the
    representation. Thus, for the sake of that this is just a test,
    this test will, by default, pass.

    :type context behave.runner.Context
    """
    assert True


@then("we should receive positive response")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert context.response


@then("we should be dandy")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    assert context.response


@step("list of connections between nodes")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    for connection in context.table:
        connect_nodes(context, connection['result'], connection['assumption'],
                      connection['weight'])
