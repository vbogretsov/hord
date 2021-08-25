Feature: Test user management service Hord

Background:
* url 'http://hord:8080/v1/graphql'
* json jwt = java.lang.System.getenv('HASURA_GRAPHQL_JWT_SECRET');
* def jwtutil = read('classpath:jwtutil.js');
* def adminToken = 'xxx';
* def userToken = 'yyy';

Scenario: Print JWT key
  * print adminToken
  * print userToken
  * print karate.properties
