package main

import (
	"main/internal/database"
	"time"

	"github.com/google/uuid"
)

type CreateBotParams struct {
	ID         uuid.UUID `jsozn:"id" db:"id" validate:"required"`
	CreatedAt  time.Time `json:"created_at" db:"created_at" validate:"required"`
	UpdatedAt  time.Time `json:"updated_at" db:"updated_at" validate:"required"`
	Name       string    `json:"name" db:"name" validate:"required"`
	Securities []byte    `json:"securities" db:"securities" validate:"required"`
}

func databaseCreateBotToBot(botConfig database.BotConfig) CreateBotParams {
	return CreateBotParams{
		ID:         botConfig.ID,
		CreatedAt:  botConfig.CreatedAt,
		UpdatedAt:  botConfig.UpdatedAt,
		Name:       botConfig.Name,
		Securities: botConfig.Securities,
	}
}
