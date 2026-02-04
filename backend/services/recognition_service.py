# 识别服务 - PDF/图片文字识别和数据提取
import os
import json
from typing import Dict, List, Optional, Tuple
import pdfplumber
from PIL import Image
import pytesseract
import boto3
from dotenv import load_dotenv

load_dotenv()

class RecognitionService:
    def __init__(self):
        self.bedrock_client = boto3.client(
            service_name='bedrock-runtime',
            region_name=os.getenv("AWS_REGION", "us-west-2")
        )
        self.model_id = "us.anthropic.claude-3-5-haiku-20241022-v1:0"
    
    def _extract_pdf_text(self, file_path: str) -> str:
        """从 PDF 提取文本"""
        text = ""
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
        return text
    
    def _extract_structured_data(self, text: str) -> Dict:
        """使用 AWS Bedrock Claude 从文本中提取结构化数据"""
        prompt = f"""你是一个专业的高山滑雪比赛成绩数据提取助手。请从以下文本中提取比赛成绩信息。

文本内容：
{text}

请提取以下信息并以 JSON 格式返回。**只返回 JSON，不要有任何其他文字、解释或标记**：

{{
    "competition": {{
        "name": "比赛名称",
        "date": "比赛日期 (YYYY-MM-DD格式)",
        "location": "比赛地点",
        "season": "赛季"
    }},
    "event": {{
        "name": "项目名称 (滑降/回转/大回转/超级大回转/全能)"
    }},
    "results": [
        {{
            "rank": 排名,
            "athlete_name": "运动员姓名",
            "organization": "所属组织",
            "category": "组别",
            "gender": "性别 (男/女)",
            "run1_time": "第一次成绩",
            "run2_time": "第二次成绩",
            "total_time": "总成绩",
            "time_behind_leader": "与第一名差距"
        }}
    ],
    "confidence": 识别置信度
}}

重要说明：
1. **必须提取文本中的所有成绩记录**，不要遗漏任何运动员
2. 如果某个字段无法识别，请设置为 null
3. 时间格式保持原样
4. 从文本中的标题行识别组别和性别
5. **只返回纯 JSON 对象，不要包含任何解释文字、markdown 标记或其他内容**"""
        
        try:
            request_body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 8192,
                "temperature": 0.1,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            }
            
            response = self.bedrock_client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(request_body)
            )
            
            response_body = json.loads(response['body'].read())
            content = response_body['content'][0]['text']
            
            if '```json' in content:
                content = content.split('```json')[1].split('```')[0].strip()
            elif '```' in content:
                content = content.split('```')[1].split('```')[0].strip()
            
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            
            if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
                content = content[start_idx:end_idx+1]
            
            content = content.strip()
            result = json.loads(content)
            return result
        
        except Exception as e:
            print(f"❌ Bedrock 提取失败: {str(e)}")
            return {
                "competition": {},
                "event": {},
                "results": [],
                "confidence": 0.0,
                "error": str(e)
            }
