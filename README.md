# Ticket Manager CLI

Đây là một project dòng lệnh đơn giản dùng để quản lý ticket. Project được xây dựng theo phương pháp TDD.

Project gồm 2 phần chính:

* **Week 2:** Xây dựng Ticket Manager CLI cơ bản.
* **Week 3:** Mở rộng CLI để tích hợp với Knowledge Base API.

---

## 1. Tổng quan project

Project này cho phép người dùng quản lý ticket trực tiếp từ terminal. Người dùng có thể tạo ticket, xem danh sách ticket, xem chi tiết ticket và cập nhật trạng thái ticket.

Ở Week 3, project được mở rộng thêm nhóm lệnh `kb` để làm việc với Knowledge Base. CLI có thể tìm kiếm tài liệu, liệt kê tài liệu theo node path, xem nội dung tài liệu và thêm tài liệu mới vào Knowledge Base.

Knowledge Base hỗ trợ 2 chế độ:

* **Mock mode:** Dùng dữ liệu mẫu trong code để test local.
* **HTTP mode:** Gọi API thật thông qua HTTP request.

---

## 2. Tính năng

### Week 2 - Ticket Manager CLI

* Tạo ticket mới
* Xem danh sách ticket
* Lọc ticket theo trạng thái
* Lọc ticket theo độ ưu tiên
* Lọc ticket theo tag
* Xem chi tiết một ticket
* Cập nhật trạng thái ticket
* Lưu dữ liệu ticket vào file JSON
* Unit test
* CLI integration test

### Week 3 - Knowledge Base API Integration

* Tìm kiếm tài liệu trong Knowledge Base
* Liệt kê tài liệu theo node path
* Xem nội dung tài liệu theo document ID
* Thêm tài liệu mới từ file Markdown
* Mock Knowledge Base client để test local
* HTTP Knowledge Base client để gọi API thật
* Chuyển đổi client bằng environment variable
* Test cho mock client, HTTP client và CLI command

---

## 3. Cấu trúc project

```text
ticket-manager-cli/
  tickets/
    __init__.py
    __main__.py
    model.py
    service.py
    storage.py

    kb_model.py
    kb_client.py
    kb_mock.py
    kb_http.py
    kb_factory.py
    kb_command.py

  tests/
    test_service.py
    test_cli.py
    test_kb_mock.py
    test_kb_cli.py
    test_kb_http.py

  README.md
  pyproject.toml
  tickets.json
```

---

## 4. Yêu cầu môi trường

Project yêu cầu:

```text
Python >= 3.10
pytest
```

Không cần cài thêm thư viện HTTP bên ngoài vì project dùng thư viện có sẵn của Python là `urllib`.

---

## 5. Cài đặt project

Clone repository:

```bash
git clone https://github.com/ngochieu1762005/ticket-manager-cli.git
cd ticket-manager-cli
```

Cài pytest:

```bash
pip install pytest
```

---

# Week 2 - Ticket Manager CLI

## 6. Mô hình dữ liệu Ticket

Mỗi ticket gồm các thông tin:

```text
id
title
description
status
priority
tags
```

Trạng thái hợp lệ:

```text
open
doing
done
```

Độ ưu tiên hợp lệ:

```text
low
medium
high
```

---

## 7. Các lệnh quản lý ticket

### 7.1. Tạo ticket mới

```bash
python -m tickets create --title "Fix bug" --description "Fix login bug" --priority high --tags bug,backend
```

Kết quả ví dụ:

```text
Created ticket #1
Title: Fix bug
```

---

### 7.2. Xem danh sách ticket

```bash
python -m tickets list
```

Kết quả ví dụ:

```text
#1 Fix bug [open] [high]
```

---

### 7.3. Lọc ticket theo trạng thái

```bash
python -m tickets list --status open
```

---

### 7.4. Lọc ticket theo độ ưu tiên

```bash
python -m tickets list --priority high
```

---

### 7.5. Lọc ticket theo tag

```bash
python -m tickets list --tag backend
```

---

### 7.6. Xem chi tiết một ticket

```bash
python -m tickets show 1
```

Kết quả ví dụ:

```text
ID: 1
Title: Fix bug
Description: Fix login bug
Status: open
Priority: high
Tags: bug, backend
```

---

### 7.7. Cập nhật trạng thái ticket

```bash
python -m tickets update 1 --status done
```

Kết quả ví dụ:

```text
Updated ticket #1
Status: done
```

---

## 8. File lưu trữ dữ liệu

Mặc định, dữ liệu ticket được lưu trong file:

```text
tickets.json
```

Có thể dùng file khác bằng option `--file`:

```bash
python -m tickets --file test_tickets.json create --title "Test" --description "Test desc" --priority medium
```

---

# Week 3 - Knowledge Base API Integration

## 9. Mục tiêu Week 3

Week 3 mở rộng project Week 2 bằng cách thêm tính năng tích hợp với Knowledge Base API.

Mục tiêu chính là học cách kết nối CLI với một dịch vụ bên ngoài theo hướng an toàn và dễ test.

Project dùng cách làm **mock-first integration**:

```text
Viết test cho hành vi mong muốn
  -> Tạo MockKBClient
  -> Thêm CLI command
  -> Tạo HTTPKBClient
  -> Kiểm tra lại bằng test
```

Lý do cần mock trước là để có thể test logic CLI mà không phụ thuộc vào API thật, mạng, server hoặc dữ liệu production.

---

## 10. Kiến trúc Knowledge Base

```text
CLI Command
  |
  v
KB Client Interface
  |
  +-- MockKBClient
  |     |
  |     v
  |   Dữ liệu mẫu local
  |
  +-- HTTPKBClient
        |
        v
      External KB API
```

CLI không gọi trực tiếp API thật. Thay vào đó, CLI làm việc thông qua `KBClient`.

Nhờ vậy, project có thể dễ dàng chuyển đổi giữa:

```text
MockKBClient
HTTPKBClient
```

---

## 11. Mô hình dữ liệu Knowledge Base

Mỗi tài liệu trong Knowledge Base gồm:

```text
id
title
content
node_path
tags
```

Ví dụ:

```text
id: doc-001
title: Customer Response Template
content: This is an email response template for customer support.
node_path: /templates/email
tags: template, email, support
```

---

## 12. Các lệnh Knowledge Base

### 12.1. Tìm kiếm tài liệu

```bash
python -m tickets kb search "response" --top-k 3
```

Kết quả ví dụ:

```text
doc-001 | Customer Response Template | /templates/email
```

---

### 12.2. Liệt kê tài liệu theo node path

```bash
python -m tickets kb list --node /templates/email --limit 10
```

Kết quả ví dụ:

```text
doc-001 | Customer Response Template | /templates/email
```

---

### 12.3. Xem nội dung một tài liệu

```bash
python -m tickets kb retrieve doc-001
```

Kết quả ví dụ:

```text
ID: doc-001
Title: Customer Response Template
Node: /templates/email
Tags: template, email, support
Content:
This is an email response template for customer support.
```

---

### 12.4. Thêm tài liệu mới

Tạo một file Markdown:

```bash
echo "This is a new email template." > new-template.md
```

Thêm file vào Knowledge Base:

```bash
python -m tickets kb add --file new-template.md --path /templates/email --tags template,email --title "New Email Template"
```

Kết quả ví dụ:

```text
Added document doc-004
Title: New Email Template
```

---

## 13. Chế độ chạy Knowledge Base

Project hỗ trợ 2 chế độ chạy Knowledge Base.

---

### 13.1. Mock mode

Mock mode dùng dữ liệu mẫu trong code. Chế độ này phù hợp để test local.

Chạy bằng mock mode:

```bash
KB_CLIENT=mock python -m tickets kb search "response"
```

Nếu không truyền `KB_CLIENT`, project sẽ tự dùng mock mode.

Vì vậy lệnh này cũng chạy được:

```bash
python -m tickets kb search "response"
```

---

### 13.2. HTTP mode

HTTP mode dùng để kết nối với Knowledge Base API thật.

Chạy bằng HTTP mode:

```bash
KB_CLIENT=http KB_API_URL=http://localhost:3000 python -m tickets kb search "response"
```

Các environment variable cần có:

```text
KB_CLIENT=http
KB_API_URL=http://localhost:3000
```

Nếu API server chưa chạy, CLI sẽ báo lỗi kết nối.

---

## 14. API Contract

HTTP client dùng JSON request và JSON response.

---

### 14.1. Search API

Endpoint:

```text
POST /search
```

Request:

```json
{
  "query": "response",
  "topK": 5
}
```

Response:

```json
{
  "results": [
    {
      "id": "doc-001",
      "title": "Customer Response Template",
      "nodePath": "/templates/email"
    }
  ]
}
```

---

### 14.2. List API

Endpoint:

```text
POST /list
```

Request:

```json
{
  "nodePath": "/templates/email",
  "limit": 10
}
```

Response:

```json
{
  "documents": [
    {
      "id": "doc-001",
      "title": "Customer Response Template",
      "content": "Email content",
      "nodePath": "/templates/email",
      "tags": ["template", "email"]
    }
  ]
}
```

---

### 14.3. Retrieve API

Endpoint:

```text
POST /retrieve
```

Request:

```json
{
  "docId": "doc-001"
}
```

Response:

```json
{
  "document": {
    "id": "doc-001",
    "title": "Customer Response Template",
    "content": "Email content",
    "nodePath": "/templates/email",
    "tags": ["template", "email"]
  }
}
```

---

### 14.4. Add API

Endpoint:

```text
POST /add
```

Request:

```json
{
  "title": "New Template",
  "content": "Markdown content",
  "nodePath": "/templates/email",
  "tags": ["template", "email"]
}
```

Response:

```json
{
  "document": {
    "id": "doc-004",
    "title": "New Template",
    "content": "Markdown content",
    "nodePath": "/templates/email",
    "tags": ["template", "email"]
  }
}
```

---

# Testing

## 15. Chạy toàn bộ test

```bash
pytest
```

---

## 16. Chạy test Week 2

```bash
pytest tests/test_service.py
pytest tests/test_cli.py
```

---

## 17. Chạy test Week 3

```bash
pytest tests/test_kb_mock.py
pytest tests/test_kb_cli.py
pytest tests/test_kb_http.py
```

---

## 18. Nội dung được test

### Week 2

* Tạo ticket
* Kiểm tra title hợp lệ
* Kiểm tra description hợp lệ
* Kiểm tra priority hợp lệ
* Xem danh sách ticket
* Lấy ticket theo ID
* Cập nhật trạng thái ticket
* Chạy CLI create
* Chạy CLI list
* Chạy CLI show
* Chạy CLI update
* Xử lý file JSON rỗng
* Xử lý file JSON lỗi

### Week 3

* Mock KB search
* Mock KB list
* Mock KB retrieve
* Mock KB add
* Lỗi khi document không tồn tại
* CLI KB search
* CLI KB list
* CLI KB retrieve
* CLI KB add
* HTTP KB search
* HTTP KB list
* HTTP KB retrieve
* HTTP KB add

---

# Quy trình TDD

Project này làm theo quy trình TDD:

```text
Failing test
  -> Small implementation
  -> Passing test
  -> Refactor
```

Với Week 3, quy trình là:

```text
Viết test cho hành vi Knowledge Base
  -> Implement MockKBClient
  -> Thêm CLI command
  -> Implement HTTPKBClient
  -> Chạy test để xác nhận hoạt động đúng
```

---

# Ví dụ chạy thử đầy đủ

## 1. Chạy tính năng Ticket Manager

```bash
python -m tickets create --title "Fix bug" --description "Fix login bug" --priority high --tags bug,backend
python -m tickets list
python -m tickets show 1
python -m tickets update 1 --status done
```

---

## 2. Chạy tính năng Knowledge Base bằng mock client

```bash
python -m tickets kb search "response"
python -m tickets kb list --node /templates/email
python -m tickets kb retrieve doc-001
```

---

## 3. Thêm tài liệu mới vào Knowledge Base

```bash
echo "This is a new support template." > support-template.md
python -m tickets kb add --file support-template.md --path /templates/email --tags template,support --title "Support Template"
```

---

## 4. Chạy test

```bash
pytest
```

---

# Xử lý lỗi

Project có xử lý các lỗi phổ biến như:

* Ticket status không hợp lệ
* Ticket priority không hợp lệ
* Ticket không tồn tại
* File JSON rỗng
* File JSON bị lỗi format
* Document trong Knowledge Base không tồn tại
* Chế độ `KB_CLIENT` không hợp lệ
* Thiếu `KB_API_URL` khi dùng HTTP mode
* Không kết nối được với Knowledge Base API
* API trả về JSON không hợp lệ

---

# Ghi chú

* Mock mode là chế độ mặc định.
* HTTP mode chỉ dùng khi có Knowledge Base API server thật.
* Các lệnh Week 2 vẫn hoạt động sau khi thêm Week 3.
* Các lệnh Week 3 được tách riêng thành module riêng để dễ test và dễ bảo trì.
* Project giữ đúng hướng mở rộng từ Week 2 sang Week 3, không cần tạo repository mới.

---

# Repository

GitHub repository:

```text
https://github.com/ngochieu1762005/ticket-manager-cli
```
