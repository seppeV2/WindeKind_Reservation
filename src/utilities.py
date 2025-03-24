import os
import json
import flet as ft
from datetime import datetime, timedelta

def get_type(page):
    if page.width < 650 and page.height < 1000:
        return 'Mobile'
    else:
        return 'Desktop'
    

def get_measurements(type):
    
    if type == 'Mobile':
        return {
            'appbar_text_size' : 25,
            'appbar_font_weight' : ft.FontWeight.W_800,
            'main_button_icon_size' : 35,
            'devider_margin' : 10,
            'main_button' : 18,
            'header' : 18,
            'subheader' : 15,
            'normal' : 12,
            'card_border_size' : 2,
            'shape_color' : ft.Colors.GREEN_900,
            'text_field_width_contact' : 150,
            'text_field_width_duration' : 100,
            'entry_margin' : 20,
            'button_margin_top' : 20

        }
    
    else:
        return {
            'appbar_text_size' : 40,
            'appbar_font_weight' : ft.FontWeight.W_900,
            'main_button' : 35,
            'main_button_icon_size' : 50,
            'devider_margin' : 20,
            'header' : 25,
            'subheader' : 20,
            'normal' : 18,
            'card_border_size' : 5,
            'shape_color' : ft.Colors.GREEN_900,
            'text_field_width_contact' : 250,
            'text_field_width_duration' : 100,
            'entry_margin' : 40,
            'button_margin_top' : 40,



        }

def get_reservations():
    with open(os.path.join(os.path.dirname(__file__), 'assets','data', 'reservations.json'), 'r' ) as _f:
        reservations = json.load(_f)
    _f.close()
    return reservations
def overwrite_reservations(new_reservations):
    with open(os.path.join(os.path.dirname(__file__), 'assets','data', 'reservations.json'), 'w') as _f:
        json.dump(new_reservations, _f)
    _f.close()

def get_materials(id=None):

    with open(os.path.join(os.path.dirname(__file__), 'assets','data', 'material.json'), 'r' ) as _f:
        materials = json.load(_f)
    _f.close()

    if id:
        try:
            return materials[id]
        except KeyError:
            return None
        
    else:
        return materials

def get_camera_web_view(page, endpoint, debug = True):
    square_size = min(0.85*page.width, 0.55 * page.height)
    return ft.Container(
        content=ft.WebView(
            url = f'{endpoint}/25403b32-2720-4e16-a651-f53fdf83e99c',
            enable_javascript=True,
        ),
        width=square_size,
        height=square_size,
        border=ft.border.all(width= 4, color=ft.Colors.BLACK)


    ) if not debug else ft.Placeholder(
        width=750, 
        height=(750/9)*16
    )

def pop_view(page, refresh=False):
    from home_view import get_home_view
    page.views.pop()
    if refresh:
        page.views[-1] = get_home_view(page)
    page.update()

def is_late_return(rental_time_str, rental_duration):

    rental_time = datetime.strptime(rental_time_str, '%Y-%m-%d %H:%M:%S')
    planned_duration = float(rental_duration)*60 #in minutes
    
    real_duration_raw = (datetime.now() - rental_time) #In minutes
    real_duration = real_duration_raw.days * (24*60) + real_duration_raw.seconds//60

    late = real_duration > planned_duration
    minutes_late = real_duration - planned_duration if late else None

    return late, minutes_late

def get_end_time(timestamp_str, duration):
    timestamp = datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S')
    endtime = timestamp +timedelta(hours=float(duration))
    return endtime.strftime('%H:%M')
