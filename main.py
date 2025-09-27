if __name__ == "__main__":
    from uvicorn import run

    run("infrastructure.server:app", reload=True, port=5000, host="0.0.0.0")
