import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math

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
        self.show_segments_button = QPushButton("Show Segments")
        self.show_segments_button.clicked.connect(self.show_segments)
        self.apply_force_button = QPushButton("Apply Force")  # 新增施加力按钮
        self.apply_force_button.clicked.connect(self.apply_force_to_node)
        self.save_button = QPushButton("Save to TXT")   #将所需计算数据保存至txt文件
        self.save_button.clicked.connect(lambda: window.save_info_to_txt('计算数据.txt'))

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
        self.node_info_dict = {}  # 记录结点信息的字典
        self.force_dict = {}  # 记录节点施加的力

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
        layout.addLayout(button_layout)
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.show_nodes_button)
        button_layout.addWidget(self.show_segments_button)
        button_layout.addWidget(self.apply_force_button)  # 将施加力按钮添加到布局中
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        button_layout.addWidget(self.save_button)   #增加计算数据保存按钮

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
            self.node_info_dict[(start_x, start_y)] = {'index': self.node_index, 'support_type': 'None'}
            start_node_index = self.node_index
            self.node_index += 1
        else:
            start_node_index = self.node_dict[(start_x, start_y)]

        # 检查终点是否已经存在，如果不存在则分配编号
        if (end_x, end_y) not in self.node_dict:
            self.node_dict[(end_x, end_y)] = self.node_index
            self.node_info_dict[(end_x, end_y)] = {'index': self.node_index, 'support_type': 'None'}
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
            "segment_index": self.segment_index,
            "stiffness": 0.0
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
            if self.is_node_unused(start_coord):
                del self.node_dict[start_coord]
                del self.node_info_dict[start_coord]

            if self.is_node_unused(end_coord):
                del self.node_dict[end_coord]
                del self.node_info_dict[end_coord]

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
        # 重新绘制所有力
        for (node_x, node_y), force in self.force_dict.items():
            self.draw_force(node_x, node_y, force)
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
        self.ax.text(end_x, end_y, str(segment_data["end_node_index"]), color='blue', fontsize=12, ha='right', va='bottom')
        segment_data["line"] = line
        segment_data["mid_point"] = mid_point

    def draw_force(self, x, y, force):
        arrow_length = 0.1  # 箭头的长度
        arrow_dx = force * arrow_length * math.cos(math.radians(0))  # 假设力在x方向
        arrow_dy = force * arrow_length * math.sin(math.radians(0))  # 假设力在x方向
        self.ax.arrow(x, y, arrow_dx, arrow_dy, head_width=0.05, head_length=0.1, fc='r', ec='r')
        self.ax.text(x + arrow_dx, y + arrow_dy, f'{force}N', color='red', fontsize=12)

    def is_node_unused(self, coord):
        for segment in self.segments_dict.values():
            if segment["start_coord"] == coord or segment["end_coord"] == coord:
                return False
        return True

    def show_nodes(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Node Information")
        layout = QVBoxLayout(dialog)

        table = QTableWidget(len(self.node_info_dict), 3)
        table.setHorizontalHeaderLabels(["Node Index", "Coordinates", "Support Type"])
        for i, ((x, y), info) in enumerate(self.node_info_dict.items()):
            table.setItem(i, 0, QTableWidgetItem(str(info['index'])))
            table.setItem(i, 1, QTableWidgetItem(f"({x}, {y})"))
            table.setItem(i, 2, QTableWidgetItem(info['support_type']))
        layout.addWidget(table)

        dialog.setLayout(layout)
        dialog.exec_()

    def show_segments(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Segment Information")
        layout = QVBoxLayout(dialog)

        table = QTableWidget(len(self.segments_dict), 3)
        table.setHorizontalHeaderLabels(["Segment Index", "Start Node", "End Node"])
        for i, segment_data in enumerate(self.segments_dict.values()):
            table.setItem(i, 0, QTableWidgetItem(str(segment_data["segment_index"])))
            table.setItem(i, 1, QTableWidgetItem(str(segment_data["start_node_index"])))
            table.setItem(i, 2, QTableWidgetItem(str(segment_data["end_node_index"])))
        layout.addWidget(table)

        dialog.setLayout(layout)
        dialog.exec_()

    def apply_force_to_node(self):
        node_index, ok = QInputDialog.getInt(self, "Apply Force", "Enter node index:")
        if not ok:
            return
        force, ok = QInputDialog.getDouble(self, "Apply Force", "Enter force magnitude (N):")
        if not ok:
            return

        # 查找对应的节点坐标
        node_coord = None
        for coord, info in self.node_info_dict.items():
            if info['index'] == node_index:
                node_coord = coord
                break

        if node_coord is None:
            QMessageBox.warning(self, "Apply Force Failed", "Node index not found.")
            return

        self.force_dict[node_coord] = force
        self.draw_graph()

    def save_info_to_txt(self, filename):
        with open(filename, 'w') as f:
            f.write("Nodes:\n")
            for coord, info in self.node_info_dict.items():
                f.write(f"Node {info['index']}: Coordinates: {coord}, Support Type: {info['support_type']}\n")

            f.write("\nSegments:\n")
            for segment_data in self.segments_dict.values():
                f.write(f"Segment {segment_data['segment_index']}: Start Node: {segment_data['start_node_index']}, "
                        f"End Node: {segment_data['end_node_index']}, Start Coord: {segment_data['start_coord']}, "
                        f"End Coord: {segment_data['end_coord']}\n")

            f.write("\nForces:\n")
            for (node_x, node_y), force in self.force_dict.items():
                f.write(f"Node at ({node_x}, {node_y}): Force: {force} N\n")


class TrussAnalysisWidget(QWidget):
    def __init__(self, truss_widget):
        super().__init__()
        self.truss_widget = truss_widget
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.combo_box = QComboBox(self)
        self.combo_box.addItems(["Select an analysis type", "Type 1", "Type 2", "Type 3"])
        layout.addWidget(self.combo_box)

        self.setLayout(layout)

        self.combo_box.currentIndexChanged.connect(self.on_combobox_changed)

    def on_combobox_changed(self, index):
        if index == 0:
            return  # 忽略第一个选项
        analysis_type = self.combo_box.itemText(index)
        QMessageBox.information(self, "Analysis Selected", f"You selected {analysis_type} analysis.")


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.truss_widget = TrussDrawingWidget()
        self.analysis_widget = TrussAnalysisWidget(self.truss_widget)

        layout = QVBoxLayout()
        layout.addWidget(self.truss_widget)
        layout.addWidget(self.analysis_widget)

        self.setLayout(layout)
        self.setWindowTitle("Truss Analysis Application")
        self.setGeometry(100, 100, 800, 600)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
