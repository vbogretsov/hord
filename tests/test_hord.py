def test_admin_create_user(request, endpoint, admin, user_1):
    def fin():
        query = "mutation {{ delete_users_by_pk(id: {0}) {{ id }} }}".format(user_1["id"])
        admin.post(f"{endpoint}/v1/graphql", json={"query": query})

    request.addfinalizer(fin)

    resp = admin.post(f"{endpoint}/api/rest/users", json=user_1)
    assert resp.status_code == 200


def test_admin_get_claims(endpoint, admin, user_1):
    resp = admin.get(f"{endpoint}/api/rest/claims", params={"id": user_1["id"]})
    assert resp.status_code == 200
    assert resp.json() == {"users_by_pk": {"hasura": {""}}}