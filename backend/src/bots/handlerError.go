package bots

import (
	"net/http"
)

func HandlerErr(w http.ResponseWriter, r *http.Request) {
	RespondWithError(w, http.StatusInternalServerError, "An error occurred")
}
