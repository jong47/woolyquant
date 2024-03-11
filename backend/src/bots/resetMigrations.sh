cd sql/schema
goose postgres postgres://postgres:postgres@localhost:5432/postgres down 
goose postgres postgres://postgres:postgres@localhost:5432/postgres down 
goose postgres postgres://postgres:postgres@localhost:5432/postgres up 
goose postgres postgres://postgres:postgres@localhost:5432/postgres up
cd ../..
sqlc generate
echo "Database reset and sqlc generated"