import sys
from PyQt5.QtWidgets import QApplication, QWidget,QInputDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class TrussDrawingWidget(QWidget):
    def __init__(self):
        super().__init__()

        # 创建界面元素
        self.start_x_label = QLabel("Start X:")
        self.start_x_input = QLineEdit()
        self.start_y_label = QLabel("Start Y:")
        self.start_y_input = QLineEdit()
        self.end_x_label = QLabel("End X:")
        self.end_x_input = QLineEdit()
        self.end_y_label = QLabel("End Y:")
        self.end_y_input = QLineEdit()
        self.add_button = QPushButton("Add Segment")
        self.add_button.clicked.connect(self.add_segment)
        self.undo_button = QPushButton("Undo")
        self.undo_button.clicked.connect(self.undo_segment)
        self.show_nodes_button = QPushButton("Show Nodes")
        self.show_nodes_button.clicked.connect(self.show_nodes)

        # 创建 Matplotlib 绘图窗口
        self.fig = Figure()
        self.canvas = FigureCanvas(self.fig)

        # 初始化 Matplotlib 绘图
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True)

        # 初始化线段和结点的计数器和字典
        self.segment_index = 1
        self.node_index = 1
        self.node_dict = {}
        self.segments_dict = {}

        # 设置布局
        layout = QVBoxLayout()
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.start_x_label)
        form_layout.addWidget(self.start_x_input)
        form_layout.addWidget(self.start_y_label)
        form_layout.addWidget(self.start_y_input)
        layout.addLayout(form_layout)
        form_layout = QHBoxLayout()
        form_layout.addWidget(self.end_x_label)
        form_layout.addWidget(self.end_x_input)
        form_layout.addWidget(self.end_y_label)
        form_layout.addWidget(self.end_y_input)
        layout.addLayout(form_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.undo_button)
        button_layout.addWidget(self.show_nodes_button)
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_segment(self):
        # 获取用户输入
        start_x = float(self.start_x_input.text())
        start_y = float(self.start_y_input.text())
        end_x = float(self.end_x_input.text())
        end_y = float(self.end_y_input.text())

        # 计算线段中点坐标
        mid_x = (start_x + end_x) / 2
        mid_y = (start_y + end_y) / 2

        # 检查起点是否已经存在，如果不存在则分配编号
        if (start_x, start_y) not in self.node_dict:
            self.node_dict[(start_x, start_y)] = self.node_index
            start_node_index = self.node_index
            self.node_index += 1
        else:
            start_node_index = self.node_dict[(start_x, start_y)]

        # 检查终点是否已经存在，如果不存在则分配编号
        if (end_x, end_y) not in self.node_dict:
            self.node_dict[(end_x, end_y)] = self.node_index
            end_node_index = self.node_index
            self.node_index += 1
        else:
            end_node_index = self.node_dict[(end_x, end_y)]

        # 绘制线段
        line, = self.ax.plot([start_x, end_x], [start_y, end_y], 'b-')
        mid_point, = self.ax.plot(mid_x, mid_y, 'ro')  # 在中点处标注红点
        self.ax.text(mid_x, mid_y, str(self.segment_index), color='red', fontsize=12, ha='center', va='center')

        # 绘制结点
        start_point, = self.ax.plot(start_x, start_y, 'bo')  # 起点
        self.ax.text(start_x, start_y, str(start_node_index), color='blue', fontsize=12, ha='right', va='bottom')
        end_point, = self.ax.plot(end_x, end_y, 'bo')  # 终点
        self.ax.text(end_x, end_y, str(end_node_index), color='blue', fontsize=12, ha='right', va='bottom')

        # 记录线段对象和对应的结点编号和坐标
        segment_data = {
            "line": line,
            "mid_point": mid_point,
            "start_point": start_point,
            "end_point": end_point,
            "start_node_index": start_node_index,
            "end_node_index": end_node_index,
            "start_coord": (start_x, start_y),
            "end_coord": (end_x, end_y),
            "segment_index": self.segment_index
        }
        self.segments_dict[self.segment_index] = segment_data

        # 更新线段序号
        self.segment_index += 1

        # 更新图形
        self.ax.axis('equal')
        self.canvas.draw()

    def undo_segment(self):
        if self.segments_dict:
            last_segment_index = max(self.segments_dict.keys())
            last_segment = self.segments_dict.pop(last_segment_index)
            start_coord = last_segment["start_coord"]
            end_coord = last_segment["end_coord"]
            # 删除对应的线段和结点
            del last_segment["line"]
            del last_segment["mid_point"]
            del last_segment["start_point"]
            del last_segment["end_point"]
            if self.is_node_unused(start_coord):
                del self.node_dict[start_coord]
            if self.is_node_unused(end_coord):
                del self.node_dict[end_coord]
            # 重新绘制图形
            self.draw_graph()
        else:
            QMessageBox.warning(self, "Undo Failed", "No segments to undo.")

    def draw_graph(self):
        # 清空画布
        self.ax.clear()
        # 重新绘制所有结点和线段
        for segment_data in self.segments_dict.values():
            self.draw_segment(segment_data)
        for coord, node_index in self.node_dict.items():
            self.draw_node(coord, node_index)
        # 更新图形
        self.ax.axis('equal')
        self.ax.grid(True)
        self.canvas.draw()

    def draw_graph(self):
        # 清空画布
        self.ax.clear()
        # 重新绘制所有结点和线段
        for segment_data in self.segments_dict.values():
            self.draw_segment(segment_data)
        # 更新图形
        self.ax.axis('equal')
        self.ax.grid(True)
        self.canvas.draw()

    def draw_segment(self, segment_data):
        start_x, start_y = segment_data["start_coord"]
        end_x, end_y = segment_data["end_coord"]
        mid_x, mid_y = (start_x + end_x) / 2, (start_y + end_y) / 2
        line = self.ax.plot([start_x, end_x], [start_y, end_y], 'b-')[0]
        mid_point = self.ax.plot(mid_x, mid_y, 'ro')[0]
        self.ax.text(mid_x, mid_y, str(segment_data["segment_index"]), color='red', fontsize=12, ha='center',
                     va='center')
        self.ax.plot(start_x, start_y, 'bo')  # 起点
        self.ax.text(start_x, start_y, str(segment_data["start_node_index"]), color='blue', fontsize=12, ha='right',
                     va='bottom')
        self.ax.plot(end_x, end_y, 'bo')  # 终点
        self.ax.text(end_x, end_y, str(segment_data["end_node_index"]), color='blue', fontsize=12, ha='right',
                     va='bottom')

    def is_node_unused(self, coord):
        for segment_data in self.segments_dict.values():
            if segment_data["start_coord"] == coord or segment_data["end_coord"] == coord:
                return False
        return True

    def show_nodes(self):
        # 创建一个空字符串用于记录结点信息
        nodes_info = ""
        for i, segment_data in self.segments_dict.items():
            start_node_index = segment_data["start_node_index"]
            start_coord = segment_data["start_coord"]
            end_node_index = segment_data["end_node_index"]
            end_coord = segment_data["end_coord"]
            nodes_info += f"Segment {i} : Node {start_node_index} {start_coord}, Node {end_node_index} {end_coord}\n"

        # 弹出消息框显示结点信息
        QMessageBox.information(self, "Segments Information", nodes_info)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrussDrawingWidget()
    window.setWindowTitle("Truss Drawing")
    window.show()
    sys.exit(app.exec_())
