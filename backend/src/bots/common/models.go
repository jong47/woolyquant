package common

import (
	"main/internal/database"
	"time"

	"github.com/google/uuid"
)

type CreateBotParams struct {
	ID         uuid.UUID `json:"id"`
	CreatedAt  time.Time `json:"created_at"`
	UpdatedAt  time.Time `json:"updated_at"`
	Name       string    `json:"name"`
	Securities []byte    `json:"securities"`
	ApiKey     string    `json:"api_key"`
}

func DatabaseCreateBotToBot(botConfig database.BotConfig) CreateBotParams {
	return CreateBotParams{
		ID:         botConfig.ID,
		CreatedAt:  botConfig.CreatedAt,
		UpdatedAt:  botConfig.UpdatedAt,
		Name:       botConfig.Name,
		Securities: botConfig.Securities,
		ApiKey:     botConfig.ApiKey,
	}
}
