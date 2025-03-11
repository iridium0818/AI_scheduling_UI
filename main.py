import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QFileDialog, QTabWidget, QScrollArea, QTextEdit, QDialog, QFormLayout,
    QTableWidget, QTableWidgetItem, QSizePolicy, QHeaderView
)
from PySide6.QtCore import Qt
from PySide6 import QtGui


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('智能排班系统')
        self.setFixedSize(800, 600)

        # 创建 QTabWidget 用于切换界面
        self.tab_widget = QTabWidget()

        # 创建页面并添加到 QTabWidget
        self.model_training_page = ModelTrainingPage()
        self.employee_management_page = EmployeeManagementPage()
        self.scheduling_page = SchedulingPage()

        self.tab_widget.addTab(self.model_training_page, "模型训练界面")
        self.tab_widget.addTab(self.scheduling_page, "排班界面")
        self.tab_widget.addTab(self.employee_management_page, "员工管理界面")

        # 主布局
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tab_widget)
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


class ModelTrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        top_left_layout = self.create_project_path_group()
        top_right_layout = self.create_param_group()

        top_layout = QHBoxLayout()
        top_layout.addWidget(top_left_layout)
        top_layout.addWidget(top_right_layout)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.create_log_group())

        self.setLayout(main_layout)

    def create_project_path_group(self):
        group_box = QGroupBox("项目文件路径设置")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        paths = [" 项目路径 ", " 数据集路径 ", " 模型文件保存路径 ", " train.py路径 "]
        for path in paths:
            h_layout = QHBoxLayout()
            label = QLabel(path)
            line_edit = QLineEdit()
            button = QPushButton(" 选择路径 ")
            button.clicked.connect(lambda _, le=line_edit: self.select_file(le))
            h_layout.addWidget(label)
            h_layout.addWidget(line_edit)
            h_layout.addWidget(button)
            layout.addLayout(h_layout)
        group_box.setLayout(layout)
        return group_box

    def select_file(self, line_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "所有文件 (*.*)")
        if file_path:
            line_edit.setText(file_path)

    def create_param_group(self):
        group_box = QGroupBox("参数设置")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)

        params = [
            (" Epochs ", "10"), (" Batch Size ", "1"), (" Learning Rate ", "0"), (" demand ", "10"),
            (" product ", "10"), (" workflow ", "6"), (" workers ", "2"), (" Equipment number ", "0")
        ]

        for i in range(0, len(params), 2):
            row_layout = QHBoxLayout()
            if i < len(params):
                param1, default_value1 = params[i]
                label1 = QLabel(param1)
                line_edit1 = QLineEdit(default_value1)
                row_layout.addWidget(label1)
                row_layout.addWidget(line_edit1)
            if i + 1 < len(params):
                param2, default_value2 = params[i + 1]
                label2 = QLabel(param2)
                line_edit2 = QLineEdit(default_value2)
                row_layout.addWidget(label2)
                row_layout.addWidget(line_edit2)
            layout.addLayout(row_layout)

        start_button = QPushButton("开始")
        stop_button = QPushButton("停止")
        exit_button = QPushButton("退出")
        layout.addWidget(start_button)
        layout.addWidget(stop_button)
        layout.addWidget(exit_button)
        group_box.setLayout(layout)
        return group_box

    def create_log_group(self):
        group_box = QGroupBox("结果输出")
        layout = QVBoxLayout()
        layout.setContentsMargins(10, 20, 10, 10)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("background-color: #e8f0fe;")
        self.log_text.setPlaceholderText("结果将在此显示...")

        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.log_text)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setStyleSheet("""
                            QScrollBar:vertical {
                                border: none;
                                background: #e8f0fe;
                                width: 10px;
                                margin: 5px 0px 5px 0px;
                            }
                            QScrollBar::handle:vertical {
                                background: #367fa9;
                                min-height: 20px;
                                border-radius: 5px;
                            }
                            QScrollBar::handle:vertical:hover {
                                background: #285f7f;
                            }
                            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                                border: none;
                                background: none;
                            }
                        """)

        # 将滚动区域添加到布局中
        layout.addWidget(scroll_area)
        group_box.setLayout(layout)
        return group_box


class EmployeeManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 定义多个参数组
        param_groups = [
            [
                (" total demands ", "10"), (" workers ", "2"),
                (" day shift time ", "10"), (" night shift time ", "6")
            ],
            [
                (" total demands ", "10"), (" workers ", "2"),
                (" day shift time ", "10"), (" night shift time ", "6")
            ],
            [
                (" total demands ", "10"), (" workers ", "2"),
                (" day shift time ", "10"), (" night shift time ", "6")
            ],
            [
                (" total demands ", "10"), (" workers ", "2"),
                (" day shift time ", "10"), (" night shift time ", "6")
            ]
        ]

        titles = ["员工增添/删减", "拉线增添/删减", "员工修改", "本周生产情况修改"]

        # 循环创建多个排班参数输入框
        for params, title in zip(param_groups, titles):
            input_group = self.create_input_group(params, title)
            main_layout.addWidget(input_group)

        self.setLayout(main_layout)

    def create_input_group(self, params, title):
        input_group = QGroupBox(title)
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(10, 20, 10, 10)

        for i in range(0, len(params), 2):
            row_layout = QHBoxLayout()
            if i < len(params):
                param1, default_value1 = params[i]
                label1 = QLabel(param1)
                line_edit1 = QLineEdit(default_value1)
                row_layout.addWidget(label1)
                row_layout.addWidget(line_edit1)
            if i + 1 < len(params):
                param2, default_value2 = params[i + 1]
                label2 = QLabel(param2)
                line_edit2 = QLineEdit(default_value2)
                row_layout.addWidget(label2)
                row_layout.addWidget(line_edit2)
            input_layout.addLayout(row_layout)

        input_group.setLayout(input_layout)
        return input_group



class SchedulingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 创建一个水平布局来放置排班参数输入框和产品参数输入框
        input_horizontal_layout = QHBoxLayout()

        # 排班参数输入框
        input_group = QGroupBox("排班参数输入")
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(10, 20, 10, 10)

        params = [
            (" total demands ", "10"), (" workers ", "2"),
            (" day shift time ", "10"), (" night shift time ", "6")
        ]

        for param, default_value in params:
            row_layout = QHBoxLayout()
            label = QLabel(param)
            line_edit = QLineEdit(default_value)
            row_layout.addWidget(label)
            row_layout.addWidget(line_edit)
            input_layout.addLayout(row_layout)

        input_group.setLayout(input_layout)
        input_horizontal_layout.addWidget(input_group)

        # 产品参数输入框
        product_group = QGroupBox("产品参数输入")
        product_layout = QHBoxLayout()
        product_layout.setContentsMargins(10, 20, 10, 10)

        self.product_table = QTableWidget()
        self.product_table.setColumnCount(2)
        self.product_table.setHorizontalHeaderLabels(["  P/N  ", "  产品产量  "])
        self.product_table.setStyleSheet("background-color: #e8f0fe;")

        # 设置表格的列宽自适应内容
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        # 隐藏垂直滚动条
        self.product_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 隐藏水平滚动条
        self.product_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # 将表格添加到布局中
        product_layout.addWidget(self.product_table)

        button_layout = QVBoxLayout()

        add_product_button = QPushButton(" 添加产品 ")
        add_product_button.clicked.connect(self.open_add_product_dialog)
        button_layout.addWidget(add_product_button)

        delete_product_button = QPushButton(" 删除产品 ")
        delete_product_button.clicked.connect(self.open_delete_product_dialog)
        button_layout.addWidget(delete_product_button)

        product_layout.addLayout(button_layout)
        product_group.setLayout(product_layout)
        input_horizontal_layout.addWidget(product_group)

        # 将水平布局添加到主垂直布局
        main_layout.addLayout(input_horizontal_layout)

        # 排班结果输出框
        output_group = QGroupBox("排班结果输出")
        output_layout = QVBoxLayout()
        output_layout.setContentsMargins(10, 20, 10, 10)

        self.scheduling_result_text = QTextEdit()
        self.scheduling_result_text.setReadOnly(True)
        self.scheduling_result_text.setStyleSheet("background-color: #e8f0fe;")
        self.scheduling_result_text.setPlaceholderText("排班结果将在此显示...")

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.scheduling_result_text)
        scroll_area.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        scroll_area.setStyleSheet("""
                    QScrollBar:vertical {
                        border: none;
                        background: #e8f0fe;
                        width: 10px;
                        margin: 5px 0px 5px 0px;
                    }
                    QScrollBar::handle:vertical {
                        background: #367fa9;
                        min-height: 20px;
                        border-radius: 5px;
                    }
                    QScrollBar::handle:vertical:hover {
                        background: #285f7f;
                    }
                    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                        border: none;
                        background: none;
                    }
                """)
        output_layout.addWidget(scroll_area)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # 生成排班结果按钮
        generate_button = QPushButton("生成排班结果")
        generate_button.clicked.connect(self.generate_scheduling_result)
        main_layout.addWidget(generate_button)

        self.setLayout(main_layout)

    def open_add_product_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("设置产品参数")
        layout = QFormLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        product_name_label = QLabel("P/N")
        product_name_label.setStyleSheet("font-size: 14px; color: #333;")
        product_name_input = QLineEdit()
        product_name_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        layout.addRow(product_name_label, product_name_input)

        quantity_label = QLabel("产品产量")
        quantity_label.setStyleSheet("font-size: 14px; color: #333;")
        quantity_input = QLineEdit()
        quantity_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        layout.addRow(quantity_label, quantity_input)

        confirm_button = QPushButton("确定")
        confirm_button.setStyleSheet("""
                    background-color: #367fa9;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 3px;
                """)
        confirm_button.clicked.connect(
            lambda: self.add_product(product_name_input.text(), quantity_input.text(), dialog))
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: #f9f9f9;")
        dialog.exec()

    def add_product(self, name, quantity, dialog):
        if name and quantity:
            row_position = self.product_table.rowCount()
            self.product_table.insertRow(row_position)
            self.product_table.setItem(row_position, 0, QTableWidgetItem(name))
            self.product_table.setItem(row_position, 1, QTableWidgetItem(quantity))
        dialog.close()

    def open_delete_product_dialog(self):
        dialog = QDialog()
        dialog.setWindowTitle("删除产品参数")
        layout = QFormLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        product_name_label = QLabel("P/N")
        product_name_label.setStyleSheet("font-size: 14px; color: #333;")
        product_name_input = QLineEdit()
        product_name_input.setStyleSheet("padding: 5px; border: 1px solid #ccc; border-radius: 3px;")
        layout.addRow(product_name_label, product_name_input)

        confirm_button = QPushButton("确定")
        confirm_button.setStyleSheet("""
                    background-color: #367fa9;
                    color: white;
                    padding: 8px 16px;
                    border: none;
                    border-radius: 3px;
                """)
        confirm_button.clicked.connect(
            lambda: self.delete_product(product_name_input.text(), dialog))
        layout.addWidget(confirm_button)

        dialog.setLayout(layout)
        dialog.setStyleSheet("background-color: #f9f9f9;")
        dialog.exec()

    def delete_product(self, name, dialog):
        for row in range(self.product_table.rowCount()):
            item = self.product_table.item(row, 0)
            if item and item.text() == name:
                self.product_table.removeRow(row)
                break
        dialog.close()

    def generate_scheduling_result(self):
        self.scheduling_result_text.setText(
            "排班结果：\n\n- 员工A:  \n- 员工B:  \n- 员工C:  \n...\n(测试文本)"
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)

    pixmap_logo = QtGui.QPixmap('icons/logo.png')
    app.setWindowIcon(pixmap_logo)

    mw = MainWindow()
    mw.show()

    sys.exit(app.exec())