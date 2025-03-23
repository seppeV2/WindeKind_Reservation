import flet as ft
import json
import os
import datetime

async def reservation_page(page: ft.Page):
    print(page.url)
    rt = ft.TemplateRoute(page.url)
    if rt.match(':prefix//:domain/reservation/:material_id/:action'):
        material_id = str(rt.material_id)
        try:
            with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'material.json'), 'r') as _f:
                material_catalog = json.load(_f)
            _f.close()
            reservation_page = ReservationPage(material_id, material_catalog[material_id], rt.action)
            reservation_page.create_content(page)

        except KeyError:
            url_not_found_page = UrlNotFoundPage(page.url)
            url_not_found_page.create_content(page)


class ReservationPage(ft.Container):

    def __init__(self, id: str, material_properties: dict, action: str):
        self.id = id
        self.material_properties = material_properties
        self.action = action
        super().__init__()

    def create_content(self, page):
        if self.action == 'rental': 
            page.views.clear()
            page.views.append(
                ft.View(
                    appbar= ft.AppBar(
                        leading=ft.Text(), 
                        title = ft.Text('Register a new rental'),
                        center_title=True
                    ),
                    controls=[
                        ft.Text(f'Material properties:\n\tBrand: {self.material_properties['brand']}\n\tType: {self.material_properties['type']}'), 
                        ft.Divider(height = 3),
                        ft.Text('Enter the durtion of the rental'),
                        textinput := ft.TextField(label = 'enter a duration'),
                        ft.TextButton('Submit', on_click= lambda _: self.add_rental(textinput.value, page))
                    ],
                )
            )
            page.update()
        elif self.action == 'return':

            with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'reservations.json'), 'r') as _f:
                reservations = json.load(_f)
            _f.close()

            rental_properties = reservations[self.id]

            rental_time = datetime.datetime.strptime(rental_properties['timestamp'], "%Y-%m-%d %H:%M:%S")
            planned_duration = float(rental_properties['duration'])
            real_duration = (datetime.datetime.now() - rental_time).seconds/60

            late = real_duration > planned_duration

            if late: minutes_over = round(real_duration - planned_duration*60)

            content = ft.Text('Received in time', size=20, color =ft.Colors.GREEN) if not late else ft.Text(f'Received to late\n{minutes_over} minutes over', size = 20, color=ft.Colors.RED)
            page.views.clear()
            page.views.append(
                ft.View(
                    appbar= ft.AppBar(
                        leading=ft.Text(), 
                        title = ft.Text('Return of a rental'),
                        center_title=True
                    ),
                    controls=[
                        ft.Text(f'Material properties:\n\tBrand: {self.material_properties['brand']}\n\tType: {self.material_properties['type']}'), 
                        ft.Divider(height = 3),
                        content,
                        ft.TextButton('Remove reservation', on_click= lambda _: self.remove_rental(page, reservations))
                    ],
                )
            )
            page.update()


            

    def remove_rental(self, page, reservations):
        reservations.pop(self.id)
        with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'reservations.json'), 'w') as _f:
                json.dump(reservations, _f)
        _f.close()
        page.views[-1].controls = [
            ft.Text('Removed', size = 40)
        ]

        page.update()
        

    def add_rental(self, duration, page):
        with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'reservations.json'), 'r') as _f:
            reservations = json.load(_f)
        _f.close()

        reservations[self.id] = {
            "timestamp" : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "duration" : duration
        }

        with open(os.path.join(os.path.dirname(__file__), 'assets', 'data', 'reservations.json'), 'w') as _f:
            json.dump(reservations, _f)
        _f.close()

        page.views[-1].controls = [
            ft.Text('Submitted', size = 40)
        ]

        page.update()


class UrlNotFoundPage(ft.Container):
    def __init__(self, socket_path: str):
        super().__init__()
        self.socket_path = socket_path


    def create_content(self, page):
        page.views.clear()
        page.views.append(
            ft.View(
                controls=[
                    ft.Text(f'404 Page not found for socket {self.socket_path}')
                ],
            )
        )

        page.update()