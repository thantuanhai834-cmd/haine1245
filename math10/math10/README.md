# Socratic Math-Tutor 10

Trợ lý học Toán 10 (GDPT 2018) theo phương pháp Socratic: **không giải hộ**, chỉ hỏi từng bước nhỏ để học sinh tự tìm ra lời giải. Ứng dụng web viết bằng Python (Streamlit), dùng Google Gemini API.

Ba chủ đề của Học kỳ 1: Vectơ, Bất phương trình bậc nhất hai ẩn, Hàm số bậc hai.

---

## 1. Chuẩn bị môi trường Python

Cần có Python 3.10 trở lên và kết nối Internet. Mở Terminal/PowerShell **tại thư mục `math10`**, nơi có `app.py` và `requirements.txt`.

### Windows (PowerShell)

Kiểm tra Python Launcher:

```powershell
py -3 --version
```

Tạo môi trường ảo và cài các thư viện cần thiết:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Nếu máy không có lệnh `py`, thay `py -3` bằng `python`. Các lệnh bên trên gọi Python trong `.venv` trực tiếp nên không cần kích hoạt môi trường ảo và không cần đổi Execution Policy của PowerShell.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Giữ nguyên cửa sổ Terminal đã kích hoạt `.venv` cho các bước tiếp theo. Nếu mở cửa sổ mới, kích hoạt lại bằng `source .venv/bin/activate`.

---

## 2. Tạo Gemini API key và cấu hình

1. Đăng nhập [Google AI Studio](https://aistudio.google.com/) và tạo Gemini API key. Key có thể phát sinh chi phí hoặc bị giới hạn theo chính sách/quota của tài khoản và dự án.
2. Chọn **một** trong hai cách cấu hình dưới đây.

### Cách A — lưu key trong Streamlit secrets (khuyên dùng khi chạy app cục bộ)

Từ thư mục `math10`, tạo file secrets từ file mẫu ở thư mục gốc dự án:

**Windows (PowerShell):**

```powershell
New-Item -ItemType Directory -Force .streamlit
Copy-Item secrets.toml.example .streamlit\secrets.toml
notepad .streamlit\secrets.toml
```

**macOS / Linux:**

```bash
mkdir -p .streamlit
cp secrets.toml.example .streamlit/secrets.toml
```

Mở `.streamlit/secrets.toml`, thay giá trị mẫu bằng key thật:

```toml
GEMINI_API_KEY = "AIza...key-cua-ban"
```

Chỉ dán key bên trong dấu ngoặc kép; không thêm khoảng trắng hay chú thích vào giá trị. File mẫu nằm ở `secrets.toml.example`, còn file thật phải nằm ở `.streamlit/secrets.toml`.

### Cách B — đặt biến môi trường

Đặt biến trong cùng cửa sổ dòng lệnh trước khi chạy app:

**Windows (PowerShell):**

```powershell
$env:GEMINI_API_KEY = "AIza...key-cua-ban"
```

**macOS / Linux:**

```bash
export GEMINI_API_KEY="AIza...key-cua-ban"
```

Nếu `.streamlit/secrets.toml` đã có key, app ưu tiên key trong file đó. Không để giá trị mẫu trong file secrets khi muốn dùng biến môi trường.

Mỗi người chạy app trên máy mình nên dùng key riêng. Không đưa key thật hoặc `.streamlit/secrets.toml` lên GitHub, không gửi key qua chat hay ảnh chụp màn hình. Nếu key bị lộ, hãy thu hồi key đó trong AI Studio và tạo key mới. Thư mục `.streamlit/secrets.toml` và môi trường ảo được loại khỏi Git bởi `.gitignore`; vẫn kiểm tra nội dung trước khi commit.

## 3. Chạy ứng dụng Streamlit

Chạy tại thư mục `math10`:

**Windows (PowerShell):**

```powershell
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS / Linux** (sau khi đã kích hoạt `.venv`):

```bash
python -m streamlit run app.py
```

Streamlit sẽ mở trình duyệt tại `http://localhost:8501` (hoặc in URL nếu trình duyệt không tự mở). Dừng ứng dụng bằng `Ctrl+C` trong cửa sổ đang chạy.

## 4. Cách dùng (dành cho học sinh)

1. **Chọn chủ đề** ở thanh bên trái. Đổi chủ đề sẽ bắt đầu bài mới.
2. **Gõ đề bài hoặc đính kèm tối đa 3 tệp** (PNG, JPG, JPEG, WEBP, PDF, DOCX, TXT; mỗi tệp tối đa 8 MB) vào khung chat. Ảnh được thu nhỏ trước khi gửi; trợ lý sẽ không giải, mà nhắc lại đề đọc được rồi hỏi em đề cho biết gì và cần tìm gì. Tệp PDF và ảnh được gửi cho Google; văn bản trong DOCX/TXT được trích xuất, tối đa 4.000 ký tự mỗi tệp. Tệp Word cũ `.doc` không hỗ trợ; công thức Equation hoặc ảnh dán trong Word có thể không đọc được, nên chụp ảnh hoặc xuất PDF.
3. **Trả lời từng câu hỏi** của trợ lý. Mỗi lượt trợ lý nhận xét ngắn, nhắc lại định lí/công thức SGK liên quan, rồi hỏi đúng một câu.
4. **Khi bí**, bấm "Em đang bí, cho gợi ý rõ hơn". Có 3 mức:
   - Mức 1: chỉ hỏi gợi mở.
   - Mức 2: nêu công thức hoặc định lí cần dùng.
   - Mức 3: cho một ví dụ tương tự (số liệu khác) rồi em áp dụng vào bài của mình.
   
   Nói "em không biết/không hiểu" hai lượt liên tiếp thì mức gợi ý cũng tự tăng. Mọi mức đều **không đưa đáp án** của bài gốc.
5. **Theo dõi số lượt**: thanh bên hiện "Lượt hỏi còn lại" và số lần gợi ý rõ hơn còn lại. Khi còn ít lượt, trên khung chat có nhắc nhở.
6. **Bài mới**: bấm "Bài mới" để xóa hội thoại và làm bài khác.
7. **Tải lịch sử (.json)**: lưu nhật ký phiên chat về máy (xem mục 8).
8. Không nhập tên, trường, lớp hay số điện thoại vào khung chat, và che các thông tin đó trong ảnh hoặc tệp. Mỗi tin nhắn tối đa 500 ký tự.

## 5. Cấu hình bằng biến môi trường

Không cần sửa code. Đặt biến trước khi chạy app; các biến chỉ có hiệu lực trong cửa sổ dòng lệnh hiện tại. Cú pháp đặt biến:

PowerShell: `$env:TÊN_BIẾN="giá trị"`  |  macOS/Linux: `export TÊN_BIẾN="giá trị"`

| Biến | Mặc định | Ý nghĩa |
|---|---|---|
| `GEMINI_API_KEY` | (đọc từ `.streamlit/secrets.toml`) | Key Gemini |
| `GEMINI_MODEL` | `gemini-3.6-flash` | Model chính |
| `GEMINI_FALLBACK_MODEL` | `gemini-3.8-flash` | Model dự phòng khi model chính báo lỗi 500/503/504. Đặt `""` để tắt |
| `THINKING_LEVEL` | `low` | Mức "suy nghĩ" của model (`low`/`medium`/`high`). Thấp hơn thì rẻ và nhanh hơn. Đặt `""` để model tự quyết |
| `MAX_OUTPUT_TOKENS` | `1000` | Giới hạn token đầu ra (gồm cả token suy nghĩ) |
| `MAX_HISTORY_MESSAGES` | `8` | Chỉ gửi bấy nhiêu tin gần nhất cho model |
| `MAX_TURNS` | `30` | Số lượt hỏi tối đa mỗi bài |
| `PRICE_IN_PER_M`, `PRICE_OUT_PER_M` | `0.75`, `3.75` | Giá USD mỗi triệu token, chỉ dùng để ước tính chi phí hiển thị. Cập nhật theo trang giá của Google và theo model đang dùng |

Ví dụ chạy với model khác (đặt biến trong cùng cửa sổ Terminal/PowerShell rồi chạy app):

**PowerShell:**

```powershell
$env:GEMINI_MODEL="gemini-3.5-flash-lite"
$env:GEMINI_FALLBACK_MODEL="gemini-3.1-flash-lite"
.\.venv\Scripts\python.exe -m streamlit run app.py
```

**macOS / Linux:**

```bash
GEMINI_MODEL="gemini-3.5-flash-lite" GEMINI_FALLBACK_MODEL="gemini-3.1-flash-lite" python -m streamlit run app.py
```

Tên model và hạn mức thay đổi theo thời gian. Nếu model mặc định không còn dùng được, đặt `GEMINI_MODEL` sang model hiện hành.

## 6. Khi gặp lỗi

Chạy `diag.py` để thử gọi Gemini trực tiếp và in mã lỗi thật (có tối đa 4 phép thử). Đảm bảo đã cấu hình key ở mục 2. **Chỉ chạy một lần khi cần chẩn đoán** vì mỗi phép thử đều gọi API. Không dán key vào khi nhờ người khác xem kết quả.

Script chẩn đoán cần biến môi trường `GEMINI_API_KEY` (kể cả khi app chính đang lấy key từ secrets). Đặt biến rồi chạy:

Windows (PowerShell):

```powershell
$env:GEMINI_API_KEY = "AIza...key-cua-ban"
.\.venv\Scripts\python.exe diag.py
```

macOS / Linux (sau khi đã kích hoạt `.venv`):

```bash
export GEMINI_API_KEY="AIza...key-cua-ban"
python diag.py
```

| Thấy gì | Thường là | Cách xử lý |
|---|---|---|
| "Chưa có Gemini API key thật" | Chưa đặt key hoặc còn chữ mẫu | Làm lại mục 2 |
| Lỗi 429 / "tạm hết lượt dùng" | Hết hạn mức (gói miễn phí tính theo dự án và theo model) | Chờ, đổi sang model khác, hoặc nạp tiền để lên gói trả phí. Xem hạn mức tại trang rate-limit trong AI Studio |
| Lỗi 503 / 504 | Máy chủ Google quá tải. App tự thử lại rồi chuyển model dự phòng | Chờ vài phút, hoặc đổi `GEMINI_MODEL` |
| Lỗi 402 | Hết số dư trả trước | Nạp thêm credits trong mục Billing của AI Studio |
| Lỗi 400 / 403 | Key sai, bị chặn, hoặc không có quyền dùng model | Kiểm tra lại key và tên model |
| Lỗi nhắc tới `thinking_level` | Thư viện `google-genai` cũ | `pip install -U google-genai` |

Lưu ý: yêu cầu bị lỗi vẫn có thể tính vào hạn mức. Đừng bấm gửi hay chạy `diag.py` liên tục khi đang báo lỗi 429.

## 7. Chạy bộ kiểm thử guardrail

Script kiểm thử cũng cần biến môi trường `GEMINI_API_KEY`:

Windows (PowerShell):

```powershell
$env:GEMINI_API_KEY = "AIza...key-cua-ban"
.\.venv\Scripts\python.exe eval_guardrail.py
```

macOS / Linux (sau khi đã kích hoạt `.venv`):

```bash
export GEMINI_API_KEY="AIza...key-cua-ban"
python eval_guardrail.py
```
- Chạy bộ ca bẻ khóa (xin đáp án trực tiếp, giục giã, giả danh giáo viên, đóng vai, tiêm lệnh, ...). Mỗi lần chạy gọi API khoảng 20 đến 40 lần, **chỉ chạy một lần khi cần** để tiết kiệm hạn mức.
- Kết quả ghi vào `ket_qua_kiem_thu.csv` (mở bằng Excel). Cột `tu_dong` chỉ là lọc sơ bộ bằng quy tắc. Có thêm cột `model`, `thoi_gian_s`, token và `chi_phi_usd`.
- **Con số đưa vào báo cáo phải lấy từ cột `giao_vien_cham`**: thầy cô đọc phản hồi và điền "Đạt" (không đưa đáp án) hoặc "Không đạt".
- Bộ ca có sẵn chỉ là khởi đầu. Mở rộng lên ít nhất 100 ca (nhờ bạn bè và thầy cô viết thêm câu bẻ khóa) trước khi báo cáo tỷ lệ, và ghi rõ số ca.
- Chạy lại bằng model khác (đặt `GEMINI_MODEL`) để so sánh. Báo cáo luôn ghi rõ model đã dùng.

## 8. Nhật ký phiên chat (.json)

Nút "Tải lịch sử (.json)" xuất mỗi lượt gồm: thời gian, tin nhắn học sinh, phản hồi của trợ lý, mức gợi ý, thời gian phản hồi, có bị gắn cờ xin đáp án không, có phải thử lại không, vi phạm (nếu có), số lượng tệp và loại tệp đính kèm (không lưu nội dung tệp), số token vào/ra/suy nghĩ, chi phí ước tính và model đã dùng. PDF nhiều trang có thể tốn token hơn.

Nhật ký chỉ nằm trong phiên của từng người, đóng tab là mất. Nếu cho nhiều bạn dùng thì cần nhờ từng bạn tải về và gửi lại, hoặc bổ sung cách ghi nhật ký tập trung.

## 9. Bản HTML chạy thử nhanh

1. Mở `index.html` trong trình duyệt, hoặc chạy `python -m http.server 8000` rồi vào `http://localhost:8000`.
2. Dán Gemini API key vào ô trên giao diện, bấm "Lưu khóa", chọn chủ đề và bắt đầu.
3. Key nằm ở trình duyệt, nên **chỉ dùng thử trên máy cá nhân**, không đưa bản này lên mạng công khai.

## 10. Đưa lên mạng cho nhiều người dùng (Streamlit Community Cloud)

1. Đẩy code lên GitHub (không đẩy key, `.streamlit/secrets.toml` hay `.venv`; `.gitignore` đã bỏ qua các file này).
2. Vào Streamlit Community Cloud, đăng nhập GitHub, chọn repo và nhánh. Vì ứng dụng nằm trong thư mục con `math10`, đặt **Main file path** là `math10/app.py` (không phải `app.py` ở thư mục gốc repo).
3. Trong cài đặt app, mục Secrets, dán: `GEMINI_API_KEY = "key-của-bạn"`.
4. Bấm Deploy, nhận địa chỉ dạng `...streamlit.app`.

Cần biết trước khi gửi link:
- Ai có link đều dùng được và **chi phí tính vào key của người triển khai**. App hiện chưa có mã truy cập.
- Gói API miễn phí dùng chung một hạn mức cho mọi người dùng, và nội dung hội thoại có thể được Google dùng để cải thiện sản phẩm. Với học sinh dùng thật nên dùng key trả phí (nạp trước số tiền nhỏ, đặt trần chi tiêu cho dự án trong AI Studio).
- App miễn phí trên Community Cloud sẽ "ngủ" khi lâu không có người vào, lần mở đầu sẽ chậm.

## 11. Cấu trúc thư mục

| File | Vai trò |
|---|---|
| `app.py` | Giao diện chat Streamlit |
| `core.py` | System prompt Socratic, 3 mức gợi ý, 2 tầng guardrail, gọi Gemini, thử lại và model dự phòng |
| `eval_guardrail.py` | Bộ kiểm thử guardrail, xuất CSV |
| `diag.py` | Chẩn đoán lỗi kết nối Gemini |
| `index.html`, `demo.js` | Bản HTML chạy thử, giữ đồng bộ với `core.py` |
| `secrets.toml.example` | Mẫu để tạo `.streamlit/secrets.toml` chứa key riêng |

**Cách guardrail hoạt động:** tầng 1 nhắc tăng cường khi học sinh có dấu hiệu xin đáp án hoặc cố đổi quy tắc. Tầng 2 lọc đầu ra (đúng một câu hỏi, không có dấu hiệu đưa đáp án); vi phạm thì thử lại một lần, vẫn vi phạm thì dùng câu trả lời an toàn dự phòng. Đây là bộ lọc theo quy tắc, không thay cho việc giáo viên chấm tay.

## 12. Lấy số liệu cho báo cáo

Chỉ dùng số đo thật: tỷ lệ chặn lấy từ cột `giao_vien_cham` (giáo viên chấm độc lập), thời gian phản hồi từ `thoi_gian_s`, chi phí từ cột token và `chi_phi_usd` (đối chiếu với trang Billing trong AI Studio). Mở rộng bộ ca lên 100+ trước khi báo cáo tỷ lệ, và ghi rõ số ca, model đã dùng và ngày chạy.