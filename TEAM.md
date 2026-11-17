# Team

## Thông tin nhóm

- Tên nhóm:
- Leader: Chu Quang Linh — 2A202603809 (kiêm C: Orchestrator).
- Lớp: L3A
- Repo nhóm: `K5-L3A-DAY08-TenNhom-FromWorkflowsToAgents` (xem [SUBMISSION.md](SUBMISSION.md))
- URL repo, nhánh nộp, commit chốt:

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Khánh Vũ (tên tác giả Git) | Chưa cung cấp | Chưa có email liên hệ được xác nhận | Chưa xác định | Draft code/test/tài liệu chung |
|   2 | Trương Thị Thu Hà | 2A202603780 | 26ai.hattt@vinuni.edu.vn | TruongThuHa (theo báo cáo cá nhân) | A: Workflow; tách code chung, thêm test T13 |
|   3 | Chưa xác nhận họ tên; tài khoản daoanh9503 | Chưa cung cấp | daoanh9503@gmail.com | daoanh9503 | B: Single; bàn giao code/test từ draft chung |
|   4 | Chu Quang Linh | 2A202603809 | quanglinh1286@gmail.com | [ArsNeonci](https://github.com/ArsNeonci) | Leader kiêm C: Orchestrator; tích hợp, kiểm thử và chốt bài nộp |
|   5 | Chưa cung cấp | Chưa cung cấp | Chưa cung cấp | Chưa cung cấp | Tổng hợp báo cáo (người dùng xác nhận); tạm bỏ qua báo cáo cá nhân trong đợt hoàn thiện này |

Thông tin được đối chiếu từ Git và báo cáo cá nhân hiện có. Riêng email/GitHub của Chu Quang Linh lấy từ cấu hình Git và remote. Các ô chưa xác nhận phải được thành viên bổ sung trước khi nộp; tên tác giả commit không tự chứng minh người đó tự viết toàn bộ code. Không tính người soạn đề trong lịch sử starter là thành viên nhóm.

Gợi ý chia vai:

- Nhóm 6 người: integration; workflow; single agent; orchestrator; ledger/policy/crash; eval/report.
- Nhóm 4 người: workflow + integration; single; orchestrator + handoff; ledger + evaluation.

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| Trương Thị Thu Hà — 2A202603780 | A: Workflow; giữ code draft của Khánh Vũ, thêm test đơn đã hoàn đủ | `ecd36fe` — Workflow và test T13 | `src/tests/test_workflow_ha.py` |
| daoanh9503 — chưa có họ tên/MSSV | B: Single; tiếp nhận code và test giống draft `f9a6c80`, chưa thấy sửa mới so với draft | `883f520` — bàn giao Single | `src/tests/test_single_shape.py` (tiếp nhận từ draft, chưa xác nhận tự viết) |
| Chu Quang Linh — 2A202603809 | C: Orchestrator; tách triển khai từ develop, loại hỗ trợ ablation, kiểm chứng handoff/trace và approval | `a42312c` — code và test Orchestrator | `src/tests/test_orchestrator_shape.py` |

Chu Quang Linh đồng thời là leader theo phân công cập nhật: điều phối tích hợp, kiểm tra xung đột và test chung, chủ trì quyết định kiến trúc/chốt commit, phối hợp thành viên 5 tổng hợp hồ sơ. Các merge `3f43b87`, `9ec463a`, `a0003e4` là bằng chứng tích hợp đã thực hiện; benchmark/ADR/research card và hồ sơ nộp cuối vẫn cần hoàn thiện, không coi phân công này là bằng chứng các việc đó đã xong. Thành viên 5 tiếp tục phụ trách tổng hợp báo cáo.

- Báo cáo cá nhân: [2A202603809_ChuQuangLinh.md](report/team/2A202603809_ChuQuangLinh.md).
- Tài liệu bàn giao kỹ thuật: [orchestrator_handoff.md](report/team/orchestrator_handoff.md).
- Báo cáo Hà: [2A202603780_TruongThiThuHa.md](report/team/2A202603780_TruongThiThuHa.md), lấy riêng từ `f1595d5` và bổ sung ghi chú phạm vi kiểm chứng; không merge develop.
- Dự thảo Single: [CHUA_CO_MSSV_daoanh9503.md](report/team/CHUA_CO_MSSV_daoanh9503.md).
- Dự thảo Khánh Vũ: [CHUA_CO_MSSV_KhanhVu.md](report/team/CHUA_CO_MSSV_KhanhVu.md). Commit `f9a6c80` chứa 23 file draft, gồm test Swarm/đối kháng/tài liệu. Commit này chưa nằm trong lịch sử main; các sản phẩm chưa tích hợp không được tự coi là đã nộp. Chưa thêm dòng đóng góp hợp lệ cho phần đó vào bảng trên.
- Thành viên 5 phụ trách tổng hợp báo cáo theo xác nhận của người dùng; tạm chưa lập báo cáo cá nhân. Không gán nhánh `quan-workflow` cho người này khi chưa có bằng chứng.
- Các merge `3f43b87`, `9ec463a`, `a0003e4` do tài khoản ArsNeonci tích hợp C, B, A; không coi chúng là bằng chứng leader đã tự viết ba kiến trúc.

Các file mang tiền tố `CHUA_` là dự thảo để xác nhận, cần đổi tên đúng `MSSV_HoTen.md` trước khi nộp. Bảng hiện tại chưa chứng minh đủ yêu cầu mỗi người có một test tự thêm/sửa; đặc biệt Single cần xác nhận phần đóng góp kỹ thuật riêng, Khánh Vũ cần xác định phần sẽ được nộp. Hồ sơ thành viên 5 được xử lý sau theo yêu cầu người dùng; yêu cầu báo cáo và đóng góp của đề bài vẫn áp dụng khi nộp chính thức.

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/20241234_NguyenVanAn.md`.

Sao chép mục dưới đây cho từng thành viên.

## MSSV_HoTen

### Phần việc phụ trách

-

### Đóng góp cụ thể

-

### Bằng chứng

-
