# Team

## Thông tin nhóm

- Tên nhóm: A80 (theo tên repo)
- Leader: Chu Quang Linh — 2A202603809 (kiêm C: Orchestrator).
- Lớp: Chờ xác nhận giữa L3B trong tên repo hiện tại và L3A trong [SUBMISSION.md](SUBMISSION.md).
- Repo nhóm: [K5-L3B-DAY08-A80-FromWorkflowsToAgents](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents)
- Bản draft được thành viên 5 đối chiếu: `develop` tại `f9a6c80`; không phải bản main hiện tại. Main đã tích hợp các nhánh cá nhân, không merge develop.
- Nhánh nộp và commit chốt: Chờ trưởng nhóm xác nhận và đối chiếu với [ADR](report/team/decision_adr.md).

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
| 1 | Vũ Duy Khánh | 2A202603865 | 26ai.khanhvd2@vinuni.edu.vn | [khanhduyvu1](https://github.com/khanhduyvu1) | Swarm và tích hợp |
| 2 | Trương Thị Thu Hà | 2A202603780 | 26ai.hattt@vinuni.edu.vn | [truongthuha](https://github.com/truongthuha) | Workflow |
| 3 | Đào Thị Ngọc Ánh | 2A202603790 | 26ai.anhdtn@vinuni.edu.vn | [daoanh9503](https://github.com/daoanh9503) | Single agent |
| 4 | Chu Quang Linh | 2A202603809 | 26ai.linhcq3@vinuni.edu.vn | [ArsNeonci](https://github.com/ArsNeonci) | Trưởng nhóm, Orchestrator, handoff và test an toàn |
| 5 | Nguyễn Minh Quân | 2A202603794 | 26ai.quannm10@vinuni.edu.vn | [nmqdhtb](https://github.com/nmqdhtb) | Tài liệu và kiểm tra hồ sơ nộp |

## Bảng đóng góp

`python -m lab8.check_submission` đọc bảng này bằng máy: giữ nguyên tiêu đề `## Bảng đóng góp` và các cột. Mỗi người một dòng: commit có nội dung và ít nhất một test đã thêm hoặc sửa.

| Người | Vai | Commit | Test đã thêm hoặc sửa |
| --- | --- | --- | --- |
| 1 — Vũ Duy Khánh | Swarm, tích hợp, benchmark và crash suite | `f9a6c80` (commit tích hợp đứng tên Khánh Vũ) | `src/tests/test_swarm_seed55.py`, `src/tests/test_adversarial_shapes.py` (thuộc draft develop, chưa có trên main) |
| 2 — Trương Thị Thu Hà | Workflow, kiểm tra ca đơn đã hoàn đủ (T13) | `ecd36fe` | `src/tests/test_workflow_ha.py` |
| 3 — Đào Thị Ngọc Ánh | Vòng ReAct và kiểm thử Single agent | `883f520` (bàn giao Single từ draft `f9a6c80`) | `src/tests/test_single_shape.py` (có trong bản tích hợp) |
| 4 — Chu Quang Linh | Trưởng nhóm, Orchestrator, handoff và test an toàn | `a42312c` (code và test), `b58ba74` (bàn giao) | `src/tests/test_orchestrator_shape.py` |
| 5 — Nguyễn Minh Quân | Tổng hợp bằng chứng, cập nhật `TEAM.md` và kiểm tra hồ sơ | `f824917` (tài liệu và test hồ sơ) | `src/tests/test_adr_required_fields.py` |

Các nhánh của Hà, Ánh và Linh đã được tích hợp vào main qua `a0003e4` và các commit cha. Các sản phẩm riêng của draft develop chưa được coi là đã nộp. Leader Chu Quang Linh điều phối tích hợp, kiểm thử và chốt hồ sơ; Nguyễn Minh Quân phụ trách tổng hợp báo cáo.

Báo cáo hiện có:

- [Chu Quang Linh](report/team/2A202603809_ChuQuangLinh.md).
- [Trương Thị Thu Hà](report/team/2A202603780_TruongThiThuHa.md).
- [Nguyễn Minh Quân](report/team/2A202603794_NguyenMinhQuan.md).
- [Dự thảo Single](report/team/CHUA_CO_MSSV_daoanh9503.md).
- [Dự thảo Khánh](report/team/CHUA_CO_MSSV_KhanhVu.md).
- [Bàn giao Orchestrator](report/team/orchestrator_handoff.md).

Hai dự thảo cần cập nhật danh tính/tên file theo thông tin thành viên 5 vừa bổ sung. Việc bàn giao code từ draft không được coi là tự viết mới toàn bộ code.

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
