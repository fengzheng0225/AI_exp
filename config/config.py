from typing import Dict, List
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

class OpenAIConfig:
    # Azure OpenAI配置
    ENDPOINT = os.getenv("ENDPOINT_URL", "")
    DEPLOYMENT = os.getenv("DEPLOYMENT_NAME", "")
    API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
    API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")
    TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
    TOP_P = float(os.getenv("TOP_P", "0.95"))
    FREQUENCY_PENALTY = float(os.getenv("FREQUENCY_PENALTY", "0.0"))
    PRESENCE_PENALTY = float(os.getenv("PRESENCE_PENALTY", "0.0"))

class MetricDefinition(BaseModel):
    formula: str
    dependencies: List[str]
    type: str
    description: str = ""

class DimensionDefinition(BaseModel):
    table: str
    type: str
    joins: List[Dict]
    description: str = ""

# 业务指标定义
METRICS_CONFIG = {
    "CTR": MetricDefinition(
        formula="click_cnt/impression_cnt",
        dependencies=["dwd_ad_click", "dwd_ad_impression"],
        type="ratio",
        description="点击率 = 点击数/展示数"
    ),
    "ECPM": MetricDefinition(
        formula="(cost/impression_cnt)*1000",
        dependencies=["dwd_ad_cost", "dwd_ad_impression"],
        type="currency",
        description="千次展示收入"
    )
}

# 维度定义
DIMENSIONS_CONFIG = {
    "slot_id": DimensionDefinition(
        table="dim_slot",
        type="categorical",
        joins=[{
            "table": "dwd_ad_impression",
            "condition": "using(slot_id)"
        }],
        description="广告位"
    ),
    "creative_id": DimensionDefinition(
        table="dim_creative",
        type="categorical",
        joins=[{
            "table": "dwd_ad_impression",
            "condition": "using(creative_id)"
        }],
        description="创意"
    )
}

# 数据模型定义
DATA_MODELS = {
    "dwd_ad_impression": {
        "columns": {
            "impression_id": "string",
            "slot_id": "string",
            "creative_id": "string",
            "impression_time": "timestamp",
            "cost": "decimal(16,4)",
            "dt": "string"
        },
        "partition_key": "dt"
    },
    "dwd_ad_click": {
        "columns": {
            "click_id": "string",
            "impression_id": "string",
            "click_time": "timestamp",
            "dt": "string"
        },
        "partition_key": "dt"
    }
}

# SQL模板
SQL_TEMPLATES = {
    "basic_metrics": """
    WITH base AS (
        SELECT 
            {dimensions},
            {metrics}
        FROM {main_table}
        {joins}
        WHERE {time_filter}
            AND {other_filters}
        GROUP BY {dimensions}
    )
    SELECT * FROM base
    ORDER BY {sort_fields}
    """
}

# 提示词模板
PROMPT_TEMPLATES = {
    "text_translator": """
    你是一个广告分析专家，需要将用户的自然语言查询转换为结构化的分析需求。
    
    已知指标定义：
    {metrics_definition}
    
    已知维度定义：
    {dimensions_definition}
    
    用户输入：{user_input}
    
    请将用户需求转换为以下JSON格式：
    {
        "metrics": ["指标列表"],
        "dimensions": ["维度列表"],
        "time_range": {
            "type": "relative/absolute",
            "value": "时间范围"
        },
        "filters": ["过滤条件列表"]
    }
    """,
    
    "sql_generator": """
    你是一个SparkSQL专家，需要根据结构化需求生成SQL查询。
    
    数据模型定义：
    {data_models}
    
    分析需求：
    {structured_requirement}
    
    请生成符合以下规范的SparkSQL：
    1. 必须包含分区字段过滤
    2. 使用ANSI SQL语法
    3. 添加必要的性能优化提示
    4. 包含完整的注释说明
    """
}

# Azure OpenAI 配置
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY", "")
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT", "")
AZURE_OPENAI_DEPLOYMENT = os.getenv("AZURE_OPENAI_DEPLOYMENT", "")
AZURE_OPENAI_API_VERSION = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview")

# 模型参数配置
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2000"))
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
TOP_P = float(os.getenv("TOP_P", "0.95"))
FREQUENCY_PENALTY = float(os.getenv("FREQUENCY_PENALTY", "0.0"))
PRESENCE_PENALTY = float(os.getenv("PRESENCE_PENALTY", "0.0"))
