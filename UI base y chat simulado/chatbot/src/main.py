import flet as ft

def main(page: ft.Page):
    page.title = "Chatbot - Parte 1"
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
        
    def enviar_click(e):
        texto = prompt.value.strip()
        if not texto:
            return
        mensajes.controls.append(burbuja(texto, chatsito=True))
        prompt.value = ""
        page.update()
        mensajes.controls.append(burbuja("Hola,soy una simulacion", chatsito=False))
        page.update()
        
    def limpiar_chat():
        mensajes.controls.clear()
        page.update()
        
        prompt.on_submit = enviar_click

    boton_enviar = ft.ElevatedButton("Enviar", on_click=enviar_click, bgcolor=ft.Colors.BLACK54, color=ft.Colors.CYAN)

    
    page.add(
        ft.Column([
            mensajes,
            ft.Row([ft.TextButton("Limpiar", on_click=limpiar_chat,)], alignment=ft.MainAxisAlignment.START),
            mensajes,
            ft.Row([prompt, boton_enviar], vertical_alignment=ft.CrossAxisAlignment.END,)
        ], expand=True)
    )
    
ft.app(target=main)
