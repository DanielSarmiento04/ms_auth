from . import app
# debug
import logging
from .routes import Clients


@app.get(
    "/get"
)
async def main():
    return {"message": "Hello, World!"}


app.include_router(Clients.router)