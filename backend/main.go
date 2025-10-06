package main

import (
	"github.com/labstack/echo/v4"
	"github.com/labstack/echo/v4/middleware"
)

func main() {
	e := echo.New()
	e.Use(middleware.Logger())
	e.Use(middleware.Recover())

	e.GET("/", handleWelcome)
	e.GET("/health", handleHealth)
	e.Logger.Fatal(e.Start(":8080"))
}

func handleWelcome(c echo.Context) error {
	return c.JSON(200, map[string]string{
		"message": "ClassSphere API",
		"version": "1.0.0",
	})
}

func handleHealth(c echo.Context) error {
	return c.JSON(200, map[string]string{"status": "healthy"})
}

func setupTestApp() *echo.Echo {
	e := echo.New()
	e.GET("/", handleWelcome)
	e.GET("/health", handleHealth)
	return e
}