import flet as ft
from utilities import get_camera_web_view, pop_view, get_reservations, overwrite_reservations
from datetime import datetime

def go_to_reservation_out(page: ft.Page):

    page.views.append(
        ft.View(
            route = '/reservationOut',
            appbar= ft.AppBar(
                leading= ft.IconButton(
                    icon=ft.Icons.ARROW_BACK_IOS,
                    icon_color=ft.Colors.BLACK, 
                    icon_size=page.sizes['main_button_icon_size'],
                    on_click=lambda _: pop_view(page)
                    ),
                title=ft.Text("Windekind rental out", size=page.sizes['appbar_text_size'],weight=page.sizes['appbar_font_weight']),
                center_title=True,
                bgcolor=ft.Colors.GREEN_200

            ),
            controls=[
                ft.Row(
                    controls = [
                        ft.Row(
                            controls = [
                                contactPerson := ft.TextField(label= 'Contact Person', width=page.sizes['text_field_width_contact'], text_size=page.sizes['normal'], label_style=ft.TextStyle(size = page.sizes['normal'])),
                                hoursInput := ft.TextField(label= 'Duration',width=page.sizes['text_field_width_duration'], text_size=page.sizes['normal'], label_style=ft.TextStyle(size = page.sizes['normal']))
                            ]
                        ),
                        ft.TextButton(
                            text = 'Confirm', 
                            icon=ft.Icons.CHECK, 
                            on_click = lambda _: submit_reservations(page, hoursInput.value, contactPerson.value)
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_EVENLY
                ),
                get_camera_web_view(page, page.endpoint, debug=False),
                ft.ListView(
                    data=[],
                    expand=True
                )
            ],
            horizontal_alignment= ft.CrossAxisAlignment.CENTER
        ),
    
    )

    page.update()


def submit_reservations(page, hoursInput, contactPerson):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    duration = hoursInput

    reservations = get_reservations()
    for id in page.views[-1].controls[-1].data:
        reservations[id] = {
            "timestamp": now, 
            "duration": str(duration),
            "contact_person" : contactPerson
        }

    overwrite_reservations(reservations)

    page.views[-1].controls[-1].data.clear()
    page.views[-1].controls[-1].controls.clear()
    pop_view(page, refresh = True)
