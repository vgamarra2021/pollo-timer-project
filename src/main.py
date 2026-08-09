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

print(DATABASE_URL)

# Inicializar BD
if(DB_PATH.exists()):
    print("Database already exists. Skipping initialization.")
else:
    print("Database does not exist. Initializing...")
    initialize_database()

engine = create_engine(DATABASE_URL, echo=False)

import flet as ft

def main(page: ft.Page):
    page.title = "Pollo Timer App - Home"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.window.width = 800
    page.window.height = 300

    # Estado del timer
    timer_running = False
    timer_elapsed_seconds = 0

    async def timer_loop():
        nonlocal timer_elapsed_seconds
        while timer_running:
            await asyncio.sleep(1)
            if timer_running:
                timer_elapsed_seconds += 1
                timer.value = time.strftime(
                    "%H:%M:%S",
                    time.gmtime(timer_elapsed_seconds)
                )
                page.update()

    def historic_click(e):
        print("Historic button clicked")

    def start_pause_click(e):
        nonlocal timer_running
        
        if(toggle_button.icon == ft.Icons.PLAY_ARROW): #Sea play
            print('click en play')
            toggle_button.icon = ft.Icons.PAUSE
            timer_running = True
            asyncio.create_task(timer_loop())
            process_action("play", engine)
            
        else: #Sea pause
            print('click en pause')
            toggle_button.icon = ft.Icons.PLAY_ARROW
            timer_running = False
            process_action("pause", engine)

    def stop_click(e):
        print('click en stop')
        nonlocal timer_running, timer_elapsed_seconds
        process_action("stop", engine, timer_elapsed_seconds)
        timer_elapsed_seconds = 0
        toggle_button.icon = ft.Icons.PLAY_ARROW
        timer.value = "00:00:00"
        timer_running = False
        
        
    button_style = ft.ButtonStyle(
        icon_size=150,
        padding=30,
        alignment=ft.Alignment.CENTER,
        shape=ft.RoundedRectangleBorder(radius=10)
    )
    
    toggle_button = ft.Button(
        content="",
        icon=ft.Icons.PLAY_ARROW,
        on_click=start_pause_click,
        icon_color=ft.Colors.WHITE,
        style=button_style
    )
    
    timer = ft.Text("00:00:00", size=24, weight=ft.FontWeight.W_600)

    page.add(
        ft.Row(
            spacing=30,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                timer
            ],
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
        )
    )

ft.run(main)