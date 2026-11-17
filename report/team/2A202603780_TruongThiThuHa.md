# Báo cáo cá nhân — 2A202603780_TruongThiThuHa

## 1. Thông tin thành viên

- Họ tên: Trương Thị Thu Hà
- MSSV: 2A202603780
- Email: 26ai.hattt@vinuni.edu.vn
- GitHub: TruongThuHa

## 2. Phần việc phụ trách

Thuyết trình Shape A — Workflow (vai 2 trong bảng phân công của nhóm), kèm một test bổ sung cho Workflow.

- Code `src/lab8/shapes/workflow.py` và `src/tests/test_workflow_shape.py` do bạn Khánh Vũ viết (nhánh `develop`). Tôi không viết lại phần này.
- Phần của tôi: đọc hiểu code Workflow, chuẩn bị slide và kịch bản thuyết trình, viết thêm một test cho tình huống T13.

## 3. Đóng góp cụ thể

- Commit `ecd36fe` trên nhánh `ha-workflow`: tách riêng phần Workflow của nhóm (giữ nguyên code) và thêm test `src/tests/test_workflow_ha.py`.
- Test `test_workflow_denies_order_already_refunded` (claim C-013, T13): đơn O-505 đã được hoàn 35.000đ từ claim trước, ticket nói "chưa nhận được tiền". Test kiểm Workflow phải trả `denied`, `proposal_amount` = 35.000 (quote đầy đủ), không ghi thêm dòng ledger, và host có ghi audit `policy_denied`.
- Lý do chọn test này: bộ test của nhóm đã có T02 (ticket nói sai số ngày trễ) và T14 (chỉ hoàn phần chênh), nhưng chưa có test riêng cho Workflow ở trường hợp đơn đã được hoàn đủ.
- Chuẩn bị bài thuyết trình 8 slide và kịch bản lời thoại cho phần Workflow: ranh giới code/model, luồng 7 bước, 4 nguyên tắc trong implementation notes, hai ví dụ C-002 và C-013, số liệu benchmark, an toàn và giới hạn.

## 4. Bằng chứng

- Nhánh `ha-workflow`, commit `ecd36fe` (tác giả TruongThuHa).
- File test: `src/tests/test_workflow_ha.py`.
- Kết quả chạy trên máy (thư mục `src/`, nhánh `ha-workflow`):
  - `python -m pytest -q` → 70 passed
  - `python -m pytest -q -m student -o addopts= -k workflow` → 62 passed
- Số liệu dùng khi thuyết trình lấy từ `src/reports/benchmark.json` và `report/team/decision_adr.md` của nhóm: Workflow pass rate 1.000, pass^5 1.000, variance 0, cost/success 28.80 VND (mô phỏng); crash suite 20/20.

## 5. Công cụ AI đã dùng

- Claude (claude.ai): giải thích nội dung repo và luồng xử lý của Workflow, vẽ sơ đồ hệ thống bằng draw.io, hướng dẫn từng bước dùng VS Code và git (clone, tạo nhánh, commit, push), gợi ý nội dung test T13, soạn slide và kịch bản thuyết trình.
- Cách tự kiểm tra:
  - Chạy lại test trên máy mình (`pytest` ra 70 passed, test Workflow 62 passed) trước khi commit.
  - Kiểm tra trên GitHub rằng nhánh `ha-workflow` chỉ thêm đúng 3 file và không làm thay đổi nhánh `main`, `develop` của nhóm.
  - Đối chiếu số liệu trên slide với file `decision_adr.md` và `benchmark.json` của nhóm, không dùng số tự đặt ra.
  - Tự đọc lại `workflow.py` theo từng `# Step` để có thể tự giải thích khi giảng viên hỏi.

## 6. Tự đánh giá

- Hiểu và giải thích được các ý cốt lõi của Workflow: ranh giới "code quyết tiền, model chỉ viết chữ", lý do truyền quote đầy đủ cho host (T14), lý do không bắt `InjectedCrash` (T12), và vì sao trace cố ý không ghi ticket, SĐT, địa chỉ hay secret.
- Tìm ra một tình huống bộ test của nhóm chưa phủ riêng cho Workflow (T13, đơn đã hoàn đủ) và bổ sung test cho tình huống đó; test chạy xanh cùng toàn bộ 70 test của nhánh.
- Tự thực hiện quy trình git hoàn chỉnh: clone repo nhóm, tạo nhánh riêng, chỉ lấy đúng các file cần thiết, chạy test, commit và push mà không ảnh hưởng tới nhánh `main` và `develop` của nhóm.
- Biến kết quả kỹ thuật thành phần trình bày dễ hiểu (sơ đồ 7 bước, hai ví dụ cụ thể, bảng số liệu), phù hợp với thế mạnh phân tích dữ liệu của tôi.
- Hướng phát triển: lần sau tự viết thử một shape trước khi đọc bản của nhóm, để hiểu sâu hơn phần ReAct và handoff.
