-- Gold-layer star schema. Compatible conceptually with Fabric Warehouse,
-- Snowflake, Databricks SQL, or SQL Server with minor type adjustments.

CREATE TABLE dim_customer (
    customer_key INTEGER NOT NULL,
    customer_id VARCHAR(30) NOT NULL,
    customer_segment VARCHAR(50) NOT NULL,
    state VARCHAR(2) NOT NULL,
    created_date DATE NOT NULL,
    CONSTRAINT pk_dim_customer PRIMARY KEY (customer_key),
    CONSTRAINT uq_dim_customer_id UNIQUE (customer_id)
);

CREATE TABLE dim_account (
    account_key INTEGER NOT NULL,
    account_id VARCHAR(30) NOT NULL,
    customer_key INTEGER NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    status VARCHAR(20) NOT NULL,
    opened_date DATE NOT NULL,
    CONSTRAINT pk_dim_account PRIMARY KEY (account_key),
    CONSTRAINT uq_dim_account_id UNIQUE (account_id),
    CONSTRAINT fk_account_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

CREATE TABLE fact_transaction (
    transaction_key BIGINT NOT NULL,
    event_id VARCHAR(40) NOT NULL,
    account_key INTEGER NOT NULL,
    customer_key INTEGER NOT NULL,
    event_date DATE NOT NULL,
    event_type VARCHAR(20) NOT NULL,
    channel VARCHAR(20) NOT NULL,
    amount DECIMAL(18, 2) NOT NULL,
    signed_amount DECIMAL(18, 2) NOT NULL,
    is_exception BOOLEAN NOT NULL,
    CONSTRAINT pk_fact_transaction PRIMARY KEY (transaction_key),
    CONSTRAINT uq_fact_event_id UNIQUE (event_id),
    CONSTRAINT fk_fact_account FOREIGN KEY (account_key) REFERENCES dim_account(account_key),
    CONSTRAINT fk_fact_customer FOREIGN KEY (customer_key) REFERENCES dim_customer(customer_key)
);

