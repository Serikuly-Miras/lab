-- Tables
CREATE TABLE IF NOT EXISTS public.users (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL UNIQUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.shops (
    id          SERIAL PRIMARY KEY,
    name        TEXT NOT NULL,
    city        TEXT NOT NULL,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS public.orders (
    id          SERIAL PRIMARY KEY,
    user_id     INT NOT NULL REFERENCES public.users(id),
    shop_id     INT NOT NULL REFERENCES public.shops(id),
    amount      NUMERIC(10, 2) NOT NULL,
    status      TEXT NOT NULL DEFAULT 'pending',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- Enable logical replication for all three tables
ALTER TABLE public.users  REPLICA IDENTITY FULL;
ALTER TABLE public.shops  REPLICA IDENTITY FULL;
ALTER TABLE public.orders REPLICA IDENTITY FULL;

-- Debezium signals table (used to trigger ad-hoc incremental snapshots)
CREATE TABLE IF NOT EXISTS public.debezium_signals (
    id      VARCHAR(42) PRIMARY KEY,
    type    VARCHAR(32) NOT NULL,
    data    VARCHAR(2048)
);

-- Publication for Debezium (must be created by superuser)
CREATE PUBLICATION debezium_pub FOR ALL TABLES;

-- Seed users
INSERT INTO public.users (name, email) SELECT
    'User ' || i,
    'user' || i || '@example.com'
FROM generate_series(1, 10) i;

-- Seed shops
INSERT INTO public.shops (name, city) SELECT
    'Shop ' || i,
    (ARRAY['New York','London','Berlin','Tokyo','Paris','Sydney','Dubai','Toronto','Singapore','Amsterdam'])[i]
FROM generate_series(1, 10) i;

-- Seed 1000 random orders
INSERT INTO public.orders (user_id, shop_id, amount, status, created_at) SELECT
    (random() * 9 + 1)::INT,
    (random() * 9 + 1)::INT,
    round((random() * 990 + 10)::NUMERIC, 2),
    (ARRAY['pending','paid','shipped','cancelled'])[(random() * 3 + 1)::INT],
    now() - (random() * INTERVAL '90 days')
FROM generate_series(1, 1000);