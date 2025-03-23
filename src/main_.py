import flet as ft
import cv2
import base64
import uvicorn
import flet.fastapi as flet_fastapi
import time
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
from html import get_html

app = flet_fastapi.FastAPI()


@app.get('/video')
def return_video():
    global endpoint
    return HTMLResponse(get_html(endpoint))

@app.post('/qr_receive')
async def store_qr_code(request: Request):
    print('request received')
    body = await request.body()
    print(body.decode('utf-8'))


def main(page: ft.Page):
    global endpoint

    ph = ft.PermissionHandler()
    page.overlay.append(ph)
    def grant_camera_permission():
        permission_type = ft.PermissionType.CAMERA
        print(ph.check_permission(permission_type))
        ph.request_permission(permission_type)
        print(ph.check_permission(permission_type))

    endpoint = page.url.replace('ws://', 'http://')
    webview = ft.WebView(
        url = f"{endpoint}/video",
        enable_javascript=True,
        expand=True
    )

    page.views.append(
        ft.View(
            controls = [
                ft.Text("this is the main page"),
                ft.TextButton("start video stream", on_click=lambda _: grant_camera_permission()),
                webview
            ]
        )
    )

    page.update()

app.mount('/', flet_fastapi.app(main))

if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0')