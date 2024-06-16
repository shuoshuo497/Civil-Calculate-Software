import matplotlib.pyplot as plt
import re

# 打开并读取文件
with open('C:\\Users\\li_ju\\Desktop\\homework\\计算结果.txt', 'r') as file:
    lines = file.readlines()

# 初始化存储数据的字典
bar_forces = {}
node_forces = {}
node_displacements = {}

# 正则表达式模式
bar_pattern = re.compile(r'(\d+)号杆的力是([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')
node_force_pattern = re.compile(r'结点(\d+)力:([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*,\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)')
node_displacement_pattern = re.compile(r'结点(\d+)位移:L/EA\(([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\s*,\s*([-+]?\d*\.?\d+(?:[eE][-+]?\d+)?)\)')

# 遍历每一行并提取信息
for line in lines:
    bar_match = bar_pattern.search(line)
    if bar_match:
        bar_id = int(bar_match.group(1))
        bar_force = float(bar_match.group(2))
        bar_forces[bar_id] = bar_force
        continue
    
    node_force_match = node_force_pattern.search(line)
    if node_force_match:
        node_id = int(node_force_match.group(1))
        force_x = float(node_force_match.group(2))
        force_y = float(node_force_match.group(3))
        node_forces[node_id] = (force_x, force_y)
        continue

    node_displacement_match = node_displacement_pattern.search(line)
    if node_displacement_match:
        node_id = int(node_displacement_match.group(1))
        displacement_x = float(node_displacement_match.group(2))
        displacement_y = float(node_displacement_match.group(3))
        node_displacements[node_id] = (displacement_x, displacement_y)
        continue

print("各杆件力:", bar_forces)
print("各结点力:", node_forces)
print("各结点位移:", node_displacements)

# 创建图形
fig, ax = plt.subplots()

# 绘制各杆件力柱状图
bar_width = 0.35
bars_index = list(bar_forces.keys())
bars_forces = list(bar_forces.values())
index = range(len(bars_index))

bar1 = plt.bar(index,bars_forces, bar_width, label='bars_forces')

# 添加标签和标题
plt.xlabel('segments_index')
plt.ylabel('segments_forces')
plt.title('Forces at Different Segments')
plt.xticks([i + bar_width / 2 for i in index], bars_index)
plt.legend()
# 显示图形
plt.show()

# 创建图形
fig, ax = plt.subplots()

# 绘制各结点力柱状图
bar_width = 0.35
nodes_index = list(node_forces.keys())
nodes_forces = list(node_forces.values())
index = range(len(nodes_index))

# 分离X方向和Y方向的力
forces_x = [force[0] for force in nodes_forces]
forces_y = [force[1] for force in nodes_forces]

bar1 = plt.bar(index,forces_x, bar_width, label='forces_x')
bar2 = plt.bar([i + bar_width for i in index], forces_y, bar_width, label='forces_y')
# 添加标签和标题
plt.xlabel('nodes_index')
plt.ylabel('nodes_forces')
plt.title('Forces at Different nodes')
plt.xticks([i + bar_width / 2 for i in index], nodes_index)
plt.legend()
# 显示图形
plt.show()


# 创建图形
fig, ax = plt.subplots()

# 绘制各结点位移列表图
bar_width = 0.35
nodes_index = list(node_displacements.keys())
nodes_displacements = list(node_displacements.values())
index = range(len(nodes_index))
# 分离X方向和Y方向的位移
displacements_x = [displacement[0] for displacement in nodes_displacements]
displacements_y = [displacement[1] for displacement in nodes_displacements]
bar1 = plt.bar(index,displacements_x, bar_width, label='displacements_x')
bar2 = plt.bar([i + bar_width for i in index], displacements_y, bar_width, label='displacements_y')
# 添加标签和标题
plt.xlabel('nodes_index')
plt.ylabel('nodes_displacements')
plt.title('Displacements at Different nodes(L/EA)')
plt.xticks([i + bar_width / 2 for i in index], nodes_index)
plt.legend()
# 显示图形
plt.show()