import os
import time
import certifi
from pathlib import Path
import asyncio

#Fix for MacOS SSL certificate verification issue
os.environ.setdefault("SSL_CERT_FILE", certifi.where())
os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())

from dotenv import load_dotenv
from sqlalchemy import create_engine
from db.init_database import initialize_database
from services.llm_service import call_llm_with_sdk, call_llm_with_http
from services.session_service import process_action

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

#Variables Generales
DB_PATH = Path(__file__).resolve().parent / "db/app.db"
DATABASE_URL = f"sqlite:///{DB_PATH}"

#------- INIT BD ---------
if(DB_PATH.exists()):
    print("Database already exists. Skipping initialization.")
else:
    print("Database does not exist. Initializing...")
    initialize_database()

engine = create_engine(DATABASE_URL, echo=False)

#------- UI ---------

import flet as ft

@ft.component
def Home():
    page = ft.context.page
    store = page.session.store
    timer_running = bool(store.get("timer_running") or False)
    timer_elapsed_seconds = int(store.get("timer_elapsed_seconds") or 0)

    def render_app():
        page.render(App)

    def historic_click(e):
        ft.context.page.navigate("/historic")

    async def timer_loop():
        while bool(page.session.store.get("timer_running") or False):
            await asyncio.sleep(1)
            if bool(page.session.store.get("timer_running") or False):
                current_elapsed = int(page.session.store.get("timer_elapsed_seconds") or 0)
                page.session.store.set("timer_elapsed_seconds", current_elapsed + 1)
                render_app()

    def stop_click(e):
        print('click en stop')
        process_action("stop", engine, timer_elapsed_seconds)
        page.session.store.set("timer_running", False)
        page.session.store.set("timer_elapsed_seconds", 0)
        render_app()

    def start_pause_click(e):
        if not timer_running: #Sea play
            print('click en play')
            page.session.store.set("timer_running", True)
            asyncio.create_task(timer_loop())
            process_action("play", engine)
            render_app()
            
        else: #Sea pause
            print('click en pause')
            page.session.store.set("timer_running", False)
            process_action("pause", engine)
            render_app()

    button_style = ft.ButtonStyle(
        icon_size=150,
        padding=30,
        alignment=ft.Alignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=10)
    )

    timer = ft.Text(
        time.strftime("%H:%M:%S", time.gmtime(timer_elapsed_seconds)),
        size=24,
        weight=ft.FontWeight.W_600
    )
    toggle_button = ft.Button(
        content="",
        icon=ft.Icons.PAUSE if timer_running else ft.Icons.PLAY_ARROW,
        on_click=start_pause_click,
        icon_color=ft.Colors.WHITE,
        style=button_style
    )


    return ft.Column(
        spacing=30,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        controls=[
            ft.Row(
                spacing=30,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[timer],
            ),
            ft.Row(
                spacing=30,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Button(
                        content="",
                        icon=ft.Icons.HISTORY,
                        on_click=historic_click,
                        icon_color=ft.Colors.WHITE,
                        style=button_style
                    ),
                    toggle_button,
                    ft.Button(
                        content="",
                        icon=ft.Icons.STOP,
                        on_click=stop_click,
                        icon_color=ft.Colors.WHITE,
                        style=button_style
                    ),
                ],
            ),
        ],
    )

        

@ft.component
def Historic():
    return ft.Button("Go to Home", on_click=lambda: ft.context.page.navigate("/"))


@ft.component
def App():
    return ft.Router([
        ft.Route(index=True, path="home", component=Home),
        ft.Route(path="historic", component=Historic),
    ])


def main(page: ft.Page):
    page.title = "Pollo Timer App - Home"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 800
    page.window.height = 350

    page.render(App)

ft.run(main)