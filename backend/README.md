# Backend for Wooly Quant
This backend is written in 100% Golang. It primarily uses the in-built net/http library with chi router and chi cors. 

# Dependencies
- [Chi Router](https://github.com/go-chi/chi/v5)
- [Chi Cors](https://github.com/go-chi/cors)
- [Godot Env](https://github.com/joho/godotenv)

This backend also uses [sqlc](https://docs.sqlc.dev/en/latest/overview/install.html) for type-safe SQL code and [goose](https://github.com/pressly/goose) for database migrations.

