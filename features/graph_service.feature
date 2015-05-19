# Created by Tymoteusz Paul at 16/5/2015
Feature: Operating on graphs as service
  Testing functionality of graphs when accessed via service api.


  Background: We are connected to graph service
    Given that we are working with clear graph service
    When we attempt to connect to graph service backend
    Then we should be succesfull


  @graph-service
  @dev-only
  Scenario Outline: Creating nodes
    Given that we try to create a "<kind>" node with "<uid>", "<date>" and "<name>"
    Then we should receive positive response

    Examples: Observations
      | kind        | uid   | date      | name        |
      | observation | 1     | 20150110  |             |
      | observation | 2     | 20150115  |             |

    Examples: Hypothesis
      | kind        | uid   | date      | name        |
      | hypothesis  | 3     |           | impossible  |
      | hypothesis  | 4     |           | possible    |


  @graph-service
  @dev-only
  Scenario Outline: Connecting nodes
    Given that we are working with clear graph service
    And a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    When we try to connect result "<result>" with a given "<assumption>" and set weight to "<weight>"
    Then we should be dandy

      Examples:
        | result      | assumption  | weight  |
        | 1   | 3  | 0.1     |
        | 1   | 4 | 0.2     |
        | 2  | 4 | 0.3     |


  @graph-service
  @dev-only
  Scenario: Retrieving empty set of nodes
    Given that we try to retrieve nodes for non-existing dimension "Phnglui"
    Then we should receive an empty set


  @graph-service
  @dev-only
  Scenario Outline: Retrieving sets of nodes
    Given that we are working with clear graph service
    And a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    And list of connections between nodes
      | result      | assumption  | weight  |
      | 1   | 3  | 0.1     |
      | 1   | 4 | 0.2     |
      | 2  | 4 | 0.3     |
    When when we try to retrieve nodes for dimension "<dimension>"
    Then count of elements returned should be "<set_count>"

      Examples:
        | dimension   | set_count |
        | observation | 2         |
        | hypothesis  | 2         |


  """
  Test disabled due to the fact that stringifying function is,
  in essence, untestable. Would have to be overhauled.

  @graph-service
  @dev-only
  Scenario: Retrieving printout for all nodes and their connections
    Given a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    And list of connections between nodes
      | result      | assumption  | weight  |
      | 1   | 3  | 0.1     |
      | 1   | 4 | 0.2     |
      | 2  | 4 | 0.3     |
    When we retrieve string representation of nodes and their connections
    Then it should match match the representational string
    """
    """
    hypothesis  connections
    '2' <=   '2' (observation)
      <=   '1' (observation)
    '1' <=   '1' (observation)

    """