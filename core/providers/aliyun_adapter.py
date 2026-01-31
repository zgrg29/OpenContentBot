import os
import json
import re
import requests
from dotenv import load_dotenv
from .base_adapter import BaseAdapter

# 预先加载环境变量
load_dotenv()

class Adapter(BaseAdapter):
    def __init__(self, config):
        """
        config 同样是 modules.processor 的内容
        """
        api_key = os.getenv("ALIYUN_API_KEY")
        if not api_key:
            raise ValueError("环境变量 ALIYUN_API_KEY 未设置，请检查 .env 文件。")
        
        self.api_key = api_key
        self.model = config.get('model', 'deepseek-r1')
        self.temperature = config.get('temperature', 0.7)
        self.base_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"
        
        # 日志级别控制
        self.debug = os.getenv("ALIYUN_DEBUG", "false").lower() == "true"

    def _log(self, message, level="info"):
        """简单的日志记录"""
        if self.debug or level == "error":
            prefix = {
                "info": "[INFO]",
                "warning": "[WARNING]",
                "error": "[ERROR]",
                "debug": "[DEBUG]"
            }.get(level, "[INFO]")
            print(f"{prefix} {message}")

    def _clean_json_response(self, content_str):
        """
        清理API返回的JSON字符串，移除代码块标记和其他非JSON内容
        
        Args:
            content_str: API返回的原始字符串
            
        Returns:
            清理后的JSON字符串
        """
        if not content_str:
            return ""
            
        # 移除 ```json 和 ``` 标记
        content_str = re.sub(r'^```json\s*', '', content_str, flags=re.IGNORECASE)
        content_str = re.sub(r'\s*```$', '', content_str, flags=re.IGNORECASE)
        
        # 移除可能的前后空白
        content_str = content_str.strip()
        
        # 如果仍然以 ``` 开头（可能是其他语言的代码块）
        if content_str.startswith('```'):
            content_str = re.sub(r'^```\w*\s*', '', content_str)
            content_str = re.sub(r'\s*```$', '', content_str)
            content_str = content_str.strip()
        
        self._log(f"清理后的JSON字符串: {content_str[:200]}...", "debug")
        return content_str

    def _extract_json_from_text(self, text):
        """
        从文本中提取JSON对象
        
        Args:
            text: 可能包含JSON的文本
            
        Returns:
            提取的JSON字符串，如果找不到则返回原始文本
        """
        if not text:
            return ""
            
        # 尝试查找JSON对象
        json_pattern = r'\{[\s\S]*?\}'
        matches = re.findall(json_pattern, text)
        
        if matches:
            # 返回最长的匹配（最可能是完整的JSON）
            longest_match = max(matches, key=len)
            self._log(f"从文本中提取到JSON: {longest_match[:200]}...", "debug")
            return longest_match
            
        return text

    def generate_content(self, raw_data, system_prompt):
        """
        请求阿里云百炼并返回结构化数据
        
        Args:
            raw_data: 原始输入数据
            system_prompt: 系统提示词
            
        Returns:
            处理后的结构化数据字典
        """
        try:
            # 验证输入
            if not raw_data or not isinstance(raw_data, str):
                self._log(f"无效的原始数据: {raw_data}", "warning")
                return self._get_error_response("无效的输入数据")
                
            if not system_prompt or not isinstance(system_prompt, str):
                self._log(f"无效的系统提示词: {system_prompt}", "warning")
                return self._get_error_response("无效的系统提示词")

            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            # 格式化用户消息
            user_message = f"请处理以下原始数据并按 JSON 格式输出：\n{raw_data}"
            
            payload = {
                "model": self.model,
                "input": {
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_message}
                    ]
                },
                "parameters": {
                    "result_format": "message",
                    "temperature": self.temperature
                }
            }
            
            self._log(f"发送请求到阿里云API，模型: {self.model}, 温度: {self.temperature}", "debug")
            self._log(f"原始数据长度: {len(raw_data)} 字符", "debug")
            
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                self._log(f"API响应成功，请求ID: {result.get('request_id', '未知')}", "debug")
                
                # 获取生成的内容
                if 'output' not in result or 'choices' not in result['output']:
                    self._log(f"API响应格式异常: {result}", "error")
                    return self._get_error_response("API响应格式异常")
                
                content_str = result['output']['choices'][0]['message']['content']
                self._log(f"原始API响应内容: {content_str[:300]}...", "debug")
                
                # 清理JSON响应
                cleaned_content = self._clean_json_response(content_str)
                
                # 如果清理后仍然不是有效的JSON，尝试从文本中提取
                try:
                    parsed_data = json.loads(cleaned_content)
                except json.JSONDecodeError:
                    self._log("清理后的内容不是有效JSON，尝试提取JSON", "debug")
                    extracted_json = self._extract_json_from_text(cleaned_content)
                    try:
                        parsed_data = json.loads(extracted_json)
                    except json.JSONDecodeError:
                        self._log(f"无法解析JSON内容: {extracted_json[:200]}...", "error")
                        return self._get_error_response("无法解析AI生成的JSON内容")
                
                # 验证返回的数据结构
                validated_data = self._validate_response_structure(parsed_data)
                self._log(f"成功生成内容: {validated_data.get('caption', '')[:50]}...", "info")
                
                return validated_data
                
            else:
                error_msg = f"阿里云百炼 API 错误: {response.status_code} - {response.text[:200]}"
                self._log(error_msg, "error")
                return self._get_error_response(f"API错误 {response.status_code}")
            
        except requests.exceptions.Timeout:
            self._log("API请求超时", "error")
            return self._get_error_response("请求超时")
        except requests.exceptions.ConnectionError:
            self._log("网络连接错误", "error")
            return self._get_error_response("网络连接错误")
        except Exception as e:
            self._log(f"未预期的错误: {str(e)}", "error")
            return self._get_error_response(f"未预期的错误: {str(e)}")

    def _validate_response_structure(self, data):
        """
        验证并确保返回的数据结构符合预期
        
        Args:
            data: 解析后的数据字典
            
        Returns:
            验证和补全后的数据字典
        """
        expected_fields = ["caption", "image_prompt", "tags"]
        validated = {}
        
        for field in expected_fields:
            if field in data:
                validated[field] = data[field]
            else:
                # 为缺失的字段提供默认值
                defaults = {
                    "caption": "内容生成中...",
                    "image_prompt": "generic placeholder image",
                    "tags": []
                }
                validated[field] = defaults[field]
                self._log(f"响应中缺少字段: {field}，使用默认值", "warning")
        
        # 确保tags是列表
        if not isinstance(validated["tags"], list):
            if isinstance(validated["tags"], str):
                # 尝试将字符串转换为列表
                validated["tags"] = [tag.strip() for tag in validated["tags"].split(",")]
            else:
                validated["tags"] = []
        
        return validated

    def _get_error_response(self, error_message):
        """
        获取错误响应
        
        Args:
            error_message: 错误信息
            
        Returns:
            错误响应字典
        """
        return {
            "caption": f"内容生成失败: {error_message}",
            "image_prompt": "Error placeholder image",
            "tags": ["#error"]
        }