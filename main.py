import os
import sys
from geocoder import *
import requests
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5.QtCore import Qt
from PyQt5 import uic

SCREEN_SIZE = [600, 450]


class App(QMainWindow):
    def __init__(self, z):
        super().__init__()
        uic.loadUi('design_for_map.ui', self)  # Загружаем дизайн
        self.z = z
        self.search_btn.clicked.connect(self.req)

    def getImage(self):
        print('xa', self.address_ll)
        map_params = {
            "ll": self.address_ll,
            #"spn": delta,
            "z": self.z,  # 0 - 21
            "l": "map",
            "pt": f"{self.address_ll},pm2dgl"
        }
        map_api_server = "http://static-maps.yandex.ru/1.x/"
        response = requests.get(map_api_server, params=map_params)

        if not response:
            print("Ошибка выполнения запроса:")
            print(map_api_server)
            print("Http статус:", response.status_code, "(", response.reason, ")")
        else:
            # Запишем полученное изображение в файл.
            self.map_file = "map.png"
            with open(self.map_file, "wb") as file:
                file.write(response.content)


    def req(self):
        self.address_ll = self.search_line.text()
        self.initUI(self.address_ll)

    def initUI(self, address_ll):
        self.getImage()
        self.setWindowTitle('Отображение карты')
        self.pixmap = QPixmap(self.map_file)
        self.image = self.map_label
        self.image.move(0, 0)
        self.image.resize(600, 450)
        self.image.setPixmap(self.pixmap)


if __name__ == '__main__':
    z = 6
    app = QApplication(sys.argv)
    ex = App(z)
    ex.show()
    sys.exit(app.exec())
