import json
import traceback
import os
from datetime import datetime

import streamlit as st

from core import TOPICS, ask_tutor, get_client, looks_stuck, prepare_file, MAX_FILES

st.set_page_config(page_title="Socratic Math-Tutor 10", page_icon="📐", layout="centered")

# ---------- Khóa API ----------
api_key = st.secrets.get("GEMINI_API_KEY", None) if hasattr(st, "secrets") else None
api_key = api_key or os.environ.get("GEMINI_API_KEY")
if not api_key or "dán-khóa" in api_key.casefold():
    st.error(
        "Chưa có Gemini API key thật. Hãy thay giá trị mẫu trong "
        ".streamlit/secrets.toml bằng key lấy từ Google AI Studio."
    )
    st.stop()
if not api_key.isascii():
    st.error(
        "Gemini API key có ký tự không hợp lệ. Hãy dán nguyên key từ Google AI Studio; "
        "không thêm chữ giải thích, dấu ngoặc, hoặc khoảng trắng."
    )
    st.stop()


@st.cache_resource
def _client(key):
    return get_client(key)


client = _client(api_key)

# ---------- Trạng thái ----------
ss = st.session_state
ss.setdefault("messages", [])  # [{'role','content'}]
ss.setdefault("log", [])  # nhật ký phục vụ nghiên cứu
ss.setdefault("hint_level", 1)
ss.setdefault("stuck_count", 0)

for message in ss.messages:
    if "image" in message and "files" not in message:
        image = message.pop("image")
        message["files"] = [{"kind": "image", "name": "image", **image}] if image else []

MAX_CHARS = 500  # độ dài tối đa mỗi tin nhắn của học sinh
MAX_TURNS = int(os.environ.get("MAX_TURNS", "30"))  # số lượt hỏi tối đa mỗi bài (đổi bằng biến môi trường MAX_TURNS)


def turns_used():
    """Số tin nhắn học sinh đã gửi trong bài hiện tại."""
    return sum(1 for m in ss.messages if m["role"] == "user")


def reset_problem():
    ss.messages = []
    ss.hint_level = 1
    ss.stuck_count = 0


# ---------- Thanh bên ----------
with st.sidebar:
    st.header("Cài đặt")
    topic = st.selectbox("Chủ đề", list(TOPICS.keys()), on_change=reset_problem)

    st.markdown(f"**Lượt hỏi còn lại: {max(0, MAX_TURNS - turns_used())}/{MAX_TURNS}**")
    st.markdown(f"**Mức gợi ý hiện tại: {ss.hint_level}/3** (còn {3 - ss.hint_level} lần gợi ý rõ hơn)")
    if st.button("Em đang bí, cho gợi ý rõ hơn", disabled=ss.hint_level >= 3, use_container_width=True):
        ss.hint_level = min(3, ss.hint_level + 1)
        st.rerun()
    st.caption("Gợi ý rõ hơn vẫn không cho đáp án. Trợ lý chỉ nêu công thức hoặc ví dụ tương tự.")

    if st.button("Bài mới", use_container_width=True):
        reset_problem()
        st.rerun()

    st.divider()
    st.markdown("**Xuất dữ liệu học tập**")
    export = {
        "exported_at": datetime.now().isoformat(timespec="seconds"),
        "topic": topic,
        "turns": ss.log,
    }
    st.download_button(
        "Tải lịch sử (.json)",
        data=json.dumps(export, ensure_ascii=False, indent=2),
        file_name="lich_su_hoi_thoai.json",
        mime="application/json",
        use_container_width=True,
        disabled=not ss.log,
    )
    st.caption(f"Ước tính chi phí phiên này: ${sum(t.get('cost_usd', 0) for t in ss.log):.4f}")
    st.caption("Không nhập tên, trường, lớp, số điện thoại vào chat, và che các thông tin đó trong ảnh hoặc tệp.")

# ---------- Giao diện chính ----------
st.title("Socratic Math-Tutor 10")
st.write(
    "Mình sẽ không giải hộ. Mình hỏi từng bước nhỏ để em tự tìm ra lời giải. "
    "Gõ đề bài hoặc đính kèm tệp vào khung bên dưới để bắt đầu."
)

def show_files(files):
    for f in files:
        if f["kind"] == "image":
            st.image(f["bytes"], width=320)
        else:
            st.caption(f"📎 {f['name']}")


for m in ss.messages:
    with st.chat_message("user" if m["role"] == "user" else "assistant"):
        show_files(m.get("files", []))
        st.markdown(m["content"])

_left = MAX_TURNS - turns_used()
if ss.messages and _left <= 5:
    st.caption(f"Còn {max(0, _left)} lượt cho bài này. Hãy hỏi vào điều em thấy quan trọng nhất.")

sub = st.chat_input(
    "Nhập đề bài, hoặc đính kèm ảnh, PDF, Word...",
    accept_file="multiple",
    file_type=["png", "jpg", "jpeg", "webp", "pdf", "docx", "txt"],
)
if sub:
    prompt = (sub.text or "").strip()
    files = []
    uploaded = list(sub.files or [])
    if len(uploaded) > MAX_FILES:
        st.warning(f"Mỗi tin chỉ đính kèm tối đa {MAX_FILES} tệp. Em chọn lại nhé.")
        st.stop()
    for uf in uploaded:
        try:
            files.append(prepare_file(uf.name, uf.getvalue()))
        except ValueError as err:
            st.warning(f"Tệp «{uf.name}»: {err}.")
            st.stop()
    if not prompt:
        if not files:
            st.stop()
        prompt = "Đây là đề bài của em (trong tệp đính kèm)."

    if len(prompt) > MAX_CHARS:
        st.warning(f"Tin nhắn dài quá {MAX_CHARS} ký tự. Em rút gọn lại nhé.")
        st.stop()
    if turns_used() >= MAX_TURNS:
        st.info("Bài này đã đủ số lượt tối đa. Bấm 'Bài mới' ở thanh bên để làm bài khác.")
        st.stop()

    # Tự nâng mức gợi ý nếu học sinh nói bí hai lượt liên tiếp
    if looks_stuck(prompt):
        ss.stuck_count += 1
        if ss.stuck_count >= 2:
            ss.hint_level = min(3, ss.hint_level + 1)
            ss.stuck_count = 0
    else:
        ss.stuck_count = 0

    ss.messages.append({"role": "user", "content": prompt, "files": files})
    with st.chat_message("user"):
        show_files(files)
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Đang suy nghĩ..."):
            try:
                out = ask_tutor(client, ss.messages, topic, ss.hint_level)
            except Exception as e:  # lỗi mạng, hết hạn mức, khóa sai
                out = None
                traceback.print_exc()  # chi tiết đầy đủ hiện ở cửa sổ dòng lệnh đang chạy streamlit
                if getattr(e, "code", None) == 429:
                    st.error("Trợ lý tạm hết lượt dùng. Em chờ một lát rồi thử lại nhé.")
                elif getattr(e, "code", None) in (500, 503, 504):
                    st.error(f"Máy chủ Gemini đang bận (mã {e.code}). Em thử lại sau ít phút nhé.")
                else:
                    st.error(f"Không kết nối được trợ lý ({type(e).__name__}, mã {getattr(e, 'code', '?')}). Em thử lại sau ít phút nhé.")
        if out:
            st.markdown(out["reply"])

    if out:
        ss.messages.append({"role": "assistant", "content": out["reply"]})
        ss.log.append(
            {
                "time": datetime.now().isoformat(timespec="seconds"),
                "student": prompt,
                "tutor": out["reply"],
                "hint_level": ss.hint_level,
                "latency_s": out["latency_s"],
                "flagged_request": out["flagged_request"],
                "retried": out["retried"],
                "violation": out["violation"],
                "n_files": len(files),
                "file_kinds": [f["kind"] for f in files],
                "tokens_in": out["tokens_in"],
                "tokens_out": out["tokens_out"],
                "tokens_thought": out["tokens_thought"],
                "cost_usd": out["cost_usd"],
                "model": out["model"],
            }
        )
        st.rerun()  # làm mới thanh bên (mức gợi ý, nút tải lịch sử)
    else:
        ss.messages.pop()  # bỏ tin nhắn lỗi để không lệch lịch sử