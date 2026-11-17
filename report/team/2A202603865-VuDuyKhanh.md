# Báo cáo cá nhân — Vũ Duy Khánh

## 1. Thông tin thành viên

- Tên hiển thị tác giả commit: Vũ Duy Khánh
- MSSV: 2A202603865
- Github: khanhduy1609@gmail.com
- Nhánh chứa đóng góp: `develop`, commit `f9a6c80`.
- Vai trò có bằng chứng: tạo draft chung gồm code, test, thí nghiệm và tài liệu. Leader theo phân công hiện tại là Chu Quang Linh — 2A202603809.

## 2. Phần việc phụ trách

### Bonus B3 — Swarm gốc và baseline

- Được giao rà baseline Swarm, giải thích lỗi tin số ngày trong ticket ở seed 55; so bản gốc với `src/bonus/swarm_verified.py` để xác nhận giữ peer/parse/draft, investigator và host.
- Đối chiếu Budget, số model/tool calls và test `test_no_mismatch_keeps_swarm_calls_and_only_adds_read_cost` trong `src/tests/test_bonus_swarm_verified.py`; đọc thêm `src/tests/test_swarm_seed55.py`.
- Bàn giao: mô tả trước/sau sửa, chi phí thêm và giải thích vì sao verifier vẫn chưa tạo lợi thế hơn Workflow trên task hiện tại.
- Câu cần giải thích: vì sao seed 55 có thể làm Swarm trả sai, còn seed 11 không mắc cùng lỗi?

Bản bonus chung: `1be14a8`, có hỗ trợ Codex. Kết quả chung đã đo: public Swarm 69/70, verified 70/70; đối kháng 44/50 và 50/50. Đây không phải khai báo cá nhân đã tự chạy. Thành viên cần ghi xác nhận rà soát, output thực chạy và commit thay đổi có ý nghĩa nếu có. Không nhận phần code do người khác/AI tạo là tự viết mới.

### Phần bài chính

Commit draft bổ sung triển khai A/B/C, test theo shape, bộ đối kháng, test điểm yếu Swarm seed 55, kiểm tra tài liệu, script xuất fixture, báo cáo benchmark/crash/ablation và nội dung báo cáo nhóm.

## 3. Đóng góp cụ thể

`f9a6c80` thay đổi 23 file. Các nhóm nội dung ghi nhận được:

- Triển khai `workflow.py`, `single.py`, `orchestrator.py`.
- Test `test_workflow_shape.py`, `test_single_shape.py`, `test_orchestrator_shape.py`, `test_swarm_seed55.py`, `test_adversarial_shapes.py`, `test_submission_docs.py`.
- Dữ liệu đối kháng và script `export_adversarial_cases.py`.
- Biến thể hai investigator tại `src/ablation/orchestrator_two_investigators.py`.
- Báo cáo JSON public, crash, đối kháng, ablation và tài liệu quyết định kiến trúc/research card của bản draft.

Đây là phạm vi được ghi dưới tên tác giả commit, không tự nó chứng minh mọi dòng code được viết thủ công bởi một người. Workflow và Single sau đó được bàn giao qua các nhánh thành viên; Orchestrator được tách, bỏ ablation và bàn giao riêng.

## 4. Bằng chứng

- Commit gốc: `f9a6c800614d18ca7d9b79cfa57a5f2cfc347ff4` — `draft`.
- Lệnh đối chiếu: `git show --stat f9a6c80` và `git show f9a6c80:<đường-dẫn-file>`.
- Ví dụ test trong draft: `test_team_shapes_pass_adversarial_claims` ở `src/tests/test_adversarial_shapes.py`.
- Sau tích hợp phần code/test từ các nhánh được chọn, `main` tại `a0003e4` có 90 test mặc định và 248 test student pass. Đây là kiểm chứng tích hợp, không thay thế kết quả riêng của draft.

Commit `f9a6c80` chưa được merge vào main theo yêu cầu loại trừ develop. Nhiều test, fixture, thí nghiệm và báo cáo của draft chưa có trong cây file main. Vì vậy chưa coi toàn bộ sản phẩm trên là đã được nộp; leader cần chọn phần cần tích hợp và tái lập kết quả ở bản cuối. Không chép số liệu draft vào ADR của main khi chưa đối chiếu lại.

## 5. Công cụ AI đã dùng

Codex hỗ trợ tra lịch sử và soạn báo cáo hiện tại. Chưa có khai báo của Khánh Vũ về công cụ AI dùng cho draft hoặc cách tự kiểm tra cá nhân. Thành viên cần tự bổ sung, không lấy thông tin của người khác để điền thay.

## 6. Tự đánh giá

Bản draft bao phủ nhiều phần kỹ thuật và nghiên cứu. Giới hạn cần trình bày: MockLLM không phải LLM thật; B/C dùng code cố định để quyết định hành động; chi phí là mô phỏng và latency là `unavailable`. Hiện còn thiếu thông tin cá nhân, xác nhận vai trò, trải nghiệm thực hiện và bằng chứng nộp cuối cho các phần chưa tích hợp.
