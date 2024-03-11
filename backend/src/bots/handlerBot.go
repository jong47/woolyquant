package main

import (
	"encoding/json"
	"fmt"
	"main/common"
	"main/internal/database"
	"net/http"
	"time"

	"github.com/google/uuid"
)

func (apiConf *apiConfig) HandlerCreateBot(w http.ResponseWriter, r *http.Request) {
	type parameters struct {
		Name       string `json:"name"`
		Securities []struct {
			Stock string  `json:"stock"`
			Qty   uint32  `json:"qty"`
			Price float64 `json:"price"`
		} `json:"securities"`
	}

	decoder := json.NewDecoder(r.Body)
	params := parameters{}
	err := decoder.Decode(&params)

	defer r.Body.Close()

	if err != nil {
		RespondWithError(w, http.StatusBadRequest, fmt.Sprintf("Client-side error, Invalid JSON:", err))
		return
	}

	buf, _ := json.Marshal(params.Securities)
	testBot, err := apiConf.Queries.CreateBot(r.Context(), database.CreateBotParams{
		ID:         uuid.New(),
		CreatedAt:  time.Now().UTC(),
		UpdatedAt:  time.Now().UTC(),
		Name:       params.Name,
		Securities: buf,
	})

	if err != nil {
		RespondWithError(w, http.StatusInternalServerError, fmt.Sprintf("Server-side error with creating bot: %v", err))
		return
	}

	RespondWithJSON(w, http.StatusCreated, common.DatabaseCreateBotToBot(testBot))
}

// HandlerGetBotByAPIKey returns the bot with the given API key
// This essentially acts as a "login" endpoint for bots
// It is used to authenticate the bot and get the bot's ID
// The bot's ID is then used to make other requests
// This is essentially a middleware router and will allow for other requests to be made
func (apiConf *apiConfig) HandlerGetBotByAPIKey(w http.ResponseWriter, r *http.Request, bot database.BotConfig) {
	RespondWithJSON(w, http.StatusOK, common.DatabaseCreateBotToBot(bot))
}
