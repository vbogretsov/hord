import datasets
import json
import jwt
import os
import psycopg2
import pytest
import requests
import schema
import time

from requests_toolbelt import sessions


ENV = {
    "TEST_URL": {
        "name": "url",
        "required": True,
        "help": "Test server URL.",
        "schema": schema.Schema(str),
    },
    "TEST_DSN": {
        "name": "dsn",
        "required": True,
        "help": "Test database DSN.",
        "schema": schema.Schema(str),
        
    },
    "HASURA_GRAPHQL_JWT_SECRET": {
        "name": "jwt",
        "required": True,
        "help": "Hasura JWT token config, more details in the docs: https://hasura.io/docs/latest/graphql/core/deployment/graphql-engine-flags/reference.html",
        "schema": schema.Schema(schema.And(str, schema.Use(json.loads), schema.Schema({
            "key": schema.And(str),
            "type": schema.And(str),
            "claims_namespace": schema.And(str),
        }))),
    },
}


def session(base_url, token):
    s = sessions.BaseUrlSession(base_url=base_url)
    s.headers["Content-Type"] = "application/json; charset=utf-8"
    if token:
        s.headers["Authorization"] = f"Bearer {token}"
    return s


@pytest.fixture(scope="session")
def env():
    env = {}
    for name, meta in ENV.items():
        val = os.environ.get(name, None)
        if val is None and meta["required"]:
            pytest.exit(f"required environment variable is not set: {name}")
        try:
            env[meta["name"]] = meta["schema"].validate(val)
        except schema.SchemaError as e:
            pytest.exit(f"unable to parse environment variable {name}: {e}")
    return env


@pytest.fixture(scope="session")
def app(env):
    host = env["url"]

    n = 20
    while n > 0:
        try:
            resp = requests.get(f"{host}/healthz")
            if resp.status_code == 200:
                return host
        except:
            time.sleep(1)
            n -= 1

    if n == 0:
        pytest.exit(f"unable tp connect test server {host}")


@pytest.fixture(scope="session")
def seed(request, env, app):
    def exec(sql):
        conn = psycopg2.connect(env["dsn"])
        try:
            with conn:
                with conn.cursor() as curs:
                    curs.execute(sql)
        finally:
            conn.close()

    def to_sql(user):
        uid = user["id"]
        data = json.dumps(user["data"])
        roles = json.dumps(user["roles"])
        return f"('{uid}', '{data}', '{roles}')"

    vals = "\n,".join(to_sql(u) for u in datasets.USERS)
    exec(f"INSERT INTO users(id, data, roles) VALUES {vals};")

    def fin():
        exec("DELETE FROM users;")

    request.addfinalizer(fin)


@pytest.fixture(scope="session")
def issuer(env):
    return lambda token: jwt.encode(token, env["jwt"]["key"], env["jwt"]["type"])


@pytest.fixture(scope="session")
def admin(app, seed, issuer):
    return session(app, issuer(datasets.TOKENS["admin"]))


@pytest.fixture(scope="session")
def user(app, seed, issuer):
    return session(app, issuer(datasets.TOKENS["user"]))
