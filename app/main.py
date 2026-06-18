from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.users import router as users_router


app = FastAPI(
    title="TicketFlow API",
    version="1.0.0",
)

app.include_router(auth_router)
app.include_router(users_router)


