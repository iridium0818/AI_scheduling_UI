import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget
)
from PySide6 import QtGui
from SchedulingPage import SchedulingPage
from ModelTrainingPage import ModelTrainingPage
from ManagementPage import ManagementPage

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('智能排班系统')
        self.setMinimumSize(800, 600)  # 改为不是固定尺寸

        # 创建 QTabWidget 用于切换界面
        self.tab_widget = QTabWidget()

        # 创建页面并添加到 QTabWidget
        self.model_training_page = ModelTrainingPage()
        self.management_page = ManagementPage()
        self.scheduling_page = SchedulingPage()

        self.tab_widget.addTab(self.model_training_page, "模型训练界面")
        self.tab_widget.addTab(self.scheduling_page, "排班界面")
        self.tab_widget.addTab(self.management_page, "管理界面")

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)  # 设置边距
        self.setLayout(main_layout)

        # 应用美化样式
        self.apply_stylesheet()

    def apply_stylesheet(self):
        self.setStyleSheet('''
            QWidget {
                background-color: #e8f0fe;
            }
            QGroupBox {
                background-color: white;
                border: 1px solid #367fa9;
                border-radius: 5px;
                margin-top: 10px;
            }
            QGroupBox::title {
                subcontrol-origin: padding;
                subcontrol-position: top left;
                padding: 0 5px;
                color: #32779f;
            }
            QLabel {
                color: #32779f;
            }
            QLineEdit {
                background: #e8f0fe;
                height: 30px;
                border: none;
                color: #32779f;
            }
            QPushButton {
                height: 30px;
                background: #367fa9;
                color: white;
                border: 1px solid #367fa9;
                border-radius: 5px;
            }
            QPushButton:hover {
                background: #285f7f;
            }
            QTabWidget::pane {
                border: none;
            }
            QTabBar::tab {
                background: #e8f0fe;
                color: #32779f;
                padding: 5px 10px;
            }
            QTabBar::tab:selected {
                background: white;
                border: 1px solid #367fa9;
                border-bottom: none;
            }
        ''')

if __name__ == "__main__":
    app = QApplication(sys.argv)

    pixmap_logo = QtGui.QPixmap('icons/logo.png')
    app.setWindowIcon(pixmap_logo)

    mw = MainWindow()
    mw.showMinimized()  # 初始以最小化窗口显示

    sys.exit(app.exec())