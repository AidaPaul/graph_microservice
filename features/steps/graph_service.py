from behave import *

use_step_matcher("re")


@given("that we are working with clear graph service")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@when("we attempt to connect to graph service backend")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then("we should be succesfull")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@given('that we try to create a "(?P<kind>.+)" node with "(?P<uid>.+)", "(?P<date>.+|)" and "(?P<name>.+|)"')
def step_impl(context, kind, uid, date, name):
    """
    :type context behave.runner.Context
    :type kind str
    :type uid str
    :type date str
    :type name str
    """
    pass


@then("we should receive new node details back")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@step('they should match with "(?P<kind>.+)", "(?P<uid>.+)", "(?P<date>.+|)" and "(?P<name>.+|)"')
def step_impl(context, kind, uid, date, name):
    """
    :type context behave.runner.Context
    :type kind str
    :type uid str
    :type date str
    :type name str
    """
    pass


@given("a set of nodes present in the service")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@when('we try to connect result "(?P<result>.+)" with a given "(?P<assumption>.+)" and set weight to "(?P<weight>.+)"')
def step_impl(context, result, assumption, weight):
    """
    :type context behave.runner.Context
    :type result str
    :type assumption str
    :type weight str
    """
    pass


@then("we should receive None response")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@given('that we try to retrieve nodes for non-existing dimension "Phnglui"')
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then("we should receive an empty set")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@when('when we try to retrieve nodes for dimension "(?P<dimension>.+)"')
def step_impl(context, dimension):
    """
    :type context behave.runner.Context
    :type dimension str
    """
    pass


@then('count of elements returned should be "(?P<set_count>.+)"')
def step_impl(context, set_count):
    """
    :type context behave.runner.Context
    :type set_count str
    """
    pass


@when("we retrieve string representation of nodes and their connections")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then("it should match match the representational string")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass


@then("we should receive positive response")
def step_impl(context):
    """
    :type context behave.runner.Context
    """
    pass