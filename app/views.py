from . import app
# debug
from fastapi import (
    Request,
    Form,
)
import logging
from .routes import (
    Clients,
    User
)
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from .database.User import (
    UserDB
)
from .routes.User import (
    verify
)
from .models.User import (
    UserInDb
)

templates = Jinja2Templates(directory="app/templates")

@app.post(
    "/",
)
async def login(
    username: str = Form(...),
    password: str = Form(...),
    # req: Request
):
    '''
        This is the main route of the application
        Returns:

    '''

    print(username, password)

    user = await verify(
        UserInDb(
            username=username,
            password=password
        )
    )
    print(user)

    return "200"


@app.get(
    "/",
    response_class=HTMLResponse
)
async def main(
    request: Request
):
    '''
        This is the main route of the application

        Returns:
    '''

    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )

@app.get(
    "/register",
    response_class=HTMLResponse
)
async def main(
    request: Request
):
    '''
        This is the main route of the application

        Returns:
    '''

    return templates.TemplateResponse(
        request=request,
        name="register.html",
    )


app.include_router(Clients.router)
app.include_router(User.router)
