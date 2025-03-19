from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from app.agents import TextToSQLPipeline
from app.models import TextToSQLResponse

app = FastAPI(
    title="Text2SQL API",
    description="将自然语言转换为SQL查询的API服务",
    version="1.0.0"
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/")
async def read_root():
    """返回主页"""
    return FileResponse("app/static/index.html")

class TextToSQLRequest(BaseModel):
    text: str
    context: Optional[dict] = None

@app.post("/api/v1/text2sql", response_model=TextToSQLResponse)
async def text_to_sql(request: TextToSQLRequest):
    """
    将自然语言转换为SQL查询
    
    Args:
        request: 包含查询文本和可选上下文的请求对象
        
    Returns:
        TextToSQLResponse: 包含SQL查询和元数据的响应对象
    """
    try:
        pipeline = TextToSQLPipeline()
        result = pipeline.process(request.text)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
