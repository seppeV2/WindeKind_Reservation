import flet as ft
from reservation_in import go_to_reservation_in
from reservation_out import go_to_reservation_out
from utilities import get_reservations, is_late_return, get_materials, get_end_time
from datetime import datetime

def get_home_view(page: ft.Page):


    return ft.View(
        route='/',
        appbar= ft.AppBar(
            leading = ft.Text(),
            title=ft.Text("Windekind material rental management", size=40),
            center_title=True
        ),
        controls=[
            ft.Container(
                content = ft.Divider(
                    height = 7, 
                    color = ft.Colors.WHITE),
                    margin = 20
                

            ),
            ft.Row(
                controls=[
                    ft.TextButton(
                        text = 'Material OUT  ', 
                        icon= ft.Icons.ARROW_UPWARD, 
                        on_click=lambda _: go_to_reservation_out(page),
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size = 40, color=ft.Colors.WHITE),
                            icon_size=50,
                            side = ft.BorderSide(color = ft.Colors.WHITE, width = 2),
                            padding=10,
                            shape = ft.RoundedRectangleBorder(5)
                            
                        ),
                        
                        
                    ), 
                    ft.TextButton(
                        text = 'Material IN  ', 
                        icon= ft.Icons.ARROW_DOWNWARD, 
                        on_click=lambda _: go_to_reservation_in(page),
                        style=ft.ButtonStyle(
                            text_style=ft.TextStyle(size = 40, color=ft.Colors.WHITE),
                            icon_size=50,
                            side = ft.BorderSide(color = ft.Colors.WHITE, width = 2),
                            padding=10,
                            shape = ft.RoundedRectangleBorder(5)
                            
                        ),
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_EVENLY
            ), 
            ft.Container(
                content = ft.Divider(
                    height = 7, 
                    color = ft.Colors.WHITE),
                    margin = 20
                

            ),
            ft.Text(f"Currently {len(get_reservations())} pieces rented out", color = ft.Colors.WHITE, size = 20),
            get_current_reservation_list()
        ]
    )

def get_current_reservation_list():
    reservation_dict = get_reservations()


    return ft.ListView(
        controls = [
            reservation_list_tile(material_id, reservation_dict[str(material_id)]) for material_id in reservation_dict.keys()
        ],
    )

class reservation_list_tile(ft.Container):

    def __init__(self, material_id: str, reservation_properties : dict):
        self.material_id = material_id

        is_late, minutes_late = is_late_return(reservation_properties['timestamp'], reservation_properties['duration'])
        self.is_late = is_late
        self.minutes_late = minutes_late if not is_late else round(minutes_late)
        self.end_time = get_end_time(reservation_properties['timestamp'], reservation_properties['duration'])
        self.contactperson = reservation_properties["contact_person"]

        self.color = ft.Colors.RED if is_late else ft.Colors.GREEN
        self.trailing = ft.Text(f'{self.minutes_late} minutes late', color=self.color, size = 20) if is_late else ft.Text()

        material_properties = get_materials(self.material_id)
        self.brand = material_properties['brand']
        self.type = material_properties['type']

        super().__init__(
            content = ft.ListTile( 
                title=ft.Row(
                    controls = [
                        ft.Text(f'{self.brand} {self.type}', color=self.color, size=25),
                        ft.Text(f'({self.material_id})', color=self.color, size=18),
                    ]
                    ),
                subtitle=ft.Column(
                    controls = [
                        ft.Text(f'Contact person: {self.contactperson}', color=self.color, size = 20),
                        ft.Text(f'Rented until: {self.end_time}', color=self.color, size = 18),
                    ]
                ),
                trailing=self.trailing,
                shape = ft.RoundedRectangleBorder(5),
                
            ),
            border=ft.border.all(5, self.color),
            border_radius=15,
            margin=ft.margin.all(10)

        )