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
    Then we should receive new node details back
    And they should match with "<kind>", "<uid>", "<date>" and "<name>"

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
    Given a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    When we try to connect result "<result>" with a given "<assumption>" and set weight to "<weight>"
    Then we should receive None response
    """
    Connecting nodes either crashes or returns nothing, very retro, but it really should return something
    """

      Examples:
        | result      | assumption  | weight  |
        | first_obs   | first_hypo  | 0.1     |
        | first_obs   | second_hypo | 0.2     |
        | second_obs  | second_hypo | 0.3     |


  @graph-service
  @dev-only
  Scenario: Retrieving empty set of nodes
    Given that we try to retrieve nodes for non-existing dimension "Phnglui"
    Then we should receive an empty set


  @graph-service
  @dev-only
  Scenario Outline: Retrieving sets of nodes
    Given a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    When when we try to retrieve nodes for dimension "<dimension>"
    Then count of elements returned should be "<set_count>"

      Examples:
        | dimension   | set_count |
        | observation | 2         |
        | hypothesis  | 2         |


  @graph-service
  @dev-only
  Scenario: Retrieving printout for all nodes and their connections
    Given a set of nodes present in the service
      | kind        | uid   | date      | name        | code_name   |
      | observation | 1     | 20150110  |             | first_obs   |
      | observation | 2     | 20150115  |             | second_obs  |
      | hypothesis  | 3     |           | impossible  | first_hypo  |
      | hypothesis  | 4     |           | possible    | second_hypo |
    When we retrieve string representation of nodes and their connections
    Then it should match match the representational string
    """
    "hypothesis\tconnections\n'2'\t<=\t '2' (observation) \n\t<=\t '1' (observation) \n'1'\t<=\t '1' (observation) \n"
    """