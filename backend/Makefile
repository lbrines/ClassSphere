.PHONY: run test tidy lint coverage

run:
	go run ./cmd/api

test:
	go test ./...

coverage:
	go test ./... -coverprofile=coverage.out
	go tool cover -func=coverage.out

lint:
	golangci-lint run

tidy:
	go mod tidy
