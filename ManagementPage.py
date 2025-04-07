from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QScrollArea, QDialog, QFormLayout,
    QTableWidget, QHeaderView, QLineEdit, QMessageBox,
    QTableWidgetItem, QFileDialog, QAbstractScrollArea, QLabel
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QDoubleValidator
from typing import Dict, List
from yaml_ManagementDataManager import YamlManager

class ManagementPage(QWidget):
    def __init__(self):
        super().__init__()
        # Store references to all tables
        self.employee_table = None
        self.line_table = None
        self.special_station_table = None
        self.production_table = None
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()

        # Add Excel file selection box at the top
        excel_group = self.create_excel_selection_group()
        main_layout.addWidget(excel_group)

        # 定义标题
        titles = ["员工增添", "拉线增添", "特殊工位", "生产情况"]

        # 创建两行布局
        row1_layout = QHBoxLayout()
        row2_layout = QHBoxLayout()

        # 循环创建多个组
        for i, title in enumerate(titles):
            scroll_area = self.create_scrollable_group(title)
            if title == "生产情况":
                row2_layout.addWidget(scroll_area)
                row2_layout.setStretch(0, 1)
            else:
                row1_layout.addWidget(scroll_area)
                stretch_factor = 1 if title == "员工增添" else 1
                row1_layout.setStretch(i, stretch_factor)

        main_layout.addLayout(row1_layout)
        main_layout.addLayout(row2_layout)

        # 添加保存/加载按钮
        control_layout = QHBoxLayout()
        save_button = QPushButton("保存配置")
        load_button = QPushButton("加载配置")

        save_button.clicked.connect(self.save_config)
        load_button.clicked.connect(self.load_config)

        control_layout.addWidget(save_button)
        control_layout.addWidget(load_button)
        main_layout.addLayout(control_layout)

        self.setLayout(main_layout)

    def create_excel_selection_group(self):
        """创建Excel文件选择组"""
        group = QGroupBox()
        layout = QHBoxLayout()

        # 文件路径显示
        self.file_path_label = QLabel()
        self.file_path_label.setStyleSheet("""
            QLabel {
                color: #666;
                font-size: 12px;
                border: 1px solid #ccc;
                padding: 5px;
                min-width: 200px;
            }
        """)

        # 选择文件按钮
        select_button = QPushButton("选择Excel文件")
        select_button.setFixedSize(120, 30)
        select_button.clicked.connect(self.select_excel_file)

        # 导入按钮
        import_button = QPushButton("导入数据")
        import_button.setFixedSize(100, 30)
        import_button.clicked.connect(self.import_excel_data)

        layout.addWidget(self.file_path_label)
        layout.addWidget(select_button)
        layout.addWidget(import_button)

        group.setLayout(layout)
        return group

    def select_excel_file(self):
        """选择Excel文件"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择Excel文件", "", "Excel文件 (*.xlsx *.xls)"
        )
        if file_path:
            self.file_path_label.setText(file_path)
            self.file_path_label.setToolTip(file_path)

    def import_excel_data(self):
        """导入Excel数据"""
        file_path = self.file_path_label.text()
        if file_path == "未选择文件":
            QMessageBox.warning(self, "警告", "请先选择Excel文件")
            return

        try:
            # TODO: 实现Excel数据导入逻辑
            # 这里可以调用你的Excel导入函数
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Icon.Information)
            msg_box.setWindowTitle("提示")
            msg_box.setText("Excel数据导入成功！")
            msg_box.addButton(QMessageBox.StandardButton.Ok)
            msg_box.exec()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"导入失败: {str(e)}")

    def show_custom_message(self, title, text, icon):
        """显示统一风格的自定义消息框"""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(text)
        msg_box.setIcon(icon)

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
                padding: 5px 15px;
                min-width: 80px;
                min-height: 30px;
                font-size: 14px;
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

        # 添加确定按钮并调整大小
        ok_button = msg_box.addButton("确定", QMessageBox.ButtonRole.AcceptRole)
        ok_button.setFixedSize(100, 35)  # 固定按钮大小
        msg_box.exec()

    def create_scrollable_group(self, title):
        """创建可滚动的表格组"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        container = QWidget()
        layout = QVBoxLayout(container)

        input_group = self.create_input_group(title)
        layout.addWidget(input_group)
        scroll.setWidget(container)

        return scroll

    def create_input_group(self, title):
        input_group = QGroupBox(title)

        # 根据标题设置表头
        headers = self.get_table_headers(title)
        table = self.create_table(headers)

        # Store table reference based on type
        if title == "员工增添":
            self.employee_table = table
        elif title == "拉线增添":
            self.line_table = table
        elif title == "特殊工位":
            self.special_station_table = table
        elif title == "生产情况":
            self.production_table = table

        # 创建按钮
        button_layout = QHBoxLayout() if title != "生产情况" else QVBoxLayout()
        add_button = QPushButton("添加")
        delete_button = QPushButton("删除")

        # Connect buttons to appropriate functions
        if title == "员工增添":
            add_button.clicked.connect(self.open_add_employee_dialog)
            delete_button.clicked.connect(self.delete_employee)
        elif title == "拉线增添":
            add_button.clicked.connect(self.open_add_line_dialog)
            delete_button.clicked.connect(self.delete_line)
        elif title == "特殊工位":
            add_button.clicked.connect(self.open_add_special_station_dialog)
            delete_button.clicked.connect(self.delete_special_station)
        elif title == "生产情况":
            add_button.clicked.connect(self.open_add_production_dialog)
            delete_button.clicked.connect(self.delete_production)

        # 设置按钮大小 - 只在"生产情况"时增大按钮
        if title == "生产情况":
            add_button.setFixedSize(80, 30)
            delete_button.setFixedSize(80, 30)
        else:
            add_button.setFixedSize(80, 30)
            delete_button.setFixedSize(80, 30)

        button_layout.addWidget(add_button)
        button_layout.addWidget(delete_button)

        # 设置布局
        if title == "生产情况":
            input_layout = QHBoxLayout()
            input_layout.addWidget(table)
            input_layout.addLayout(button_layout)
            input_layout.setSpacing(20)  # 增加表格和按钮之间的间距
        else:
            input_layout = QVBoxLayout()
            input_layout.addWidget(table)
            input_layout.addLayout(button_layout)

        input_layout.setContentsMargins(10, 20, 10, 10)
        input_group.setLayout(input_layout)
        return input_group

    @staticmethod
    def get_table_headers(title):
        """根据标题返回对应的表头"""
        if title == "员工增添":
            return ["工号", "姓名", "设备编号", "P/N", "工位", "基础产出"]
        elif title == "拉线增添":
            return ["P/N", "设备编号", "所需工位"]
        elif title == "生产情况":
            return ["排班批次", "日期", "班次", "P/N", "设备", "姓名", "产出", "工时"]
        elif title == "特殊工位":
            return ["特殊工位类型"]
        return []

    @staticmethod
    def create_table(headers):
        """创建表格并优化列宽分配"""
        table = QTableWidget()
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)

        # 设置表格属性
        table.setSizeAdjustPolicy(QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents)
        table.horizontalHeader().setDefaultSectionSize(120)  # 默认列宽
        table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        table.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        # 根据表格类型应用不同的样式
        if headers[0] in ["工号", "P/N","特殊工位类型"]:  # 员工增添、拉线增添、特殊工位
            table.setStyleSheet("""
                QTableWidget {
                    font-size: 12px;
                    gridline-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #e8f0fe;
                    font-size: 12px;
                    text-align: center;
                }
                QTableCornerButton::section {
                    background-color: #e8f0fe;
                    padding: 1px;
                }
            """)
        else:  # 生产情况
            table.setStyleSheet("""
                QTableWidget {
                    font-size: 12px;
                    gridline-color: #e0e0e0;
                }
                QHeaderView::section {
                    background-color: #e8f0fe;
                    padding: 5px;
                    font-size: 12px;
                    text-align: center;
                }
                QTableCornerButton::section,QHeaderView::section{
                    background-color:#e8f0fe;
                    padding:5px;
                }
            """)

        return table

    @staticmethod
    def adjust_table_columns(table):
        """均匀分配列宽并考虑内容长度"""
        header = table.horizontalHeader()
        total_width = table.viewport().width()  # 使用视口宽度更准确

        # 生产情况表格的特殊处理
        if table.horizontalHeaderItem(0) and table.horizontalHeaderItem(0).text() == "排班批次":
            header.setStretchLastSection(True)  # 最后一列自动拉伸
            for col in range(table.columnCount() - 1):
                header.setSectionResizeMode(col, QHeaderView.ResizeMode.ResizeToContents)
        else:
            # 其他表格的原有处理方式
            char_width = 8  # 每个字符的预估像素宽度
            min_col_width = 80  # 最小列宽
            max_col_width = 200  # 最大列宽

            col_widths = []
            for col in range(table.columnCount()):
                header_text = table.horizontalHeaderItem(col).text()
                # 根据表头文本长度计算基础宽度
                base_width = len(header_text) * char_width + 20  # 加20像素边距
                # 限制在最小/最大宽度之间
                col_width = max(min(base_width, max_col_width), min_col_width)
                col_widths.append(col_width)

            # 计算总需求宽度
            total_needed = sum(col_widths)

            # 如果总宽度足够，按计算值分配
            if total_needed <= total_width:
                for col, width in enumerate(col_widths):
                    header.resizeSection(col, width)
            else:
                # 如果总宽度不足，按比例压缩
                ratio = total_width / total_needed
                for col, width in enumerate(col_widths):
                    header.resizeSection(col, int(width * ratio))

            header.setStretchLastSection(False)  # 禁用最后一列拉伸

    def open_add_employee_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加员工信息")
        dialog.setStyleSheet(self.get_dialog_stylesheet())
        layout = QFormLayout(dialog)

        # Create input fields
        id_input = QLineEdit()
        name_input = QLineEdit()
        device_input = QLineEdit()
        pn_input = QLineEdit()
        station_input = QLineEdit()
        production_input = QLineEdit()

        # Add to layout
        layout.addRow("工号:", id_input)
        layout.addRow("姓名:", name_input)
        layout.addRow("设备编号:", device_input)
        layout.addRow("P/N:", pn_input)
        layout.addRow("工位:", station_input)
        layout.addRow("基础产出:", production_input)

        confirm_button = QPushButton("确定")
        confirm_button.clicked.connect(lambda: self.add_employee(
            id_input.text(), name_input.text(), device_input.text(),
            pn_input.text(), station_input.text(), dialog
        ))
        layout.addWidget(confirm_button)

        dialog.exec()

    def add_employee(self, emp_id, name, device, pn, station, dialog):
        if not all([emp_id, name, device, pn, station]):
            QMessageBox.warning(dialog, "输入错误", "请填写所有字段")
            return

        row = self.employee_table.rowCount()
        self.employee_table.insertRow(row)
        self.employee_table.setItem(row, 0, QTableWidgetItem(emp_id))
        self.employee_table.setItem(row, 1, QTableWidgetItem(name))
        self.employee_table.setItem(row, 2, QTableWidgetItem(device))
        self.employee_table.setItem(row, 3, QTableWidgetItem(pn))
        self.employee_table.setItem(row, 4, QTableWidgetItem(station))
        dialog.close()

    def delete_employee(self):
        selected = self.employee_table.selectedItems()
        if not selected:
            self.show_custom_message("提示", "请先选择要删除的行", QMessageBox.Icon.Warning)
            return

        rows = {item.row() for item in selected}
        for row in sorted(rows, reverse=True):
            self.employee_table.removeRow(row)


    def open_add_line_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加拉线信息")
        dialog.setStyleSheet(self.get_dialog_stylesheet())
        layout = QFormLayout(dialog)

        pn_input = QLineEdit()
        device_input = QLineEdit()
        station_input = QLineEdit()

        layout.addRow("P/N:", pn_input)
        layout.addRow("设备编号:", device_input)
        layout.addRow("所需工位:", station_input)

        confirm_button = QPushButton("确定")
        confirm_button.clicked.connect(lambda: self.add_line(
            pn_input.text(), device_input.text(), station_input.text(), dialog
        ))
        layout.addWidget(confirm_button)

        dialog.exec()

    def add_line(self, pn, device, station, dialog):
        if not all([pn, device, station]):
            QMessageBox.warning(dialog, "输入错误", "请填写所有字段")
            return

        row = self.line_table.rowCount()
        self.line_table.insertRow(row)
        self.line_table.setItem(row, 0, QTableWidgetItem(pn))
        self.line_table.setItem(row, 1, QTableWidgetItem(device))
        self.line_table.setItem(row, 2, QTableWidgetItem(station))
        dialog.close()

    def delete_line(self):
        selected = self.line_table.selectedItems()
        if not selected:
            self.show_custom_message("提示", "请先选择要删除的行", QMessageBox.Icon.Warning)
            return

        rows = {item.row() for item in selected}
        for row in sorted(rows, reverse=True):
            self.line_table.removeRow(row)

    def open_add_special_station_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加特殊工位")
        dialog.setStyleSheet(self.get_dialog_stylesheet())
        layout = QFormLayout(dialog)

        station_input = QLineEdit()
        layout.addRow("特殊工位类型:", station_input)

        confirm_button = QPushButton("确定")
        confirm_button.clicked.connect(lambda: self.add_special_station(
            station_input.text(), dialog
        ))
        layout.addWidget(confirm_button)

        dialog.exec()

    def add_special_station(self, station_type, dialog):
        if not station_type:
            QMessageBox.warning(dialog, "输入错误", "请输入特殊工位类型")
            return

        row = self.special_station_table.rowCount()
        self.special_station_table.insertRow(row)
        self.special_station_table.setItem(row, 0, QTableWidgetItem(station_type))
        dialog.close()

    def delete_special_station(self):
        selected = self.special_station_table.selectedItems()
        if not selected:
            self.show_custom_message("提示", "请先选择要删除的行", QMessageBox.Icon.Warning)
            return

        rows = {item.row() for item in selected}
        for row in sorted(rows, reverse=True):
            self.special_station_table.removeRow(row)

    def open_add_production_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("添加生产情况")
        dialog.setStyleSheet(self.get_dialog_stylesheet())
        layout = QFormLayout(dialog)

        # 创建带提示语的输入框
        batch_input = self._create_line_edit_with_placeholder("请输入排班批次")
        date_input = self._create_line_edit_with_placeholder("请输入日期")
        shift_input = self._create_line_edit_with_placeholder("请输入：白班/夜班")
        pn_input = self._create_line_edit_with_placeholder("请输入P/N")
        device_input = self._create_line_edit_with_placeholder("请输入设备编号")
        name_input = self._create_line_edit_with_placeholder("请输入姓名")
        output_input = self._create_line_edit_with_placeholder("请输入产出数量")
        hours_input = self._create_line_edit_with_placeholder("请输入工作时长(小时)")

        # 设置数字输入框的验证器
        output_input.setValidator(QDoubleValidator())
        hours_input.setValidator(QDoubleValidator())

        layout.addRow("排班批次:", batch_input)
        layout.addRow("日期:", date_input)
        layout.addRow("班次:", shift_input)
        layout.addRow("P/N:", pn_input)
        layout.addRow("设备:", device_input)
        layout.addRow("姓名:", name_input)
        layout.addRow("产出:", output_input)
        layout.addRow("工时:", hours_input)

        confirm_button = QPushButton("确定")
        confirm_button.clicked.connect(lambda: self.add_production(
            batch_input.text(), date_input.text(), shift_input.text(),
            pn_input.text(), device_input.text(), name_input.text(),
            output_input.text(), hours_input.text(), dialog
        ))
        layout.addWidget(confirm_button)

        dialog.exec()

    @staticmethod
    def _create_line_edit_with_placeholder(placeholder_text):
        """创建带提示语的输入框"""
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(placeholder_text)
        line_edit.setStyleSheet("""
            QLineEdit {
                color: #808080;  /* 浅灰色提示文字 */
                font-style: normal;
            }
            QLineEdit:focus {
                color: #000000;  /* 黑色输入文字 */
                font-style: normal;
            }
        """)
        return line_edit

    def add_production(self, batch, date, shift, pn, device, name, output, hours, dialog):
        if not all([batch, date, shift, pn, device, name, output, hours]):
            QMessageBox.warning(dialog, "输入错误", "请填写所有字段")
            return

        try:
            float(output)
            float(hours)
        except ValueError:
            QMessageBox.warning(dialog, "输入错误", "产出和工时必须是数字")
            return

        row = self.production_table.rowCount()
        self.production_table.insertRow(row)
        self.production_table.setItem(row, 0, QTableWidgetItem(batch))
        self.production_table.setItem(row, 1, QTableWidgetItem(date))
        self.production_table.setItem(row, 2, QTableWidgetItem(shift))
        self.production_table.setItem(row, 3, QTableWidgetItem(pn))
        self.production_table.setItem(row, 4, QTableWidgetItem(device))
        self.production_table.setItem(row, 5, QTableWidgetItem(name))
        self.production_table.setItem(row, 6, QTableWidgetItem(output))
        self.production_table.setItem(row, 7, QTableWidgetItem(hours))
        dialog.close()

    def delete_production(self):
        selected = self.production_table.selectedItems()
        if not selected:
            self.show_custom_message("提示", "请先选择要删除的行", QMessageBox.Icon.Warning)
            return

        rows = {item.row() for item in selected}
        for row in sorted(rows, reverse=True):
            self.production_table.removeRow(row)

    @staticmethod
    def get_dialog_stylesheet():
        return """
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
        """

    def save_config(self):
        """保存当前配置到YAML文件"""
        # 从表格收集数据
        config = {
            'employees_excel_path': self.file_path_label.text() if self.file_path_label.text() != "未选择文件" else "",
            'employees': self.get_employee_data(),
            'lines': self.get_line_data(),
            'special_stations': self.get_special_station_data(),
            'productions': self.get_production_data()
        }

        # 选择保存路径
        file_path, _ = QFileDialog.getSaveFileName(
            self, "保存配置文件", "", "YAML文件 (*.yml *.yaml)"
        )

        if file_path:
            if not file_path.endswith(('.yml', '.yaml')):
                file_path += '.yml'

            if YamlManager.save_to_yaml(config, file_path, self):
                self.show_custom_message("提示", "数据配置保存成功!", QMessageBox.Icon.Information)

    def load_config(self):
        """从YAML文件加载配置"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "加载配置文件", "", "YAML文件 (*.yml *.yaml)"
        )

        if file_path:
            config = YamlManager.load_from_yaml(file_path, self)
            if config:
                # 加载Excel路径
                excel_path = config.get('employees_excel_path', "")
                if excel_path:
                    self.file_path_label.setText(excel_path)
                    self.file_path_label.setToolTip(excel_path)
                else:
                    self.file_path_label.setText("未选择文件")

                # 加载其他数据
                self.set_employee_data(config.get('employees', []))
                self.set_line_data(config.get('lines', []))
                self.set_special_station_data(config.get('special_stations', []))
                self.set_production_data(config.get('productions', []))
                self.show_custom_message("加载成功", "配置已从YAML文件成功加载", QMessageBox.Icon.Information)

    def get_employee_data(self) -> List[Dict]:
        """从员工表格获取数据"""
        data = []
        for row in range(self.employee_table.rowCount()):
            data.append({
                '工号': self.employee_table.item(row, 0).text(),
                '姓名': self.employee_table.item(row, 1).text(),
                '设备编号': self.employee_table.item(row, 2).text(),
                'P/N': self.employee_table.item(row, 3).text(),
                '工位': self.employee_table.item(row, 4).text()
            })
        return data

    def get_line_data(self) -> List[Dict]:
        """从拉线表格获取数据"""
        data = []
        for row in range(self.line_table.rowCount()):
            data.append({
                '设备编号': self.line_table.item(row, 1).text(),
                'P/N': self.line_table.item(row, 0).text(),
                '所需工位': self.line_table.item(row, 2).text().split(',')
            })
        return data

    def get_special_station_data(self) -> List[Dict]:
        """从特殊工位表格获取数据"""
        data = []
        for row in range(self.special_station_table.rowCount()):
            data.append({
                '特殊工位类型': self.special_station_table.item(row, 0).text()
            })
        return data

    def get_production_data(self) -> List[Dict]:
        """从生产情况表格获取数据"""
        data = []
        for row in range(self.production_table.rowCount()):
            data.append({
                '排班批次': self.production_table.item(row, 0).text(),
                '日期': self.production_table.item(row, 1).text(),
                '班次': self.production_table.item(row, 2).text(),
                'P/N': self.production_table.item(row, 3).text(),
                '设备': self.production_table.item(row, 4).text(),
                '姓名': self.production_table.item(row, 5).text(),
                '产出': float(self.production_table.item(row, 6).text()),
                '工时': float(self.production_table.item(row, 7).text())
            })
        return data

    def set_employee_data(self, employees: List[Dict]):
        """设置员工表格数据"""
        self.employee_table.setRowCount(0)
        for emp in employees:
            row = self.employee_table.rowCount()
            self.employee_table.insertRow(row)
            self.employee_table.setItem(row, 0, QTableWidgetItem(emp['工号']))
            self.employee_table.setItem(row, 1, QTableWidgetItem(emp['姓名']))
            self.employee_table.setItem(row, 2, QTableWidgetItem(emp['设备编号']))
            self.employee_table.setItem(row, 3, QTableWidgetItem(emp['P/N']))
            self.employee_table.setItem(row, 4, QTableWidgetItem(emp['工位']))

    def set_line_data(self, lines: List[Dict]):
        """设置拉线表格数据"""
        self.line_table.setRowCount(0)
        for line in lines:
            row = self.line_table.rowCount()
            self.line_table.insertRow(row)
            self.line_table.setItem(row, 0, QTableWidgetItem(line['P/N']))
            self.line_table.setItem(row, 1, QTableWidgetItem(line['设备编号']))
            self.line_table.setItem(row, 2, QTableWidgetItem(','.join(line['所需工位'])))

    def set_special_station_data(self, stations: List[Dict]):
        """设置特殊工位表格数据"""
        self.special_station_table.setRowCount(0)
        for station in stations:
            row = self.special_station_table.rowCount()
            self.special_station_table.insertRow(row)
            self.special_station_table.setItem(row, 0, QTableWidgetItem(station['特殊工位类型']))

    def set_production_data(self, productions: List[Dict]):
        """设置生产情况表格数据"""
        self.production_table.setRowCount(0)
        for prod in productions:
            row = self.production_table.rowCount()
            self.production_table.insertRow(row)
            self.production_table.setItem(row, 0, QTableWidgetItem(prod['排班批次']))
            self.production_table.setItem(row, 1, QTableWidgetItem(prod['日期']))
            self.production_table.setItem(row, 2, QTableWidgetItem(prod['班次']))
            self.production_table.setItem(row, 3, QTableWidgetItem(prod['P/N']))
            self.production_table.setItem(row, 4, QTableWidgetItem(prod['设备']))
            self.production_table.setItem(row, 5, QTableWidgetItem(prod['姓名']))
            self.production_table.setItem(row, 6, QTableWidgetItem(str(prod['产出'])))
            self.production_table.setItem(row, 7, QTableWidgetItem(str(prod['工时'])))