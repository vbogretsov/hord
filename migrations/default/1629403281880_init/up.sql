CREATE TABLE IF NOT EXISTS public.users (
    id      varchar(32) not null primary key,
    data    jsonb not null,
    claims  jsonb not null
);
