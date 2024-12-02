from . import app
# debug
import logging
from .routes import (
    Clients,
    User
)

@app.get(
    "/"
)
async def main():
    return {"message": "Hello, World!"}


app.include_router(Clients.router)
app.include_router(User.router)
