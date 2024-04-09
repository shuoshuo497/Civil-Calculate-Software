import sys  # 导入系统模块
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, \
    QMainWindow  # 导入PyQt5模块

# 模拟用户数据库
users = {}


class MainWindow(QWidget):  # 主页面类
    def __init__(self, username):
        super().__init__()

        self.setWindowTitle("Main Page")  # 设置主页面标题
        self.setGeometry(900, 500, 650, 550)  # 设置窗口位置和大小

        self.show()  # 确保主页面在创建时就显示出来

        layout = QVBoxLayout()  # 创建垂直布局

        welcome_label = QLabel("Welcome, " + username + "!")  # 创建欢迎标签
        layout.addWidget(welcome_label)  # 将欢迎标签添加到布局中

        self.logout_button = QPushButton("Logout")  # 创建注销按钮
        self.logout_button.clicked.connect(self.close)  # 连接按钮点击事件到关闭窗口方法
        layout.addWidget(self.logout_button)  # 将注销按钮添加到布局中

        self.setLayout(layout)  # 设置布局


class LoginWindow(QWidget):  # 登录页面类
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")  # 设置登录页面标题

        layout = QVBoxLayout()  # 创建垂直布局

        self.username_label = QLabel("Username:")  # 创建用户名标签
        layout.addWidget(self.username_label)  # 将用户名标签添加到布局中

        self.username_input = QLineEdit()  # 创建用户名输入框
        layout.addWidget(self.username_input)  # 将用户名输入框添加到布局中

        self.password_label = QLabel("Password:")  # 创建密码标签
        layout.addWidget(self.password_label)  # 将密码标签添加到布局中

        self.password_input = QLineEdit()  # 创建密码输入框
        self.password_input.setEchoMode(QLineEdit.Password)  # 设置密码输入框为密码模式
        layout.addWidget(self.password_input)  # 将密码输入框添加到布局中

        self.login_button = QPushButton("Login")  # 创建登录按钮
        self.login_button.clicked.connect(self.login)  # 连接按钮点击事件到登录方法
        layout.addWidget(self.login_button)  # 将登录按钮添加到布局中

        self.register_button = QPushButton("Register")  # 创建注册按钮
        self.register_button.clicked.connect(self.register)  # 连接按钮点击事件到注册方法
        layout.addWidget(self.register_button)  # 将注册按钮添加到布局中

        self.setLayout(layout)  # 设置布局
        self.adjustSize()  # 调整窗口大小

    def login(self):  # 登录方法
        username = self.username_input.text()  # 获取用户名输入框的文本
        password = self.password_input.text()  # 获取密码输入框的文本
        if username in users and users[username] == password:  # 如果用户名在用户数据库中且密码正确
            self.hide()  # 隐藏登录页面
            self.main_window = MainWindow(username)  # 创建主页面
            self.main_window.show()  # 显示主页面
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")

    def register(self):
        username = self.username_input.text()  # 获取用户名输入框的文本
        password = self.password_input.text()  # 获取密码输入框的文本
        if username in users:
            QMessageBox.warning(self, "Registration Failed",
                                "Username already exists. Please choose another username.")  # 如果用户名已存在
        else:
            users[username] = password
            QMessageBox.information(self, "Registration Successful", "User registered successfully!")  # 注册成功


if __name__ == "__main__":  # 如果运行的是当前脚本
    app = QApplication(sys.argv)  # 创建应用程序
    window = LoginWindow()  # 创建登录页面
    window.show()  # 显示登录页面
    sys.exit(app.exec_())  # 运行应用程序

