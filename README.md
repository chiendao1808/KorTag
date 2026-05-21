# NIKL Newspaper Text Extractor

Tool Python để trích xuất text từ các file JSON của NIKL Newspaper Corpus (국립국어원 신문 말뭉치).

## 🎯 Tính năng

- ✅ **Streaming processing**: Xử lý file lớn (đến 1GB) mà không tràn RAM
- ✅ **Trích xuất text**: Lấy tất cả nội dung từ field `form` trong các `paragraph`
- ✅ **Lọc theo keyword**: Hỗ trợ lọc text theo nhiều từ khóa
- ✅ **Loại bỏ HTML tags**: Tự động clean các tag `<p>`, `</p>`
- ✅ **Output có cấu trúc**: Đánh dấu rõ ràng document và paragraph
- ✅ **UTF-8 BOM**: Tương thích hoàn hảo với Windows (Notepad, Excel)
- ✅ **Progress indicator**: Hiển thị tiến trình xử lý real-time

## 📋 Yêu cầu

- Python 3.6 trở lên
- Không cần cài thêm thư viện (chỉ dùng Python standard library)

## 🚀 Cách sử dụng

### 1. Xử lý tất cả file JSON trong thư mục hiện tại

```bash
python extract_text.py
```

Output sẽ được lưu trong thư mục `./output/`

### 2. Xử lý một file cụ thể

```bash
python extract_text.py -f NLRW2400000001.json
```

### 3. Lọc theo keyword

Chỉ lấy các paragraph chứa từ khóa "울산" hoặc "환경":

```bash
python extract_text.py -f NIRW2400000001.json -k "아쉽_VA" "아깝_VA" "안타깝_VA"
```

### 4. Chỉ xử lý file có prefix cụ thể

Chỉ xử lý file NLRW và NPRW:

```bash
python extract_text.py -p NLRW NPRW
```

### 5. Chỉ định thư mục input/output

```bash
python extract_text.py -i ./input_folder -o ./output_folder
```

### 6. Giữ lại file JSONL trung gian

Mặc định file JSONL tạm sẽ bị xóa sau khi xử lý. Để giữ lại:

```bash
python extract_text.py --keep-jsonl
```

## 📖 Tất cả tùy chọn

```bash
python extract_text.py --help
```

### Các tham số:

| Tham số | Mô tả | Mặc định |
|---------|-------|----------|
| `-i, --input-dir` | Thư mục chứa file JSON | `.` (thư mục hiện tại) |
| `-o, --output-dir` | Thư mục lưu file txt output | `./output` |
| `-f, --file` | Xử lý một file JSON cụ thể | None (xử lý tất cả) |
| `-p, --prefixes` | Prefix của file cần xử lý | `NIRW NLRW NPRW NZRW NWRW` |
| `-k, --keywords` | Keywords để lọc text | None (lấy tất cả) |
| `--keep-jsonl` | Giữ lại file JSONL sau khi xử lý | False |

## 📄 Cấu trúc output

File txt output có cấu trúc rõ ràng, dễ đọc:

```
============================================================
[DOCUMENT 1] ID: NLRW2400000005.1
Title: 울산제일일보 2023년 기사
Date: 20230101
Topic: 사회
============================================================

[Paragraph 1]
울산시민의 식수, 바다에서 구하는 방안

[Paragraph 2]
김두겸 울산시장의 기억에 남는 세밑 화두 가운데 하나는...

[Paragraph 3]
해수담수화 사업은 이웃 부산시에서 먼저 손댔다가...

------------------------------------------------------------
Total paragraphs in this document: 10
------------------------------------------------------------

============================================================
[DOCUMENT 2] ID: NLRW2400000005.2
...
```

## 💡 Ví dụ thực tế

### Ví dụ 1: Trích xuất tất cả text từ file NLRW

```bash
python extract_text.py -p NLRW
```

### Ví dụ 2: Tìm tất cả bài viết về "기후변화" (biến đổi khí hậu)

```bash
python extract_text.py -k "기후변화"
```

### Ví dụ 3: Xử lý file lớn và giữ JSONL để debug

```bash
python extract_text.py -f NLRW2400000001.json --keep-jsonl
```

### Ví dụ 4: Tìm bài viết có nhiều keyword

```bash
python extract_text.py -k "울산" "환경" "해수담수화"
```

## 🔧 Cách hoạt động

1. **Convert JSON → JSONL**: Chuyển đổi file JSON lớn thành JSONL để streaming
2. **Streaming processing**: Đọc từng document một, không load toàn bộ vào RAM
3. **Extract & Filter**: Trích xuất text từ field `form`, lọc theo keyword nếu có
4. **Clean HTML**: Loại bỏ các HTML tags
5. **Format output**: Thêm markers cho document và paragraph
6. **Save to file**: Lưu vào file txt với encoding UTF-8-BOM

## 📊 Hiệu năng

- **File 1GB**: Xử lý mượt mà trên máy i5 13400 + 32GB RAM
- **Memory usage**: Chỉ load từng document một, không tràn RAM
- **Speed**: ~100-200 documents/giây (tùy kích thước document)

## 🐛 Xử lý lỗi

Tool tự động xử lý các lỗi phổ biến:

- ✅ File JSON bị lỗi format → Skip và tiếp tục
- ✅ Document thiếu field → Bỏ qua và xử lý document tiếp theo
- ✅ Encoding issues → Sử dụng UTF-8-BOM để tương thích Windows

## 📝 Supported File Prefixes

Tool hỗ trợ các prefix sau (theo NIKL Newspaper Corpus):

- `NIRW` - 인터넷 신문 (Internet newspapers)
- `NLRW` - 지역 종합지 (Regional newspapers)
- `NPRW` - 전문지 (Professional newspapers)
- `NZRW` - 잡지 (Magazines)
- `NWRW` - 주간지 (Weekly newspapers)

## 🤝 Đóng góp

Nếu gặp lỗi hoặc có đề xuất cải tiến, vui lòng tạo issue hoặc pull request.

## 📜 License

MIT License - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 👨‍💻 Tác giả

Tool được phát triển để xử lý NIKL Newspaper Corpus 2024 v1.0

---

**Lưu ý**: Tool này được tối ưu cho môi trường Windows với encoding UTF-8-BOM để đảm bảo hiển thị đúng tiếng Hàn trên Notepad và các ứng dụng Windows khác.
