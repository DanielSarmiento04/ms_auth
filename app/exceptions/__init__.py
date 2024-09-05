from .. import app
from fastapi import Request
from fastapi.responses import JSONResponse
from colorama import Fore


class NoFoundException(Exception):
    """
        Class used to raise a no use found user in the database
    """
    def __init__(self, user_id : str, context: str):
        self.user_id = user_id
        self.context = context
        # super().__init__(self.user_id, self.context)

@app.exception_handler(NoFoundException)
async def no_found_exception_handler(request: Request, exc: NoFoundException):
    print(Fore.LIGHTCYAN_EX, f"No found exception {exc.user_id} - {exc.context}", Fore.RESET)
    return JSONResponse(
        status_code=404,
        content={"detail": f"{exc.context} no found - {exc.user_id}"},
        headers={"Content-Type": "application/json"},
    )

