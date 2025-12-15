import flet as ft

from metro_paris.model.model import Model
from metro_paris.UI.view import View
from metro_paris.UI.controller import Controller

def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()

ft.app(target=main)
