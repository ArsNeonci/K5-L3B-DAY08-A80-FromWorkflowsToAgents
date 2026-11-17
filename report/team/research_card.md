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
| SOURCE | Paper/blog, năm, URL, loại bằng chứng (benchmark, production report, blog kinh nghiệm) | Kim và cộng sự, *Towards a Science of Scaling Agent Systems* ([arXiv, bản tiền ấn phẩm 2025](https://arxiv.org/abs/2512.08296)). Benchmark có kiểm soát trên nhiều kiến trúc và họ LLM. |
| CLAIM | Một kết luận gốc của nguồn. Không viết rộng hơn phạm vi paper | Trên các tác vụ suy luận tuần tự được khảo sát, các biến thể đa agent trong nghiên cứu giảm hiệu năng 39–70% so với single agent. |
| BOUNDARY | Model / dataset / setup giới hạn kết luận đó | Nghiên cứu dùng ba họ LLM và bốn benchmark. LogiX-VN dùng MockLLM, tính tiền bằng code và để host duy nhất ghi refund. Thí nghiệm trong lab đo một cấu hình cụ thể của Orchestrator. |
| HYPOTHESIS | Nếu đổi shape A→B (hoặc bật/tắt một thành phần), metric X sẽ đổi theo hướng nào, khoảng bao nhiêu | Tách một investigator thành hai giữ nguyên pass rate và làm cost/success tăng 10–25%. Cấu hình hai investigator phát sinh thêm lượt gọi MockLLM và đọc claim ở các ca cần điều tra. |
| METHOD | Biến giữ cố định: model, tools, seed, corpus, giá, evaluator. Biến duy nhất được thay đổi: … | Giữ nguyên MockLLM, tập công cụ, host, 14 claim public, seed 11, 22, 33, 44, 55, bảng giá và evaluator. Thay cấu hình phân công từ một investigator dùng cả bốn công cụ sang hai investigator. Nhóm thứ nhất tra đơn và tính quote. Nhóm thứ hai tra policy và lịch sử hoàn. Cả hai nhóm chạy lần lượt trong cùng luồng Orchestrator. |
| FAILURE / METRIC | Một lỗi dự kiến và cách đo nó: pass rate, pass^5, variance, cost/success, leak, bypass | Khi tách công cụ theo nhóm, bước tính quote có thể thiếu dữ liệu đơn. Giữ `lookup_order` và `compute_compensation` trong cùng nhóm. Đo pass rate, pass^5, phương sai theo seed, cost/success và số lượt gọi model/công cụ. |

## Kết quả ablation

- Lệnh ghi trong bản tích hợp (chạy từ `src/`): `python -m lab8.benchmark --shapes orchestrator,orchestrator_2inv --extra-shape orchestrator_2inv=ablation.orchestrator_two_investigators:run_claim --cases data/public_claims.jsonl --seeds 11,22,33,44,55 --out reports/ablation_r1.json`
- Run id / file report: `R-orchestrator-C-014-s11` và `R-orchestrator_2inv-C-014-s11`. Số liệu lấy từ [ablation_r1.json](../../src/reports/ablation_r1.json) tại commit tích hợp `f1595d5`.
- **Kết quả phù hợp với giả thuyết.** Hai cấu hình đều đạt 70/70, pass^5 = 100% và phương sai theo seed bằng 0. Cost/success tăng từ 59.12 lên 69.98 VND (+18.4%). Số lần gọi model trung bình tăng từ 2.86 lên 3.79, số lần gọi công cụ tăng từ 5.57 lên 6.50.
- Giới hạn của kết quả. Bộ public có 14 claim và cấu hình một investigator đã đạt trần 100%. Hai nhóm công cụ chạy tuần tự, latency là `unavailable`. Kết luận về chi phí áp dụng cho MockLLM và bảng giá mô phỏng của lab.

Muốn đi xa hơn một ablation để lấy điểm cộng thì xem [docs/bonus_topics.md](../../docs/bonus_topics.md).
