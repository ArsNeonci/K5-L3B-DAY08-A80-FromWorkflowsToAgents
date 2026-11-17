# Báo cáo cá nhân — Nguyễn Minh Quân

## 1. Thông tin thành viên

- Họ tên: Nguyễn Minh Quân
- MSSV: 2A202603794
- Email: 26ai.quannm10@vinuni.edu.vn
- GitHub: [nmqdhtb](https://github.com/nmqdhtb)

## 2. Phần việc phụ trách

Thành viên số 5 của nhóm A80, phụ trách tài liệu và kiểm tra hồ sơ nộp Lab 8 LogiX-VN.

## 3. Đóng góp cụ thể

- Cập nhật thông tin và vai trò của năm thành viên trong [TEAM.md](../../TEAM.md), đối chiếu bảng đóng góp với các nhánh bàn giao.
- Tổng hợp [báo cáo nhóm](group_report.md), hoàn thiện [ADR](decision_adr.md) và [research card R1](research_card.md) dựa trên mã nguồn và kết quả lưu ở bản tích hợp `f1595d5`. Trong ADR, dùng cùng bộ claim, seed và bảng giá để so sánh các kiến trúc. Workflow đạt 70/70 lượt public với chi phí mô phỏng thấp nhất, 28,80 VND/lần đạt.
- Bổ sung test `test_blank_run_id_is_reported_as_a_failure` để kiểm tra trình kiểm hồ sơ báo lỗi khi dòng run ID trong ADR để trống.
- Commit đóng góp cá nhân: sẽ bổ sung sau khi commit phần tài liệu và test trên nhánh `quan-workflow`.

## 4. Bằng chứng

- Bản tích hợp dùng để đối chiếu: `f1595d5`. Hai run ID trên cùng ca C-002 ở seed 55 là `R-workflow-C-002-s55` (đạt) và `R-swarm-C-002-s55` (trượt). Crash suite lưu trong bản tích hợp đạt 20/20.
- Ablation R1 giữ nguyên 70/70 lượt đạt khi tăng từ một lên hai investigator. Chi phí mô phỏng mỗi lượt đạt tăng từ 59,12 lên 69,98 VND (+18,4%).
- Test cá nhân nằm trong [test_adr_required_fields.py](../../src/tests/test_adr_required_fields.py). Chạy từ `src/` bằng `python3.12 -B -m unittest discover -s tests -p test_adr_required_fields.py -v`. Kết quả: 1 test đạt.

## 5. Công cụ AI đã dùng

Dùng Codex để đọc lịch sử nhánh, đối chiếu số liệu trong các file JSON, biên tập hồ sơ theo mẫu và viết test kiểm tra ADR. Tôi dùng file benchmark, crash và ablation tại commit tích hợp làm căn cứ cho các con số. Run ID được đối chiếu với danh sách trial, còn test ADR được chạy riêng trên Python 3.12.

## 6. Tự đánh giá

Phần việc của tôi giúp truy xuất số liệu và quyết định kiến trúc về đúng bản tích hợp. Test mới kiểm tra một lỗi định dạng có thể khiến ADR thiếu bằng chứng. Trước khi nộp, tôi cần đối chiếu lại hash và các tài liệu với nhánh chốt, rồi chạy kiểm tra toàn bộ hồ sơ trên bản đó.
