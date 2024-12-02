from . import app
# debug
from fastapi import Request
import logging
from .routes import (
    Clients,
    User
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


templates = Jinja2Templates(directory="app/templates")


@app.get(
    "/",
    response_class=HTMLResponse
)
async def main(request: Request):
    '''
        This is the main route of the application

        Returns:
    '''
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


app.include_router(Clients.router)
app.include_router(User.router)
