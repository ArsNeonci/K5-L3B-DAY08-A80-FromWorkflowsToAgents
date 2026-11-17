# Báo cáo nhóm — Lab 8 LogiX-VN

Tối đa 5 trang ngoài phụ lục. Số liệu lấy từ file trong `src/reports/`, không chép tay từ terminal.

## 1. Thông tin nhóm

- Tên nhóm: TODO-NHÓM
- Thành viên: xem `TEAM.md` (5 người: Leader/Swarm + tích hợp, Workflow, Single agent, Orchestrator, Tài liệu + hồ sơ nộp)
- Commit chốt (trùng `report/team/decision_adr.md`): TODO-LEADER

## 2. Mục tiêu và cách tiếp cận

Bài toán: xử lý claim hoàn phí ship của LogiX-VN theo bốn kiến trúc có cùng chữ ký `run_claim`, rồi dựa vào số đo để chọn kiến trúc ít tự chủ nhất mà vẫn làm được việc. Nhóm chốt ba nguyên tắc trước khi viết code, sau khi đọc `business_rules.md`, `contracts.md` và `swarm_reference.py`:

1. **Sự thật nằm ở dữ liệu có cấu trúc.** Order row và policy có `is_current` là nguồn duy nhất. Chữ trong ticket là dữ liệu người dùng, không bao giờ được parse thành số ngày, mã đơn hay số tiền.
2. **Tiền do code tính, host là người ghi duy nhất.** Mọi shape lấy quote từ `compute_compensation` và truyền **quote đầy đủ** vào `durability.issue_refund`. Host tự kiểm approval của chính claim, trần theo approved/paid và trần theo đơn, rồi trừ phần claim khác đã nhận (T13, T14). Shape tự trừ trước thì host sẽ trừ lần hai.
3. **Trace là ranh giới bảo mật.** Chỉ ghi field đã qua allowlist, ghi ở mọi nhánh return và cả lúc crash.

Chia việc theo bảng phân công của nhóm: Leader đọc swarm và điểm yếu seed 55, chuẩn hóa giao diện chung và tích hợp; ba thành viên viết ba shape song song trên cùng khung (đọc claim → order → quote → host → `finish()`); thành viên 5 phụ trách hồ sơ. Thứ tự làm: workflow trước làm chuẩn tham chiếu, rồi single và orchestrator đối chiếu với nó. Sau đó chạy crash, benchmark, bộ đối kháng tự viết và ablation.

## 3. Giải pháp

Cả ba shape mở connection riêng và đóng trong `finally` (tránh khóa file trên Windows), dựng kết quả bằng `lab8.shapes.common.finish()`, ghi trace bằng `lab8.trace.Trace`, gọi tool qua `lab8.runtime.dispatch` để Budget tính giá giống nhau. Khi gặp `InjectedCrash`, shape flush trace rồi raise lại.

| | A — Workflow | B — Single ReAct | C — Orchestrator |
|---|---|---|---|
| Đọc gì | `get_claim_view` → `lookup_order` → `compute_compensation` | Agent tự chọn từng read tool: claim → order → policy → refund history → quote | Orchestrator đọc claim; investigator đọc order, policy, refund history, quote |
| Ai quyết định gì | Code quyết toàn bộ | `decide()` chọn tool, tối đa 8 bước, `worker=True` nên tool ghi bị `dispatch` từ chối. Sau vòng lặp, code kiểm quote | Orchestrator định tuyến `needs_info` / unknown, dựng handoff, duyệt báo cáo investigator |
| Model làm gì | 1 lần `draft` (soạn câu trả lời) | 1 lần `react` mỗi bước + 1 lần `draft` | `plan` + `investigate` + `draft` |
| Ai gọi host | Shape | Code của shape sau vòng lặp | Orchestrator |

**Ranh giới code / model.** Model không bao giờ chọn số tiền, không tạo approval, không gọi tool ghi. Ở single, scratchpad của agent chỉ chứa output của tool. Agent ghi lại đúng order mà nó gửi vào `compute_compensation`. Nếu order đó khác order mà `lookup_order` trả về (ví dụ agent sửa `delay_days` theo ticket), code tính lại quote từ order thật; test `test_quote_on_a_tampered_order_is_recomputed_by_code` chứng minh điều này. Ở orchestrator, nếu báo cáo investigator thiếu quote thì orchestrator tự tính lại bằng tool tất định.

**Handoff.** Orchestrator dựng handoff bằng `make_handoff`: `facts={}` và `allowed_tools` là 4 read tool, `lookup_order` đứng trước `compute_compensation` vì investigator quote đúng order nó vừa tra. `sanitize` bỏ mọi khóa ngoài allowlist và từ chối nếu còn `CANARY_SECRET_`, `parent_secret`, `raw_headers` hoặc tool ghi. Model call của investigator chỉ nhận handoff đã sanitize, không thấy ticket. Test `test_investigator_model_never_sees_the_ticket` kiểm điều này.

**Trace.** Các event: `claim` (found, has_order_id), `order` (6 field quyết định), `quote`, `host`, `result`. Single thêm `react_step` / `observation`; orchestrator thêm `handoff` / `investigator`. Không ghi ticket, claim row, header, SĐT, địa chỉ, ghi chú nội bộ, tên hàng, `principal_id`, prompt hay text model.

## 4. Kết quả

**Bộ public** (`src/reports/benchmark.json`, 14 claim × seed 11,22,33,44,55, chạy lại cho ra file giống hệt):

| Shape | Pass | Pass^5 | Seed min–max | Variance | Cost/success (VND) | Model calls TB | Tool calls TB | Steps TB / p95 |
|---|---:|---:|---|---:|---:|---:|---:|---|
| workflow | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.80 | 1.00 | 2.79 | 4.43 / 5 |
| single | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 53.89 | 6.50 | 4.50 | 13.50 / 15 |
| orchestrator | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 59.12 | 2.86 | 5.57 | 5.36 / 6 |
| swarm | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 | 3.00 | 4.66 | 2.80 / 3 |

Swarm chỉ fail `R-swarm-C-002-s55`: ticket ghi "trễ 5 ngày", order ghi 2 ngày, swarm tin ticket và trả 20.000 thay vì từ chối. Cả ba shape của nhóm pass trial này.

**Crash safety** (`src/reports/crash.json`): 20/20. T11 (gọi lại) và T12 (crash `after_effect_before_checkpoint` rồi resume) xanh trên cả ba shape. Ma trận student: 248/248 passed.

**Bộ đối kháng tự viết** (`src/reports/adversarial_benchmark.json`, 17 claim × 5 seed, nhãn viết tay theo luật nghiệp vụ). Bộ này mô phỏng các nhóm của hidden: ticket nói quá, injection, đơn `in_transit` / `cancelled`, biên 3 ngày, phí ship 0, nói dối hỏng hàng, stacking ship + damage, principal lẫn, homoglyph `О-107` (chữ O Cyrillic), approval bị thu hồi / mượn / hết hạn / thiếu / thấp hơn quote, cap theo `paid_vnd`, ticket chứa canary, thiếu `order_id` mà ticket có mã đơn. Kết quả: workflow, single, orchestrator 85/85; swarm 84/85.

**Tự kiểm hidden:** nhóm chưa nhận `student_drop/` lúc viết báo cáo. TODO-NHÓM: chạy lệnh trong `src/README.md` và ghi `reports/hidden_selfcheck.json` nếu có.

**Ablation R1** (`src/reports/ablation_r1.json`): tách 1 investigator thành 2 giữ nguyên pass 1.000 nhưng tăng cost/success từ 59.12 lên 69.98 VND (+18.4%). Chi tiết ở `research_card.md`.

Quyết định kiến trúc và lý do: xem `report/team/decision_adr.md` (chọn **workflow**). Phiếu nghiên cứu và ablation: xem `report/team/research_card.md`.

## 5. Khó khăn và cách xử lý

- **Phiên bản Python.** Venv có sẵn trên một máy dùng Python 3.14, ngoài dải 3.11–3.13 mà lab yêu cầu. Nhóm tạo venv bằng `python3.13 -m venv`, rồi chạy `python -m lab8.smoke` (`lab8.smoke pass`, `python 3.13.0 | Darwin arm64`) và cổng host trước khi chia việc.
- **Lọc test theo shape.** `pytest -m student -o addopts= -k single` khớp cả tên test `test_public_single_run_cases` của mọi shape, nên báo nhầm 60 lỗi (thực ra là của orchestrator lúc còn stub). Cách xử lý: lọc bằng `-k "single]"`.
- **Lỗi logic do test phát hiện ở single.** Bản đầu ghi `quote_order` bằng order của `lookup_order` chứ không phải order agent thực sự gửi vào `compute_compensation`, nên phép kiểm "quote trên order bị sửa" không bao giờ kích hoạt. Test `test_quote_on_a_tampered_order_is_recomputed_by_code` lộ ra lỗi này. Nhóm sửa bằng cách ghi lại tham số ngay khi agent chọn tool.
- **Chọn biến cho ablation.** Để chỉ thay đổi một biến, nhóm cho `orchestrator._run` nhận `investigator_groups` (mặc định 1 investigator, hành vi của shape chấm không đổi). Biến thể `ablation/orchestrator_two_investigators.py` chạy qua `--extra-shape`, không sửa `lab8/shapes/__init__.py`.

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong `TEAM.md` (bảng đóng góp) và báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện

- MockLLM không phải model sản xuất; latency là `unavailable`. Pass 1.000 của single và orchestrator đến từ `decide()` bằng code. Với LLM thật, B và C có thêm rủi ro bị ticket dẫn dắt (lỗi của swarm seed 55 chính là dạng này). Lợi ích có thể có là đọc được ticket mơ hồ thì lab không đo được.
- `steps` là số event trong trace và phụ thuộc độ chi tiết của tracer (swarm ghi ít event nhất). Không dùng `steps` để so khối lượng công việc.
- Bộ đối kháng do chính nhóm viết nên có thể mang cùng điểm mù với code. Kết quả hidden chính thức do grader của giảng viên chấm.
- Kết luận đảo lại khi: ticket cần trích xuất bằng model thật; có bước điều tra độc lập tốn latency thật (song song có lợi); hoặc hidden có loại claim mà luật cố định của workflow không bao phủ.
- Hướng cải thiện: thêm verifier bằng code cho single/orchestrator (đối chiếu mọi dữ kiện dùng để quote với order có cấu trúc, như B3); đo latency mô phỏng theo critical path (B1).

## 8. Tài liệu tham khảo

- Tài liệu lab: `docs/business_rules.md`, `docs/contracts.md`, `docs/architecture.md`, `docs/metrics.md`.
- Google Research 2026, *Towards a Science of Scaling Agent Systems* (thư viện tham khảo slide 68–69, bài N8).
- Code tham chiếu: `src/lab8/shapes/swarm_reference.py`, `src/lab8/runtime.py`, `src/lab8/handoff.py`, `src/lab8/durability.py`.
