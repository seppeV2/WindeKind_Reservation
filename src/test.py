import flet as ft 
import flet.fastapi as flet_fastapi
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles

import uvicorn

from reservation_page import reservation_page
from home_page import home_page


app = flet_fastapi.FastAPI()

# Mount Flet for reservation
app.mount('/reservation/{id}', flet_fastapi.app(reservation_page), 'Reservation Page')
app.mount('/', flet_fastapi.app(home_page), 'Home Page')

if __name__ == "__main__":
    uvicorn.run('test:app', host='0.0.0.0')