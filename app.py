import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, FigureCanvas
from matplotlib.figure import Figure
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
from PySide2.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Plot Function")
        self.setGeometry(100, 100, 1000, 500)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.function_label = QLabel("Enter function:")
        self.layout.addWidget(self.function_label)

        self.function_edit = QLineEdit()
        self.layout.addWidget(self.function_edit)

        self.xmin_label = QLabel("Enter minimum value of x:")
        self.layout.addWidget(self.xmin_label)

        self.xmin_edit = QLineEdit()
        self.layout.addWidget(self.xmin_edit)

        self.xmax_label = QLabel("Enter maximum value of x:")
        self.layout.addWidget(self.xmax_label)

        self.xmax_edit = QLineEdit()
        self.layout.addWidget(self.xmax_edit)

        self.plot_button = QPushButton("Plot Function")
        self.plot_button.clicked.connect(self.plot_function)
        self.layout.addWidget(self.plot_button)

        fig = Figure(figsize=(5, 4), dpi=100)
        self.canvas = FigureCanvas(fig)
        ax = fig.add_subplot()
        ax.plot([0], [0])
        self.layout.addWidget(self.canvas)

    def plot_function(self):
        try:
            self.layout.removeWidget(self.canvas)
            self.canvas.deleteLater()

            function = self.function_edit.text()
            xmin = float(self.xmin_edit.text())
            xmax = float(self.xmax_edit.text())

            if function == "":
                raise ValueError("Function cannot be empty")

            x = list(range(int(xmin), int(xmax) + 1))
            y = []
            for i in x:
                f = function.lower()
                valid_chars = "0123456789+-*/^.()x "
                for char in f:
                    if char not in valid_chars:
                        raise ValueError("Function is not correct")
                f = f.replace("x", str(i))
                f = f.replace("^", "**")
                print(eval(f))
                y.append(eval(f))
            
            fig = Figure(figsize=(5, 4), dpi=100)
            self.canvas = FigureCanvas(fig)
            ax = fig.add_subplot(111)
            ax.plot(x, y)
            self.layout.addWidget(self.canvas)
          
        except Exception as e:
            error_dialog = QMessageBox()
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setText(str(e))
            error_dialog.setWindowTitle("Error")
            error_dialog.exec_()
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()

import pytest
from PySide2.QtWidgets import QApplication

@pytest.fixture
def app(qtbot):
    test_app = QApplication([])
    qtbot.addWidget(MainWindow())
    return test_app

def test_empty_function_input(app, qtbot):
    window = app.activeWindow()
    window.function_edit.setText('')
    window.xmin_edit.setText('0')
    window.xmax_edit.setText('10')

    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert len(qtbot.get_windows()) == 1
    assert qtbot.activeWindow().windowTitle() == "Error"
    assert qtbot.activeWindow().children()[1].text() == "Function cannot be empty"

def test_invalid_xmin_input(app, qtbot):
    window = app.activeWindow()
    window.function_edit.setText('x**2')
    window.xmin_edit.setText('a')
    window.xmax_edit.setText('10')

    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert len(qtbot.get_windows()) == 1
    assert qtbot.activeWindow().windowTitle() == "Error"
    assert qtbot.activeWindow().children()[1].text() == "invalid literal for float(): 'a'"

def test_invalid_xmax_input(app, qtbot):
    window = app.activeWindow()
    window.function_edit.setText('x**2')
    window.xmin_edit.setText('10')
    window.xmax_edit.setText('a')

    qtbot.mouseClick(window.plot_button, Qt.LeftButton)
    assert len(qtbot.get_windows()) == 1
    assert qtbot.activeWindow().windowTitle() == "Error"
    assert qtbot.activeWindow().children()[1].text() == "invalid literal for float(): 'a'"

