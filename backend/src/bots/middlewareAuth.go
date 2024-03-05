package bots

import (
	"bots/internal/auth"
	"bots/internal/database"
	"fmt"
	"net/http"
)

type authedHandler func(http.ResponseWriter, *http.Request, database.BotConfig)

func (cfg *apiConfig) MiddlewareAuth(handler authedHandler) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		apiKey, err := auth.GetAPIKey(r.Header)
		if err != nil {
			RespondWithError(w, http.StatusForbidden, fmt.Sprintf("client-side auth error, unable to get bot without valid api key: %v", err))
			return
		}

		// Most important thing we can do with contexts is to cancel them, since Go allows us to track context states
		// This checks if the API key exists on our database
		bot, err := cfg.DB.GetBotByAPIKey(r.Context(), apiKey)
		if err != nil {
			RespondWithError(w, http.StatusNotFound, fmt.Sprintf("server-side error, bot id not found, %v", err))
			return
		}

		// Pass back arguments so golang can return the anonymous function
		handler(w, r, bot)
	}
}
