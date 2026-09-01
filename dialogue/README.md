# Hướng dẫn Sử dụng - Module Trích xuất Văn bản Hội thoại NIKL

Công cụ Python để trích xuất và phân tích đoạn hội thoại từ các file JSON của NIKL Spoken Dialogue Corpus (국립국어원 구어 말뭉치) với khả năng trích xuất có ngữ cảnh.

## 🎯 Tính năng Đặc biệt

- ✅ **Trích xuất có ngữ cảnh**: Lấy cả câu trước và câu sau của mỗi utterance
- ✅ **Theo dõi người nói**: Giữ thông tin speaker_id trong kết quả
- ✅ **Xử lý streaming**: Xử lý file lớn mà không tràn RAM
- ✅ **Gán nhãn POS**: Tự động gán nhãn từ loại bằng Kkma
- ✅ **Lọc theo từ khóa**: Lọc utterance theo từ khóa trong văn bản đã gán nhãn
- ✅ **Kết quả gộp**: Tất cả kết quả khớp trong 1 file duy nhất
- ✅ **Kết quả kép**: Văn bản gốc và văn bản đã gán nhãn với ngữ cảnh

## 📋 Yêu cầu Hệ thống

- Python 3.6 trở lên
- **KoNLPy**: Thư viện NLP tiếng Hàn
- **JDK/JRE**: Java Development Kit (yêu cầu bởi KoNLPy)

### Cài đặt

```bash
pip install konlpy
```

**Lưu ý**: KoNLPy yêu cầu Java. Xem [Hướng dẫn cài đặt KoNLPy](https://konlpy.org/en/latest/install/)

## 📁 Cấu trúc thư mục

```
dialogue/
├── extract_text.py              # Script chính
├── README.md                    # File này
├── input/                       # File JSON nguồn (3227 files)
│   ├── SARW2400000001.json
│   ├── SBRW2400000001.json
│   ├── SCRW2400000001.json
│   ├── SDRW2400000001.json
│   └── ...
└── output/                      # Kết quả từ script
    ├── tagged/                  # Văn bản đã gán nhãn + ngữ cảnh
    │   ├── combined_tagged_아깝_VA.txt
    │   └── SARW2400000061_아깝_VA.jsonl (nếu --keep-jsonl)
    └── raw/                     # Văn bản gốc + ngữ cảnh
        └── combined_raw_아깝_VA.txt
```

## 🔄 Quy trình Xử lý

```
File JSON → JSONL → Đọc từng dòng → Xử lý tuần tự các utterance
                                    (cần truy cập câu trước/sau)
                                    ↓
                            Gán nhãn POS (Kkma)
                                    ↓
                            Lọc theo từ khóa
                                    ↓
                            Trích xuất ngữ cảnh:
                            - Câu trước (raw)
                            - Câu khớp (tagged)
                            - Câu sau (raw)
                            - Speaker ID
                                    ↓
                            Ghi vào file gộp (APPEND mode)
```

**⚠️ Lưu ý**: Xử lý tuần tự (không song song) vì cần truy cập câu trước/sau

## 🚀 Cách sử dụng

### 1. Tìm tất cả utterances chứa từ khóa

```bash
python extract_text.py -i input -o output -k "아깝_VA"
```

**Kết quả**:
- `output/tagged/combined_tagged_아깝_VA.txt` - Tất cả utterances (đã gán nhãn)
- `output/raw/combined_raw_아깝_VA.txt` - Văn bản gốc với ngữ cảnh

### 2. Tìm nhiều từ khóa (từ đồng nghĩa)

```bash
python extract_text.py -i input -o output -k "아쉽_VA" "아깝_VA" "안타깝_VA"
```

Tìm utterances chứa "아쉽다" (tiếc), "아깝다" (lãng phí), hoặc "안타깝다" (đáng tiếc).

### 3. Xử lý một file cụ thể

```bash
python extract_text.py -f input/SARW2400000001.json -k "좋다_VA"
```

### 4. Xử lý chỉ loại file cụ thể

```bash
python extract_text.py -i input -p SARW -k "생각_NNG"  # Chỉ monologue
```

### 5. Giữ lại file JSONL để debug

```bash
python extract_text.py -i input -k "환경_NNG" --keep-jsonl
```

## 📖 Tham số Dòng lệnh

| Tham số | Viết tắt | Mặc định | Mô tả |
|---------|----------|----------|-------|
| **Input Directory** | `-i` | `.` | Thư mục chứa file JSON |
| **Output Directory** | `-o` | `./output` | Thư mục lưu kết quả |
| **Single File** | `-f` | `None` | Xử lý 1 file cụ thể |
| **Prefixes** | `-p` | `SARW SBRW SCRW SDRW` | Tiền tố file cần xử lý |
| **Keywords** | `-k` | `None` | **BẮT BUỘC**: Từ khóa để lọc |
| **Keep JSONL** | `--keep-jsonl` | `False` | Giữ lại file JSONL |

### Chi tiết tham số quan trọng:

#### `-k, --keywords` **⚠️ BẮT BUỘC**
- Tìm kiếm trong **văn bản đã gán nhãn** (sau POS tagging)
- Không phân biệt hoa/thường
- Logic OR (chỉ cần khớp 1 từ khóa)
- Có thể search cả từ hoặc từ_Nhãn

**Ví dụ**:
```bash
# Tìm động từ "아깝다"
python extract_text.py -i input -k "아깝_VA"

# Tìm danh từ "환경"
python extract_text.py -i input -k "환경_NNG"

# Nhiều từ khóa
python extract_text.py -i input -k "좋다_VA" "훌륭하다_VA" "멋지다_VA"
```

## 📄 Cấu trúc Dữ liệu

### Input JSON (Dialogue Corpus)

```json
{
  "id": "SARW2400000001",
  "document": [
    {
      "metadata": {
        "topic": "스포츠/레저/취미",
        "speaker": [{"id": "SD2401801", "age": "30대", "sex": "남성"}]
      },
      "utterance": [
        {
          "id": "SARW2400000001.1.1.1",
          "form": "저는 개인적으로 복사가 터졌으면 좋겠어요.",
          "speaker_id": "SD2401801",
          "start": 0.129,
          "end": 3.259
        }
      ]
    }
  ]
}
```

### Output Files

#### 1. `combined_raw_{từ-khóa}.txt` - Văn bản Gốc với Ngữ cảnh

```
speaker_id-SD2401817 
예를 들어서 크루즈 여행. 1억을 줘도 안 아깝다라고 이거 전보다 아주 인기가 높아졌다란 기사 내용도 있었고.

speaker_id-SD2401295 
그걸 하나도 못 먹었던 거 같아. 그 동생들하고 이렇게 줘야 된다고 너무너무 아까워 가지고. 빵은 너무너무 귀한 거고...
```

**Format**: `speaker_id-{ID}` + `{câu trước}. {câu khớp} {câu sau}.`

#### 2. `combined_tagged_{từ-khóa}.txt` - Đã gán nhãn với Ngữ cảnh

```
Previous sentence:예를 들어서 크루즈 여행
speaker_id:SD2401817:1_NR 억_NR 을_JKO 주_VV 어도_ECD 안_MAG 아깝_VA 다_EFN 라고_JKQ 이거_NP 
Next sentence:전보다 아주 인기가 높아졌다란 기사 내용도 있었고.

Previous sentence:그걸 하나도 못 먹었던 거 같아.
speaker_id:SD2401295:그_MDT 동생_NNG 들_XSN 하_VV 고_ECE...
Next sentence:빵은 너무너무 귀한 거고...
```

**Format**: 
- `Previous sentence:{văn bản gốc}`
- `speaker_id:{ID}:{văn bản đã gán nhãn}`
- `Next sentence:{văn bản gốc}`

## 💡 Ví dụ Thực tế

### Ví dụ 1: Nghiên cứu từ vựng cảm xúc

Tìm tất cả cách dùng "아깝다" (tiếc/lãng phí):

```bash
python extract_text.py -i input -o output -k "아깝_VA"
```

**Kết quả**: Corpus với ~10-20 ví dụ về cách người Hàn dùng "아깝다" trong hội thoại thực tế.

### Ví dụ 2: So sánh từ đồng nghĩa

So sánh 3 từ về "tiếc nuối":

```bash
python extract_text.py -i input -k "아쉽_VA"
python extract_text.py -i input -k "아깝_VA"
python extract_text.py -i input -k "안타깝_VA"
```

### Ví dụ 3: Tìm patterns ngữ pháp

Tìm cấu trúc "N + 이/가 + 아깝다":

```bash
python extract_text.py -i input -k "아깝_VA"
# Sau đó phân tích trong file kết quả
```

### Ví dụ 4: Nghiên cứu chủ đề

Tìm cách nói về "thời gian":

```bash
python extract_text.py -i input -k "시간_NNG"
```

### Ví dụ 5: Phân tích collocation

Tìm các từ đi với "환경" (môi trường):

```bash
python extract_text.py -i input -k "환경_NNG"
```

## ⚠️ LƯU Ý QUAN TRỌNG

### 🔴 CRITICAL: Chế độ Append

**Script sử dụng APPEND mode - PHẢI xóa file cũ trước khi chạy lại!**

```bash
# ❌ SAI - Sẽ bị trùng lặp dữ liệu:
python extract_text.py -k "아깝_VA"  # Lần 1
python extract_text.py -k "아깝_VA"  # Lần 2 → DỮ LIỆU BỊ TRÙNG!

# ✅ ĐÚNG - Xóa trước khi chạy lại:
Remove-Item output/tagged/*.txt
Remove-Item output/raw/*.txt
python extract_text.py -k "아깝_VA"  # Bây giờ an toàn
```

### Lý do Append Mode

- Cho phép gộp kết quả từ nhiều file vào 1 file
- Tiện cho phân tích tập trung
- NHƯNG cần cẩn thận khi chạy lại

## 🔧 Chi tiết Kỹ thuật

### Xử lý Tuần tự (Không Song song)

```python
# KHÔNG thể song song vì cần truy cập câu trước/sau
for i in range(len(utterances)):
    prev = utterances[i-1] if i > 0 else None
    curr = utterances[i]
    next = utterances[i+1] if i < len(utterances)-1 else None
    
    if keyword_match(curr):
        save_with_context(prev, curr, next, speaker_id)
```

**Trade-off**:
- ❌ Chậm hơn module newspapers (~50% tốc độ)
- ✅ Có ngữ cảnh quan trọng cho phân tích hội thoại

### So sánh với Module Newspapers

| Đặc điểm | Newspapers | Dialogue |
|----------|-----------|----------|
| **Tốc độ** | 100-200 docs/giây | 50-100 docs/giây |
| **Xử lý** | Song song (8 workers) | Tuần tự |
| **Ngữ cảnh** | Không | Có (prev+next) |
| **Speaker** | Không | Có tracking |
| **Output** | Per-file | Gộp (combined) |
| **Dùng cho** | Phân tích văn bản | Phân tích hội thoại |

## 📊 Hiệu suất

### Môi trường Test
- **CPU**: i5 13400
- **RAM**: 32GB
- **Dataset**: 3227 file JSON hội thoại

### Điểm chuẩn

| Chỉ số | Giá trị |
|--------|---------|
| Tốc độ xử lý | 50-100 docs/giây |
| Tốc độ gán nhãn Kkma | 100-500ms/utterance |
| Bộ nhớ/document | ~100KB-1MB |
| Điểm nghẽn | Gán nhãn Kkma |

## 🐛 Khắc phục Sự cố

### 1. File output bị trùng lặp
**Nguyên nhân**: Chạy lại mà không xóa file cũ  
**Giải pháp**: Xóa file output trước:
```bash
Remove-Item output/tagged/*.txt
Remove-Item output/raw/*.txt
```

### 2. Không có kết quả
**Nguyên nhân**: Không có utterance nào khớp từ khóa  
**Giải pháp**:
- Kiểm tra từ khóa có đúng không
- Thử từ khóa tổng quát hơn: `"환경"` thay vì `"환경_NNG"`
- Thử với file cụ thể: `-f input/SARW2400000001.json`

### 3. ImportError: konlpy
**Giải pháp**: `pip install konlpy`

### 4. Java không tìm thấy
**Giải pháp**: Cài Java và đặt JAVA_HOME

### 5. OutOfMemoryError
**Giải pháp**: Tăng heap trong code:
```python
kkma: Kkma = Kkma(max_heap_size=4096)
```

## 📝 Tiền tố File Hỗ trợ

| Tiền tố | Loại | Mô tả |
|---------|------|-------|
| `SARW` | 공적 독백 | Monologue công khai |
| `SBRW` | 공적 대화 | Đối thoại công khai |
| `SCRW` | 사적 독백 | Monologue riêng tư |
| `SDRW` | 사적 대화 | Hội thoại hàng ngày |

## 🔍 Ứng dụng Nghiên cứu

### 1. Nghiên cứu Ngôn ngữ học
- Phân tích từ đồng nghĩa với ngữ cảnh
- Nghiên cứu patterns hội thoại
- Phân tích diễn ngôn
- Đặc điểm người nói

### 2. Học Ngôn ngữ
- Câu ví dụ thực tế
- Học theo ngữ cảnh
- Patterns hội thoại tự nhiên

### 3. Dữ liệu NLP
- Phân tích cảm xúc
- Hệ thống đối thoại
- Training data cho chatbot

### 4. Ngôn ngữ học Xã hội
- Biến thể register
- Patterns theo tuổi/giới tính
- Phân tích theo chủ đề

## 🤝 Đóng góp

Hoan nghênh đóng góp! Báo lỗi hoặc đề xuất tính năng qua GitHub Issues.

## 📜 Giấy phép

Giấy phép MIT - Tự do sử dụng.

## 👨‍💻 Cảm ơn

- **NIKL** (국립국어원) - Cung cấp corpus
- **KoNLPy Team** - Thư viện NLP tiếng Hàn
- **Kkma** - Phân tích hình thái học

---

**Cập nhật**: 01/09/2026  
**Phiên bản**: 1.0  
**Python**: 3.6+  
**Dataset**: NIKL Spoken Dialogue Corpus 2024 (3227 files)
