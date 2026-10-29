"""Chẩn đoán lỗi kết nối Gemini: chạy 4 phép thử và in mã lỗi thật.

    python diag.py            (cần biến môi trường GEMINI_API_KEY, hoặc có .streamlit/secrets.toml)

Gửi toàn bộ kết quả (không kèm khóa API) cho người hỗ trợ nếu vẫn lỗi.
"""
import os
import time

from google import genai
from google.genai import types

import core

key = os.environ.get("GEMINI_API_KEY")
if not key:
    try:
        import tomllib
        with open(".streamlit/secrets.toml", "rb") as f:
            key = tomllib.load(f).get("GEMINI_API_KEY")
    except Exception:
        pass
if not key:
    raise SystemExit("Không tìm thấy GEMINI_API_KEY")

client = genai.Client(api_key=key, http_options=types.HttpOptions(timeout=30_000))
turn3 = [
    types.Content(role="user", parts=[types.Part(text="xin chào thầy cô ạ")]),
    types.Content(role="model", parts=[types.Part(text="Chào em! Hôm nay em muốn học gì?")]),
    types.Content(role="user", parts=[types.Part(text="vector là gì")]),
]


def run(name, model, contents, config=None):
    t = time.perf_counter()
    try:
        r = client.models.generate_content(model=model, contents=contents, config=config)
        print(f"[OK ] {name}: {time.perf_counter() - t:.1f}s | {(r.text or '')[:60]!r}")
    except Exception as e:
        print(f"[LỖI] {name}: {type(e).__name__} code={getattr(e, 'code', None)} | {str(e)[:200]}")


print("Model chính:", core.MODEL, "| dự phòng:", core.FALLBACK_MODEL or "(tắt)")
run("1. 1 lượt, cấu hình mặc định", core.MODEL, "xin chào")
run("2. 3 lượt, cấu hình mặc định", core.MODEL, turn3)
run("3. 3 lượt, giống app (thinking + system prompt)", core.MODEL, turn3, core._make_config("Bạn là trợ lý Toán 10. Hỏi lại học sinh đúng một câu."))
if core.FALLBACK_MODEL:
    run("4. 3 lượt, model dự phòng", core.FALLBACK_MODEL, turn3, core._make_config("Bạn là trợ lý Toán 10. Hỏi lại học sinh đúng một câu."))
