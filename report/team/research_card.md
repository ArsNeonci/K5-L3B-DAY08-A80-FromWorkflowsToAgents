# Research card

File này nằm cố định ở `report/team/research_card.md`; `python -m lab8.check_submission` đọc cột "Nhóm điền" bằng máy.

Phần này nối tiếp phần mini research ở buổi lý thuyết (slide 62–63). Chọn **một** câu R1–R4, điền 6 dòng, rồi biến nó thành **một ablation** chạy được trong lab: giữ nguyên model (MockLLM), tool, seed, corpus và giá, chỉ thay đổi một biến.

| Câu | Nguồn (thư viện tham khảo, slide 68–69) | Câu hỏi gợi ý cho lab |
| --- | --- | --- |
| R1 · Scaling | Google Research 2026, *Towards a Science of Scaling Agent Systems* | Task claims chủ yếu tuần tự hay song song được? Dự đoán thêm investigator sẽ làm pass rate và cost/success thay đổi thế nào. |
| R2 · Failure taxonomy | MAST, NeurIPS 2025, *Why Do Multi-Agent LLM Systems Fail?* | Các trial fail của swarm (seed 55) thuộc nhóm nào: lỗi giao việc, lệch mục tiêu, hay lỗi kiểm chứng? |
| R3 · Architecture choices | AgentArch, AACL 2026 | Nếu đổi topology mà giữ nguyên mọi thứ khác, biến nào phải cố định để kết luận còn đúng? |
| R4 · Evaluation confounders | EMNLP 2026, *Rethinking Evaluation of MAS Efficiency* | Làm sao chứng minh chênh lệch giữa A/B/C/D là do topology, không phải do prompt, tool hay seed? |

## Phiếu của nhóm

Điền vào cột cuối. Không xóa hai cột đầu.

| Field | Hướng dẫn | Nhóm điền |
| --- | --- | --- |
| CÂU | R1 / R2 / R3 / R4 | R1 · Scaling |
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Google Research 2026, *Towards a Science of Scaling Agent Systems* (thư viện tham khảo slide 68–69 bài N8; slide 15, 24, 33, 41). Loại bằng chứng: benchmark có kiểm soát trên nhiều task và kiến trúc agent. TODO-NHÓM: dán URL từ thư viện slide |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Multi-agent chỉ có lợi khi task chia song song được; với task tuần tự, các biến thể multi-agent trong nghiên cứu giảm hiệu năng 39–70% so với single agent |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Kết luận đo trên LLM thật với các bộ task của nghiên cứu, nơi lỗi phối hợp và chi phí giao tiếp giữa agent là có thật. Không đo trên claims flow có tiền do code tính và host là người ghi duy nhất như LogiX; MockLLM ở đây không mắc lỗi phối hợp |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Claims flow chủ yếu tuần tự (quote cần order, host cần quote). Tách investigator của orchestrator từ 1 thành 2 (nhóm `lookup_order`+`compute_compensation` và nhóm `lookup_policy`+`lookup_refund_history`) sẽ giữ nguyên pass rate (1.000), còn cost/success tăng khoảng 10–25%, vì mỗi trial có điều tra phải trả thêm 1 model call và 1 tool call `get_claim_view` |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ cố định: MockLLM; 6 read tool và host `durability.issue_refund`; seed 11,22,33,44,55; 14 claim public; `config/pricing.yaml`; evaluator `lab8.metrics`; cùng code orchestrator (`orchestrator._run`). Biến duy nhất thay đổi: số investigator, 1 → 2 (`investigator_groups`), qua `--extra-shape orchestrator_2inv=ablation.orchestrator_two_investigators:run_claim` |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Lỗi dự kiến: tách investigator làm `compute_compensation` mất order cần quote (rơi dữ kiện khi giao việc), dẫn tới thiếu quote hoặc quote sai. Đo bằng pass rate, pass^5, cost/success, model/tool calls trung bình, secret leak = 0. Đã chặn lỗi này từ thiết kế: `lookup_order` và `compute_compensation` nằm cùng một nhóm |

## Kết quả ablation

- Lệnh đã chạy (copy nguyên văn): `python -m lab8.benchmark --shapes orchestrator,orchestrator_2inv --extra-shape orchestrator_2inv=ablation.orchestrator_two_investigators:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_r1.json`
- Run id / file report: `src/reports/ablation_r1.json`; ví dụ `R-orchestrator-C-014-s11` so với `R-orchestrator_2inv-C-014-s11`
- Kết quả so với hypothesis (đúng / sai / không kết luận được), kèm số liệu: **Đúng.** Pass rate 1.000 → 1.000, pass^5 1.000 → 1.000, variance 0 → 0. Cost/success 59.12 → 69.98 VND (+18.4%, nằm trong khoảng dự đoán 10–25%). Model calls trung bình 2.86 → 3.79, tool calls 5.57 → 6.50, steps 5.36 → 6.29. Thêm agent trên task tuần tự không tăng độ đúng mà chỉ tăng chi phí. Kết quả cùng hướng với claim của nguồn, nhưng không chứng minh được con số "giảm 39–70%": MockLLM không tạo lỗi phối hợp, nên ở đây pass không giảm.
- Giới hạn: MockLLM không phải model sản xuất, latency là `unavailable`. Phần lợi duy nhất mà song song hóa có thể mang lại là latency, và lab không đo được latency. Chỉ có 14 claim public.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
