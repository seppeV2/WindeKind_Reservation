import flet as ft
from utilities import get_camera_web_view, pop_view, get_reservations, overwrite_reservations
from datetime import datetime

def go_to_reservation_in(page: ft.Page):

    page.views.append(
        ft.View(
            route = '/reservationIn',
            appbar= ft.AppBar(
                leading= ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS,
                    on_click=lambda _: pop_view(page)
                    ),
                title=ft.Text("Windekind rental in", size=40),
                center_title=True
            ),
            controls=[
                ft.TextButton(
                    text = "Confirm", 
                    icon = ft.Icons.CHECK,
                    on_click= lambda _: submit_receival(page)
                ),
                get_camera_web_view(page, page.endpoint, debug=False),
                ft.ListView(
                    data = []
                )
            ], 
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
    )

    page.update()


def submit_receival(page):
    reservations = get_reservations()
    for id in page.views[-1].controls[-1].data:
        reservations.pop(id)

    overwrite_reservations(reservations)
    
    page.views[-1].controls[-1].data.clear()
    page.views[-1].controls[-1].controls.clear()
    pop_view(page, refresh = True)