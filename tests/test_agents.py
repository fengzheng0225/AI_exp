import pytest
from text2sql.app.models import StructuredRequirement, TimeRange, SQLResponse, TextToSQLResponse
from text2sql.tests.utils import SQLTestUtils, TestDataGenerator

def test_text_translator_basic(text_translator):
    """测试基本的文本翻译功能"""
    queries = TestDataGenerator.generate_sample_queries()
    text = queries[0]  # 使用第一个样例查询
    result = text_translator.translate(text)
    
    assert isinstance(result, StructuredRequirement)
    assert "CTR" in result.metrics
    assert "slot_id" in result.dimensions
    assert result.time_range.type == "relative"
    assert result.time_range.value == "last_7_days"

def test_text_translator_complex(text_translator):
    """测试复杂查询的文本翻译"""
    queries = TestDataGenerator.generate_sample_queries()
    text = queries[1]  # 使用第二个样例查询
    result = text_translator.translate(text)
    
    assert isinstance(result, StructuredRequirement)
    assert "CTR" in result.metrics
    assert "creative_id" in result.dimensions
    assert "slot_id" in result.dimensions
    assert any("industry" in filter_ for filter_ in result.filters)

def test_sql_generator_basic(sql_generator):
    """测试基本的SQL生成功能"""
    requirement = StructuredRequirement(**TestDataGenerator.generate_structured_requirement())
    result = sql_generator.generate_sql(requirement)
    
    assert isinstance(result, SQLResponse)
    assert SQLTestUtils.validate_sql_structure(result.sql)
    assert SQLTestUtils.check_metrics_included(result.sql, requirement.metrics)
    assert SQLTestUtils.check_dimensions_included(result.sql, requirement.dimensions)
    assert SQLTestUtils.validate_performance_hints(result.performance_hints)

def test_sql_generator_complex(sql_generator):
    """测试复杂SQL的生成"""
    requirement = StructuredRequirement(**TestDataGenerator.generate_structured_requirement())
    result = sql_generator.generate_sql(requirement)
    
    sql = SQLTestUtils.normalize_sql(result.sql)
    assert isinstance(result, SQLResponse)
    assert "join" in sql
    assert "group by" in sql
    assert "industry = 'ecommerce'" in sql

def test_pipeline_success(pipeline):
    """测试完整流程 - 成功场景"""
    queries = TestDataGenerator.generate_sample_queries()
    text = queries[0]
    result = pipeline.process(text)
    
    assert isinstance(result, TextToSQLResponse)
    assert result.status == "success"
    assert isinstance(result.data, SQLResponse)
    assert SQLTestUtils.validate_sql_structure(result.data.sql)

def test_pipeline_clarification(pipeline):
    """测试完整流程 - 需要澄清场景"""
    text = "查看表现好的广告位"  # 模糊的需求
    result = pipeline.process(text)
    
    assert isinstance(result, TextToSQLResponse)
    assert result.status == "clarify"
    assert isinstance(result.data, list)
    assert len(result.data) > 0  # 确保有澄清问题

def test_error_handling(pipeline):
    """测试错误处理"""
    text = ""  # 空输入
    result = pipeline.process(text)
    
    assert isinstance(result, TextToSQLResponse)
    assert result.status == "error"
    assert isinstance(result.data, str)
    assert len(result.data) > 0  # 确保有错误信息

def test_multiple_queries(pipeline):
    """测试多个查询的一致性"""
    queries = TestDataGenerator.generate_sample_queries()
    results = []
    
    for query in queries:
        result = pipeline.process(query)
        results.append(result)
    
    # 验证所有查询都得到了有效响应
    assert all(isinstance(r, TextToSQLResponse) for r in results)
    # 验证成功的查询生成了有效的SQL
    success_results = [r for r in results if r.status == "success"]
    assert all(SQLTestUtils.validate_sql_structure(r.data.sql) for r in success_results)
