#!/usr/bin/env python3
"""
Tool để trích xuất text từ các file JSON của NIKL Newspaper Corpus
Hỗ trợ streaming cho file lớn và lọc theo keyword
"""

import json
import os
import sys
import argparse
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from pathlib import Path
from typing import List, Optional
from konlpy.tag import Kkma

keywords: Optional[List[str]] = None
raw_text_field_name = "raw_text"
tagged_text_field_name = "tagged_text"
kkma: Kkma = Kkma(max_heap_size=2048)
max_time_kkma_pos = 0


def clean_utf8(value: bytes | str) -> str:
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")

    if isinstance(value, str):
        return (
            value
            .encode("utf-8", errors="replace")
            .decode("utf-8", errors="replace")
        )

    raise TypeError("value must be bytes or str")


def json_to_jsonl(json_file: str, jsonl_file: str) -> int:
    """
    Convert JSON file sang JSONL format
    Mỗi document trong array sẽ thành 1 dòng riêng
    Trả về số lượng documents đã convert
    """
    print(f"Converting {json_file} to JSONL format...")

    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = data.get('document', [])

    with open(jsonl_file, 'w', encoding='utf-8') as f:
        for doc in documents:
            f.write(json.dumps(doc, ensure_ascii=False) + '\n')

    print(f"Created {jsonl_file} with {len(documents)} documents")
    return len(documents)


def extract_text_from_sentence(sentence):
    para_result = {
        "idx": sentence["idx"]
    }
    form_text = sentence.get('form', '')
    content = re.sub(r'<[^>]+>', '', form_text).strip()
    # làm sạch text
    clean_text = clean_utf8(content)
    if not clean_text:
        return ['', '']

    # Kiểm tra keyword
    try:
        start_time = time.time() * 1000
        tagged_list = kkma.pos(clean_text)
        total_time = time.time() * 1000 - start_time
        global max_time_kkma_pos
        if total_time > max_time_kkma_pos:
            max_time_kkma_pos = total_time
    except Exception as error:
        print(f"text error {error}:\n {clean_text}")
        tagged_list = []

    if tagged_list:
        tagged_text = ' '.join(list(map(lambda item: '_'.join(item), tagged_list)))
        if keywords is not None:
            if any(keyword.lower() in tagged_text.lower() for keyword in keywords):
                para_result[tagged_text_field_name] = tagged_text
                para_result[raw_text_field_name] = clean_text
        else:
            para_result[tagged_text_field_name] = tagged_text
            para_result[raw_text_field_name] = clean_text
    return para_result


def extract_text_from_document(doc: dict):
    """
    Trích xuất text từ field 'form' trong các paragraph
    Lọc theo keywords nếu được cung cấp
    Chỉ trả về nội dung câu, không có metadata
    """
    total_tagged_texts = []
    total_raw_texts = []
    paragraphs = doc.get('paragraph', [])
    for i in range(len(paragraphs)):
        paragraphs[i]["idx"] = i

    # Loop map
    with ThreadPoolExecutor(max_workers=8) as executor:
        results = list(executor.map(lambda sentence:
                                    extract_text_from_sentence(sentence),
                                    paragraphs))
        for i in range(len(results)):
            sentence_result = results[i]
            if raw_text_field_name in sentence_result and sentence_result[raw_text_field_name]:
                total_raw_texts.insert(sentence_result["idx"], sentence_result[raw_text_field_name])
            if tagged_text_field_name in sentence_result and sentence_result[tagged_text_field_name]:
                total_tagged_texts.insert(sentence_result["idx"], sentence_result[tagged_text_field_name])

    return total_tagged_texts, total_raw_texts


def process_jsonl_streaming(jsonl_file: str, output_file: str, raw_file: str) -> int:
    """
    Xử lý JSONL file theo streaming để tiết kiệm memory
    Trả về số lượng text đã trích xuất
    """
    print(f"Processing {jsonl_file}...")
    if keywords:
        print(f"Filtering by keywords: {', '.join(keywords)}")

    total_texts = 0
    total_docs = 0

    with open(raw_file, 'w', encoding='utf-8') as f_raw_out, \
            open(output_file, 'w', encoding='utf-8') as f_tagged_out, \
            open(jsonl_file, 'r', encoding='utf-8') as f_in:

        for line_num, line in enumerate(f_in, 1):
            if line.strip():
                try:
                    doc = json.loads(line)
                    tagged_texts, raw_texts = extract_text_from_document(doc)

                    if tagged_texts:
                        total_docs += 1
                        for tagged_text in tagged_texts:
                            f_tagged_out.write(tagged_text + '\n\n')  # Mỗi paragraph cách nhau 1 dòng trống
                        total_texts += len(tagged_texts)

                    if raw_texts:
                        for raw_text in raw_texts:
                            f_raw_out.write(raw_text + '\n\n')  # Mỗi paragraph cách nhau 1 dòng trống

                    # Progress indicator mỗi 100 documents
                    if line_num % 100 == 0:
                        print(f"Processed {line_num} documents, extracted {total_texts} paragraphs...", end='\r')

                except json.JSONDecodeError as e:
                    print(f"\nWarning: Error parsing line {line_num}: {e}")
                    continue

    print(f"\nCompleted! Processed {total_docs} documents, extracted {total_texts} paragraphs to {output_file}")
    return total_texts


def process_json_file(json_file: str, output_dir: str, keep_jsonl: bool = False) -> None:
    """
    Xử lý 1 file JSON:
    1. Convert sang JSONL
    2. Extract text theo streaming
    3. Lưu vào file txt
    """
    json_path = Path(json_file)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Tên file output
    base_name = json_path.stem
    jsonl_file = output_path / f"{base_name}.jsonl"
    txt_tagged_file = output_path / f"{base_name}_tagged.txt"
    txt_raw_file = output_path / f"{base_name}_raw.txt"

    # Step 1: Convert to JSONL
    doc_count = json_to_jsonl(json_file, str(jsonl_file))

    # Step 2: Extract text
    total = process_jsonl_streaming(str(jsonl_file), str(txt_tagged_file), str(txt_raw_file))

    # Step 3: Cleanup JSONL nếu không cần giữ
    if not keep_jsonl:
        jsonl_file.unlink()
        print(f"Removed temporary file {jsonl_file}")

    print(f"✓ Completed {json_file}: {total} paragraphs extracted from {doc_count} documents\n")


def process_directory(input_dir: str, output_dir: str, prefixes: List[str], keep_jsonl: bool = False) -> None:
    """
    Xử lý tất cả file JSON trong thư mục có prefix phù hợp
    """
    input_path = Path(input_dir)
    json_files = []

    # Tìm tất cả file JSON với prefix phù hợp
    for prefix in prefixes:
        json_files.extend(input_path.glob(f"{prefix}*.json"))

    if not json_files:
        print(f"No JSON files found with prefixes: {', '.join(prefixes)}")
        return

    print(f"Found {len(json_files)} JSON files to process\n")

    for idx, json_file in enumerate(json_files, 1):
        print(f"[{idx}/{len(json_files)}] Processing {json_file.name}...")
        try:
            process_json_file(str(json_file), output_dir, keep_jsonl)
        except Exception as e:
            print(f"Error processing {json_file}: {e}\n")
            continue


def main():
    parser = argparse.ArgumentParser(
        description='Extract text from NIKL Newspaper JSON files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Xử lý tất cả file trong thư mục hiện tại
  python extract_text.py
  
  # Xử lý file cụ thể
  python extract_text.py -f NLRW2400000001.json
  
  # Lọc theo keyword
  python extract_text.py -k "울산" "환경"
  
  # Chỉ xử lý file có prefix NLRW và NPRW
  python extract_text.py -p NLRW NPRW
  
  # Giữ lại file JSONL
  python extract_text.py --keep-jsonl
        """
    )

    parser.add_argument('-i', '--input-dir', default='.',
                        help='Input directory chứa file JSON (default: thư mục hiện tại)')
    parser.add_argument('-o', '--output-dir', default='./output',
                        help='Output directory cho file txt (default: ./output)')
    parser.add_argument('-f', '--file',
                        help='Xử lý 1 file JSON cụ thể')
    parser.add_argument('-p', '--prefixes', nargs='+',
                        default=['NIRW', 'NLRW', 'NPRW', 'NZRW', 'NWRW'],
                        help='Prefix của file cần xử lý (default: NIRW NLRW NPRW NZRW NWRW)')
    parser.add_argument('-k', '--keywords', nargs='+',
                        help='Keywords để lọc text (chỉ lấy text chứa keyword)')
    parser.add_argument('--keep-jsonl', action='store_true',
                        help='Giữ lại file JSONL sau khi xử lý')

    args = parser.parse_args()
    # Giữ keyword global để không phải truyền nhiều
    global keywords
    if args.keywords:
        keywords = args.keywords

    print("=" * 60)
    print("NIKL Newspaper Text Extractor")
    print("=" * 60)
    print()

    print(f"Started at {datetime.now()}")
    start_time_ms = int(time.time() * 1000)
    if args.file:
        # Xử lý 1 file cụ thể
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            sys.exit(1)
        process_json_file(args.file, args.output_dir, args.keep_jsonl)
    else:
        # Xử lý tất cả file trong thư mục
        process_directory(args.input_dir, args.output_dir, args.prefixes, args.keep_jsonl)

    print(f"max_pos_kkma_time is {max_time_kkma_pos}ms")
    print("=" * 60)
    print("All done!")
    print("=" * 60)
    print(f"Completed after {time.time() * 1000 - start_time_ms}ms")


if __name__ == '__main__':
    main()
