import yaml
from typing import Dict, Optional
from PySide6.QtWidgets import QMessageBox


class YamlManager:
    @staticmethod
    def validate_config(config: Dict) -> bool:
        """验证配置数据的有效性"""
        try:
            if 'employees_excel_path' in config:
                if not isinstance(config['employees_excel_path'], str):
                    return False
            # 验证员工数据
            if 'employees' in config:
                for emp in config['employees']:
                    if not all(key in emp for key in ['工号', '姓名', '设备编号', 'P/N', '工位', '基础产出']):
                        return False
                    # 添加类型检查
                    if not (
                            isinstance(emp['工号'], (str, int))  # 工号可以是字符串或数字
                            and isinstance(emp['姓名'], str)
                            and isinstance(emp['设备编号'], str)
                            and isinstance(emp['P/N'], str)
                            and isinstance(emp['工位'], str)
                            and isinstance(emp['基础产出'], int)
                    ):
                        return False

            # 验证拉线数据
            if 'lines' in config:
                for line in config['lines']:
                    if not all(key in line for key in ['设备编号', 'P/N', '所需工位']):
                        return False
                    if not isinstance(line['所需工位'], list):
                        return False
                    # 验证列表中的元素类型
                    if not all(isinstance(station, str) for station in line['所需工位']):
                        return False

            # 验证特殊工位
            if 'special_stations' in config:
                for station in config['special_stations']:
                    if '特殊工位类型' not in station:
                        return False
                    # 添加类型检查
                    if not isinstance(station['特殊工位类型'], str):
                        return False

            # 验证生产情况
            if 'productions' in config:
                for prod in config['productions']:
                    required_keys = ['排班批次', '日期', '班次', 'P/N', '设备', '姓名', '产出', '工时']
                    if not all(key in prod for key in required_keys):
                        return False
                    try:
                        float(prod['产出'])
                        float(prod['工时'])
                    except (ValueError, TypeError):
                        return False
                    # 添加其他字段类型检查
                    if not isinstance(prod['排班批次'], str) or \
                            not isinstance(prod['日期'], str) or \
                            not isinstance(prod['班次'], str) or \
                            not isinstance(prod['P/N'], str) or \
                            not isinstance(prod['设备'], str) or \
                            not isinstance(prod['姓名'], str):
                        return False

            return True
        except (KeyError, TypeError, AttributeError):
            return False

    @staticmethod
    def save_to_yaml(config: Dict, file_path: str, parent_widget=None) -> bool:
        """保存配置到YAML文件"""
        if not YamlManager.validate_config(config):
            if parent_widget:
                QMessageBox.warning(parent_widget, "配置错误", "配置数据格式无效")
            return False

        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                yaml.dump({'config': config}, f, allow_unicode=True, sort_keys=False)
            return True
        except (IOError, OSError, yaml.YAMLError) as e:
            if parent_widget:
                QMessageBox.warning(parent_widget, "保存失败", f"保存YAML文件时出错: {str(e)}")
            return False

    @staticmethod
    def load_from_yaml(file_path: str, parent_widget=None) -> Optional[Dict]:
        """从YAML文件加载配置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)

            if 'config' not in data or not YamlManager.validate_config(data['config']):
                if parent_widget:
                    QMessageBox.warning(parent_widget, "加载失败", "YAML文件内容格式无效")
                return None

            return data['config']
        except (IOError, OSError, yaml.YAMLError) as e:
            if parent_widget:
                QMessageBox.warning(parent_widget, "加载失败", f"加载YAML文件时出错: {str(e)}")
            return None

    @staticmethod
    def create_empty_config() -> Dict:
        """创建空配置模板"""
        return {
            'employees_excel_path': "",
            'employees': [],
            'lines': [],
            'special_stations': [],
            'productions': []
        }