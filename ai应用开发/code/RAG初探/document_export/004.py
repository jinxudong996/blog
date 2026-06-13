'''
Author: jinxudong 18751241086@163.com
Date: 2025-11-27 21:41:35
LastEditors: jinxudong 18751241086@163.com
LastEditTime: 2025-11-27 22:20:00
FilePath: \code\RAG初探\document_export\004.py
Description: 使用 DeepSeek-VL 调用多模态大模型，解读本地图片含义。
'''
import os
import base64
import mimetypes
import json
import requests
from dotenv import load_dotenv


def _get_deepseek_key() -> str:
	load_dotenv()
	key = os.getenv("DEEPSEEK_API_KEY")
	if not key:
		raise RuntimeError("未找到 DEEPSEEK_API_KEY，请在 .env 或系统环境中配置")
	return key


def _read_image_as_data_url(image_path: str) -> str:
	if not os.path.exists(image_path):
		raise FileNotFoundError(f"图片不存在: {image_path}")
	mime = mimetypes.guess_type(image_path)[0] or "image/jpeg"
	with open(image_path, "rb") as f:
		b64 = base64.b64encode(f.read()).decode("utf-8")
	return f"data:{mime};base64,{b64}"


def describe_image_with_deepseek(image_path: str, prompt: str = None) -> str:
	api_key = _get_deepseek_key()
	image_data_url = _read_image_as_data_url(image_path)

	# DeepSeek-VL 推理接口（示例，若你的具体域名不同请替换）
	url = "https://api.deepseek.com/v1/chat/completions"
	headers = {
		"Authorization": f"Bearer {api_key}",
		"Content-Type": "application/json",
	}

	user_prompt = prompt or (
		"你是一名资深图像理解助手，请：\n"
		"1) 用中文概述图片的主要内容和风格；\n"
		"2) 列出你能识别到的关键元素（角色、文字、场景、符号）；\n"
		"3) 给出图片可能表达的含义或主题；\n"
		"要求精炼但信息完整。"
	)

	payload = {
		"model": "deepseek-vl",  # 多模态视觉模型
		"messages": [
			{
				"role": "user",
				"content": [
					{"type": "text", "text": user_prompt},
					{"type": "input_image", "image": image_data_url},
				],
			}
		],
		"max_tokens": 800,
	}

	resp = requests.post(url, headers=headers, data=json.dumps(payload), timeout=60)
	resp.raise_for_status()
	data = resp.json()
	# 兼容常见返回结构
	try:
		return data["choices"][0]["message"]["content"]
	except Exception:
		return json.dumps(data, ensure_ascii=False, indent=2)


if __name__ == "__main__":
	image_path = "../../data/黑悟空英文.jpg"
	print("=== DeepSeek-VL 图片解读 ===")
	print(f"图片路径: {image_path}")
	try:
		result = describe_image_with_deepseek(image_path)
		print("\n模型解读：")
		print(result)
	except Exception as e:
		print(f"调用出错: {e}")