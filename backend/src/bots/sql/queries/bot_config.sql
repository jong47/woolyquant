-- name: CreateBot :one
INSERT INTO bot_config (id, created_at, updated_at, name, securities, api_key) 
VALUES ($1, $2, $3, $4, $5,
    encode(sha256(random()::text::bytea), 'hex')
) 
RETURNING *;

-- name: GetBotByAPIKey :one
SELECT * FROM bot_config WHERE api_key = $1;
