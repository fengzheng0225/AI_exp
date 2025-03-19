from typing import Dict, List, Any
import re

class SQLTestUtils:
    @staticmethod
    def normalize_sql(sql: str) -> str:
        """标准化SQL字符串以便比较"""
        # 移除多余的空白字符
        sql = re.sub(r'\s+', ' ', sql.strip())
        # 转换为小写
        return sql.lower()

    @staticmethod
    def validate_sql_structure(sql: str) -> bool:
        """验证SQL基本结构是否正确"""
        required_clauses = ['select', 'from']
        sql_lower = sql.lower()
        return all(clause in sql_lower for clause in required_clauses)

    @staticmethod
    def check_metrics_included(sql: str, metrics: List[str]) -> bool:
        """检查SQL是否包含所有必需的指标"""
        sql_lower = sql.lower()
        return all(metric.lower() in sql_lower for metric in metrics)

    @staticmethod
    def check_dimensions_included(sql: str, dimensions: List[str]) -> bool:
        """检查SQL是否包含所有必需的维度"""
        sql_lower = sql.lower()
        return all(dimension.lower() in sql_lower for dimension in dimensions)

    @staticmethod
    def validate_performance_hints(hints: List[str]) -> bool:
        """验证性能提示是否有效"""
        required_topics = ['partition', 'index', 'join']
        hints_lower = [hint.lower() for hint in hints]
        return any(topic in ' '.join(hints_lower) for topic in required_topics)

class TestDataGenerator:
    @staticmethod
    def generate_structured_requirement() -> Dict[str, Any]:
        """生成测试用的结构化需求"""
        return {
            "metrics": ["CTR", "ECPM"],
            "dimensions": ["slot_id", "creative_id"],
            "time_range": {
                "type": "relative",
                "value": "last_7_days"
            },
            "filters": ["industry = 'ecommerce'"]
        }

    @staticmethod
    def generate_sample_queries() -> List[str]:
        """生成测试用的自然语言查询样例"""
        return [
            "查看最近7天各资源位的CTR趋势",
            "分析上个月各创意在不同资源位的曝光量和点击率",
            "统计电商行业的广告位表现",
            "对比不同创意的转化效果",
            "查看点击率top10的广告位"
        ] 