# FastAPI 主应用
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
import uvicorn

app = FastAPI(
    title="高山滑雪比赛成绩查询系统",
    description="支持成绩查询、PDF/图片导入和统计分析",
    version="1.0.0"
)

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 初始化数据库
@app.on_event("startup")
async def startup_event():
    init_db()
    print("✅ 数据库初始化完成")

@app.get("/")
async def root():
    return {
        "message": "高山滑雪比赛成绩查询系统 API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# 导入路由
from routes import results, import_data, statistics
app.include_router(results.router, prefix="/api/results", tags=["成绩查询"])
app.include_router(import_data.router, prefix="/api/import", tags=["数据导入"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["统计分析"])

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)