# Báo cáo cá nhân — Chu Quang Linh

## 1. Thông tin thành viên

- Họ tên: Chu Quang Linh.
- MSSV: 2A202603809.
- Email: quanglinh1286@gmail.com (theo cấu hình Git hiện tại).
- GitHub: [ArsNeonci](https://github.com/ArsNeonci) (theo remote repo hiện tại).
- Vai trò: leader kiêm phụ trách C: Orchestrator (thành viên 4).

## 2. Phần việc phụ trách

### Bonus B3 — Verifier và tích hợp (leader)

- Phụ trách rà `src/bonus/swarm_verified.py`: đọc lại order theo principal, đối chiếu mọi `ORDER_FIELDS`, quote lại tối đa một lần khi sai, kiểm tra trước cả nhánh quote 0 và trước `issue_refund`.
- Kiểm tra allowlist/trace, không ghi ticket hoặc PII, tính đủ chi phí lookup và quote sửa; giữ nguyên host và reference Swarm.
- Đối chiếu `test_overstated_ticket_is_fixed_before_any_refund` và `test_ticket_canary_never_enters_output_or_trace` trong `src/tests/test_bonus_swarm_verified.py`; phối hợp tích hợp phần rà soát của các thành viên.
- Bàn giao: chốt code, kết quả test chung, an toàn và giới hạn của verifier; phối hợp Quân hoàn thiện báo cáo.

Commit triển khai bonus chung `1be14a8` được tạo trong phiên hỗ trợ Codex; đã chạy 62 test bonus, 162 test mặc định, 248 test student và kiểm tra hồ sơ 0 FAIL. Không gán các kết quả chạy bằng công cụ thành bằng chứng thành viên tự chạy ngoài phiên. Câu cần giải thích: verifier tin order/policy và tool nào, và vì sao không phát hiện được lỗi nội tại của DB/quote khi các dữ kiện vẫn khớp?

### Phần bài chính

Bàn giao kiến trúc C độc lập trên bản starter: orchestrator nhận claim, giao điều tra qua handoff đã lọc, nhận báo cáo từ investigator chỉ đọc, rồi gọi host để xử lý refund. Kèm test an toàn, mô tả kỹ thuật và bằng chứng chạy lại.

Theo phân công cập nhật, kiêm leader: điều phối tích hợp các nhánh, kiểm tra xung đột và test chung, chủ trì chọn kiến trúc/chốt commit, phối hợp thành viên 5 tổng hợp báo cáo và chuẩn bị bài nộp.

## 3. Đóng góp cụ thể

- Commit kỹ thuật: `a42312c` — `feat(orchestrator): isolate member 4 shape and safety tests`.
- Tích hợp nhánh Orchestrator, Single và Workflow qua các merge `3f43b87`, `9ec463a`, `a0003e4`; không merge develop. Tại `a0003e4`, kiểm chứng chung trong phiên hỗ trợ đạt 90 test mặc định và 248 test student pass. Đây là phần tích hợp có bằng chứng, không phải khai nhận tự viết code của các thành viên khác.
- Tiếp nhận code Orchestrator và test từ bản draft chung `f9a6c80` trên `develop`; tách phần này sang `main` trên nền starter `034c6c4`. Đây là phần được tiếp nhận và hoàn thiện với trợ giúp AI, không khai nhận toàn bộ bản draft là do cá nhân tự viết.
- Loại tham số và vòng lặp dành cho ablation nhiều investigator; bản bàn giao giữ một investigator, bốn tool đọc và một nơi gọi host ghi tiền.
- Dùng `make_handoff` với `facts={}` và allowlist tool đọc; không chuyển ticket, parent context hoặc secret vào payload investigator.
- Truyền quote đầy đủ vào `durability.issue_refund`, giữ `crash_at`, flush trace rồi ném lại `InjectedCrash` để caller kiểm tra crash/resume.
- Dùng `finish()` ở các nhánh kết quả để ghi trace và lấy bằng chứng refund từ ledger. Đóng connection trong `finally`.
- Bàn giao test `src/tests/test_orchestrator_shape.py`: kiểm handoff, prompt investigator, trace, approval mượn từ claim khác và tính lại quote khi investigator thiếu kết quả.

Chi tiết luồng và ranh giới quyền: [orchestrator_handoff.md](orchestrator_handoff.md).

## 4. Bằng chứng

Các lệnh dưới đây đã chạy lại bằng Python 3.12.6 trên Windows trong phiên hoàn thiện bài, trên code thuộc commit `a42312c`. Chạy từ `src/`, sau khi cài `requirements.txt` và kích hoạt môi trường Python:

```powershell
python -m pytest -q
python -m pytest -q -m student -o addopts= -k orchestrator
```

| Kiểm tra | Kết quả thực tế |
| --- | --- |
| Test mặc định: host và test Orchestrator bổ sung | 63 passed, 248 deselected |
| Ma trận student riêng Orchestrator | 62 passed, 249 deselected |
| `git diff --check` trước commit kỹ thuật | Không báo lỗi |

Các test bàn giao:

- `test_handoff_is_allowlisted_and_read_only` (tham số hóa trên 5 claim).
- `test_investigator_model_never_sees_the_ticket`.
- `test_trace_records_the_sanitized_handoff_not_the_parent`.
- `test_borrowed_approval_is_denied_by_the_host_with_audit`.
- `test_missing_investigator_quote_is_recomputed_by_the_orchestrator`.

Ma trận public của Orchestrator kiểm thêm các trường hợp nghiệp vụ, T11 gọi lại và T12 crash rồi resume. Các kết quả trên không phải điểm hidden, không thay thế benchmark của cả nhóm hoặc crash report bắt buộc.

## 5. Công cụ AI đã dùng

Codex hỗ trợ đọc đề, đánh giá code, trích phần Orchestrator từ draft chung, loại phần ngoài phạm vi, chạy test, lập tài liệu và commit. Bằng chứng kiểm chứng là output test thực tế và commit kỹ thuật đã nêu; không dùng số liệu tự sinh hoặc chép số benchmark của nhánh khác làm kết quả của bản bàn giao.

Để chuẩn bị bảo vệ bài, thành viên cần tự chạy lại các lệnh trên và giải thích luồng claim → handoff → investigator → quote → host; lý do truyền quote đầy đủ; vì sao chỉ host được ghi tiền; vì sao trace không ghi dữ liệu thô. Báo cáo này không khẳng định các bước tự kiểm tra cá nhân đó đã được thực hiện ngoài phiên hỗ trợ.

## 6. Tự đánh giá và giới hạn

Phần triển khai và test kiến trúc C đáp ứng bộ public đã chạy. Bản bàn giao riêng tại `a42312c` chỉ gồm Orchestrator; bản tích hợp tại `a0003e4` đã có cả Workflow và Single. Các số 63/62 ở mục 4 là bằng chứng của bản bàn giao riêng, không phải số test hiện tại của toàn nhóm. Với vai trò leader, còn cần chủ trì quyết định kiến trúc cuối cùng, tạo bộ report chính thức và phối hợp hoàn thiện ADR, research card, hồ sơ nộp cùng thành viên tổng hợp báo cáo.

MockLLM được gọi ở các bước `plan`, `investigate`, `draft`, nhưng output model không quyết định kế hoạch hoặc tool; Python ấn định danh sách tool. Do đó đây là mô phỏng ranh giới orchestrator/investigator, chưa chứng minh năng lực tự điều phối của LLM thật. Latency là `unavailable`; chưa có kết quả hidden chính thức.

Nếu investigator thiếu quote, orchestrator có nhánh tính lại. Nếu investigator trả quote có cấu trúc hợp lệ, code tin kết quả của tool tất định; chưa có verifier độc lập đối chiếu lại toàn bộ dữ kiện quote. Không suy rộng kết quả public thành bảo đảm tuyệt đối trên mọi dữ liệu hoặc LLM thật.
