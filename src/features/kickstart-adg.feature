@aws-kickstart-adg
@test
Feature: Kickstart adg process, to source data and valid final tables for expected outcome

  @fixture.s3.clear.kickstart.start
  @fixture.terminate.kickstart.cluster
  Scenario: Kickstart adg end to end test for vacancy, application data with delta extract
    Given The template file 'record_template.json' as an input
    And Generate '10' records per table for 'vacancy' with PII flag as 'False' and upload to s3 bucket
    And Generate '10' records per table for 'application' with PII flag as 'True' and upload to s3 bucket
    When Start kickstart adg emr process for modules 'vacancy, application' with 'delta' extract and get step ids
    And  Add validation steps 'vacancy-hive-validation-queries' to kickstart adg emr cluster for 'vacancy' with 'delta' extract and add step Ids to the list
    And  Add validation steps 'vacancy-hive-validation-queries' to kickstart adg emr cluster for 'vacancy' with 'incremental' extract and add step Ids to the list
    And  Add validation steps 'application-hive-validation-queries' to kickstart adg emr cluster for 'application' with 'delta' extract and add step Ids to the list
    Then Wait for all the steps to complete
    And The input result matches with final output for module 'vacancy' with 'delta' extract
    And The input result matches with final output for module 'vacancy' with 'incremental' extract
    And The input result matches with final output for module 'application' with 'delta' extract

