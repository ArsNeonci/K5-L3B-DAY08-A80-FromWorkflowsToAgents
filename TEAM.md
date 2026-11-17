# Team

## Thông tin nhóm

- Tên nhóm: A80 (theo tên repo)
- Lớp: Chờ xác nhận giữa L3B trong tên repo hiện tại và L3A trong [SUBMISSION.md](SUBMISSION.md).
- Repo nhóm: [K5-L3B-DAY08-A80-FromWorkflowsToAgents](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents)
- Bản tích hợp đã đối chiếu: `origin/develop` tại `f9a6c80`.
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
| 1 — Vũ Duy Khánh | Swarm, tích hợp, benchmark và crash suite | `f9a6c80` (commit tích hợp đứng tên Khánh Vũ) | `src/tests/test_swarm_seed55.py`, `src/tests/test_adversarial_shapes.py` (có trong bản tích hợp) |
| 2 — Trương Thị Thu Hà | Workflow, kiểm tra ca đơn đã hoàn đủ (T13) | `ecd36fe` | `src/tests/test_workflow_ha.py` |
| 3 — Đào Thị Ngọc Ánh | Vòng ReAct và kiểm thử Single agent | `f9a6c80` (có triển khai trong bản tích hợp, chờ xác nhận commit cá nhân) | `src/tests/test_single_shape.py` (có trong bản tích hợp) |
| 4 — Chu Quang Linh | Trưởng nhóm, Orchestrator, handoff và test an toàn | `a42312c` (code và test), `b58ba74` (bàn giao) | `src/tests/test_orchestrator_shape.py` |
| 5 — Nguyễn Minh Quân | Tổng hợp bằng chứng, cập nhật `TEAM.md` và kiểm tra hồ sơ | Chờ commit phần tài liệu | `src/tests/test_adr_required_fields.py` |

Khi chốt bài, đối chiếu các commit và test với lịch sử nhánh nộp. Các commit riêng của Hà và Linh hiện nằm trên nhánh bàn giao.

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
