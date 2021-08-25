import datetime
import json
import jwt
import pytest
import requests
import os
import time


HASURA_DOCS = "https://hasura.io/docs/latest/graphql/core/deployment/graphql-engine-flags/reference.html HASURA_GRAPHQL_JWT_SECRET"

USERS = [
    {
        "id": "100000000",
        "data": {
            "first_name": "Don",
            "last_name": "Knuth",
        },
        "claims": {
            "hasura": {
                "x-hasura-allowed-roles": ["admin"],
                "x-hasura-default-role": ["admin"],
            }
        }
    },
    {
        "id": "100000001",
        "data": {
            "first_name": "Ken",
            "last_name": "Thompson",
        },
        "claims": {
            "hasura": {
                "x-hasura-allowed-roles": ["admin"],
                "x-hasura-default-role": ["admin"],
            }
        }
    },
    {
        "id": "100000002",
        "data": {
            "first_name": "Dennis",
            "last_name": "Ritchie",
        },
        "claims": {
            "hasura": {
                "x-hasura-allowed-roles": ["user"],
                "x-hasura-default-role": ["user"],
            }
        }
    },
    {
        "id": "100000003",
        "data": {
            "first_name": "Rob",
            "last_name": "Pike",
        },
        "claims": {
            "hasura": {
                "x-hasura-allowed-roles": ["user"],
                "x-hasura-default-role": ["user"],
            }
        }
    },
]


def ensure_prop(conf, name):
    if not conf.get(name, None):
        raise ValueError(f"missing property {name} in jwt config, see {HASURA_DOCS} for more details")


def env(name):
    v = os.getenv(name, None)
    if not v:
        raise ValueError(f"environment variable {name} is not set")
    return v


def session(token):
    s = requests.Session()
    s.headers["Content-Type"] = "application/json; charset=utf-8"
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


@pytest.fixture(scope="session")
def issue():
    conf = json.loads(env("HASURA_GRAPHQL_JWT_SECRET"))
    ensure_prop(conf, "key")
    ensure_prop(conf, "type")
    ensure_prop(conf, "claims_namespace")

    def fn(sub, role):
        return jwt.encode(
            {
                "iss": "https://example.org",
                "iat": int(time.time()),
                "sub": sub,
                conf["claims_namespace"]: {
                    "x-hasura-allowed-roles": [role],
                    "x-hasura-default-role": role,
                },
            },
            conf["key"],
            conf["type"],
        )

    return fn


@pytest.fixture(scope="session")
def admin_token(issue):
    return issue("admin@example.org", "admin")


@pytest.fixture(scope="session")
def user_token(issue):
    return issue("user@example.org", "user")


@pytest.fixture(scope="session")
def admin(admin_token):
    return session(admin_token)


@pytest.fixture(scope="session")
def user(user_token):
    return session(user_token)


@pytest.fixture(scope="session")
def guest():
    return session(None)


@pytest.fixture(scope="session")
def endpoint(admin):
    retry = 10
    host = env("HASURA_GRAPHQL_ENDPOINT")

    query = """
    mutation CreateUsers {{
        insert_users(objects: {0})
    }}
    """.format(USERS)

    while retry > 0:
        resp = admin.post(f"{host}/v1/graphql", json={"query": query})
        if resp.status_code == 200:
            return host

        time.sleep(1)
        retry -= 1

    raise ValueError(f"endpoint {host} is unreachable")


@pytest.fixture
def user_1():
    return {
        "id": "123456",
        "data": {
            "first_name": "Adi",
            "last_name": "Shamir",
        },
    }
