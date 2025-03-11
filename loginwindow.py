from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QLabel, \
    QLineEdit, QPushButton
from PySide6 import QtGui, QtCore
import main  # 导入主界面所在的模块

app = QApplication([])

pixmap_logo = QtGui.QPixmap('icons/logo.png')
app.setWindowIcon(pixmap_logo)


class LoginWindow(QFrame):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('智能排班系统 - 登录')
        self.setFixedSize(800, 600)

        self.setStyleSheet('''background: #e7ebf2;''')

        layout = QHBoxLayout(self)

        layout.addStretch()  # layout 开头 `addStretch`

        layout_1 = QVBoxLayout()  # 垂直布局
        layout.addLayout(layout_1)

        layout_1.addStretch(1)
        # 公司名称，logo
        layout_1.addLayout(self.titleLayout())

        layout_1.addSpacing(20)
        # 登录输入框
        layout_1.addWidget(self.loginBox())

        layout_1.addStretch(2)

        layout.addStretch()  # layout 结尾 `addStretch`

    def titleLayout(self):
        layout = QHBoxLayout()

        layout.addStretch(2)

        label = QLabel()
        # 设置label显示的pixmap
        # label.setPixmap(pixmap_logo.scaledToWidth(55, QtCore.Qt.SmoothTransformation))
        layout.addWidget(label)

        layout.addSpacing(20)

        label = QLabel('智能排班系统')

        label.setStyleSheet('font-family: 微软雅黑;font-size:30px;color:#32779f;font-weight:bold')
        layout.addWidget(label)

        layout.addStretch(3)

        return layout

    def loginBox(self):
        box = QFrame()
        box.setStyleSheet(
            '''
           .QFrame {background: white}

            * {    
                font-family: consolas, 微软雅黑 ;
                font-size:15px;
            }  

            QLineEdit{    
                background: #e8f0fe;
                height: 30px;  
                border: none;
                color: #32779f;
            }

            QPushButton{  
                height: 30px;  
                background: #367fa9;
                color:white;    
                border: 1px solid #367fa9;
            }

            ''')

        box.setFixedWidth(360)

        layout = QVBoxLayout(box)
        layout.setContentsMargins(30, 10, 30, 30)  # 左、上、右、下

        layout.addSpacing(16)

        label = QLabel('输入账号、密码登录')
        label.setStyleSheet('font-size:14px;color:#666;background:white')
        layout.addWidget(label, alignment=QtGui.Qt.AlignCenter)

        layout.addSpacing(16)

        username = QLineEdit('')
        username.setAlignment(QtGui.Qt.AlignCenter)  # 居中
        username.addAction(QtGui.QIcon('icons/icon-user.png'), QLineEdit.LeadingPosition)
        layout.addWidget(username)

        layout.addSpacing(10)

        password = QLineEdit('')
        password.setAlignment(QtGui.Qt.AlignCenter)
        password.addAction(QtGui.QIcon('icons/icon-passwd.png'), QLineEdit.LeadingPosition)
        password.setEchoMode(QLineEdit.Password)  # 密码遮掩
        layout.addWidget(password)

        layout.addSpacing(20)

        okBtn = QPushButton('登录')
        okBtn.clicked.connect(self.show_main_window)  # 连接点击信号到槽函数
        layout.addWidget(okBtn)

        return box

    def show_main_window(self):
        self.main_window = main.MainWindow()  # 创建主界面实例
        self.main_window.show()  # 显示主界面
        self.hide()  # 隐藏登录界面


lw = LoginWindow()
lw.show()

app.exec()