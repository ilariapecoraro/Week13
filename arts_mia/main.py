import flet as ft

from arts_mia.model.model import Model
from arts_mia.UI.view import View
from arts_mia.UI.controller import Controller


def main(page: ft.Page):
    my_model = Model()
    my_view = View(page)
    my_controller = Controller(my_view, my_model)
    my_view.set_controller(my_controller)
    my_view.load_interface()


ft.app(target=main)
