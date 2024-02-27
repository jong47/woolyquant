package main

import (
	"encoding/json"
	"fmt"
	"main/internal/auth"
	"main/internal/database"
	"net/http"
	"time"

	"github.com/google/uuid"
)

func (apiConf *apiConfig) handlerCreateBot(w http.ResponseWriter, r *http.Request) {
	type parameters struct {
		Name string `json:"name" validate:"required"`
	}

	decoder := json.NewDecoder(r.Body)
	params := parameters{}
	err := decoder.Decode(&params)

	if err != nil {
		respondWithError(w, http.StatusBadRequest, fmt.Sprintf("Client-side error, Invalid JSON:", err))
		return
	}

	testBot, err := apiConf.DB.CreateBot(r.Context(), database.CreateBotParams{
		ID:         uuid.New(),
		CreatedAt:  time.Now().UTC(),
		UpdatedAt:  time.Now().UTC(),
		Name:       params.Name,
		Securities: []byte(`{,	"securities": [	{			"symbol": "AAPL",			"quantity": 10		},		{			"symbol": "GOOGL",			"quantity": 5		}	]}`),
	})

	if err != nil {
		respondWithError(w, http.StatusInternalServerError, fmt.Sprintf("Server-side error with creating bot: %v", err))
		return
	}

	respondWithJSON(w, http.StatusCreated, databaseCreateBotToBot(testBot))
}

// handlerGetBotByAPIKey returns the bot with the given API key
// This essentially acts as a "login" endpoint for bots
// It is used to authenticate the bot and get the bot's ID
// The bot's ID is then used to make other requests
// This is essentially a middleware router and will allow for other requests to be made
func (apiConf *apiConfig) handlerGetBotByAPIKey(w http.ResponseWriter, r *http.Request) {
	apiKey, err := auth.GetAPIKey(r.Header)
	if err != nil {
		respondWithError(w, http.StatusForbidden, fmt.Sprintf("Client-side error, Invalid API key: %v", err))
		return
	}

	// Most important thing we can do with contexts is to cancel them, since Go allows us to track context states
	bot, err := apiConf.DB.GetBotByAPIKey(r.Context(), apiKey)
	if err != nil {
		respondWithError(w, http.StatusNotFound, fmt.Sprintf("Server-side error, Bot not found: %v", err))
		return
	}

	respondWithJSON(w, http.StatusOK, databaseCreateBotToBot(bot))
}
