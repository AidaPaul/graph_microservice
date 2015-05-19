# Created by Tymoteusz Paul at 19/5/2015
Feature: REST entry point for graphs
  Brief tests for the REST entry point just to make sure that methods exist
  and do not crash on us. Logic behind them is already well tested in
  graph_service.feature

  Scenario Outline: Making sure that GET calls exist
    When we try to "GET" "<uri>"
    Then the response code should be "200"

    Examples:
      | uri                           |
      | /nodes                        |
      | /nodes_from_graph/hypothesis  |
      | /graph_printout               |


  Scenario Outline: Making sure that POST calls exist
    When we try to "POST" "<uri>"
    Then the response code should be "400"
    """
    We want it to be 400 as we are sending empty posts
    """

    Examples:
      | uri           |
      | /nodes        |
      | /connections  |



