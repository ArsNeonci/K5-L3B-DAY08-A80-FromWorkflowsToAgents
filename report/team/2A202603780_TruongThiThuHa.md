# Báo cáo cá nhân — 2A202603780_TruongThiThuHa

## 1. Thông tin thành viên

- Họ tên: Trương Thị Thu Hà
- MSSV: 2A202603780
- Email: 26ai.hattt@vinuni.edu.vn
- GitHub: TruongThuHa

## 2. Phần việc phụ trách

### Bonus B3 — Dữ liệu đối kháng và đáp án

- Được giao rà 10 claim và nhãn ở `src/bonus/cases.jsonl`, `world.json`, cùng kịch bản `build_cases.py`; đối chiếu trực tiếp luật nghiệp vụ, không dùng hàm quote để sinh đáp án.
- Kiểm tra các ca thực tế trễ 2 nhưng ticket nói quá, trễ 4 nhưng ticket nói ít, biên 3 ngày, hỏng đã/chưa verify, stacking lấy max, đơn hủy/đang giao và thiếu approval.
- Đối chiếu Workflow với nhãn và test `test_hand_labelled_adversarial_cases` trong `src/tests/test_bonus_swarm_verified.py`.
- Bàn giao: giải thích từng số quote/refund và tình huống cần `policy_denied`; nêu điểm mù có thể có của bộ dữ liệu tự xây.

Bản bonus chung: `1be14a8`, có hỗ trợ Codex. Các nhãn là hằng số ghi theo luật, chưa có xác nhận Hà đã tự rà toàn bộ. Thành viên cần ghi kết quả rà/chạy thật và việc dùng AI; không biến phân công thành tuyên bố đã hoàn thành. Câu cần giải thích: vì sao claim 08 có quote 35.000 VND nhưng refund 0, còn claim 07 lấy 150.000 thay vì cộng ship và damage?

### Phần bài chính

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


## 7. Ghi chú đối chiếu trên bản tích hợp

Báo cáo gốc được lấy riêng từ commit f1595d5; không merge develop. Các mô tả tự kiểm tra, công cụ Claude và slide ở trên là khai báo của tác giả trong báo cáo gốc, chưa được xác minh độc lập qua file slide.

Trên main tại a0003e4, phiên kiểm tra tích hợp ghi nhận 90 test mặc định và 248 test student pass. Đây là kết quả chung, khác phạm vi 70/62 test tác giả ghi cho nhánh riêng. Benchmark và crash report chính thức chưa được commit trên main; các số liệu nhánh draft ở trên cần được thay bằng bằng chứng của bản nộp cuối khi tích hợp.
