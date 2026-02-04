# 高山滑雪比赛成绩查询系统

一个支持 PDF/图片导入、多维度查询和统计分析的高山滑雪比赛成绩管理系统。

## 功能特性

- ✅ **多维度成绩查询**：按运动员、项目、组别、组织、日期查询
- ✅ **智能数据导入**：支持 PDF/图片识别（OCR + LLM 双路识别）
- ✅ **高级统计分析**：历史最佳名次、成绩趋势图表、运动员对比
- ✅ **DNF/DSQ 支持**：完整支持未完成比赛的特殊状态
- ✅ **响应式设计**：支持桌面和移动浏览器

## 技术栈

### 后端
- **框架**：Python FastAPI
- **数据库**：SQLite + SQLAlchemy ORM
- **OCR**：Tesseract
- **LLM**：Amazon Bedrock
- **文件存储**：AWS S3

### 前端
- **框架**：React 18
- **UI 库**：Ant Design
- **图表**：ECharts
- **HTTP 客户端**：Axios

## 快速开始

详见 [QUICKSTART.md](QUICKSTART.md)

## 部署

详见 [DEPLOYMENT.md](DEPLOYMENT.md)

## 项目结构

```
skiresultsystem/
├── backend/          # 后端代码
├── frontend/         # 前端代码
├── aidlc-docs/       # AI-DLC 设计文档
└── test_files/       # 测试文件
```

## 许可证

MIT License
