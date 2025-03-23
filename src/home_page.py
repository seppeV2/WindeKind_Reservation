import flet as ft

def route_change(route: ft.RouteChangeEvent, page: ft.Page):
    
    route_trace = ft.TemplateRoute(route.route)
    pass

    """
    if route_trace.match('/reservation/:id'):
        
        page.views.clear()
        page.views.append(
            ft.View(
                route = route_trace.route,
                controls = [
                    ft.Text(f'Reservation Page for item {route_trace.id}')
                ]
            )
        )
        page.update()
    """
async def home_page(page: ft.Page):

    page.views.append(
        ft.View(
            route = '/',
            controls=[
                ft.Text('This is main'),
                ft.TextButton(
                    'Go to reservation',
                    on_click= lambda _: page.go('/reservation/'))
            ]
        )
    )
    page.on_route_change = lambda e: route_change(e, page)
    page.update()
