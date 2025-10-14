import flet as ft
import requests
import json 

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5:3b"

def main(page: ft.Page):
    page.title = "Chatbot - Parte 2"
    page.bgcolor = ft.Colors.BLUE

    mensajes = ft.ListView(expand=True, spacing=10, padding=20, auto_scroll=True)
    prompt = ft.TextField(label="Escribe tu mensaje...", expand=True, multiline=True, min_lines=1, max_lines=4)

    def burbuja(texto, chatsito):
        return ft.Row(
            [
                ft.Container(
                    content=ft.Text(
                    texto,
                    color=ft.Colors.BLACK54 if chatsito else  ft.Colors.BLACK54,
                    size=15,
                    selectable=True,    
                ),
                bgcolor=ft.Colors.BROWN_200 if chatsito else ft.Colors.BROWN_200,
                padding=12,
                border_radius=30,
                width=350,
                )
            ],
            alignment=ft.MainAxisAlignment.END if chatsito else ft.MainAxisAlignment.START,
        )
        
    def enviar_click_streaming(e):
        texto = prompt.value.strip()
        if not texto:
            return
        mensajes.controls.append(burbuja(texto, chatsito=True))
        prompt.value = ""
        page.update()
        mensajes.controls.append(burbuja("Hola,soy una simulacion", chatsito=False))
        page.update()
        
        live_text = ft.Text("", color=ft.Colors.BLACK, size=15, selectable=True)
        cont = ft.Row([
            ft.Container(content=live_text, bgcolor=ft.Colors.GREY_300, padding=12, border_radius=30, width=350),
        ], alignment=ft.MainAxisAlignment.START)
        mensajes.controls.append(cont)
        page.update()

        try:
            r = requests.post(
                OLLAMA_URL,
                json={"model": MODEL, "prompt": texto, "stream": True},
                stream=True,
                timeout=300,
            )
            r.raise_for_status()
            completo = ""
            for line in r.iter_lines():
                if not line:
                    continue
                data = json.loads(line)
                if "response" in data:
                    completo += data["response"]
                    live_text.value = completo
                    page.update()
        except Exception as ex:
            live_text.value = f"Error: {ex}"
            page.update()
        
    def limpiar_chat():
        mensajes.controls.clear()
        page.update()
        
        prompt.on_submit = enviar_click_streaming

    boton_enviar = ft.ElevatedButton("Enviar", on_click=enviar_click_streaming, bgcolor=ft.Colors.BLACK54, color=ft.Colors.CYAN)

    
    page.add(
        ft.Column([
            mensajes,
            ft.Row([ft.TextButton("Limpiar", on_click=limpiar_chat,)], alignment=ft.MainAxisAlignment.START),
            mensajes,
            ft.Row([prompt, boton_enviar], vertical_alignment=ft.CrossAxisAlignment.END,)
        ], expand=True)
    )
    
ft.app(target=main)