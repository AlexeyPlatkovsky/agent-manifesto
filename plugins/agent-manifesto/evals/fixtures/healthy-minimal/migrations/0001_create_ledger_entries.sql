-- reversible: see 0001_create_ledger_entries.down.sql
CREATE TABLE ledger_entries (
    id          BIGSERIAL PRIMARY KEY,
    booked_at   TIMESTAMPTZ NOT NULL
);
