from . import app
# debug
import logging



@app.get(
    "/get"
)
async def main():
    return {"message": "Hello, World!"}