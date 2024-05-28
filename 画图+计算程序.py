import sys
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, QComboBox, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import math
from numpy import *
from math import *
import sys,os,codecs
from PyQt5.QtCore import QProcess


#画图部分
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
        self.save_button = QPushButton("Save to TXT")   #将所需计算数据保存至txt文件
        self.save_button.clicked.connect(lambda: window.save_info_to_txt('计算数据.txt'))
        # self.calculate = QPushButton("calculate")   
        # self.calculate.clicked.connect(lambda: window.cal)
        self.run_button = QPushButton("calculate")
        self.run_button.clicked.connect(self.run_another_script)
 
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
        layout.addLayout(button_layout)
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        button_layout.addWidget(self.save_button)   #增加计算数据保存按钮
        # button_layout.addWidget(self.calculate)
        button_layout.addWidget(self.run_button) 
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
            print(self.node_info_dict)
            print(self.node_dict)
            # 更新线段序号
            self.segment_index -= 1
            del last_segment["line"]
            del last_segment["mid_point"]
            del last_segment["start_point"]
            del last_segment["end_point"]
            if self.is_node_unused(start_coord):
                del self.node_dict[start_coord]
                del self.node_info_dict[start_coord]

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

    def show_segments(self):
        # 创建显示线段信息的对话框
        dialog = self.ShowSegmentsDialog(self.node_info_dict, self.segments_dict, parent=self)
        dialog.exec_()

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
    # 显示所有线段的表格
    # 用来填写刚度
    class ShowSegmentsDialog(QDialog):
        def __init__(self, node_info_dict, segments_dict, parent=None):
            super().__init__(parent=parent)

            self.node_info_dict = node_info_dict
            self.segments_dict = segments_dict


            self.setWindowTitle("Segment Information")
            self.layout = QVBoxLayout()

            # 创建线段信息表格
            self.segment_table = QTableWidget()
            self.segment_table.setColumnCount(6)  # 6 列: 线段序号、起点、坐标、终点、坐标、刚度
            self.segment_table.setHorizontalHeaderLabels(["Segment Index", "Start Node", "Start Coord",
                                                          "End Node", "End Coord", "Stiffness"])
            self.layout.addWidget(self.segment_table)

            # 创建确认按钮
            self.confirm_button = QPushButton("Confirm")
            self.confirm_button.clicked.connect(self.confirm_stiffness)
            self.layout.addWidget(self.confirm_button)

            self.setLayout(self.layout)

            # 显示线段信息
            self.show_segment_info()

        def show_segment_info(self):
            self.segment_table.setRowCount(len(self.segments_dict))
            for i, segment_data in enumerate(self.segments_dict.values()):
                self.segment_table.setItem(i, 0, QTableWidgetItem(str(segment_data["segment_index"])))
                self.segment_table.setItem(i, 1, QTableWidgetItem(str(segment_data["start_node_index"])))
                self.segment_table.setItem(i, 2, QTableWidgetItem(str(segment_data["start_coord"])))
                self.segment_table.setItem(i, 3, QTableWidgetItem(str(segment_data["end_node_index"])))
                self.segment_table.setItem(i, 4, QTableWidgetItem(str(segment_data["end_coord"])))
                self.segment_table.setItem(i, 5, QTableWidgetItem(str(segment_data["stiffness"])))

        def confirm_stiffness(self):
            for i in range(self.segment_table.rowCount()):
                segment_index = int(self.segment_table.item(i, 0).text())
                stiffness_item = float(self.segment_table.item(i, 5).text())
                print(segment_index)
                print(stiffness_item)
                for index, segment_data in self.segments_dict.items():
                    print(segment_data['stiffness'])
                    if index == segment_index:
                        segment_data['stiffness'] = stiffness_item

            self.parent().draw_graph()  # 在确认更新结点支撑类型后重新绘制图形

            # 关闭对话框
            self.accept()


    def calculate_segment_angle_and_length(self, segment_data):
        start_x, start_y = segment_data["start_coord"]
        end_x, end_y = segment_data["end_coord"]
        dx = end_x - start_x
        dy = end_y - start_y
        length = math.sqrt(dx**2 + dy**2)
        angle = math.degrees(math.atan2(dy, dx))
        return angle, length

    def calculate_node_displacements_and_forces(self):
        # 计算节点的位移和受力
        node_displacements_forces_dict= {}  # 存储节点位移和力的字典
        # 假设我们有一个外部力字典，它给出了每个节点的力和方向 如下
        external_forces = {1:('x1','y1'), 2:('x2', 'y2'), 3:(0,0), 4:('x4', 'y4')}
        for node_data in self.node_info_dict.values():
            node_index = node_data['index']
            support_type = node_data['support_type']
            if support_type == 'Pinned Support':    
                displacement_x, displacement_y = 0, 0
            else:
            # 其他类型的支撑，这里需要根据实际的分析方法来计算位移
            # 这里只是一个示例，实际情况可能需要更复杂的计算
                displacement_x, displacement_y = 1, 1
            def are_all_strings(tuple_values):      #检查元组中的所有元素是否都是字符串
                return all(isinstance(value, str) for value in tuple_values)
            if are_all_strings(external_forces[node_index]):
                force_x = external_forces[node_index][0]
                force_y = external_forces[node_index][1]
            else:
                force_x, force_y = external_forces[node_index]

            force_x = external_forces[node_index][0]
            force_y = external_forces[node_index][1]
            node_displacements_forces_dict[node_index] = (displacement_x, displacement_y, force_x, force_y )
        return node_displacements_forces_dict
    
    def save_info_to_txt(self, filename):
        # 计算杆件数和节点数
        num_segments = len(self.segments_dict)
        num_nodes = len(self.node_info_dict)

        # 构建杆件信息行
        segment_lines = []
        for segment_data in self.segments_dict.values():
            angle, length = self.calculate_segment_angle_and_length(segment_data)
            start_node = segment_data['start_node_index']
            end_node = segment_data['end_node_index']
            segment_lines.append(f"{start_node} {end_node} {angle} {length}")

        # 构建节点信息行
        node_lines = []
        node_displacements_forces = self.calculate_node_displacements_and_forces()
        for node_data in self.node_info_dict.values():
            node_index = node_data['index']
            displacement_x, displacement_y, force_x, force_y = node_displacements_forces[node_index]
            node_lines.append(f"{displacement_x} {displacement_y} {force_x} {force_y}")

        # 按照指定格式构建整个文本
        text = f"{num_segments} {num_nodes}\n"
        text += "\n".join(segment_lines) + "\n"
        text += "\n".join(node_lines)

        # 写入文件
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(text)
        print("Saved already!")
    #计算部分
    def run_another_script(self):
        script_path = "E:\\pycharm\\Civil-Calculate-Software\\计算程序.py"  # 替换为.py文件路径
        process = QProcess(self)
        process.startDetached("python", [script_path])

        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TrussDrawingWidget()
    window.setWindowTitle("Truss Drawing")
    window.show()
    sys.exit(app.exec_())
