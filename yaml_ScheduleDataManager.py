import yaml
from typing import Dict, Optional
from PySide6.QtWidgets import QMessageBox, QWidget


class ScheduleDataManager:
    @staticmethod
    def validate_schedule_data(data: Dict, parent_widget: Optional[QWidget] = None) -> bool:
        """验证排班数据是否有效"""
        required_keys = {
            'total_work_hours': (int, float),
            'day_shift_hours': (int, float),
            'night_shift_hours': (int, float),
            'demands': list  # 注意: 原代码中可能是拼写错误 'demands' vs 'demands'
        }

        for key, types in required_keys.items():
            if key not in data:
                QMessageBox.warning(parent_widget, "数据验证错误", f"缺少必需的键: {key}")
                return False

            if not isinstance(data[key], types):
                QMessageBox.warning(parent_widget, "数据验证错误", f"{key} 应该是 {types} 类型")
                return False

        for demand in data['demands']:
            if not isinstance(demand, dict):
                QMessageBox.warning(parent_widget, "数据验证错误", "demands列表中的每个元素应该是字典")
                return False

            if 'P_N' not in demand or 'demand' not in demand:
                QMessageBox.warning(parent_widget, "数据验证错误", "每个demand字典应包含P_N和demand键")
                return False

            if not isinstance(demand['demand'], (int, float)) or demand['demand'] <= 0:
                QMessageBox.warning(parent_widget, "数据验证错误", "demand值应该是正数")
                return False

        total = data['day_shift_hours'] + data['night_shift_hours']
        if abs(total - data['total_work_hours']) > 1e-6:
            QMessageBox.warning(parent_widget, "数据验证错误", "白班和夜班时间总和应与总工作时间一致")
            return False

        return True

    @staticmethod
    def save_to_yaml(data: Dict, file_path: str, parent_widget: Optional[QWidget] = None) -> bool:
        """将排班数据保存到YAML文件"""
        if not ScheduleDataManager.validate_schedule_data(data, parent_widget):
            return False

        try:
            yaml_data = {'schedule': data}
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump(yaml_data, f, allow_unicode=True, sort_keys=False)
            return True
        except (IOError, yaml.YAMLError) as e:
            QMessageBox.warning(parent_widget, "保存错误", f"保存YAML文件时出错: {str(e)}")
            return False

    @staticmethod
    def load_from_yaml(file_path: str, parent_widget: Optional[QWidget] = None) -> Optional[Dict]:
        """从YAML文件加载排班数据"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                yaml_data = yaml.safe_load(f)

            if 'schedule' not in yaml_data:
                QMessageBox.warning(parent_widget, "加载错误", "YAML文件中缺少'schedule'键")
                return None

            if not ScheduleDataManager.validate_schedule_data(yaml_data['schedule'], parent_widget):
                return None

            return yaml_data['schedule']
        except (IOError, yaml.YAMLError) as e:
            QMessageBox.warning(parent_widget, "加载错误", f"加载YAML文件时出错: {str(e)}")
            return None