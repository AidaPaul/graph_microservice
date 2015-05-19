from behave import *
import settings
import requests

use_step_matcher("re")


@when('we try to "(?P<method>.+)" "(?P<uri>.+)"')
def step_impl(context, method, uri):
    """
    :type context behave.runner.Context
    :type method str
    :type uri str
    """
    url = "%s%s" % (settings.rest_prefix, uri)
    if method == 'GET':
        context.response = requests.get(url)
    elif method == 'POST':
        context.response = requests.post(url)
    else:
        assert False


@then('the response code should be "(?P<code>\d+)"')
def step_impl(context, code):
    """
    :type context behave.runner.Context
    :type code int
    """
    assert context.response.status_code == int(code)
