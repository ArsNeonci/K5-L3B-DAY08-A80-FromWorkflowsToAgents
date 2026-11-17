# Team

## Thông tin nhóm

- Tên nhóm: A80
- Lớp: L3B
- Repo nhóm: K5-L3B-DAY08-A80-FromWorkflowsToAgents
- Url: https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents
- Nhánh: `main`

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
| 1 — Vũ Duy Khánh | Swarm, tích hợp, benchmark và crash suite | `f9a6c80` (commit tích hợp đứng tên Khánh Vũ) | `src/tests/test_swarm_seed55.py` (đưa từ commit gốc vào hồ sơ kiểm tra cuối) |
| 2 — Trương Thị Thu Hà | Workflow, kiểm tra ca đơn đã hoàn đủ (T13) | `ecd36fe` | `src/tests/test_workflow_ha.py` |
| 3 — Đào Thị Ngọc Ánh | Vòng ReAct và kiểm thử Single agent | `883f520` (bàn giao Single từ draft `f9a6c80`) | `src/tests/test_single_shape.py` (có trong bản tích hợp) |
| 4 — Chu Quang Linh | Trưởng nhóm, Orchestrator, handoff và test an toàn | `a42312c` (code và test), `b58ba74` (bàn giao) | `src/tests/test_orchestrator_shape.py` |
| 5 — Nguyễn Minh Quân | Tổng hợp bằng chứng, cập nhật `TEAM.md` và kiểm tra hồ sơ | `f824917` (tài liệu và test hồ sơ) | `src/tests/test_adr_required_fields.py` |


Báo cáo hiện có:

- [Chu Quang Linh](report/team/2A202603809_ChuQuangLinh.md).
- [Trương Thị Thu Hà](report/team/2A202603780_TruongThiThuHa.md).
- [Nguyễn Minh Quân](report/team/2A202603794_NguyenMinhQuan.md).
- [Đào Thị Ngọc Ánh](report/team/2A202603790-DaoThiNgocAnh.md).
- [Vũ Duy Khánh](report/team/2A202603865-VuDuyKhanh.md).
- [Bàn giao Orchestrator](report/team/orchestrator_handoff.md).


## Phân công bonus B3

Bản triển khai chung và bằng chứng bonus nằm tại `1be14a8`, được hoàn thiện với hỗ trợ Codex. Bảng sau giao trách nhiệm rà soát, kiểm chứng và trình bày; không tự coi việc phân công là bằng chứng từng người đã tự viết code hoặc tự chạy test. Giữ nguyên các commit đóng góp bài chính ở bảng trên; bổ sung commit cá nhân khi có công việc thực tế mới.

| Thành viên | Trách nhiệm bonus | File/bằng chứng cần đối chiếu | Tiêu chí bàn giao |
| --- | --- | --- | --- |
| Vũ Duy Khánh — 2A202603865 | Swarm gốc và baseline; giải thích seed 55, so peer/parse/draft và tool cost trước/sau verifier | `src/bonus/swarm_verified.py`; `src/tests/test_swarm_seed55.py`; `test_no_mismatch_keeps_swarm_calls_and_only_adds_read_cost` trong `src/tests/test_bonus_swarm_verified.py` | Chỉ ra lỗi gốc, phần giữ nguyên và chi phí thêm; không sửa reference Swarm |
| Trương Thị Thu Hà — 2A202603780 | Rà 10 claim đối kháng và đáp án theo luật; đối chiếu Workflow | `src/bonus/build_cases.py`, `cases.jsonl`, `world.json`; `test_hand_labelled_adversarial_cases` | Giải thích từng quote/refund; bao phủ biên 3 ngày, stacking, trạng thái đơn và thiếu approval; không sinh nhãn bằng quote |
| Đào Thị Ngọc Ánh — 2A202603790 | Kiểm thử verifier, một vòng sửa, retry/crash và early return | `src/tests/test_bonus_swarm_verified.py`: `test_verifier_checks_all_three_required_fields`, `test_crash_resume_and_repeated_retry_are_safe`, `test_early_return_trace_contract` | Rà phát hiện sai delay/status/damage và chạy được bộ test; ghi đúng output thực tế |
| Chu Quang Linh — 2A202603809 | Leader; verifier, scope principal, bảo mật trace, tính Budget và tích hợp | `src/bonus/swarm_verified.py`; `test_overstated_ticket_is_fixed_before_any_refund`, `test_ticket_canary_never_enters_output_or_trace` | Kiểm tra trước cả denied quote 0 và ghi tiền; giữ host duy nhất ghi; chốt test và hồ sơ chung |
| Nguyễn Minh Quân — 2A202603794 | Benchmark, safety sweep, bảng số liệu và báo cáo bonus | `src/bonus/evaluate.py`; `src/reports/bonus_b3_public.json`, `bonus_b3_adversarial.json`; `report/team/bonus_report.md` | So cùng corpus/seed; đối chiếu pass/pass^5/variance/cost và safety; ghi giới hạn MockLLM, điều kiện hidden |

Kết quả chung đã kiểm chứng trong phiên hỗ trợ: 62 test bonus, 162 test mặc định và 248 test student pass; kiểm tra hồ sơ 0 FAIL. Lệnh tái lập ở [README bonus](src/bonus/README.md). Mỗi thành viên xác nhận phần đã rà/chạy, cách dùng AI và đóng góp mới trong báo cáo cá nhân trước khi nộp. Điểm bonus vẫn phụ thuộc gate hidden do giảng viên chấm.

## Báo cáo cá nhân theo mẫu

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
