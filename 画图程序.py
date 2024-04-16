import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, QDialog
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
        
        # 初始化线段和结点的计数器和字典
        self.segment_index = 1
        self.node_index = 1
        self.node_dict = {}
        self.segments_dict = {}
        self.node_info_dict = {}  # 记录结点信息的字典

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
            print(end_node_index)
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
            last_segment_key = max(self.segments_dict.keys())
            last_segment_value = self.segments_dict[last_segment_key]
            last_segment = self.segments_dict[last_segment_key]
            start_coord = last_segment["start_coord"]
            end_coord = last_segment["end_coord"]

            if self.is_node_unused(start_coord):
                del self.node_dict[start_coord]
                del self.node_info_dict[start_coord]

            # 原始字典转换为列表
            self.segments_dict_items = list(self.segments_dict.items()) 

            # 删除键为"2"的项
            self.segments_dict_items.remove((last_segment_key, last_segment_value))

            # 重新索引键
            self.segments_dict = {str(i+1): v for i, (k, v) in enumerate(self.segments_dict_items)}

            if self.is_node_unused(end_coord):
                del self.node_dict[end_coord]
                del self.node_info_dict[end_coord]


            print(self.node_info_dict)
            print(self.node_dict)
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
        # 创建结点信息对话框，并设置父对象为当前窗口
        self.node_info_dialog = self.NodeInfoDialog(self.node_info_dict, self.segments_dict, parent=self)
        self.node_info_dialog.exec_()

    def node_dialog_closed(self):
        if self.node_info_dialog.result() == QDialog.Accepted:
            self.draw_graph()

    class NodeInfoDialog(QDialog):
        def __init__(self, node_info_dict, segments_dict, parent=None):
            super().__init__(parent=parent)

            self.node_info_dict = node_info_dict
            self.segments_dict = segments_dict

            self.setWindowTitle("Node Information")
            self.layout = QVBoxLayout()

            # 创建结点信息表格
            self.node_table = QTableWidget()
            self.node_table.setColumnCount(4)  # 增加一个列用于选择承接条件
            self.node_table.setHorizontalHeaderLabels(["Node Index", "X Coord", "Y Coord", "Support Type"])
            self.layout.addWidget(self.node_table)

            # 创建确认按钮
            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.confirm_support_type)
            self.layout.addWidget(self.confirm_button)

            self.setLayout(self.layout)

            # 显示结点信息
            self.show_node_info()

        def show_node_info(self):

            self.node_table.setRowCount(len(self.node_info_dict))
            for i, (coord, node_data) in enumerate(self.node_info_dict.items()):
                node_index = node_data['index']
                x_coord, y_coord = coord
                self.node_table.setItem(i, 0, QTableWidgetItem(str(node_index)))
                self.node_table.setItem(i, 1, QTableWidgetItem(str(x_coord)))
                self.node_table.setItem(i, 2, QTableWidgetItem(str(y_coord)))
                # 创建下拉菜单
                combo_box = QComboBox()
                combo_box.addItem("No Support")
                combo_box.addItem("Pinned Support")
                combo_box.addItem("Sliding Support")
                combo_box.addItem("Fixed Support")
                support_type = node_data['support_type']
                combo_box.setCurrentText(support_type)
                self.node_table.setCellWidget(i, 3, combo_box)

        def confirm_support_type(self):
            for i in range(self.node_table.rowCount()):
                node_index = int(self.node_table.item(i, 0).text())
                print(node_index)
                support_type = self.node_table.cellWidget(i, 3).currentText()
                print(support_type)
                # 更新结点支撑类型信息
                for coord, node_data in self.node_info_dict.items():
                    if node_data['index'] == node_index:
                        node_data['support_type'] = support_type

            self.parent().draw_graph()  # 在确认更新结点支撑类型后重新绘制图形
            # 关闭对话框
            self.accept()


        def closeEvent(self, event):
            self.parent().node_dialog_closed()
            event.accept()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrussDrawingWidget()
    window.setWindowTitle("Truss Drawing")
    window.show()
    sys.exit(app.exec_())
