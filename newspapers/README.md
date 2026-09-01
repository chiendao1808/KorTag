# Hướng dẫn Sử dụng - Module Trích xuất Văn bản Báo chí NIKL

Công cụ Python để trích xuất văn bản từ các file JSON của NIKL Newspaper Corpus (국립국어원 신문 말뭉치) và thực hiện gán nhãn từ loại (POS) bằng KoNLPy.

## 🎯 Tính năng

- ✅ **Xử lý streaming**: Xử lý file lớn (đến 1GB) mà không tràn RAM
- ✅ **Trích xuất văn bản**: Lấy tất cả nội dung từ field `form` trong các `paragraph`
- ✅ **Gán nhãn POS**: Tự động gán nhãn từ loại bằng Kkma (Korean Morphological Analyzer)
- ✅ **Xử lý song song**: Xử lý đa luồng (8 workers) để tăng tốc độ
- ✅ **Lọc theo từ khóa**: Hỗ trợ lọc văn bản theo nhiều từ khóa trong văn bản đã gán nhãn
- ✅ **Loại bỏ thẻ HTML**: Tự động làm sạch các thẻ `<p>`, `</p>`
- ✅ **Kết quả kép**: Tạo cả văn bản gốc và văn bản đã gán nhãn
- ✅ **Mã hóa UTF-8**: Làm sạch và xử lý lỗi mã hóa tự động
- ✅ **Hiển thị tiến trình**: Hiển thị tiến trình xử lý thời gian thực

## 📋 Yêu cầu Hệ thống

- Python 3.6 trở lên
- **KoNLPy**: Thư viện NLP tiếng Hàn
- **JDK/JRE**: Java Development Kit (yêu cầu bởi KoNLPy)

### Cài đặt thư viện

```bash
pip install konlpy
```

**Lưu ý**: KoNLPy yêu cầu Java. Tham khảo [Hướng dẫn cài đặt KoNLPy](https://konlpy.org/en/latest/install/) để cài đặt đầy đủ.

## 📁 Cấu trúc thư mục

```
newspapers/
├── extract_text.py              # Script chính
├── HDSD.md                      # File này
├── PHAN_TICH_CODE.md           # Phân tích kỹ thuật
├── plan.md                      # Tài liệu kế hoạch
├── POS_tagger_(kkma).ipynb     # Jupyter notebook thử nghiệm
├── processed/                   # Chứa file JSON nguồn (115 files)
│   ├── NIRW2400000001.json
│   ├── NIRW2400000002.json
│   └── ...
├── unprocessed/                 # Chứa file JSON chưa xử lý
├── output/                      # Kết quả từ script (JSONL + TXT)
│   ├── NIRW2400000001.jsonl    # File JSONL trung gian
│   ├── NIRW2400000001_tagged.txt  # Kết quả đã gán nhãn POS
│   └── NIRW2400000001_raw.txt     # Kết quả văn bản gốc
├── tagged/                      # Thư mục cho kết quả đã gán nhãn
└── untagged/                    # Thư mục cho kết quả chưa gán nhãn
```

## 🔄 Quy trình Thực hiện

```
┌─────────────────┐
│ File JSON đầu vào│ (NIRW*.json, NLRW*.json, v.v.)
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 1. Chuyển đổi JSON → JSONL      │  Chuyển toàn bộ mảng document
│    - Load toàn bộ JSON          │  thành JSONL để streaming
│    - Trích xuất mảng document   │
│    - Ghi 1 document/dòng        │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 2. Xử lý Streaming               │  Đọc từng dòng JSONL
│    - Đọc từng dòng một          │  (tiết kiệm RAM)
│    - Phân tích mỗi document     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 3. Xử lý Paragraph Song song    │  ThreadPoolExecutor (8 workers)
│    Với mỗi paragraph:           │
│    ├─ Xóa thẻ HTML             │  Regex: <[^>]+>
│    ├─ Làm sạch mã hóa UTF-8    │  Xử lý lỗi encoding
│    ├─ Gán nhãn POS (Kkma)      │  형태소 분석
│    └─ Định dạng: từ_Nhãn       │  Ví dụ: 아쉽_VA 다_EC
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 4. Lọc Từ khóa (Tùy chọn)      │  Nếu có tham số -k
│    - Kiểm tra từ khóa trong    │  Tìm trong văn bản đã gán nhãn
│      văn bản đã gán nhãn        │  (không phân biệt hoa thường)
│    - Chỉ giữ paragraph khớp     │
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 5. Ghi Kết quả                  │
│    ├─ *_tagged.txt              │  Đã gán nhãn (từ_Nhãn từ_Nhãn)
│    └─ *_raw.txt                 │  Văn bản gốc (tiếng Hàn sạch)
└────────┬────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│ 6. Dọn dẹp (Tùy chọn)          │  Nếu không dùng --keep-jsonl
│    - Xóa file JSONL             │
└─────────────────────────────────┘
```

## 🚀 Cách sử dụng

### 1. Xử lý tất cả file JSON trong thư mục hiện tại

```bash
python extract_text.py
```

Kết quả sẽ được lưu trong thư mục `./output/`:
- `TÊN-FILE_tagged.txt` - Văn bản đã gán nhãn POS
- `TÊN-FILE_raw.txt` - Văn bản gốc (đã làm sạch)
- `TÊN-FILE.jsonl` - File trung gian (sẽ bị xóa nếu không dùng `--keep-jsonl`)

### 2. Xử lý một file cụ thể

```bash
python extract_text.py -f processed/NLRW2400000001.json
```

### 3. Lọc theo từ khóa (trong văn bản đã gán nhãn)

Chỉ lấy các paragraph có chứa nhãn POS "아쉽_VA", "아깝_VA" hoặc "안타깝_VA":

```bash
python extract_text.py -f processed/NIRW2400000001.json -k "아쉽_VA" "아깝_VA" "안타깝_VA"
```

**Lưu ý**: Tìm kiếm từ khóa được thực hiện trên **văn bản đã gán nhãn** (sau khi gán nhãn POS), không phải văn bản gốc. Tìm kiếm không phân biệt hoa/thường.

### 4. Chỉ xử lý file có tiền tố cụ thể

Chỉ xử lý file NLRW và NPRW:

```bash
python extract_text.py -i processed -p NLRW NPRW
```

### 5. Chỉ định thư mục đầu vào/đầu ra

```bash
python extract_text.py -i ./processed -o ./tagged
```

### 6. Giữ lại file JSONL trung gian

Mặc định file JSONL tạm sẽ bị xóa sau khi xử lý. Để giữ lại (để debug):

```bash
python extract_text.py --keep-jsonl
```

## 📖 Tham số Dòng lệnh

Xem tất cả tùy chọn:
```bash
python extract_text.py --help
```

### Bảng tham số chi tiết:

| Tham số | Viết tắt | Dạng đầy đủ | Kiểu dữ liệu | Mặc định | Mô tả |
|---------|----------|-------------|--------------|----------|-------|
| **Thư mục đầu vào** | `-i` | `--input-dir` | chuỗi | `.` | Thư mục chứa file JSON nguồn |
| **Thư mục đầu ra** | `-o` | `--output-dir` | chuỗi | `./output` | Thư mục lưu file kết quả (tagged.txt, raw.txt) |
| **File đơn** | `-f` | `--file` | chuỗi | `None` | Đường dẫn đến 1 file JSON cụ thể cần xử lý |
| **Tiền tố** | `-p` | `--prefixes` | danh sách | `NIRW NLRW NPRW NZRW NWRW` | Danh sách tiền tố của file cần xử lý |
| **Từ khóa** | `-k` | `--keywords` | danh sách | `None` | Danh sách từ khóa để lọc (tìm trong văn bản đã gán nhãn) |
| **Giữ JSONL** | - | `--keep-jsonl` | cờ | `False` | Giữ lại file JSONL trung gian (không xóa) |

### Chi tiết từng tham số:

#### `-i, --input-dir` (chuỗi)
- **Mục đích**: Chỉ định thư mục chứa file JSON nguồn
- **Mặc định**: `.` (thư mục hiện tại)
- **Ví dụ**: 
  ```bash
  python extract_text.py -i ./processed
  python extract_text.py --input-dir ../data/newspapers
  ```

#### `-o, --output-dir` (chuỗi)
- **Mục đích**: Chỉ định thư mục lưu file kết quả
- **Mặc định**: `./output`
- **File kết quả**: `TÊN-FILE_tagged.txt`, `TÊN-FILE_raw.txt`, `TÊN-FILE.jsonl` (nếu giữ)
- **Ví dụ**: 
  ```bash
  python extract_text.py -o ./tagged
  python extract_text.py --output-dir ./results/batch1
  ```

#### `-f, --file` (chuỗi)
- **Mục đích**: Xử lý một file JSON cụ thể thay vì xử lý hàng loạt
- **Mặc định**: `None` (xử lý tất cả file theo tiền tố)
- **Ví dụ**: 
  ```bash
  python extract_text.py -f processed/NIRW2400000001.json
  python extract_text.py --file ./data/NLRW2400000005.json
  ```
- **Lưu ý**: Khi dùng `-f`, các tham số `-i` và `-p` sẽ bị bỏ qua

#### `-p, --prefixes` (danh sách)
- **Mục đích**: Lọc file theo tiền tố (chỉ xử lý file có tên bắt đầu với tiền tố này)
- **Mặc định**: `NIRW NLRW NPRW NZRW NWRW` (tất cả tiền tố NIKL Newspaper)
- **Ví dụ**: 
  ```bash
  python extract_text.py -p NIRW          # Chỉ xử lý file NIRW
  python extract_text.py -p NLRW NPRW     # Xử lý NLRW và NPRW
  python extract_text.py --prefixes NZRW  # Chỉ xử lý tạp chí
  ```

#### `-k, --keywords` (danh sách)
- **Mục đích**: Lọc paragraph theo từ khóa (chỉ giữ paragraph có chứa ít nhất 1 từ khóa)
- **Mặc định**: `None` (lấy tất cả paragraph)
- **Cơ chế**: 
  - Tìm kiếm được thực hiện trên **văn bản đã gán nhãn** (sau khi gán nhãn POS)
  - Không phân biệt hoa/thường
  - Chỉ cần khớp 1 từ khóa là giữ lại paragraph
- **Định dạng từ khóa**: Có thể tìm cả từ hoặc từ_Nhãn
- **Ví dụ**: 
  ```bash
  # Tìm paragraph có chứa các động từ "아쉽다", "아깝다", "안타깝다"
  python extract_text.py -k "아쉽_VA" "아깝_VA" "안타깝_VA"
  
  # Tìm paragraph có chứa từ "환경" (bất kỳ nhãn POS nào)
  python extract_text.py -k "환경"
  
  # Kết hợp nhiều từ khóa
  python extract_text.py -k "울산" "환경" "해수담수화"
  ```

#### `--keep-jsonl` (cờ)
- **Mục đích**: Giữ lại file JSONL trung gian (không xóa sau khi xử lý)
- **Mặc định**: `False` (tự động xóa để tiết kiệm dung lượng)
- **Khi nào dùng**: Debug, kiểm tra dữ liệu trung gian, hoặc muốn tái sử dụng JSONL
- **Ví dụ**: 
  ```bash
  python extract_text.py --keep-jsonl
  python extract_text.py -f large_file.json --keep-jsonl  # Debug file lớn
  ```

## 📄 Cấu trúc Đầu vào/Đầu ra

### Cấu trúc JSON Đầu vào

File JSON nguồn có cấu trúc như sau:

```json
{
  "id": "NLRW2400000005",
  "metadata": {
    "title": "국립국어원 신문 말뭉치 NLRW2400000005",
    "category": "신문 > 지역 종합지",
    "year": "2024"
  },
  "document": [
    {
      "id": "NLRW2400000005.1",
      "metadata": {
        "title": "울산제일일보 2023년 기사",
        "date": "20230101",
        "topic": "사회"
      },
      "paragraph": [
        {
          "id": "NLRW2400000005.1.1",
          "form": "<p>울산시민의 식수, 바다에서 구하는 방안</p>"
        },
        {
          "id": "NLRW2400000005.1.2",
          "form": "<p>김두겸 울산시장의 기억에...</p>"
        }
      ]
    }
  ]
}
```

**Dữ liệu được trích xuất**: Field `form` trong mỗi `paragraph`

### File Kết quả

Script tạo ra **2 loại file kết quả** cho mỗi file JSON:

#### 1. `*_raw.txt` - Văn bản Gốc (Tiếng Hàn sạch)

```
울산시민의 식수, 바다에서 구하는 방안

김두겸 울산시장의 기억에 남는 세밑 화두 가운데 하나는 '해수담수화(海水淡水化) 검토'였다.

해수담수화 사업은 이웃 부산시에서 먼저 손댔다가...
```

- Đã loại bỏ thẻ HTML (`<p>`, `</p>`)
- Mã hóa UTF-8 sạch
- Mỗi paragraph cách nhau 2 dòng trống

#### 2. `*_tagged.txt` - Văn bản đã Gán nhãn POS

```
울산_NNG 시민_NNG 의_JKG 식수_NNG ,_SP 바다_NNG 에서_JKM 구하_VV 는_ETD 방안_NNG

김두겸_NNP 울산_NNP 시장_NNG 의_JKG 기억_NNG 에_JKM 남_VV 는_ETD 세밑_NNG 화두_NNG 가운데_NNG 하나_NNG 는_JX '_SS 해수_NNG 담수_NNG 화_XSN (_SS 海_SH 水_SH 淡_SH 水_SH 化_SH )_SS 검토_NNG '_SS 였_VCP 다_EFN ._SF

해수_NNG 담수_NNG 화_XSN 사업_NNG 은_JX 이웃_NNG 부산시_NNP 에서_JKM 먼저_MAG 손대_VV 었_EPT 다가_ECS ...
```

- Định dạng: `từ_Nhãn` (nhãn từ loại POS)
- Mỗi paragraph một dòng, các từ cách nhau bằng khoảng trắng
- Mỗi paragraph cách nhau 2 dòng trống

### Các Nhãn POS Phổ biến (Kkma)

| Nhãn | Loại từ | Ví dụ |
|------|---------|-------|
| `NNG` | Danh từ chung (명사) | 사람, 환경, 시장 |
| `NNP` | Danh từ riêng (고유명사) | 울산, 김두겸 |
| `VV` | Động từ (동사) | 하다, 가다, 보다 |
| `VA` | Tính từ (형용사) | 아쉽다, 좋다, 크다 |
| `MAG` | Trạng từ chung (부사) | 매우, 아주, 잘 |
| `JKS` | Trợ từ chủ ngữ (주격조사) | 이, 가 |
| `JKO` | Trợ từ tân ngữ (목적격조사) | 을, 를 |
| `JKG` | Trợ từ sở hữu (관형격조사) | 의 |
| `EFN` | Vĩ tố kết thúc bình thường (평서형 종결어미) | 다, 니다 |
| `SF` | Dấu câu kết thúc (마침표) | ., ?, ! |
| `SP` | Dấu phân cách (쉼표) | , |

Xem thêm: [Bộ nhãn Kkma](https://konlpy.org/en/latest/api/konlpy.tag/#module-konlpy.tag._kkma)

## 💡 Ví dụ Thực tế

### Ví dụ 1: Xử lý tất cả file trong thư mục processed/

```bash
python extract_text.py -i processed -o output
```

**Kết quả**: 
- Xử lý tất cả file NIRW, NLRW, NPRW, NZRW, NWRW trong thư mục `processed/`
- Tạo kết quả trong `output/`

### Ví dụ 2: Xử lý chỉ báo địa phương (NLRW)

```bash
python extract_text.py -i processed -o tagged -p NLRW
```

**Kết quả**: 
- Chỉ xử lý các file có tiền tố `NLRW` (지역 종합지 - báo địa phương)

### Ví dụ 3: Tìm tất cả paragraph chứa động từ "아쉽다", "아깝다", "안타깝다"

```bash
python extract_text.py -i processed -o output -k "아쉽_VA" "아깝_VA" "안타깝_VA"
```

**Kết quả**: 
- Chỉ lưu các paragraph có chứa ít nhất 1 trong 3 động từ này
- Hữu ích để phân tích cảm xúc hoặc nghiên cứu ngữ nghĩa

### Ví dụ 4: Xử lý một file lớn với chế độ debug

```bash
python extract_text.py -f processed/NLRW2400000001.json -o output --keep-jsonl
```

**Kết quả**: 
- Xử lý file cụ thể
- Giữ lại file JSONL để kiểm tra nếu có vấn đề

### Ví dụ 5: Xử lý hàng loạt với nhiều từ khóa

```bash
python extract_text.py -i processed -o results -k "환경" "기후변화" "탄소중립" "재생에너지"
```

**Kết quả**: 
- Trích xuất tất cả paragraph về chủ đề môi trường
- Hữu ích cho nghiên cứu về biến đổi khí hậu trong truyền thông Hàn Quốc

## 🔧 Cách hoạt động (Chi tiết Kỹ thuật)

### Quy trình Xử lý

1. **Chuyển đổi JSON → JSONL**
   - Load toàn bộ file JSON vào bộ nhớ
   - Trích xuất mảng `document`
   - Ghi mỗi document thành 1 dòng JSONL
   - ⚠️ Bước này cần đủ RAM cho file JSON lớn (tối đa ~1GB)

2. **Xử lý Streaming**
   - Đọc file JSONL từng dòng (1 document/lần)
   - Tiết kiệm RAM vì không load toàn bộ file
   - Hiển thị tiến trình mỗi 100 documents

3. **Xử lý Paragraph Song song**
   - Sử dụng `ThreadPoolExecutor` với 8 workers
   - Xử lý đồng thời nhiều paragraphs trong 1 document
   - Mỗi paragraph:
     - Xóa thẻ HTML với regex: `r'<[^>]+>'`
     - Làm sạch mã hóa UTF-8 (xử lý lỗi)
     - Gán nhãn POS với Kkma
     - Định dạng: `từ_Nhãn từ_Nhãn ...`

4. **Lọc Từ khóa**
   - Tìm kiếm không phân biệt hoa thường trong văn bản đã gán nhãn
   - Chỉ cần khớp 1 từ khóa
   - Sử dụng toán tử `in` của Python

5. **Ghi Kết quả**
   - Ghi từng phần (không buffer toàn bộ)
   - Mã hóa UTF-8
   - Mỗi paragraph cách nhau 2 dòng trống

6. **Dọn dẹp**
   - Xóa file JSONL nếu không dùng `--keep-jsonl`

### Quản lý Bộ nhớ

- **Trường hợp xấu nhất**: Khi chuyển đổi JSON → JSONL, cần RAM = kích thước file JSON
- **Trường hợp tốt nhất**: Sau khi có JSONL, chỉ cần RAM cho 1 document (~1-10MB)
- **Khuyến nghị**: 8GB+ RAM cho file 1GB

### Chỉ số Hiệu suất

- **Gán nhãn POS Kkma**: Điểm nghẽn chính (thường 100-500ms/paragraph)
- **ThreadPoolExecutor**: Giảm thời gian xử lý ~6-8x với 8 workers
- **Theo dõi thời gian tối đa**: Script tự động log `max_pos_kkma_time` để giám sát

### Xử lý Lỗi

- **Lỗi giải mã JSON**: Bỏ qua dòng đó, tiếp tục xử lý
- **Lỗi mã hóa UTF-8**: Thay thế bằng ký tự placeholder
- **Lỗi Kkma**: Bắt exception, log văn bản lỗi, trả về danh sách rỗng
- **Thiếu field**: Sử dụng `.get()` với giá trị mặc định

## 📊 Hiệu năng & Thông số

### Môi trường Test
- **CPU**: i5 13400
- **RAM**: 32GB
- **GPU**: GTX 1060 6GB (không sử dụng)
- **HĐH**: Windows
- **Python**: 3.x

### Điểm chuẩn Hiệu suất

| Chỉ số | Giá trị | Ghi chú |
|--------|---------|---------|
| Kích thước file tối đa đã test | ~1GB | File JSON |
| Tốc độ xử lý | ~100-200 docs/giây | Phụ thuộc số paragraph |
| Tốc độ gán nhãn Kkma | 100-500ms/paragraph | Điểm nghẽn |
| Thời gian Kkma tối đa quan sát | Thay đổi | Được log cuối lần chạy |
| Sử dụng bộ nhớ (streaming) | ~1-10MB/document | Sau chuyển đổi JSONL |
| Sử dụng bộ nhớ (chuyển đổi) | ~Kích thước file | Bước JSON → JSONL |
| Số worker threads | 8 | Có thể cấu hình trong code |
| Kích thước heap (Kkma) | 2048MB | JVM heap cho KoNLPy |

### Mẹo Tối ưu

1. **Tăng số workers** (nếu có nhiều lõi CPU):
   ```python
   # Trong extract_text.py, dòng ~88
   with ThreadPoolExecutor(max_workers=16) as executor:
   ```

2. **Tăng JVM heap** (nếu gặp OutOfMemory):
   ```python
   # Trong extract_text.py, dòng ~16
   kkma: Kkma = Kkma(max_heap_size=4096)
   ```

3. **Giảm tần suất cập nhật tiến trình** (tăng tốc một chút):
   ```python
   # Trong extract_text.py, dòng ~120
   if line_num % 500 == 0:  # Thay vì 100
   ```

## 🐛 Xử lý Lỗi & Khắc phục Sự cố

### Vấn đề Thường gặp

#### 1. `ImportError: No module named 'konlpy'`
**Nguyên nhân**: Chưa cài KoNLPy  
**Giải pháp**:
```bash
pip install konlpy
```

#### 2. `TypeError: __init__() got an unexpected keyword argument 'max_heap_size'`
**Nguyên nhân**: Java chưa được cài đặt hoặc KoNLPy không tìm thấy Java  
**Giải pháp**:
- Cài JDK/JRE: [Tải Java](https://www.oracle.com/java/technologies/downloads/)
- Đặt biến môi trường JAVA_HOME
- Khởi động lại terminal

#### 3. `OutOfMemoryError` (Java Heap Space)
**Nguyên nhân**: JVM heap không đủ cho Kkma  
**Giải pháp**: Tăng `max_heap_size` trong code:
```python
kkma: Kkma = Kkma(max_heap_size=4096)  # Tăng lên 4GB
```

#### 4. File JSONL rất lớn và chiếm dung lượng
**Giải pháp**: Không dùng `--keep-jsonl`, file sẽ tự động bị xóa

#### 5. Gán nhãn POS quá chậm
**Nguyên nhân**: Kkma là công cụ phân tích hình thái phức tạp, chậm hơn các taggers khác  
**Giải pháp**:
- Tăng số workers trong `ThreadPoolExecutor`
- Hoặc thay Kkma bằng tagger nhanh hơn như `Okt` (Komoran):
  ```python
  from konlpy.tag import Okt
  okt = Okt()
  # Thay kkma.pos() bằng okt.pos()
  ```

#### 6. `text error ...`: Một số văn bản không gán nhãn được
**Nguyên nhân**: Văn bản có ký tự đặc biệt hoặc quá dài khiến Kkma lỗi  
**Xử lý**: Script tự động bắt exception, log văn bản lỗi, và bỏ qua paragraph đó

### Xử lý Lỗi trong Script

Script tự động xử lý các lỗi sau:

| Lỗi | Xử lý | Ảnh hưởng |
|-----|-------|-----------|
| Lỗi giải mã JSON | Bỏ qua dòng, tiếp tục | Mất 1 document |
| Lỗi mã hóa UTF-8 | Thay thế bằng placeholder | Văn bản có thể bị méo |
| Lỗi gán nhãn Kkma | Log, trả về rỗng | Paragraph bị bỏ qua |
| Thiếu field (`form`) | Trả về chuỗi rỗng | Paragraph bị bỏ qua |
| Không tìm thấy file | Thoát với thông báo lỗi | Dừng chương trình |

## 📝 Tiền tố File được Hỗ trợ

Tool hỗ trợ các tiền tố sau theo NIKL Newspaper Corpus 2024:

| Tiền tố | Loại | Mô tả (한국어) | Mô tả (Tiếng Việt) |
|---------|------|----------------|---------------------|
| `NIRW` | 인터넷 신문 | Internet newspapers | Báo trực tuyến |
| `NLRW` | 지역 종합지 | Regional newspapers | Báo địa phương |
| `NPRW` | 전문지 | Professional newspapers | Báo chuyên ngành |
| `NZRW` | 잡지 | Magazines | Tạp chí |
| `NWRW` | 주간지 | Weekly newspapers | Báo tuần |

**Mặc định**: Script xử lý tất cả 5 tiền tố trên nếu không chỉ định `-p`

## 🔍 Ứng dụng Thực tế

### 1. Nghiên cứu Ngôn ngữ học
- **Xây dựng corpus**: Tạo corpus văn bản cho nghiên cứu ngôn ngữ học
- **Thống kê POS**: Phân tích tần suất các loại từ trong báo chí
- **Phân tích kết hợp**: Nghiên cứu từ kết hợp thường gặp

### 2. Dữ liệu Huấn luyện NLP
- **Mô hình ngôn ngữ**: Dữ liệu huấn luyện cho Korean LM
- **Nhận dạng thực thể**: Trích xuất dữ liệu huấn luyện NER
- **Phân tích cảm xúc**: Tạo dataset cho phân loại cảm xúc

### 3. Phân tích Nội dung
- **Mô hình chủ đề**: Phân tích chủ đề trong báo chí Hàn Quốc
- **Trích xuất từ khóa**: Tìm từ khóa phổ biến theo thời gian
- **Phân tích so sánh**: So sánh cách dùng từ giữa các loại báo

### 4. Tìm kiếm Từ/Mẫu Cụ thể
- **Nghiên cứu từ đồng nghĩa**: Tìm các cách diễn đạt tương tự (VD: 아쉽다/아깝다/안타깝다)
- **Mẫu ngữ pháp**: Nghiên cứu các mẫu ngữ pháp
- **Diễn biến thuật ngữ**: Theo dõi sự thay đổi thuật ngữ theo thời gian

## 📚 File Liên quan

- `plan.md` - Tài liệu kế hoạch chi tiết (tiếng Việt)
- `POS_tagger_(kkma).ipynb` - Jupyter notebook để thử nghiệm gán nhãn POS
- `NIKL_NEWSPAPER_2024_v1.0.pdf` - Tài liệu chính thức về corpus (tiếng Hàn)
- `(ENG)NIKL_NEWSPAPER_2024_v1.0.pdf` - Phiên bản tiếng Anh của tài liệu corpus

## ⚠️ Lưu ý Quan trọng

### Về mã hóa
- Script sử dụng **UTF-8** (không phải UTF-8-BOM)
- Windows Notepad có thể không hiển thị đúng → Dùng Notepad++, VS Code, hoặc editor hỗ trợ UTF-8
- Nếu cần UTF-8-BOM cho Excel, thêm BOM thủ công:
  ```python
  with open(file, 'w', encoding='utf-8-sig') as f:
  ```

### Về bộ nhớ
- **Chuyển đổi JSON → JSONL**: Cần RAM = kích thước file JSON
- **Xử lý streaming**: Chỉ cần RAM cho 1 document (~1-10MB)
- **Khuyến nghị**: 8GB+ RAM cho file 1GB

### Về hiệu suất
- **Kkma là điểm nghẽn chính**: 100-500ms/paragraph
- **Xử lý song song giúp**: ~6-8x tăng tốc với 8 workers
- **Nếu chỉ cần văn bản gốc**: Có thể bỏ qua gán nhãn POS để nhanh hơn nhiều

### Về lọc từ khóa
- Tìm kiếm từ khóa trong **văn bản đã gán nhãn**, không phải văn bản gốc
- Định dạng: `từ_Nhãn` (VD: `아쉽_VA`)
- Không phân biệt hoa/thường
- Logic OR (khớp bất kỳ từ khóa nào)

### Về toàn vẹn dữ liệu
- Script **không sửa đổi** file JSON gốc
- File kết quả độc lập, an toàn để thử nghiệm
- File JSONL tạm được xóa sau khi xử lý (trừ khi dùng `--keep-jsonl`)

## 🤝 Đóng góp

Hoan nghênh các đóng góp! Nếu bạn muốn:
- Báo lỗi → Tạo issue
- Đề xuất tính năng → Tạo issue với nhãn `enhancement`
- Đóng góp code → Tạo pull request

## 📜 Giấy phép

Giấy phép MIT - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 👨‍💻 Tác giả & Cảm ơn

- **Nhà phát triển công cụ**: Được tạo để xử lý NIKL Newspaper Corpus 2024 v1.0
- **NIKL Corpus**: Cung cấp bởi 국립국어원 (Viện Ngôn ngữ Quốc gia Hàn Quốc)
- **KoNLPy**: Thư viện NLP tiếng Hàn bởi [KoNLPy team](https://konlpy.org)

---

**Cập nhật lần cuối**: 01/09/2026  
**Phiên bản**: 1.0  
**Python**: 3.6+  
**Đã test trên**: Windows 10/11, i5 13400, 32GB RAM
