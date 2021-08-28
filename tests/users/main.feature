Feature: Test user management service Hord

Background:
* url 'http://hord:8080/v1/graphql'
* def adminToken = jwtutil.encode(read('adminToken.json'));
* def userToken = jwtutil.encode(read('userToken.json'));

Scenario: Bulk insert users
  Given 
