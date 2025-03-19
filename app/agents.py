from typing import List, Optional
import openai
from openai import AzureOpenAI
from config.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_DEPLOYMENT,
    AZURE_OPENAI_API_VERSION,
    MAX_TOKENS,
    TEMPERATURE,
    TOP_P,
    FREQUENCY_PENALTY,
    PRESENCE_PENALTY
)
from .models import (
    StructuredRequirement,
    SQLResponse,
    TextToSQLResponse,
    TimeRange
)

class TextTranslatorAgent:
    """文本翻译代理，负责将自然语言转换为结构化需求"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
    def translate(self, text: str) -> StructuredRequirement:
        """
        将自然语言文本转换为结构化需求
        
        Args:
            text: 用户的自然语言查询
            
        Returns:
            StructuredRequirement: 结构化的查询需求
        """
        try:
            # 调用OpenAI API进行文本转换
            response = self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "你是一个专业的文本翻译助手，负责将用户的自然语言查询转换为结构化的查询需求。"},
                    {"role": "user", "content": text}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY_PENALTY,
                presence_penalty=PRESENCE_PENALTY
            )
            
            # 解析响应
            content = response.choices[0].message.content
            # TODO: 实现响应解析逻辑
            
            # 临时返回一个示例结构化需求
            return StructuredRequirement(
                metrics=["CTR"],
                dimensions=["slot_id"],
                time_range=TimeRange(type="relative", value="last_7_days"),
                filters=[]
            )
            
        except Exception as e:
            raise Exception(f"文本转换失败: {str(e)}")

class SQLGeneratorAgent:
    """SQL生成代理，负责将结构化需求转换为SQL查询"""
    
    def __init__(self):
        self.client = AzureOpenAI(
            api_key=AZURE_OPENAI_API_KEY,
            api_version=AZURE_OPENAI_API_VERSION,
            azure_endpoint=AZURE_OPENAI_ENDPOINT
        )
        
    def generate_sql(self, requirement: StructuredRequirement) -> SQLResponse:
        """
        将结构化需求转换为SQL查询
        
        Args:
            requirement: 结构化的查询需求
            
        Returns:
            SQLResponse: SQL查询响应
        """
        try:
            # 调用OpenAI API生成SQL
            response = self.client.chat.completions.create(
                model=AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": "你是一个专业的SQL生成助手，负责将结构化需求转换为优化的SQL查询。"},
                    {"role": "user", "content": str(requirement)}
                ],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                top_p=TOP_P,
                frequency_penalty=FREQUENCY_PENALTY,
                presence_penalty=PRESENCE_PENALTY
            )
            
            # 解析响应
            content = response.choices[0].message.content
            # TODO: 实现SQL生成逻辑
            
            # 临时返回一个示例SQL响应
            return SQLResponse(
                sql="SELECT slot_id, COUNT(*) as impressions, SUM(CASE WHEN is_click = 1 THEN 1 ELSE 0 END) / COUNT(*) as ctr FROM dwd_ad_impression WHERE dt >= DATE_SUB(CURRENT_DATE(), 7) GROUP BY slot_id",
                explanation="该SQL查询用于计算最近7天内各资源位的CTR（点击率）。通过计算点击次数除以展示次数得到CTR，并按资源位ID分组展示结果。",
                performance_hints=["建议对slot_id列创建索引", "使用分区字段dt进行查询优化"]
            )
            
        except Exception as e:
            raise Exception(f"SQL生成失败: {str(e)}")

class TextToSQLPipeline:
    """文本到SQL的转换流水线"""
    
    def __init__(self):
        self.text_translator = TextTranslatorAgent()
        self.sql_generator = SQLGeneratorAgent()
    
    def process(self, text: str) -> TextToSQLResponse:
        """
        处理文本到SQL的转换流程
        
        Args:
            text: 用户的自然语言查询
            
        Returns:
            TextToSQLResponse: 转换响应
        """
        try:
            # 1. 文本转换为结构化需求
            requirement = self.text_translator.translate(text)
            
            # 2. 结构化需求转换为SQL
            sql_response = self.sql_generator.generate_sql(requirement)
            
            # 3. 返回成功响应
            return TextToSQLResponse(
                status="success",
                data=sql_response
            )
            
        except Exception as e:
            # 返回错误响应
            return TextToSQLResponse(
                status="error",
                data=str(e)
            )
