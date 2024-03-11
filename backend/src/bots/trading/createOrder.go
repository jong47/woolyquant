package trading

import (
	"fmt"
	"io"
	"main/internal/database"
	"net/http"
	"strings"
)

type BotConf func(http.ResponseWriter, *http.Request, database.BotConfig)

func CreateSellOrder(bot BotConf) *http.Response {
	url := "https://paper-api.alpaca.markets/v2/orders"

	payload := strings.NewReader("{\"side\":\"sell\",\"type\":\"market\",\"time_in_force\":\"day\"}")

	req, _ := http.NewRequest("POST", url, payload)
	req.Header.Add("accept", "application/json")
	req.Header.Add("content-type", "application/json")

	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)
	fmt.Println(string(body))
	return res
}

func CreateBuyOrder() {
	url := "https://paper-api.alpaca.markets/v2/orders"

	payload := strings.NewReader("{\"side\":\"buy\",\"type\":\"market\",\"time_in_force\":\"day\"}")

	req, _ := http.NewRequest("POST", url, payload)
	req.Header.Add("accept", "application/json")
	req.Header.Add("content-type", "application/json")

	res, _ := http.DefaultClient.Do(req)
	defer res.Body.Close()

	body, _ := io.ReadAll(res.Body)
	fmt.Println(string(body))
}
