from fastapi import FastAPI




app = FastAPI(
    title="TicketFlow API",
    version="1.0.0",
)

@app.get("/")
async def root():
    return {"message": "TicketFlow API is running"}

