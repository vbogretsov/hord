CREATE TABLE IF NOT EXISTS public.users (
    id      varchar(32) not null primary key,
    data    jsonb not null,
    roles   jsonb not null
);

CREATE FUNCTION user_claims(user_row users)
RETURNS JSON AS $$
    SELECT row_to_json(r) FROM (
        SELECT
            roles as "x-hasura-allowed-roles",
            roles->0 as "x-hasura-default-role",
            id as "x-hasura-user-id"
        FROM users WHERE users.id = user_row.id
    ) r;
$$ LANGUAGE sql STABLE;
