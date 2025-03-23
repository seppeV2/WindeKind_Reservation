import os
import json
import flet as ft
from datetime import datetime, timedelta

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
    return ft.Container(
        content=ft.WebView(
            url = f'{endpoint}/25403b32-2720-4e16-a651-f53fdf83e99c',
            enable_javascript=True,
        ),
        width=0.75*page.width,
        height=0.5 * page.height


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

if __name__ == '__main__':
    print(get_reservations())