import copy
import datasets
import http


GRAPHQL = "/v1/graphql"


def test_admin_read_user(admin):
    query = """
        query ($id: String!) {
            users_by_pk(id: $id) {
                id
                data
                roles
            }
        }
    """
    user = datasets.USERS[1]
    resp = admin.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": user["id"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "users_by_pk": user,
        },
    }


def test_admin_list_users(admin):
    query = """
        query ($roles: jsonb!) {
            users(where: {roles: {_contains: $roles}}, order_by: {id: asc}) {
                id
                data
                roles
            }
        }
    """
    resp = admin.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "roles": ["user"],
        }
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "users": [
                datasets.USERS[2],
                datasets.USERS[3],
            ]
        }
    }


def test_admin_create_user(admin):
    query = """
        mutation ($id: String!, $data: jsonb!, $roles: jsonb!) {
            insert_users_one(object: {id: $id, data: $data, roles: $roles}) {
                id
                data
                roles
            }
        }
    """
    user = datasets.NEW_ADMIN_1
    resp = admin.post(GRAPHQL, json={
        "query": query,
        "variables": {**user},
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "insert_users_one": user,
        },
    }

def test_admin_update_user(admin):
    query = """
        mutation ($id: String!, $data: jsonb!, $roles: jsonb!) {
            update_users_by_pk(pk_columns: {id: $id}, _set: {data: $data, roles: $roles}) {
                id
                data
                roles
            }
        }
    """
    updated = copy.deepcopy(datasets.NEW_ADMIN_1)
    updated["data"]["last_name"] = "Super Admin"
    updated["roles"] = ["admin", "roles"]
    resp = admin.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": updated["id"],
            "data": updated["data"],
            "roles": updated["roles"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "update_users_by_pk": {
                "id": updated["id"],
                "data": updated["data"],
                "roles": updated["roles"],
            },
        },
    }


def test_admin_delete_user(admin):
    query = """
        mutation ($id: String!) {
            delete_users_by_pk(id: $id) {
                id
            }
        }
    """
    user = datasets.NEW_ADMIN_1
    resp = admin.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": user["id"],
        }
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "delete_users_by_pk": {
                "id": user["id"],
            },
        },
    }


def test_rest_admin_read_claims(admin):
    user = datasets.USERS[1]
    resp =  admin.get("/api/rest/claims", params={"id": user["id"]})
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "users_by_pk": {
            "claims": {
                "x-hasura-allowed-roles": user["roles"],
                "x-hasura-default-role": user["roles"][0],
                "x-hasura-user-id": user["id"],
            },
        },
    }


def test_rest_admin_create_user_with_role(admin):
    user = datasets.NEW_ADMIN_2
    resp = admin.post("/api/rest/users", json=user)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "insert_users_one": {
            "id": user["id"],
            "data": user["data"],
            "roles": user["roles"],
        },
    }


def test_rest_admin_create_user_without_role(admin):
    user = datasets.NEW_USER_1
    resp = admin.post("/api/rest/users", json=user)
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "insert_users_one": {
            "id": user["id"],
            "data": user["data"],
            "roles": ["user"],
        },
    }


def test_user_can_view_self(user):
    query = """
        query ($id: String!) {
            users_by_pk (id: $id) {
                id
                data
            }
        }
    """
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": datasets.AUTHENTICATED_USER["id"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "users_by_pk": {
                "id": datasets.AUTHENTICATED_USER["id"],
                "data": datasets.AUTHENTICATED_USER["data"],
            },
        },
    }


def test_user_can_update_self_data(user):
    query = """
        mutation ($id: String!, $data: jsonb!) {
            update_users_by_pk(pk_columns: {id: $id}, _set: {data: $data}) {
                id
                data
            }
        }
    """
    updated = copy.deepcopy(datasets.AUTHENTICATED_USER)
    updated["data"]["last_name"] = "Super Dragon"
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": updated["id"],
            "data": updated["data"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "update_users_by_pk": {
                "id": updated["id"],
                "data": updated["data"],
            },
        },
    }


def test_user_can_not_update_self_roles(user):
    query = """
        mutation ($id: String!, $roles: jsonb!) {
            update_users_by_pk(pk_columns: {id: $id}, _set: {roles: $roles}) {
                id
            }
        }
    """
    updated = copy.deepcopy(datasets.AUTHENTICATED_USER)
    updated["roles"] = ["admin"]
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": updated["id"],
            "roles": updated["roles"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert "errors" in resp.json()


def test_user_can_not_update_other(user):
    query = """
        mutation ($id: String!, $data: jsonb!) {
            update_users_by_pk(pk_columns: {id: $id}, _set: {data: $data}) {
                id
                data
            }
        }
    """
    updated = copy.deepcopy(datasets.AUTHENTICATED_ADMIN)
    updated["data"]["last_name"] = "Super Dragon"
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": updated["id"],
            "data": updated["data"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert resp.json() == {
        "data": {
            "update_users_by_pk": None,
        },
    }


def test_user_can_not_create_user(user):
    query = """
        mutation ($id: String!, $data: jsonb!, $roles: jsonb!) {
            insert_users_one(object: {id: $id, data: $data, roles: $roles}) {
                id
                data
                roles
            }
        }
    """
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {**datasets.NEW_USER_2, "roles": ["admin"]},
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert "errors" in resp.json()


def test_user_can_not_read_other(user):
    query = """
        query ($id: String!) {
            users_by_pk(id: $id) {
                id
                data
                roles
            }
        }
    """
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "id": datasets.AUTHENTICATED_ADMIN["id"],
        },
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert "errors" in resp.json()


def test_user_can_not_list_others(user):
    query = """
        query ($roles: jsonb!) {
            users(where: {roles: {_contains: $roles}}, order_by: {id: asc}) {
                id
                data
                roles
            }
        }
    """
    resp = user.post(GRAPHQL, json={
        "query": query,
        "variables": {
            "roles": ["user"],
        }
    })
    assert resp.status_code == http.HTTPStatus.OK
    assert "errors" in resp.json()
