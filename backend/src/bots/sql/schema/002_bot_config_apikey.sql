-- +goose Up
ALTER TABLE bot_config ADD COLUMN api_key VARCHAR(64) UNIQUE NOT NULL DEFAULT (
    encode(sha256(random()::text::bytea), 'hex')
);

-- +goose Down
ALTER TABLE bot_config DROP COLUMN api_key;