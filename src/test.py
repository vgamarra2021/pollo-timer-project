import flet as ft

@ft.component
def Home():
    return ft.Button("Go to About", on_click=lambda: ft.context.page.navigate("/about"))

@ft.component
def About():
    return ft.Button("Go to Home", on_click=lambda: ft.context.page.navigate("/"))

@ft.component
def App():
    return ft.Router([
        ft.Route(index=True, component=Home),
        ft.Route(path="about", component=About),
    ])

ft.run(lambda page: page.render(App))