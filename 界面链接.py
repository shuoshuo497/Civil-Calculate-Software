import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel
from 画图程序 import TrussDrawingWidget  # 导入正确的结点坐标绘图类


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("主界面")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.btn_node_coordinates = QPushButton("结点坐标作图", self)
        self.btn_node_coordinates.clicked.connect(self.open_truss_drawing)
        layout.addWidget(self.btn_node_coordinates)

        self.btn_assemble_rods = QPushButton("杆件拼装作图", self)
        self.btn_assemble_rods.clicked.connect(self.open_rod_assembly)
        layout.addWidget(self.btn_assemble_rods)

        self.setLayout(layout)

    def open_truss_drawing(self):
        self.truss_drawing_window = TrussDrawingWidget()
        self.truss_drawing_window.show()

    def open_rod_assembly(self):
        self.rod_window = QWidget()
        self.rod_window.setWindowTitle("杆件拼装作图")
        self.rod_window.setGeometry(150, 150, 400, 300)

        layout = QVBoxLayout()
        label = QLabel("这是一个临时的杆件拼装作图界面")
        layout.addWidget(label)

        self.rod_window.setLayout(layout)
        self.rod_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())
