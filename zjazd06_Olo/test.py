import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QWidget, QDialog, QFormLayout,
    QLineEdit, QComboBox, QMessageBox
)
from PyQt6.QtGui import QImage, QPainter, QPen, QColor
from PyQt6.QtCore import Qt, QPoint


class DrawingWidget(QWidget):
    def __init__(self, parent=None):  # Dodaj argument parent
        super().__init__(parent)  # Przekaż parent do konstruktora nadklasy
        self.image = QImage(400, 200, QImage.Format.Format_RGB32)  # Obraz do rysowania
        self.image.fill(Qt.GlobalColor.white)  # Wypełnij obraz białym kolorem
        self.drawing = False
        self.last_point = QPoint()

    def paintEvent(self, event):
        painter = QPainter(self)
        # Narysuj obramowanie
        painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
        painter.drawRect(self.rect())
        # Narysuj obraz
        painter.drawImage(self.rect(), self.image, self.image.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.pos()  # Pobierz współrzędne myszy względem widgetu

    def mouseMoveEvent(self, event):
        if self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.GlobalColor.black, 2, Qt.PenStyle.SolidLine))
            current_point = event.pos()  # Pobierz współrzędne myszy względem widgetu
            painter.drawLine(self.last_point, current_point)
            self.last_point = current_point
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = False

    def clear(self):
        self.image.fill(Qt.GlobalColor.white)
        self.update()

    def get_image(self):
        return self.image


class AddEditDialog(QDialog):
    def __init__(self, data=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Dodaj/Edytuj rekord")
        self.setModal(True)

        # Pola formularza
        self.name_input = QLineEdit()
        self.city_input = QLineEdit()
        self.gender_input = QComboBox()
        self.gender_input.addItems(["Mężczyzna", "Kobieta"])

        # Układ formularza
        layout = QFormLayout()
        layout.addRow("Imię:", self.name_input)
        layout.addRow("Miasto:", self.city_input)
        layout.addRow("Płeć:", self.gender_input)

        # Przyciski
        self.save_button = QPushButton("Zapisz")
        self.save_button.clicked.connect(self.accept)
        layout.addRow(self.save_button)

        self.setLayout(layout)

        # Wypełnij pola, jeśli edytujemy rekord
        if data:
            self.name_input.setText(data[0])
            self.city_input.setText(data[1])
            self.gender_input.setCurrentText(data[2])

    def get_data(self):
        return [
            self.name_input.text(),
            self.city_input.text(),
            self.gender_input.currentText()
        ]


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Aplikacja z tabelą i rysowaniem")
        self.setGeometry(100, 100, 800, 800)

        # Tabela
        self.table = QTableWidget(self)
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Imię", "Miasto", "Płeć"])
        self.table.setRowCount(0)
        self.table.setGeometry(10, 10, 500, 400)  # Pozycja i rozmiar tabeli

        # Przyciski
        self.add_button = QPushButton("Dodaj rekord", self)
        self.add_button.setGeometry(520, 10, 150, 30)  # Pozycja i rozmiar przycisku
        self.add_button.clicked.connect(self.add_record)

        self.edit_button = QPushButton("Edytuj rekord", self)
        self.edit_button.setGeometry(520, 50, 150, 30)  # Pozycja i rozmiar przycisku
        self.edit_button.clicked.connect(self.edit_record)

        self.delete_button = QPushButton("Usuń rekord", self)
        self.delete_button.setGeometry(520, 90, 150, 30)  # Pozycja i rozmiar przycisku
        self.delete_button.clicked.connect(self.delete_record)

        # Pole do rysowania
        self.drawing_widget = DrawingWidget(self)  # Przekazanie self jako parent
        self.drawing_widget.setGeometry(10, 420, 500, 200)  # Pozycja i rozmiar pola do rysowania

        # Przycisk do czyszczenia rysunku
        self.clear_drawing_button = QPushButton("Wyczyść rysunek", self)
        self.clear_drawing_button.setGeometry(520, 420, 150, 30)  # Pozycja i rozmiar przycisku
        self.clear_drawing_button.clicked.connect(self.drawing_widget.clear)

        # Przechowywanie rysunków
        self.images = []

    def add_record(self):
        dialog = AddEditDialog()
        if dialog.exec() == QDialog.DialogCode.Accepted:
            data = dialog.get_data()
            row_position = self.table.rowCount()
            self.table.insertRow(row_position)
            for col, value in enumerate(data):
                self.table.setItem(row_position, col, QTableWidgetItem(value))
            # Zapisz rysunek
            self.images.append(self.drawing_widget.get_image().copy())
            self.drawing_widget.clear()

    def edit_record(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            data = [
                self.table.item(selected_row, 0).text(),
                self.table.item(selected_row, 1).text(),
                self.table.item(selected_row, 2).text()
            ]
            dialog = AddEditDialog(data)
            if dialog.exec() == QDialog.DialogCode.Accepted:
                new_data = dialog.get_data()
                for col, value in enumerate(new_data):
                    self.table.setItem(selected_row, col, QTableWidgetItem(value))
                # Zaktualizuj rysunek
                self.images[selected_row] = self.drawing_widget.get_image().copy()
                self.drawing_widget.clear()
        else:
            QMessageBox.warning(self, "Błąd", "Wybierz rekord do edycji.")

    def delete_record(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            self.table.removeRow(selected_row)
            self.images.pop(selected_row)
        else:
            QMessageBox.warning(self, "Błąd", "Wybierz rekord do usunięcia.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())