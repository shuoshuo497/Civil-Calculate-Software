import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np

class TrussDrawingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建界面元素
        self.angle_label = QLabel("Angle (degrees):")
        self.angle_input = QLineEdit()
        self.length_label = QLabel("Length:")
        self.length_input = QLineEdit()
        self.start_x_label = QLabel("Start X:")
        self.start_x_input = QLineEdit()
        self.start_y_label = QLabel("Start Y:")
        self.start_y_input = QLineEdit()
        self.add_button = QPushButton("Add Member")
        self.add_button.clicked.connect(self.add_member)

        # 设置布局
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.angle_label)
        form_layout.addWidget(self.angle_input)
        form_layout.addWidget(self.length_label)
        form_layout.addWidget(self.length_input)
        layout.addLayout(form_layout)
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.start_x_label)
        form_layout.addWidget(self.start_x_input)
        form_layout.addWidget(self.start_y_label)
        form_layout.addWidget(self.start_y_input)
        layout.addLayout(form_layout)
        layout.addWidget(self.add_button)

        # 创建 Matplotlib 绘图窗口
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # 初始化 Matplotlib 绘图
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)

    def add_member(self):
        # 获取用户输入
        angle = float(self.angle_input.text())
        length = float(self.length_input.text())
        start_x = float(self.start_x_input.text())
        start_y = float(self.start_y_input.text())

        # 将角度转换为弧度
        angle_rad = np.radians(angle)

        # 计算结束点坐标
        end_x = start_x + length * np.cos(angle_rad)
        end_y = start_y + length * np.sin(angle_rad)

        # 绘制桁架杆件
        self.ax.plot([start_x, end_x], [start_y, end_y], 'b-')
        self.ax.plot(start_x, start_y, 'ro')  # 起点
        self.ax.plot(end_x, end_y, 'ro')      # 终点

        # 更新图形
        self.ax.axis('equal')
        self.canvas.draw()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrussDrawingWidget()
    window.setWindowTitle("Truss Drawing")
    window.show()
    sys.exit(app.exec_())
