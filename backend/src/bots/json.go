package bots

import (
	"encoding/json"
	"log"
	"net/http"
)

func RespondWithError(w http.ResponseWriter, code int, message string) {
	if code > 499 {
		log.Println("500 Internal Server Error: " + message)
	}

	type errResponse struct {
		Error string `json:"error"`
	}

	RespondWithJSON(w, code, errResponse{Error: message})
}

func RespondWithJSON(w http.ResponseWriter, code int, payload interface{}) {
	var data []byte = nil
	var err error = nil

	data, err = json.Marshal(payload)
	if err != nil {
		w.WriteHeader(http.StatusInternalServerError)
		log.Printf("Error marshalling JSON: %s", err)
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	// Adds a response header to HTTP header signifying that the response body is JSON
	w.Header().Add("Content-Type", "application/json")
	w.WriteHeader(code)
	w.Write(data)
}
