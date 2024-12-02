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
from fastapi.responses import HTMLResponse, RedirectResponse
from pydantic import BaseModel
from .database.User import (
    UserDB
)
from .routes.User import (
    verify
)
from .models.User import (
    UserInDb,
    User as UserDto
)

templates = Jinja2Templates(directory="app/templates")

@app.post(
    "/",
    response_class=HTMLResponse
)
async def login(
    username: str = Form(...),
    password: str = Form(...),
):
    '''
        This is the main route of the application
        Returns:

    '''

    user = await verify(
        UserInDb(
            username=username,
            password=password
        )
    )
    print(user)

    return RedirectResponse(
        url=f"/user?username={username}&role={user.role}",
        status_code=303
    )

@app.get(
    "/user",
    response_class=HTMLResponse
)
async def main(
    request: Request,
    username: str = None,
    role: str = None
):
    '''
        This is the main route of the application

        Returns:
    '''    
    user = UserDto(
        username=username,
        role=role
    )


    return templates.TemplateResponse(
        request=request,
        name="user.html",  
        context={"request": request, "user": user}
    )


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
