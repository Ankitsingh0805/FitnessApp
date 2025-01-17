from src.main import app

@app.get("/api/logs")
async def get_logs():

    return {"message": "Log system is under development"}

@app.get("/api/status")
async def get_status():

    return {"status": "API is running"}

