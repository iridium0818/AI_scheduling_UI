from typing import Dict, Optional
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QFileDialog, QScrollArea, QTextEdit, QDialog, QFormLayout,
    QTableWidget, QTableWidgetItem, QHeaderView, QMessageBox
)
from PySide6.QtCore import Qt
from yaml_ScheduleDataManager import ScheduleDataManager


class SchedulingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.line_edits = {}  # 初始化字典
        self.product_table = None  # 初始化表格
        self.scheduling_result_text = None  # 初始化文本编辑框
        self.init_ui()  # 然后在init_ui中创建实际对象

    def init_ui(self):
        main_layout = QVBoxLayout()

        # 创建一个水平布局来放置排班参数输入框和产品参数输入框
        input_horizontal_layout = QHBoxLayout()

        # 排班参数输入框
        input_group = QGroupBox("排班参数输入")
        input_layout = QVBoxLayout()
        input_layout.setContentsMargins(10, 20, 10, 10)

        params = [
            (" 一周工作总时间 ", "total_work_hours"),
            (" 白班时间 ", "day_shift_hours"),
            (" 夜班时间 ", "night_shift_hours")
        ]

        # 创建属性以便后续访问
        self.line_edits = {}

        for label_text, field_name in params:
            row_layout = QHBoxLayout()
            label = QLabel(label_text)
            line_edit = QLineEdit("0")
            self.line_edits[field_name] = line_edit  # 保存引用
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
        self.product_table.setHorizontalHeaderLabels(["P/N", "产品产量"])
        self.product_table.setStyleSheet("""
            QTableWidget::item {
                padding: 5px;
            }
            QTableCornerButton::section, QHeaderView::section {
                background-color: #e8f0fe;
                padding: 5px;
            }
        """)
        self.product_table.verticalHeader().setStyleSheet("""
            QHeaderView::section {
                background-color: #e8f0fe;
                padding: 5px;
                font-size: 12px;
                text-align: center;
            }
        """)
        self.product_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.product_table.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.product_table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

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
        output_layout.addWidget(scroll_area)
        output_group.setLayout(output_layout)
        main_layout.addWidget(output_group)

        # 按钮布局
        button_layout = QHBoxLayout()

        generate_button = QPushButton("生成排班结果")
        generate_button.clicked.connect(self.generate_scheduling_result)
        button_layout.addWidget(generate_button)

        save_button = QPushButton("保存参数配置")
        save_button.clicked.connect(self.save_to_file)
        button_layout.addWidget(save_button)

        load_button = QPushButton("加载参数配置")
        load_button.clicked.connect(self.load_from_file)
        button_layout.addWidget(load_button)

        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

    def get_current_data(self) -> Optional[Dict]:
        """从界面收集当前数据并返回字典"""
        try:
            data = {
                'total_work_hours': float(self.line_edits['total_work_hours'].text()),
                'day_shift_hours': float(self.line_edits['day_shift_hours'].text()),
                'night_shift_hours': float(self.line_edits['night_shift_hours'].text()),
                'demands': []
            }

            # 收集产品需求数据
            for row in range(self.product_table.rowCount()):
                p_n = self.product_table.item(row, 0).text()
                demand = float(self.product_table.item(row, 1).text())
                data['demands'].append({
                    'P_N': p_n,
                    'demand': demand
                })

            return data
        except ValueError:
            QMessageBox.warning(self, "输入错误", "请输入有效的数字")
            return None

    def save_to_file(self):
        """保存当前数据到文件"""
        data = self.get_current_data()
        if not data:
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存排班数据", "", "YAML文件 (*.yaml *.yml)")

        if file_path:
            if ScheduleDataManager.save_to_yaml(data, file_path):
                # 创建自定义消息框
                msg_box = QMessageBox(self)
                msg_box.setWindowTitle("提示")
                msg_box.setText("排班数据保存成功!")
                msg_box.setIcon(QMessageBox.Icon.Information)

                # 设置消息框整体样式
                msg_box.setStyleSheet("""
                    /* 主消息框样式 */
                    QMessageBox {
                        background-color: #e8f0fe;
                        font-family: "Microsoft YaHei";
                        min-width: 300px;
                        min-height: 150px;
                        padding: 15px;
                    }

                    /* 图标容器样式 */
                    QMessageBox QLabel#qt_msgboxex_icon_label {
                        padding-left: 10px;  /* 图标左内边距 */
                    }

                    /* 消息文本标签样式 */
                    QMessageBox QLabel#qt_msgbox_label {
                        color: #000;
                        font-size: 14px;
                        margin: 10px 10px 10px 20px;  /* 上右下左，增加左边距 */
                        padding-left: 5px;  /* 文字左内边距 */
                    }

                    /* 按钮默认状态样式 */
                    QMessageBox QPushButton {
                        background-color: #367fa9;
                        color: white;
                        border: 1px solid #2a5f7f;
                        border-radius: 3px;
                        padding: 3px 10px;
                        min-width: 50px;
                        min-height: 20px;
                        font-size: 12px;
                        margin: 5px;
                    }

                    /* 按钮悬停状态样式 */
                    QMessageBox QPushButton:hover {
                        background-color: #285f7f;
                        border: 1px solid #1e4a63;
                    }

                    /* 按钮按下状态样式 */
                    QMessageBox QPushButton:pressed {
                        background-color: #1e4a63;
                    }
                """)

                # 获取按钮
                msg_box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
                msg_box.exec()

    def load_from_file(self):
        """从文件加载数据到界面"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载排班数据", "", "YAML文件 (*.yaml *.yml)")

        if file_path:
            data = ScheduleDataManager.load_from_yaml(file_path)
            if data:
                self.load_data_to_ui(data)

    def load_data_to_ui(self, data: Dict):
        """将数据加载到界面"""
        # 设置工作时间
        self.line_edits['total_work_hours'].setText(str(data['total_work_hours']))
        self.line_edits['day_shift_hours'].setText(str(data['day_shift_hours']))
        self.line_edits['night_shift_hours'].setText(str(data['night_shift_hours']))

        # 清空并重新填充产品表
        self.product_table.setRowCount(0)
        for demand in data['demands']:
            row = self.product_table.rowCount()
            self.product_table.insertRow(row)
            self.product_table.setItem(row, 0, QTableWidgetItem(demand['P_N']))
            self.product_table.setItem(row, 1, QTableWidgetItem(str(demand['demand'])))

    def open_add_product_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("设置产品参数")
        dialog.setStyleSheet("""
            QDialog {
                background-color: #e8f0fe;
            }
            QLineEdit {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 3px;
                padding: 3px;
                min-width: 150px;
                color: black;
                font-size: 14px;
                font-family: "Microsoft YaHei";
            }
            QLabel {
                font-size: 14px;
                color: #000;
            }
        """)

        layout = QFormLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        product_name_input = QLineEdit()
        quantity_input = QLineEdit()

        layout.addRow("P/N:", product_name_input)
        layout.addRow("产品产量:", quantity_input)

        confirm_button = QPushButton("确定")

        confirm_button.clicked.connect(
            lambda: self.add_product(product_name_input.text(), quantity_input.text(), dialog))
        layout.addWidget(confirm_button)

        dialog.exec()

    def add_product(self, name, quantity, dialog):
        try:
            if name and quantity:
                float(quantity)  # 验证是否为数字
                row_position = self.product_table.rowCount()
                self.product_table.insertRow(row_position)
                self.product_table.setItem(row_position, 0, QTableWidgetItem(name))
                self.product_table.setItem(row_position, 1, QTableWidgetItem(quantity))
                dialog.close()
        except ValueError:
            QMessageBox.warning(dialog, "输入错误", "请输入有效的数字")

    def open_delete_product_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("删除产品参数")
        dialog.setStyleSheet("""
                    QDialog {
                        background-color: #e8f0fe;
                    }
                    QLineEdit {
                        background-color: white;
                        border: 1px solid #ccc;
                        border-radius: 3px;
                        padding: 5px;
                        min-width: 150px;
                        color: black;
                        font-size: 14px;
                        font-family: "Microsoft YaHei";
                    }
                    QLabel {
                        font-size: 14px;
                        color: #000;
                    }
                """)

        layout = QFormLayout(dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        product_name_input = QLineEdit()
        layout.addRow("P/N:", product_name_input)

        confirm_button = QPushButton("确定")

        confirm_button.clicked.connect(
            lambda: self.delete_product(product_name_input.text(), dialog))
        layout.addWidget(confirm_button)

        dialog.exec()

    def delete_product(self, name, dialog):
        for row in range(self.product_table.rowCount()):
            item = self.product_table.item(row, 0)
            if item and item.text() == name:
                self.product_table.removeRow(row)
                break
        dialog.close()

    def generate_scheduling_result(self):
        data = self.get_current_data()
        if not data:
            return

        # 这里只是示例，实际应根据排班算法生成结果
        result_text = "排班结果：\n\n"
        result_text += f"总工作时间: {data['total_work_hours']} 小时\n"
        result_text += f"白班时间: {data['day_shift_hours']} 小时\n"
        result_text += f"夜班时间: {data['night_shift_hours']} 小时\n\n"
        result_text += "产品需求:\n"

        for demand in data['demands']:
            result_text += f"- {demand['P_N']}: {demand['demand']} 件\n"

        self.scheduling_result_text.setText(result_text)