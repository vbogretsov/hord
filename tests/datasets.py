import time


USERS = [
    {
        "id": "1000000",
        "data": {
            "first_name": "Don",
            "last_name": "Knuth",
        },
        "roles": [
            "admin"
        ],
    },
    {
        "id": "1000001",
        "data": {
            "first_name": "Sergey",
            "last_name": "lebedev",
        },
        "roles": [
            "admin",
        ],
    },
    {
        "id": "1000002",
        "data": {
            "first_name": "Ken",
            "last_name": "Thompson",
        },
        "roles": [
            "user",
        ],
    },
    {
        "id": "1000003",
        "data": {
            "first_name": "Dennis",
            "last_name": "Ritchie",
        },
        "roles": [
            "user",
        ],
    },
]

NEW_ADMIN_1 = {
    "id": "1000010",
    "data": {
        "first_name": "Adi",
        "last_name": "Shamir",
    },
    "roles": [
        "admin",
    ],
}

NEW_ADMIN_2 = {
    "id": "1000011",
    "data": {
        "first_name": "Ronald",
        "last_name": "Rivest",
    },
    "roles": [
        "admin",
    ],
}

NEW_USER_1 = {
    "id": "1000021",
    "data": {
        "first_name": "Alfred",
        "last_name": "Aho",
    },
}

NEW_USER_2 = {
    "id": "1000022",
    "data": {
        "first_name": "Bon",
        "last_name": "Scott",
    },
}

AUTHENTICATED_ADMIN = USERS[0]
AUTHENTICATED_USER = USERS[2]

TOKENS = {
    "admin": {
        "sub": AUTHENTICATED_ADMIN["id"],
        "iss": "www.test.org",
        "iat": int(time.time()),
        "claims": {
            "roles": AUTHENTICATED_ADMIN["roles"],
            "x-hasura-allowed-roles": AUTHENTICATED_ADMIN["roles"],
            "x-hasura-default-role": AUTHENTICATED_ADMIN["roles"][0],
            "x-hasura-user-id": AUTHENTICATED_ADMIN["id"],
        },
    },
    "user": {
        "sub": AUTHENTICATED_USER["id"],
        "iss": "www.test.org",
        "iat": int(time.time()),
        "claims": {
            "roles": AUTHENTICATED_USER["roles"],
            "x-hasura-allowed-roles": AUTHENTICATED_USER["roles"],
            "x-hasura-default-role": AUTHENTICATED_USER["roles"][0],
            "x-hasura-user-id": AUTHENTICATED_USER["id"],
        },
    },
}
