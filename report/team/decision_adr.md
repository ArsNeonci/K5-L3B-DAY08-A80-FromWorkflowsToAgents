# Decision record

Điền sau dấu `:` trên cùng dòng, không xóa nhãn. Giảng viên và `python -m lab8.check_submission` (chạy trong `src/`) đọc các dòng này bằng máy. Không đổi tên hay dời file này khỏi `report/team/`.
`Shape chọn` phải là đúng một trong: `workflow`, `single`, `orchestrator`, `swarm`. Đây là shape được chấm cổng hidden.

- Shape chọn: workflow
- Commit hash: TODO-LEADER: ghi kết quả `git rev-parse --short HEAD` sau commit chốt
- Run id dẫn chứng: R-workflow-C-002-s55 (pass, denied), R-swarm-C-002-s55 (fail, resolved 20000), R-workflow-C-014-s11 (pass, resolved, ledger 120000), file src/reports/benchmark.json
- Pass rate / pass^5 / seed min-max / variance: workflow 1.000 / 1.000 / 1.000–1.000 / 0.000000 (70 trial = 14 claim × 5 seed, src/reports/benchmark.json)
- Cost per success (mô phỏng, VND): workflow 28.80 (single 53.89, orchestrator 59.12, swarm 49.57)
- Crash safety: 20/20 (src/reports/crash.json); T11, T12 xanh trên cả 3 shape của nhóm
- Secret leak / approval bypass: 0 / 0 (không trial nào fail vì `forbidden_substring`; mọi refund đi qua `durability.issue_refund`)

Ví dụ một dòng đã điền: `- Shape chọn: workflow`, `- Crash safety: 20/20 (src/reports/crash.json)`.

## Bảng so sánh (bộ public, seed 11, 22, 33, 44, 55)

Số liệu lấy từ `src/reports/benchmark.json`. Chạy lại lệnh benchmark hai lần cho ra file giống hệt từng byte.

| Shape | Pass | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Model calls TB | Tool calls TB | Steps TB / p95 |
|---|---:|---:|---|---:|---:|---:|---:|---|
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.80 | 1.00 | 2.79 | 4.43 / 5 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 53.89 | 6.50 | 4.50 | 13.50 / 15 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 59.12 | 2.86 | 5.57 | 5.36 / 6 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 3.00 | 4.66 | 2.80 / 3 |

Bộ đối kháng tự viết (17 claim, nhãn viết tay theo `docs/business_rules.md`, × 5 seed, `src/reports/adversarial_benchmark.json`): workflow, single, orchestrator đều 85/85; swarm 84/85 (pass 0.988, pass^5 0.941), trượt `R-swarm-C-A01-s55` (ticket ghi "trễ 9 ngày", order ghi 2).

## Vì sao shape này

Trên cùng 14 claim public × 5 seed, cùng MockLLM, cùng bảng giá, ba shape A/B/C cùng đạt pass 1.000 và pass^5 1.000, variance 0. Bộ đối kháng 85 trial cũng cho kết quả như vậy. Vì độ đúng ngang nhau, quyết định dựa vào chi phí và mức tự chủ. Workflow có cost/success thấp nhất (28.80 VND, bằng 0.53× single, 0.49× orchestrator, 0.58× swarm), chỉ gọi model 1 lần mỗi trial và chỉ để soạn câu chữ. Nó không có nhánh nào để model lái, nên không có đường nào để chữ trong ticket ảnh hưởng tới số tiền. Bài toán claim là tuần tự (claim → order → quote → host): quote phụ thuộc order, approval phụ thuộc quote. Vì vậy thêm agent không mở ra được việc song song nào đáng kể (xem ablation trong `research_card.md`). Đây là kiến trúc ít tự chủ nhất mà vẫn làm được việc.

## Có đáng đổi lấy multi-agent không

Không, ít nhất là trên dữ liệu này. Orchestrator và single không pass cao hơn workflow (cùng 1.000), nhưng tốn gấp 1.9–2.1 lần cost/success. Swarm vừa đắt hơn (1.72×) vừa có variance khác 0: seed 55 tin số ngày trong ticket. Quyết định sẽ đảo lại nếu:

1. Ticket thật mơ hồ đến mức cần model đọc và trích dữ kiện có cấu trúc (ví dụ khách không có mã đơn nhưng mô tả đủ để tra). Khi đó single hoặc orchestrator, với model thật, có thể giảm số `needs_info`. MockLLM hiện không đo được lợi ích này.
2. Có các bước điều tra độc lập tốn thời gian thật (gọi carrier API, đối soát kho). Lúc đó orchestrator chạy song song có thể rút ngắn critical path. Ablation R1 cho thấy tách investigator hiện chỉ làm tăng cost.
3. Hidden có loại claim mà luật cố định không bao phủ được, và workflow pass dưới 0.75.

## Trace và bằng chứng

Mỗi lần chạy ghi đúng một file `traces/<run_id>.json` gồm `run_id`, `steps`, `events`, ghi ở mọi nhánh return và cả khi crash (flush rồi raise lại `InjectedCrash`). Workflow ghi các event `claim` (chỉ `found`, `has_order_id`), `order` (6 field quyết định: `order_id`, `status`, `delay_days`, `shipping_fee_vnd`, `paid_vnd`, `damage_verified`), `quote` (số tiền, lý do, clause), `host` (ok, reason, conflict, amount), và `result`. Single ghi thêm `react_step` và `observation` cho từng bước; orchestrator ghi thêm `handoff` (bản `handoff.v1` đã sanitize) và `investigator` (tóm tắt theo allowlist).

Những field cố ý **không** ghi:
- `ticket`: chữ người dùng có thể chứa canary, SĐT hoặc injection (case C-A15 nhét `CANARY_SECRET_` vào ticket).
- `parent_secret`, `raw_headers`, claim row thô.
- `phone`, `address`, `internal_note`, `item_name`: các field này không bao giờ rời `lookup_order`.
- `principal_id`.
- Prompt và text của MockLLM.

Shape không in gì ra stdout và không ghi file nào khác. Mọi thứ shape ghi đều nằm trong thư mục scanner quét được. Một log nằm ngoài chỗ đó thì đội security không có cách nào chứng minh là sạch, nên nhóm chọn không ghi. Ngoài scanner của grader còn có test nhóm tự viết (`test_*_shape.py`) quét trace để tìm ticket, canary và PII.

## Giới hạn

- MockLLM không phải model sản xuất: nó không hiểu ticket. Pass 1.000 của single và orchestrator đến từ `decide()` viết bằng code, không phải từ khả năng suy luận của model. Với model thật, B và C có thể tệ hơn (bị ticket dẫn dắt) hoặc tốt hơn (xử lý được ticket mơ hồ).
- Latency là `unavailable`. Cost là giá token mô phỏng theo `config/pricing.yaml`, không phải hóa đơn API.
- Số `steps` là số event trong trace. Các shape có độ chi tiết trace khác nhau, nên không dùng `steps` để so khối lượng công việc. Dùng model calls và tool calls thay thế.
- Bộ public chỉ có 14 claim. Bộ đối kháng do nhóm tự viết nên có thể mang cùng điểm mù với code. Kết quả hidden chính thức do grader của giảng viên chấm. Không sửa JSON cho đủ 0.75.
