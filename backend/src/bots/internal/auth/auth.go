package auth

// This package contains the authentication logic for the bot service.
// It is responsible for creating and retrieving bots from the database.
// It also contains the logic for authenticating bots.

import (
	"errors"
	"net/http"
	"strings"
)

// getAPIKey extracts the Api key from the request headers and returns it as a string.
// Authorization format: <ApiKey> {Insert Api key here}
func getAPIKey(headers http.Header) (string, error) {
	var auth_key string = headers.Get("Authorization")
	if auth_key == "" {
		return "", errors.New("no api key provided")
	}

	var master_key []string = strings.Split(auth_key, " ")
	if len(master_key) != 2 {
		return "", errors.New("auth header is malformed, please include valid api key")
	}

	if master_key[0] != "ApiKey" {
		return "", errors.New("first part of auth header is malformed, please include valid api key")
	}

	return master_key[1], nil
}
