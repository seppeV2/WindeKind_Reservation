import flet as ft
import uvicorn
import flet.fastapi as flet_fastapi
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from html import get_html
from home_view import get_home_view
from utilities import get_reservations, get_materials, get_type, get_measurements
import os

app = flet_fastapi.FastAPI()



@app.get('/25403b32-2720-4e16-a651-f53fdf83e99c')
def return_video():
    square_size = min(0.85*page.width, 0.55 * page.height)
    return HTMLResponse(get_html(page.endpoint, square_size))

@app.post('/25403b32-2720-4e16-a651-f53fdf83e99c/in')
async def store_qr_code(request: Request):
    
    body = await request.body()
    code = body.decode('utf-8')

    if code not in page.views[-1].controls[-1].data:
        try:
            material_info = page.material_catalog[code]
            page.views[-1].controls[-1].controls.insert(
                0,
                ft.Container(
                    content = ft.ListTile(
                        title= ft.Text(f'{material_info["type"]} \t\t Material ID : {code}'),
                        subtitle= ft.Text(f'{material_info["brand"]}')
                    ),
                    border=ft.border.all(2, page.sizes['shape_color']),
                    border_radius=5, 
                    margin=ft.Margin(left = page.sizes['entry_margin'], right=page.sizes['entry_margin'], top = 5, bottom = 5)
                )
            )
            page.views[-1].controls[-1].data.append(code)

            page.update()
        except KeyError:
            pass


def main(_page: ft.Page):
    global page
    page = _page
    page.endpoint = page.url.replace('wss://', 'https://').replace('ws://', 'http://')
    page.theme_mode= ft.ThemeMode.LIGHT
    page.material_catalog = get_materials()
    page.sizes = get_measurements(get_type(page))

    page.views.append(
        get_home_view(page)
    )

    page.update()

app.mount('/', flet_fastapi.app(main, assets_dir=os.path.abspath('assets'), ))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')