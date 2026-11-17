# Báo cáo cá nhân — tài khoản daoanh9503

Bản dự thảo dựa trên Git; cần bổ sung họ tên, MSSV và đổi tên file đúng mẫu trước khi nộp.

## 1. Thông tin thành viên

- Họ tên: Đào Thị Ngọc Ánh
- MSSV: 2A202603790
- Git author/GitHub: daoanh9503.
- Email tác giả commit: daoanh9503@gmail.com.
- Nhánh: `feature/single-agent`.
- Vai trò có bằng chứng: bàn giao B: Single agent.

## 2. Phần việc phụ trách

Commit `883f520` đưa triển khai Single và test riêng lên nhánh từ starter. Hai file được bàn giao là `src/lab8/shapes/single.py` và `src/tests/test_single_shape.py`.

## 3. Đóng góp cụ thể

Đối chiếu Git cho thấy hai file này giống bản draft `f9a6c80` của Khánh Vũ. Đóng góp chứng minh được là tiếp nhận và bàn giao phần Single bằng commit riêng; chưa có bằng chứng sửa mới hai file so với draft. Không quy toàn bộ code/test này thành phần tự viết mới của tác giả commit.

Triển khai bàn giao sử dụng vòng `run_react`, tối đa 8 bước và `worker=True`. Scratchpad giữ kết quả tool; Python chọn tool đọc, tính quote từ order có cấu trúc, kiểm order đã dùng để quote và gọi host với quote đầy đủ. Trace không ghi ticket hoặc prompt. Khi crash, ghi trace và ném lại `InjectedCrash`.

Test bàn giao kiểm giới hạn bước, chỉ dùng tool đọc, thứ tự đọc lịch sử refund, nhánh thiếu mã đơn, chặn tool ghi, vòng lặp không kết thúc, tính lại quote khi order bị sửa và lọc trace.

## 4. Bằng chứng

- Commit kỹ thuật: `883f52050be5ea4d027ddfc230ed0fac8f5075dc`.
- Merge vào main: `9ec463a`.
- Hai file trên giống draft: `git diff f9a6c80 883f520 -- src/lab8/shapes/single.py src/tests/test_single_shape.py` không có diff.
- Phiên kiểm tra tích hợp trên `main` tại `a0003e4`: 90 test mặc định pass; 248 test student pass, gồm 62 test của Single. Đây là kết quả được trợ lý chạy, không khẳng định thành viên đã tự chạy trên máy riêng.

Lệnh chạy lại từ `src/` sau khi kích hoạt môi trường:

```powershell
python -m pytest -q tests/test_single_shape.py
python -m pytest -q -m student -o addopts= -k "single]"
```

## 5. Công cụ AI đã dùng

Codex hỗ trợ đối chiếu Git và soạn báo cáo này. Chưa có khai báo của thành viên về công cụ đã dùng để thực hiện commit gốc hoặc cách tự kiểm tra; cần bổ sung theo trải nghiệm thực tế.

## 6. Tự đánh giá

Phần bàn giao Single vượt test public khi tích hợp. MockLLM được gọi mỗi bước nhưng output không quyết định hành động; `_next_action()` là Python tất định. Kết quả chưa chứng minh khả năng model tự chọn tool hoặc xử lý ticket mơ hồ. Thành viên cần tự xác nhận mức hiểu bài, khó khăn, quá trình thực hiện và việc dùng AI trước khi nộp.
