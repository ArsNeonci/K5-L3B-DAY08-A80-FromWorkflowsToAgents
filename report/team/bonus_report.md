# Bonus report: B3

- Topic + nguồn: verifier/aggregator chống khuếch đại lỗi; Google Research 2026, error amplification, slide 17/22/42, theo [topic B3 của đề](../../docs/bonus_topics.md). Triển khai kế thừa `src/lab8/shapes/swarm_reference.py`.
- CLAIM: kiểm chứng tập trung có thể hạn chế lỗi từ các agent trước khi tạo tác động.
- BOUNDARY: nghiên cứu được đề dẫn xét hệ agent/LLM; lab dùng MockLLM và host tất định. Không dùng lab để xác nhận hệ số khuếch đại 17,2×/4,4× của nguồn.
- HYPOTHESIS: đối chiếu dữ kiện trước ghi sẽ sửa lỗi tin ticket của Swarm; pass/pass^5 tăng và variance giảm, đổi lại thêm tool cost.
- Biến cố định: claim, seed 11/22/33/44/55, MockLLM, peer/parse/draft, tool, policy, giá, evaluator và DB mới mỗi trial. Biến thay đổi: bật verifier và một vòng sửa quote từ order đáng tin cậy.

## Tái lập và thiết kế

Chạy từ `src/`, sau khi cài `requirements.txt`:

```powershell
python -m pytest -q tests/test_bonus_swarm_verified.py
python -m bonus.evaluate
```

Verifier re-read order theo principal, so sánh mọi `ORDER_FIELDS` gồm `delay_days`, `status`, `damage_verified`. Nếu lệch, code quote lại tối đa một lần và ghi `verifier_override`. Kiểm tra diễn ra trước cả nhánh denied với quote 0, nên sửa được ticket khai thiếu ngày. Host gốc vẫn duy nhất ghi tiền; reference Swarm và thước đo giữ nguyên. Test kiểm sửa dữ kiện, canary, early return, approval và crash/resume tại ba điểm.

10 claim mới và nhãn hằng số theo luật nghiệp vụ nằm ở `src/bonus/cases.jsonl`, `world.json`; không dùng quote để sinh đáp án. Có ticket nói quá/nói thiếu, nhiều con số, khai hỏng chưa verify, đơn hủy/đang giao, stacking, thiếu approval và biên 3 ngày. Chi tiết và CLI `--extra-shape`: [README bonus](../../src/bonus/README.md).

## Kết quả

Kiểm chứng trên Windows/Python 3.12.6: 62 test bonus pass; toàn bộ test mặc định 162 pass; ma trận student 248 pass; kiểm tra hồ sơ 0 FAIL. Code, nhãn và báo cáo được hoàn thiện với hỗ trợ Codex; kết quả lấy từ lệnh chạy thực tế.

Nguồn do script sinh: [public](../../src/reports/bonus_b3_public.json), [đối kháng](../../src/reports/bonus_b3_adversarial.json). Mỗi shape có 70 trial public và 50 trial đối kháng. Cost/success là VND mô phỏng, gồm trial sai.

| Corpus / shape | Pass | Pass^5 | Variance | Cost/success |
| --- | ---: | ---: | ---: | ---: |
| Public / workflow | 70/70 | 1.000 | 0 | 28.80 |
| Public / swarm | 69/70 | 0.929 | 0.000816 | 49.57 |
| Public / swarm_verified | 70/70 | 1.000 | 0 | 57.57 |
| Đối kháng / workflow | 50/50 | 1.000 | 0 | 30.94 |
| Đối kháng / swarm | 44/50 | 0.400 | 0.057600 | 61.32 |
| Đối kháng / swarm_verified | 50/50 | 1.000 | 0 | 65.76 |

Verifier thực hiện 60 check/1 override trên public, 50 check/9 override trên đối kháng. Không cần check cho nhánh thiếu mã đơn/không thấy đơn. Chỉ 6/9 lần sửa đối kháng làm thay đổi verdict của trial; các lần còn lại gặp đơn không đủ trạng thái hoặc damage đã quyết định mức max.

Safety sweep riêng chạy lại cùng corpus/seed với DB mới, đọc ledger, kiểm authorization và quét artifact với secret/PII của corpus. Cả ba shape đều có **0** approval bypass, secret leak, PII leak, invalid trace và unexpected ledger trial trên hai corpus. Đây là số đo local, không phải chứng nhận hidden.

Trace minh họa được rút gọn trong khóa `verifier_trace_example` của JSON public: `R-swarm_verified-C-002-s55` có override `delay_days`, `repair_rounds=1`, quote sau kiểm tra 0. Swarm gốc cùng claim/seed trả resolved; verifier sửa trước khi có refund.

## Kết luận và giới hạn

Kết quả ủng hộ giả thuyết trong phạm vi lỗi được cài vào reference Swarm: verifier đưa độ đúng về bằng Workflow, nhưng cost/success cao hơn Workflow khoảng 2 lần trên public. Nó giữ cấu trúc peer/parse/handoff để làm đối chứng, chưa thể hiện giá trị vượt Workflow trên task này. Không nên chọn multi-agent chỉ vì có thêm verifier.

MockLLM không suy luận như model thật; latency là `unavailable`. Verifier tin order/policy và tool quote, không phát hiện lỗi nội tại của DB hoặc quote khi dữ kiện vẫn khớp. Dữ liệu đối kháng do nhóm tự xây có thể mang cùng điểm mù. Kết luận có thể đổi khi task cần trích xuất mơ hồ hoặc điều tra độc lập mà Workflow không xử lý được. Bonus chỉ được nhận nếu shape chính qua must-pass, hidden ≥0.80 và test host xanh; chưa có hidden chính thức để xác nhận gate này.
