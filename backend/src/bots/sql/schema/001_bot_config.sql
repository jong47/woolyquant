-- +goose Up
CREATE TABLE bot_config (
    id UUID PRIMARY KEY,
    created_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITHOUT TIME ZONE NOT NULL,
    name TEXT NOT NULL,  
    securities JSON NOT NULL
);

-- +goose Down
DROP TABLE bot_config;