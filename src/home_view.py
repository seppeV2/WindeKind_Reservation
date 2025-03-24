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
            title=ft.Text("Windekind material rental management", size=page.sizes['appbar_text_size'], weight=page.sizes['appbar_font_weight']),
            center_title=True,
            bgcolor=ft.Colors.GREEN_200
        ),
        controls=[
            ft.Column(
                controls = [
                    ft.Container(
                        content = ft.Row(
                            controls=[
                                ft.TextButton(
                                    text = 'Material OUT  ', 
                                    icon= ft.Icons.ARROW_UPWARD, 
                                    on_click=lambda _: go_to_reservation_out(page),
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size = page.sizes['main_button'], color=page.sizes['shape_color']),
                                        icon_size=page.sizes['main_button_icon_size'],
                                        side = ft.BorderSide(color = page.sizes['shape_color'], width = 2),
                                        padding=10,
                                        shape = ft.RoundedRectangleBorder(5),
                                        icon_color=ft.Colors.BLACK,
                                        color=ft.Colors.BLACK
                                    ),

                                    
                                ), 
                                ft.TextButton(
                                    text = 'Material IN  ', 
                                    icon= ft.Icons.ARROW_DOWNWARD, 
                                    on_click=lambda _: go_to_reservation_in(page),
                                    style=ft.ButtonStyle(
                                        text_style=ft.TextStyle(size = page.sizes['main_button'], color=page.sizes['shape_color']),
                                        icon_size=page.sizes['main_button_icon_size'],
                                        side = ft.BorderSide(color = page.sizes['shape_color'], width = 2),
                                        padding=10,
                                        shape = ft.RoundedRectangleBorder(5),
                                        icon_color=ft.Colors.BLACK,
                                        color=ft.Colors.BLACK
                                        
                                    ),
                                )
                            ],
                            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                        ), 
                    margin=ft.Margin(top = page.sizes['button_margin_top'], bottom = 0, left = 0, right = 0)
                    ),
                    
                    ft.Container(
                        content = ft.Divider(
                            height = 7, 
                            color = page.sizes['shape_color']),
                            margin = page.sizes['devider_margin']

                    ),
                    ft.Text(f"Currently {len(get_reservations())} pieces rented out", color = ft.Colors.BLACK, size = page.sizes['subheader']),
                    get_current_reservation_list(page)
                ],
                scroll=ft.ScrollMode.ALWAYS,
                expand=True
            )
            
        ]
    )

def get_current_reservation_list(page):
    reservation_dict = get_reservations()


    return ft.ListView(
        controls = [
            reservation_list_tile(material_id, reservation_dict[str(material_id)], page) for material_id in reservation_dict.keys()
        ],
    )

class reservation_list_tile(ft.Container):

    def __init__(self, material_id: str, reservation_properties : dict, page : ft.Page):
        self.material_id = material_id

        is_late, minutes_late = is_late_return(reservation_properties['timestamp'], reservation_properties['duration'])
        self.is_late = is_late
        self.minutes_late = minutes_late if not is_late else round(minutes_late)
        self.end_time = get_end_time(reservation_properties['timestamp'], reservation_properties['duration'])
        self.contactperson = reservation_properties["contact_person"]

        self.color = ft.Colors.RED if is_late else ft.Colors.GREEN
        self.trailing = ft.Column(
            controls = [
                ft.Text(f'Until: {self.end_time}', color=self.color, size = page.sizes['subheader']),
                ft.Text(f'({self.minutes_late} min late)', color=self.color, size = page.sizes['normal'])  
            ]
        ) if is_late else ft.Column(
            controls = [
                ft.Text(f'Until: {self.end_time}', color=self.color, size = page.sizes['subheader']),
                ft.Text()  
            ]
        )

        material_properties = get_materials(self.material_id)
        self.brand = material_properties['brand']
        self.type = material_properties['type']

        super().__init__(
            content = ft.ListTile( 
                title=ft.Row(
                    controls = [
                        ft.Text(f'{self.brand} {self.type}', color=self.color, size=page.sizes['header']),
                        ft.Text(f'({self.material_id})', color=self.color, size=page.sizes['normal']),
                    ]
                    ),
                subtitle=ft.Column(
                    controls = [
                        ft.Text(f'Contact person: {self.contactperson}', color=self.color, size = page.sizes['subheader'])
                    ]
                ),
                trailing=self.trailing,
                shape = ft.RoundedRectangleBorder(5),
                
            ),
            border=ft.border.all(page.sizes['card_border_size'], self.color),
            border_radius=15,
            margin=ft.margin.all(10)

        )