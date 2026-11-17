# Decision record

- Shape chọn: workflow
- Commit hash: `11c6883`
- Run id dẫn chứng: R-workflow-C-002-s55 (đạt, denied), R-swarm-C-002-s55 (trượt, resolved), R-workflow-C-014-s11 (đạt, resolved)
- Pass rate / pass^5 / seed min-max / variance: 1.000 / 1.000 / 1.000–1.000 / 0.000000
- Cost per success (mô phỏng, VND): 28.80
- Crash safety: 20/20 theo crash suite chạy trên main
- Secret leak / approval bypass: 0 / 0 ghi nhận cho Workflow trên bộ public, trong phạm vi các ca và điều kiện của evaluator

Benchmark public và crash suite được chạy lại với code đã tích hợp trên `main` tại `11c6883`. Kết quả đối kháng và ablation thuộc bản `develop` tại `f1595d5`.

## Vì sao shape này

Chọn **Workflow** vì đạt cùng độ đúng và độ ổn định với Single agent và Orchestrator trên bộ public, đồng thời có chi phí thấp nhất. Bốn kiến trúc chạy cùng 14 claim và 5 seed (11, 22, 33, 44, 55), cùng bảng giá và evaluator.

| Kiến trúc | Trial đạt | Pass rate | Pass^5 | Seed min–max | Phương sai | VND/lần đạt |
|---|---:|---:|---:|---:|---:|---:|
| workflow | 70/70 | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 28.80 |
| single | 70/70 | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 53.89 |
| orchestrator | 70/70 | 1.000 | 1.000 | 1.000–1.000 | 0.000000 | 59.12 |
| swarm | 69/70 | 0.986 | 0.929 | 0.929–1.000 | 0.000816 | 49.57 |

Bộ đối kháng trên bản develop cho kết quả Workflow, Single và Orchestrator cùng đạt 85/85, Swarm đạt 84/85. Ở C-002, ticket khai trễ 5 ngày, dữ liệu đơn ghi 2 ngày. Workflow từ chối đúng ở seed 55, còn Swarm trả `resolved`. Ở C-014, Workflow chuyển khoản đề xuất 150.000 VND cho host. Evaluator xác nhận ledger ghi phần chênh lệch 120.000 VND sau khi trừ 30.000 VND đã hoàn.

## Có đáng đổi lấy multi-agent không

Giữ Workflow cho phạm vi hiện tại. Khi tăng số investigator trong Orchestrator từ một lên hai, số trial đạt giữ ở 70/70, còn chi phí mỗi lần đạt tăng từ 59.12 lên 69.98 VND (+18.4%). Luồng tính tiền cần dữ liệu đơn trước, sau đó host mới kiểm approval và trần hoàn. Nhóm sẽ đánh giá lại khi có bước điều tra độc lập có thể chạy song song, hoặc khi ticket mơ hồ đòi hỏi khả năng trích xuất của model thật. [Research card](research_card.md)

## Trace và bằng chứng

Workflow ghi sự kiện `claim`, `order`, `quote`, `host`, `result` theo nhánh thực thi. Khi mô phỏng crash, Workflow ghi `crash` rồi truyền tiếp `InjectedCrash`. Trace mới được ghi theo `run_id` trong thư mục `traces/` để evaluator kiểm tra. Các trường như ticket thô, `parent_secret`, header, SĐT, địa chỉ, ghi chú nội bộ và prompt được loại khỏi trace để hạn chế lộ dữ liệu. Host giữ quyền duy nhất ghi khoản hoàn, kiểm approval của đúng claim và chống ghi trùng theo claim.

Bằng chứng chạy lại trên main gồm [benchmark public](../../src/reports/benchmark.json), [crash suite](../../src/reports/crash.json). Bản develop lưu [benchmark đối kháng](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents/blob/f1595d5b3ebee52b2d69e12f1704a93afb6192dd/src/reports/adversarial_benchmark.json) và [ablation R1](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents/blob/f1595d5b3ebee52b2d69e12f1704a93afb6192dd/src/reports/ablation_r1.json). [Báo cáo nhóm](group_report.md)

## Giới hạn

MockLLM mô phỏng lời gọi model, latency là `unavailable` và chi phí là giá mô phỏng. Bộ đối kháng do nhóm xây dựng nên có thể cùng điểm mù với các triển khai. Bản tích hợp chưa có kết quả chấm hidden chính thức.
