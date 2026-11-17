# Báo cáo nhóm — Lab 8 LogiX-VN

## 1. Thông tin nhóm

- Nhóm A80. Trưởng nhóm Chu Quang Linh — 2A202603809, kiêm C: Orchestrator và tích hợp; Nguyễn Minh Quân tổng hợp báo cáo. Danh sách thành viên và bảng đóng góp nằm trong [TEAM.md](../../TEAM.md).
- Benchmark public và crash suite chạy với code trên `main` tại `11c6883`, khớp [ADR](decision_adr.md). Bộ đối kháng và ablation lấy từ bản `develop` tại `f1595d5`.

## 2. Mục tiêu và cách tiếp cận

Nhóm so sánh bốn kiến trúc xử lý yêu cầu hoàn phí vận chuyển trên LogiX-VN. Cả bốn dùng cùng giao diện `run_claim` và được đánh giá bằng cùng bộ tình huống, seed, luật nghiệp vụ và bảng giá mô phỏng. Mục tiêu là chọn kiến trúc có mức tự chủ thấp nhất vẫn đáp ứng yêu cầu về độ đúng, chi phí và an toàn hoàn tiền.

Nhóm dùng Workflow làm đường cơ sở, triển khai Single agent và Orchestrator trên cùng bộ công cụ, rồi so với Swarm tham chiếu. Bộ kiểm thử nghiệp vụ kiểm tra trạng thái, số tiền đề xuất, khoản hoàn đã ghi trong SQLite, audit và trace.

## 3. Giải pháp

| Kiến trúc | Luồng xử lý và quyền quyết định |
|---|---|
| **A · Workflow** | Python đọc claim, tra đơn theo quyền truy cập, tính khoản đề xuất theo policy hiện hành và gọi host khi khoản đề xuất dương. MockLLM chỉ soạn phản hồi. |
| **B · Single agent** | Vòng ReAct tối đa 8 bước. Hàm `decide()` chọn công cụ đọc để lấy dữ kiện về đơn, policy, lịch sử hoàn và khoản đề xuất. Code đối chiếu dữ kiện dùng để tính tiền với đơn đã tra, tính lại khi cần rồi gọi host. |
| **C · Orchestrator** | Orchestrator đọc claim và giao điều tra qua `make_handoff`. Investigator dùng công cụ đọc để tra đơn, policy, lịch sử hoàn và tính khoản đề xuất. Orchestrator kiểm tra kết quả, tính lại khi thiếu quote và gọi host. |
| **D · Swarm** | Kiến trúc tham chiếu của lab, dùng để đo ảnh hưởng của mức tự chủ và độ nhạy theo seed. |

**Hoàn tiền.** Code dùng dữ liệu đơn và policy để tính mức đủ điều kiện. Shape gửi khoản đề xuất đầy đủ vào `durability.issue_refund`. Host kiểm tra approval gắn đúng claim, trừ số đã hoàn theo đơn và áp trần trước khi ghi sổ. Ví dụ T14 đủ điều kiện 150.000 VND, đơn đã hoàn 30.000 VND, nên host chỉ ghi thêm 120.000 VND. Khóa theo claim giữ khoản hoàn duy nhất khi chạy lại sau crash.

**Handoff và trace.** Investigator nhận handoff theo danh sách trường cho phép và chỉ được cấp công cụ đọc. Trace ghi trạng thái và các sự kiện đọc dữ kiện, tính khoản đề xuất, gọi host và trả kết quả. Single có thêm bước ReAct và bản tóm tắt quan sát. Orchestrator ghi handoff đã lọc và tóm tắt điều tra. Trace dùng các trường cần cho kiểm tra, loại bỏ ticket thô, dữ liệu cá nhân, secret, header và prompt. Khi mô phỏng crash, shape ghi trace rồi truyền tiếp `InjectedCrash` cho bộ test.

## 4. Kết quả

**Benchmark public.** Mỗi kiến trúc chạy 14 claim trên 5 seed (11, 22, 33, 44, 55). Pass^5 là tỷ lệ claim đạt trên cả 5 seed. Chi phí được mô phỏng theo bảng giá của lab.

| Kiến trúc | Trial đạt (pass rate) | Pass^5 | Seed min–max | Phương sai | VND/lần đạt | Bước TB / p95 |
|---|---:|---:|---:|---:|---:|---:|
| workflow | 70/70 (100.00%) | 100.00% | 100.00%–100.00% | 0.000000 | 28.80 | 4.43 / 5 |
| single | 70/70 (100.00%) | 100.00% | 100.00%–100.00% | 0.000000 | 53.89 | 13.50 / 15 |
| orchestrator | 70/70 (100.00%) | 100.00% | 100.00%–100.00% | 0.000000 | 59.12 | 5.36 / 6 |
| swarm | 69/70 (98.57%) | 92.86% | 92.86%–100.00% | 0.000816 | 49.57 | 2.80 / 3 |

- **Ca Swarm sai ở seed 55.** `R-swarm-C-002-s55` dùng số ngày trễ ghi trong ticket (5 ngày), trong khi dữ liệu đơn ghi 2 ngày. Thử nghiệm tương ứng `R-workflow-C-002-s55` đạt yêu cầu từ chối hoàn.
- **Crash và an toàn.** Crash suite trên main đạt **20/20**. Bộ test mặc định đạt **100 test** và ma trận student đạt **248 test**. Trong benchmark public, cả ba kiến trúc nhóm viết đạt mọi trial theo evaluator, bao gồm các ca phải từ chối hoàn do approval và các ca có chuỗi cần bảo vệ. Các số liệu này thuộc bộ kiểm tra đã chạy. Chưa có kết quả chấm hidden chính thức trong bản tích hợp dùng cho báo cáo.
- **Bộ đối kháng trên develop.** Trên 17 claim × 5 seed, Workflow, Single và Orchestrator cùng đạt **85/85**. Swarm đạt **84/85**. Bộ này có các ca ticket mâu thuẫn với đơn, approval không hợp lệ, trần hoàn theo đơn và ticket chứa canary.
- **Ablation R1 trên develop.** Tăng từ một lên hai investigator giữ nguyên **70/70** trial đạt, đồng thời tăng chi phí mỗi lần đạt từ **59.12** lên **69.98 VND** (**18.4%**). Xem [research card](research_card.md).

**Quyết định kiến trúc.** Chọn **Workflow** theo [ADR](decision_adr.md). Trên bộ public và bộ đối kháng, Workflow đạt cùng tỷ lệ với Single và Orchestrator, với chi phí mỗi lần đạt thấp nhất trên benchmark public. Việc tính khoản đề xuất phụ thuộc dữ liệu đơn, rồi host mới có thể áp approval và trần hoàn. Thí nghiệm R1 cho thấy việc tăng số investigator trong luồng hiện tại làm tăng chi phí mà tỷ lệ đạt giữ nguyên.

## 5. Khó khăn và cách xử lý

- **Dữ kiện đơn thay đổi khi đi qua agent.** Single lưu đúng dữ liệu mà agent gửi vào công cụ tính tiền, đối chiếu với dữ liệu từ `lookup_order` và tính lại khi phát hiện sai lệch. Ca regression nằm trong `test_quote_on_a_tampered_order_is_recomputed_by_code`.
- **Đổi số investigator mà vẫn giữ phép so sánh nhất quán.** Biến thể R1 tái sử dụng luồng Orchestrator và thay cách nhóm công cụ qua `investigator_groups`. Hai lượt chạy dùng cùng dữ liệu, evaluator, seed và bảng giá.

## 6. Tổng hợp đóng góp

| Thành viên | Phần việc |
|---|---|
| Vũ Duy Khánh | Swarm tham chiếu, tích hợp, benchmark và crash suite |
| Trương Thị Thu Hà | Workflow và kiểm thử nghiệp vụ |
| Đào Thị Ngọc Ánh | Single agent và kiểm thử vòng ReAct |
| Chu Quang Linh | Trưởng nhóm, Orchestrator, handoff và kiểm thử an toàn |
| Nguyễn Minh Quân | Tổng hợp số liệu, cập nhật tài liệu và kiểm tra hồ sơ nộp |

Chi tiết commit và test theo [bảng đóng góp](../../TEAM.md#bảng-đóng-góp) và báo cáo cá nhân.

## 7. Hạn chế và hướng cải thiện

MockLLM mô phỏng lời gọi model. Các kết quả hiện tại phản ánh cả logic lựa chọn công cụ viết bằng code. Lab không đo độ trễ, và số bước trong bảng là số sự kiện trace, phụ thuộc mức chi tiết ghi log. Bộ public chỉ gồm 14 claim, còn bộ đối kháng do nhóm tự viết. Nhóm cần đánh giá lại lựa chọn kiến trúc nếu phải xử lý ticket mơ hồ bằng model thật hoặc có các bước điều tra độc lập đủ tốn thời gian để chạy song song.

## 8. Tài liệu tham khảo và bằng chứng

- Bonus B3 đã bổ sung: [báo cáo verifier cho Swarm](bonus_report.md), [public](../../src/reports/bonus_b3_public.json) và [10 claim đối kháng](../../src/reports/bonus_b3_adversarial.json). Số liệu bonus được đo trên main hiện tại; tách biệt với thí nghiệm R1 ở develop. Điều kiện nhận bonus vẫn chờ hidden chính thức.
- [Luật nghiệp vụ](../../docs/business_rules.md), [contract](../../docs/contracts.md), [kiến trúc](../../docs/architecture.md) và [cách tính chỉ số](../../docs/metrics.md).
- [Benchmark public](../../src/reports/benchmark.json), [crash suite](../../src/reports/crash.json), [benchmark đối kháng](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents/blob/f1595d5b3ebee52b2d69e12f1704a93afb6192dd/src/reports/adversarial_benchmark.json) và [ablation R1](https://github.com/ArsNeonci/K5-L3B-DAY08-A80-FromWorkflowsToAgents/blob/f1595d5b3ebee52b2d69e12f1704a93afb6192dd/src/reports/ablation_r1.json). Hai báo cáo đầu thuộc lượt chạy trên main. Hai báo cáo sau thuộc bản develop.
