# Text2SQL - 自然语言转SQL查询系统

这是一个基于Azure OpenAI的智能系统，可以将自然语言转换为SQL查询，特别适用于广告数据分析场景。

## 功能特点

- 🤖 智能转换：将自然语言转换为结构化的SQL查询
- 📊 广告分析：内置广告业务指标和维度定义
- 🔍 性能优化：自动生成查询优化建议
- 🌐 Web界面：提供友好的用户交互界面
- 🔒 安全可靠：支持Azure OpenAI API认证

## 技术栈

- Python 3.8+
- FastAPI
- Azure OpenAI
- TailwindCSS
- Pydantic

## 快速开始

### 1. 环境准备

```bash
# 克隆仓库
git clone https://github.com/fengzheng0225/AI_exp.git
cd AI_exp

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，填入你的Azure OpenAI配置
```

### 3. 启动服务

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问Web界面

打开浏览器访问 `http://localhost:8000`

## 项目结构

```
text2sql/
├── app/
│   ├── agents.py      # AI代理实现
│   ├── main.py        # FastAPI应用
│   ├── models.py      # 数据模型
│   └── static/        # 静态文件
├── config/
│   └── config.py      # 配置文件
├── tests/             # 测试文件
├── .env.example       # 环境变量模板
└── requirements.txt   # 项目依赖
```

## 支持的指标和维度

### 指标
- CTR (点击率)
- ECPM (千次展示收入)

### 维度
- slot_id (广告位)
- creative_id (创意)

## API接口

### 1. 文本转SQL
- 端点：`POST /api/v1/text2sql`
- 请求体：
```json
{
    "text": "查看最近7天各资源位的CTR趋势"
}
```
- 响应：
```json
{
    "status": "success",
    "data": {
        "sql": "SELECT ...",
        "explanation": "查询说明",
        "performance_hints": ["优化建议1", "优化建议2"]
    }
}
```

### 2. 健康检查
- 端点：`GET /health`
- 响应：
```json
{
    "status": "healthy"
}
```

## 开发指南

### 添加新的指标
在 `config/config.py` 中的 `METRICS_CONFIG` 添加新的指标定义：

```python
"NEW_METRIC": MetricDefinition(
    formula="your_formula",
    dependencies=["table1", "table2"],
    type="metric_type",
    description="指标说明"
)
```

### 添加新的维度
在 `config/config.py` 中的 `DIMENSIONS_CONFIG` 添加新的维度定义：

```python
"new_dimension": DimensionDefinition(
    table="dimension_table",
    type="dimension_type",
    joins=[{
        "table": "main_table",
        "condition": "join_condition"
    }],
    description="维度说明"
)
```

## 贡献指南

1. Fork 本仓库
2. 创建你的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交你的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request

## 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 联系方式

- 项目维护者：[fengzheng0225](https://github.com/fengzheng0225)
- 项目链接：[https://github.com/fengzheng0225/AI_exp](https://github.com/fengzheng0225/AI_exp) 