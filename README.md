# KorTag - Công cụ Phân tích và Gán Nhãn Từ Loại Tiếng Hàn

Bộ công cụ Python để xử lý và phân tích corpus tiếng Hàn từ NIKL (국립국어원 - Viện Ngôn ngữ Quốc gia Hàn Quốc) với tính năng gán nhãn từ loại (POS Tagging) tự động.

## 🎯 Tổng quan Dự án

KorTag bao gồm 2 module chính để xử lý 2 loại corpus khác nhau:

### 📰 Module Báo chí (Newspapers)
- **Nguồn dữ liệu**: NIKL Newspaper Corpus 2024 (말뭉치 báo chí)
- **Đặc điểm**: Xử lý song song với 8 worker threads, tốc độ cao
- **Ứng dụng**: Phân tích văn bản viết, tạo dữ liệu huấn luyện NLP
- **Dữ liệu**: 115 file JSON từ các báo (kích thước tối đa ~1GB/file)
- **Tốc độ**: 100-200 documents/giây

### 💬 Module Hội thoại (Dialogue)  
- **Nguồn dữ liệu**: NIKL Spoken Dialogue Corpus 2024 (말뭉치 hội thoại)
- **Đặc điểm**: Trích xuất có ngữ cảnh (câu trước/sau), theo dõi người nói
- **Ứng dụng**: Phân tích hội thoại, nghiên cứu diễn ngôn, ngôn ngữ học xã hội
- **Dữ liệu**: 3227 file JSON hội thoại
- **Tốc độ**: 50-100 documents/giây

## 🚀 Bắt đầu Nhanh

### Cài đặt

```bash
# Clone repository
git clone <địa-chỉ-repo-của-bạn>
cd KorTag

# Cài đặt thư viện phụ thuộc
pip install konlpy

# Cài đặt Java (yêu cầu bởi KoNLPy)
# Xem: https://konlpy.org/en/latest/install/
```

### Sử dụng Cơ bản

#### Trích xuất từ Báo chí
```bash
cd newspapers
python extract_text.py -i processed -o output -k "환경_NNG"
```

#### Trích xuất từ Hội thoại
```bash
cd dialogue
python extract_text.py -i input -o output -k "아깝_VA"
```

## 📁 Cấu trúc Dự án

```
KorTag/
├── README_VI.md                   # File này (tiếng Việt)
├── README.md                      # Phiên bản tiếng Anh
├── SO_SANH_MODULE.md              # So sánh 2 module
│
├── newspapers/                    # Module báo chí
│   ├── extract_text.py           # Script chính
│   ├── HDSD.md                   # Hướng dẫn sử dụng chi tiết
│   ├── PHAN_TICH_CODE.md        # Phân tích kỹ thuật
│   ├── plan.md                   # Tài liệu kế hoạch
│   ├── processed/                # File JSON đầu vào (115 files)
│   ├── unprocessed/              # File chưa xử lý
│   ├── output/                   # File kết quả
│   ├── tagged/                   # Kết quả đã gán nhãn
│   └── untagged/                 # Kết quả chưa gán nhãn
│
└── dialogue/                      # Module hội thoại
    ├── extract_text.py           # Script chính
    ├── HDSD.md                   # Hướng dẫn sử dụng chi tiết
    ├── PHAN_TICH_CODE.md        # Phân tích kỹ thuật
    ├── input/                    # File JSON đầu vào (3227 files)
    └── output/
        ├── tagged/               # Kết quả đã gán nhãn + ngữ cảnh
        └── raw/                  # Văn bản gốc + ngữ cảnh
```

## 🔧 Tính năng Chính

### Tính năng Chung (Cả 2 Module)

✅ **Xử lý streaming** - Xử lý file lớn hiệu quả, không tràn RAM  
✅ **Gán nhãn từ loại** - Sử dụng Kkma (Korean Morphological Analyzer)  
✅ **Lọc theo từ khóa** - Tìm kiếm từ khóa trong văn bản đã gán nhãn  
✅ **Mã hóa UTF-8** - Xử lý tiếng Hàn chính xác  
✅ **Xử lý lỗi tốt** - Phục hồi lỗi một cách robust  
✅ **Hiển thị tiến trình** - Cập nhật tiến trình thời gian thực  
✅ **Kết quả kép** - Cả văn bản gốc và văn bản đã gán nhãn  

### Tính năng Riêng của Module Báo chí

✅ **Xử lý song song** - ThreadPoolExecutor với 8 workers  
✅ **Kết quả theo file** - Mỗi file JSON → 2 file kết quả  
✅ **Tốc độ cao** - ~100-200 documents/giây  

### Tính năng Riêng của Module Hội thoại

✅ **Trích xuất ngữ cảnh** - Câu trước + Câu sau  
✅ **Theo dõi người nói** - Giữ thông tin speaker_id  
✅ **Kết quả gộp** - Tất cả kết quả khớp trong 1 file  
✅ **Luồng hội thoại** - Bảo toàn cấu trúc đối thoại  

## 📖 Tài liệu Chi tiết

| Module | Bắt đầu nhanh | Hướng dẫn đầy đủ | Phân tích kỹ thuật | So sánh |
|--------|--------------|------------------|-------------------|---------|
| **Báo chí** | [HDSD.md](newspapers/HDSD.md) | [HDSD.md](newspapers/HDSD.md) | [PHAN_TICH_CODE.md](newspapers/PHAN_TICH_CODE.md) | [SO_SANH_MODULE.md](SO_SANH_MODULE.md) |
| **Hội thoại** | [HDSD.md](dialogue/HDSD.md) | [HDSD.md](dialogue/HDSD.md) | [PHAN_TICH_CODE.md](dialogue/PHAN_TICH_CODE.md) | [SO_SANH_MODULE.md](SO_SANH_MODULE.md) |

## 🎯 Ứng dụng Thực tế

### Nghiên cứu Học thuật

#### Ngôn ngữ học
- 📊 Ngôn ngữ học corpus - Phân tích tần suất, kết hợp từ
- 🗣️ Phân tích diễn ngôn - Mẫu hội thoại, lượt nói
- 📚 Từ điển học - Cách dùng từ trong ngữ cảnh, phân tích ngữ nghĩa
- 🌏 Ngôn ngữ học xã hội - Biến thể theo ngữ cảnh, đặc điểm người nói

#### NLP & AI
- 🤖 Huấn luyện mô hình ngôn ngữ - Corpus văn bản tiếng Hàn quy mô lớn
- 💬 Phát triển chatbot - Ví dụ hội thoại có ngữ cảnh
- 😊 Phân tích cảm xúc - Cách dùng từ cảm xúc trong ngữ cảnh
- 🏷️ Nhận dạng thực thể có tên - Trích xuất dữ liệu huấn luyện

### Học ngôn ngữ

- 📝 Câu ví dụ - Ví dụ sử dụng trong thực tế
- 📖 Học theo ngữ cảnh - Thấy từ trong ngữ cảnh tự nhiên
- 🎓 Mẫu ngữ pháp - Nhận diện cấu trúc phổ biến
- 🗣️ Luyện hội thoại - Ví dụ đối thoại tự nhiên

### Phân tích Nội dung

- 📰 Nghiên cứu truyền thông - Phân tích chủ đề báo chí
- 📈 Phân tích xu hướng - Tần suất từ khóa theo thời gian
- 🔍 Nghiên cứu từ khóa - Tìm từ liên quan và kết hợp

## 🔍 Quy trình Làm việc Thông dụng

### Quy trình 1: Phân tích Từ đồng nghĩa

Nghiên cứu các từ đồng nghĩa về "tiếc nuối" trong tiếng Hàn:

```bash
# Sử dụng module hội thoại
cd dialogue

# Trích xuất "아쉽다" (tiếc, nuối tiếc)
python extract_text.py -i input -k "아쉽_VA"

# Trích xuất "아깝다" (tiếc, lãng phí)
python extract_text.py -i input -k "아깝_VA"

# Trích xuất "안타깝다" (đáng tiếc, thương tâm)
python extract_text.py -i input -k "안타깝_VA"

# So sánh kết quả để hiểu sự khác biệt tinh tế
```

### Quy trình 2: Xây dựng Corpus theo Chủ đề

Tạo corpus về "môi trường" từ báo chí:

```bash
cd newspapers

# Trích xuất bài báo về môi trường
python extract_text.py -i processed -o output_env \
    -k "환경_NNG" "기후_NNG" "탄소_NNG" "재생에너지_NNG"

# Kết quả: Corpus lớn về chủ đề môi trường
```

### Quy trình 3: Nghiên cứu Mẫu Hội thoại

Phân tích cách người Hàn diễn đạt về thời gian:

```bash
cd dialogue

# Trích xuất hội thoại đề cập "thời gian"
python extract_text.py -i input -k "시간_NNG"

# Phân tích ngữ cảnh để hiểu các mẫu
```

## 📊 Tổng quan Hiệu suất

| Chỉ số | Báo chí | Hội thoại |
|--------|---------|-----------|
| **Tốc độ** | 100-200 docs/giây | 50-100 docs/giây |
| **Xử lý** | Song song (8 workers) | Tuần tự |
| **Bộ nhớ** | 1-10MB/document | ~1MB/document |
| **Điểm nghẽn** | Gán nhãn Kkma | Gán nhãn Kkma |
| **Tối ưu** | ThreadPool giúp nhiều | Không thể song song |

**Cấu hình hệ thống test**: i5 13400, 32GB RAM, Windows 10/11

## ⚠️ Lưu ý Quan trọng

### Đối với Module Báo chí

✅ **An toàn khi chạy lại** - Ghi đè file kết quả  
⚠️ **File lớn** - Có thể cần 1GB+ RAM cho chuyển đổi JSON→JSONL  
🚀 **Xử lý song song** - Tận dụng CPU nhiều lõi  

### Đối với Module Hội thoại

🔴 **⚠️ QUAN TRỌNG: Xóa kết quả cũ trước khi chạy lại!**
```bash
# Chế độ append sẽ trùng lặp dữ liệu nếu không xóa trước
Remove-Item output/tagged/*.txt
Remove-Item output/raw/*.txt
```

✅ **Có ngữ cảnh** - Thấy câu trước/sau  
🐌 **Xử lý tuần tự** - Chậm hơn nhưng cần thiết cho ngữ cảnh  
📝 **Kết quả gộp** - Tất cả kết quả khớp trong 1 file  

## 🐛 Khắc phục Sự cố

### Vấn đề Java/KoNLPy

```bash
# Cài đặt Java
# Windows: Tải từ https://www.oracle.com/java/technologies/downloads/
# Mac: brew install openjdk
# Linux: sudo apt-get install default-jdk

# Kiểm tra Java
java -version

# Nếu vẫn gặp vấn đề, thiết lập JAVA_HOME
# Windows: setx JAVA_HOME "C:\Program Files\Java\jdk-XX"
# Linux/Mac: export JAVA_HOME=/usr/lib/jvm/java-XX-openjdk
```

### Vấn đề Bộ nhớ

```python
# Trong extract_text.py, tăng JVM heap:
kkma: Kkma = Kkma(max_heap_size=4096)  # 4GB thay vì 2GB
```

### Xử lý Chậm

- ✅ Báo chí: Đã tối ưu với xử lý song song
- ⚠️ Hội thoại: Không thể tối ưu (cần tuần tự cho ngữ cảnh)
- 💡 Thay thế: Dùng Okt thay vì Kkma (nhanh hơn nhưng kém chính xác)

## 🔄 So sánh: Nên Dùng Module Nào?

| Tình huống | Dùng Module | Lý do |
|----------|-------------|-------|
| Cần tốc độ | Báo chí | Xử lý song song |
| Cần ngữ cảnh | Hội thoại | Trích xuất ngữ cảnh |
| Văn bản viết | Báo chí | Corpus báo chí |
| Văn bản nói | Hội thoại | Corpus hội thoại |
| Khối lượng lớn | Báo chí | Xử lý nhanh hơn |
| Tìm kiếm tập trung | Hội thoại | Kết quả gộp |
| Theo dõi theo file | Báo chí | Kết quả riêng |
| Luồng hội thoại | Hội thoại | Theo dõi người nói |

📖 **So sánh đầy đủ**: Xem [SO_SANH_MODULE.md](SO_SANH_MODULE.md)

## 📚 Tra cứu Nhãn từ loại

### Các Nhãn từ loại Tiếng Hàn Phổ biến (Kkma)

| Nhãn | Loại từ | Tiếng Hàn | Ví dụ |
|------|---------|-----------|-------|
| `NNG` | Danh từ chung | 일반명사 | 사람, 환경 |
| `NNP` | Danh từ riêng | 고유명사 | 서울, 김철수 |
| `VV` | Động từ | 동사 | 하다, 가다 |
| `VA` | Tính từ | 형용사 | 좋다, 크다 |
| `MAG` | Trạng từ | 부사 | 매우, 너무 |
| `JKS` | Trợ từ chủ ngữ | 주격조사 | 이, 가 |
| `JKO` | Trợ từ tân ngữ | 목적격조사 | 을, 를 |
| `EFN` | Vĩ tố kết thúc | 종결어미 | 다, 요 |

🔗 **Danh sách đầy đủ**: [Tài liệu Kkma của KoNLPy](https://konlpy.org/en/latest/api/konlpy.tag/#module-konlpy.tag._kkma)

## 🛠️ Công nghệ Sử dụng

- **Ngôn ngữ**: Python 3.6+
- **Công cụ gán nhãn**: KoNLPy (Kkma)
- **Xử lý đồng thời**: ThreadPoolExecutor (chỉ báo chí)
- **Định dạng dữ liệu**: JSON, JSONL
- **Mã hóa**: UTF-8

## 📝 Ví dụ Kết quả

### Kết quả Báo chí (Đã gán nhãn)
```
환경_NNG 보호_NNG 를_JKO 위하_VV ㄴ_ETD 노력_NNG 이_JKS 필요_NNG 하_XSA 다_EFN ._SF
```

### Kết quả Hội thoại (Đã gán nhãn)
```
Previous sentence:그게 진짜 중요한 거 같아요
speaker_id:SD2401623:시간_NNG 이_JKS 정말_MAG 아깝_VA 다는_ETD 생각_NNG 이_JKS 듣_VV 어요_EFN ._SF
Next sentence:배우는 사람 입장에서 생각해야죠
```

## 🤝 Đóng góp

Hoan nghênh các đóng góp!

- 🐛 **Báo lỗi**: Tạo issue
- 💡 **Đề xuất tính năng**: Tạo issue với nhãn `enhancement`  
- 🔧 **Đóng góp code**: Fork → Branch → Pull Request

### Thiết lập Môi trường Phát triển

```bash
git clone <địa-chỉ-repo>
cd KorTag
pip install -r requirements.txt  # nếu có
pip install konlpy

# Chạy test (nếu đã triển khai)
python -m pytest
```

## 📜 Giấy phép

Giấy phép MIT - Tự do sử dụng cho mục đích cá nhân và thương mại.

## 🙏 Cảm ơn

- **NIKL** (국립국어원) - Cung cấp corpus
- **KoNLPy Team** - Thư viện NLP tiếng Hàn xuất sắc
- **Kkma** - Phân tích hình thái học robust

## 📧 Liên hệ & Hỗ trợ

- **Vấn đề**: Sử dụng GitHub Issues
- **Tài liệu**: Xem HDSD.md của từng module
- **Câu hỏi**: Tạo discussion thread

## 🗺️ Kế hoạch Tương lai

### Ngắn hạn
- [ ] Sửa lỗi trùng lặp append mode của module hội thoại
- [ ] Thêm type hints cho tất cả functions
- [ ] Tối ưu file I/O trong module hội thoại
- [ ] Thêm unit tests

### Trung hạn
- [ ] Hỗ trợ các công cụ gán nhãn khác (Okt, Komoran)
- [ ] Giao diện web để dễ sử dụng
- [ ] Scripts xử lý hàng loạt
- [ ] Tùy chọn định dạng kết quả (CSV, JSON)

### Dài hạn
- [ ] Xử lý tăng tốc GPU
- [ ] Xử lý streaming thời gian thực
- [ ] Tích hợp với ML pipelines
- [ ] Hỗ trợ thêm các loại corpus NIKL

## 📖 Lịch sử Phiên bản

- **v1.0** (2024) - Phát hành đầu tiên
  - Module báo chí với xử lý song song
  - Module hội thoại với trích xuất ngữ cảnh
  - Hỗ trợ gán nhãn POS đầy đủ
  - Tài liệu toàn diện

---

**Phiên bản hiện tại**: 1.0  
**Cập nhật lần cuối**: 01/09/2026  
**Python**: 3.6+  
**Nền tảng**: Windows 10/11 (đã test), Linux/Mac (nên hoạt động)

---

<p align="center">
Được tạo với ❤️ cho Nghiên cứu NLP Tiếng Hàn
</p>
