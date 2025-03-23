import flet as ft 
import flet.fastapi as flet_fastapi
from fastapi import Request, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
import os
import uvicorn
import json

from reservation_page import reservation_page
from home_page import home_page


app = flet_fastapi.FastAPI()

"""
@app.get('/reservation/{id}')
async def redirect(request: Request, id: str):
    (request.url)
    print(request.method)
    print('inside the api redirect')

    with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'reservations.json'), 'r') as _f:
        reservations = json.load(_f)
    _f.close()

    if str(id) in reservations.keys():
        return RedirectResponse(url=f'/reservation/{id}/return/')
    else:
        return RedirectResponse(url=f'/reservation/{id}/rental/')
"""

# Mount Flet for reservation
app.mount('/reservation/{id}/{action}', flet_fastapi.app(reservation_page, assets_dir=os.path.abspath('assets')), 'Reservation Page')
app.mount('/', flet_fastapi.app(home_page), 'Home Page')

if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0')