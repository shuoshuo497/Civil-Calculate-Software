from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QMessageBox, QComboBox, QLineEdit
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Drawing Page")

        self.supports_label = QLabel("Select support type:")
        self.supports_combo = QComboBox()
        self.supports_combo.addItem("Fixed")
        self.supports_combo.addItem("Hinged")
        self.supports_combo.addItem("Roller")

        self.angle_label = QLabel("Enter member angle (in degrees):")
        self.angle_input = QLineEdit()

        self.length_label = QLabel("Enter member length:")
        self.length_input = QLineEdit()

        self.draw_button = QPushButton("Draw")
        self.draw_button.clicked.connect(self.draw_structure)

        layout = QVBoxLayout()
        layout.addWidget(self.supports_label)
        layout.addWidget(self.supports_combo)
        layout.addWidget(self.angle_label)
        layout.addWidget(self.angle_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.length_input)
        layout.addWidget(self.draw_button)

        self.setLayout(layout)

    def draw_structure(self):
        support_type = self.supports_combo.currentText()
        angle = float(self.angle_input.text())
        length = float(self.length_input.text())

        # 在此处绘制桁架结构，这里只是一个示例
        # 您需要根据用户输入来绘制具体的结构

        # 绘图的代码可以在此处添加
        pass

    def paintEvent(self, event):
        # 在这里进行绘图
        painter = QPainter(self)
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        # 在这里绘制桁架结构

class MainWindow(QWidget):
    def __init__(self, username):
        super().__init
