# Pyside6_scheduling_UI
使用Pyside6完成工厂排班界面scheduling_UI。  
  
包含登陆界面loginwindow，主界面main。 
  
主界面main：包含三个widget：模型训练界面ModelTrainingPage，排班界面SchedulingPage，管理界面ManagementPage。每个page一个py文件，在文件中声明class。  
  
模型训练界面ModelTrainingPage：文件选择与文件路径显示QFileDialog、参数输入QLabel、结果输出QTextEdit（包含隐藏滚动条QScrollArea）。    
  
排班界面SchedulingPage：普通参数输入QLabel、表格参数输入QTableWidget、结果输出QTextEdit（包含隐藏滚动条QScrollArea）。  
  
管理界面ManagementPage：文件选择与文件路径显示QFileDialog、表格参数输入QTableWidget（需要时包含显式滚动条QScrollArea）、结果输出QTextEdit（包含隐藏滚动条QScrollArea）。  

界面参数保存为yml文件后传入算法代码
