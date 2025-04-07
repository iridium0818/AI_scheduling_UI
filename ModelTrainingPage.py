from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QLabel, QLineEdit,
    QPushButton, QFileDialog, QScrollArea, QTextEdit,
    QSizePolicy
)

class ModelTrainingPage(QWidget):
    def __init__(self):
        super().__init__()
        self.log_text = None  # 在 __init__ 中初始化实例属性
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

    @staticmethod
    def create_param_group():
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

        layout.addWidget(scroll_area)
        group_box.setLayout(layout)
        return group_box