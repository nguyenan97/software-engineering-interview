---
layout: default
locale: vi
translation_key: workflow
title: Cách học hằng ngày và lưu tiến độ
---

# Cách học hằng ngày và lưu tiến độ

## Từ yêu cầu đến bài học

1. Gửi **“Viết bài học hôm nay bằng tiếng Việt.”** Agent đọc skill, catalog, nguồn và state hiện tại.
2. Agent đối chiếu objectives của bài đã tạo, đang học và đã hoàn thành; chọn mục tiêu mới hợp lệ và kiểm tra technical claims phụ thuộc phiên bản.
3. Bài 30–45 phút có một mục tiêu và sáu bước được lưu thành hai phiên bản ngôn ngữ; chỉ đăng ký **một** record generated.
4. Nộp code tự sửa, output lab hoặc transcript câu trả lời. Agent nhận xét dựa trên evidence rồi ghi completion thật khi phù hợp.
5. Gửi **“Ôn tập hôm nay bằng tiếng Việt.”** để trả lời câu hỏi đến hạn trước khi xem đáp án.

Full lesson có lời giải đầy đủ trong phần có thể mở. Interactive và Mock interview chờ bạn trả lời. Tiếp tục session dùng lại lesson ID; yêu cầu bài mới không tự hoàn thành phần đang học.

Agent lưu cursor Interactive/Mock ở `learning/sessions/LESSON_ID.md`, hoặc thư mục `sessions/` bên cạnh private profile. Note chứa `step`, câu hỏi chưa trả lời, feedback đã loại thông tin riêng tư và next action. Ngôn ngữ dạy, phỏng vấn, feedback được ghi riêng nếu cần. Đổi ngôn ngữ giữ nguyên lesson ID, câu hỏi và bước; không gọi `start` chỉ vì đổi ngôn ngữ. `start` chỉ đổi status, agent phải lưu note riêng sau mỗi lượt.

## Website và bốn đường vào

[Trang học hôm nay](../index.md) hiển thị các bài đã xuất bản. **Bắt đầu bài này** mở artifact mới nhất, chưa phải gợi ý cá nhân hóa. **Học mới** cho prompt để dán vào agent. **Tiếp tục đọc** dùng browser bookmark; nếu chưa có thì mở bài mới nhất. **Ôn tập** và **Luyện phỏng vấn** cho prompt và một ví dụ luyện; agent đọc state thật để chọn bài.

Website tĩnh không có generation endpoint hoặc GitHub write integration. Sao chép prompt chưa chạy agent. Browser bookmark chỉ chứa lesson ID, đường dẫn, step và timestamp; không chứa bài làm, điểm hoặc completion. Ngôn ngữ được lưu riêng trong trình duyệt; có thể chuyển cùng bài mà không đổi lịch sử học.

English giữ các URL cũ, Vietnamese ở `/vi/`. Chuyển ngôn ngữ giữ fragment của bước đang đọc. Browser ghi nhớ lựa chọn nhưng không tự redirect một URL bạn mở trực tiếp; trang sẽ đề nghị bản đã chọn nếu có. Bản dịch thiếu dẫn tới đúng trang English và có thông báo, không mở một bài khác. Không có JavaScript vẫn đọc, chuyển trang bằng liên kết và mở lời giải được; nếu storage/clipboard bị chặn thì chọn prompt và sao chép thủ công.

Muốn resume bền vững, gửi **“Tiếp tục bài đang học.”** cho agent. Click bước hoặc ngôn ngữ không bắt đầu/hoàn thành bài. Cần bài làm thật để ghi tiến độ.

## Commands thật trong repo

Cài dependency: `python -m pip install -r requirements.txt`. Thay ngày ví dụ bằng ngày địa phương của bạn; profile hiện dùng Asia/Bangkok.

```sh
python scripts/learning.py next --date 2026-10-09 --language vi
python scripts/learning.py lesson-path 2026-10-08-messaging-idempotent-consumer --date 2026-10-09 --language vi
```

`next` và `lesson-path` chỉ đọc, không ghi trạng thái. Record lưu canonical path English và dùng metadata của bài logic. Bài mẫu đã đăng ký; không chạy `record` lần nữa chỉ để có bản dịch.

```sh
python scripts/learning.py record --lesson lessons/2026-10-08-messaging-idempotent-consumer.md --date 2026-10-08
python scripts/learning.py start 2026-10-08-messaging-idempotent-consumer --date 2026-10-09
```

Dòng `record` trên là ví dụ, với bài mẫu hiện có sẽ bị từ chối là trùng. Với bài mới, lưu cả hai phiên bản rồi đăng ký canonical một lần. Có thể đưa đường dẫn bản dịch cho `record`; CLI sẽ resolve về canonical và vẫn không cho tạo record thứ hai.

Chỉ chạy các commands sau khi đã có bài làm thật:

```sh
python scripts/learning.py complete 2026-10-08-messaging-idempotent-consumer --date 2026-10-09 --evidence /path/to/learner-attempt.md
python scripts/learning.py review 2026-10-08-messaging-idempotent-consumer --date 2026-10-10 --evidence /path/to/retrieval-attempt.md
```

Completion/review cần evidence file tồn tại, không rỗng. `--assessment /path/to/assessment.json` tùy chọn chứa năm dimension và weak points. CLI kiểm tra cấu trúc; agent đọc nội dung để đánh giá. Chưa quan sát thì `null`; `0` là kết quả đã chấm, không phải thiếu dữ liệu.

## Ngôn ngữ cá nhân trong state

Nếu muốn agent mặc định dạy bằng Vietnamese ở các lần sau, yêu cầu agent lưu preference hoặc chạy:

```sh
python scripts/learning.py language --language vi --date 2026-10-09
```

Command này chỉ cập nhật `learner_profile.preferred_language` và ngày update; không đổi lesson status, score, evidence hoặc reviews. Lựa chọn trên website không tự chạy command này. Request explicit ưu tiên hơn preference; thiếu preference thì mặc định English. Phỏng vấn vẫn luyện English, trừ khi bạn yêu cầu khác; feedback có thể bằng Vietnamese.

## Lịch ôn và điều chỉnh

D+1/3/7/14/30 bắt đầu từ completion thật, không phải ngày tạo hay ngày dịch. Generated chưa có lịch ôn. Một bài làm review đáp ứng một due interval; không tự đánh dấu mọi lượt quá hạn hoặc tăng số bài mới.

Sau recall evidence thật, agent có thể đổi một interval **chưa thực hiện** nếu có lý do. Ví dụ dưới đây giả định completion ngày 9 và một review thật ngày 10:

```sh
python scripts/learning.py reschedule 2026-10-08-messaging-idempotent-consumer --date 2026-10-10 --from-date 2026-10-12 --to-date 2026-10-11 --reason "Observed rollback gap; retry sooner" --evidence /path/to/retrieval-attempt.md
```

Audit lưu ngày cũ/mới, ngày điều chỉnh, reason, evidence và `review_count` để giữ thứ tự thao tác cùng ngày. Validator tái dựng plan từ completion không đổi. Không dời lượt đã làm, chọn ngày quá khứ hoặc trùng interval khác. Một review đến sau trên ngày đã tái sử dụng không làm vô hiệu adjustment trước đó. Không có evidence thì giữ lịch mặc định.

## Schema và phục hồi

Xem [schema](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/state.schema.json), [state hiện tại](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/state.json), [state reference](https://github.com/nguyenan97/software-engineering-interview/blob/main/learning/README.md), [empty profile](https://github.com/nguyenan97/software-engineering-interview/blob/main/agent/LEARNING_STATE_TEMPLATE.json).

State không được xuất bản trên Pages. Private profile dùng `--state /path/to/state.json` **trước subcommand** và lưu session notes bên cạnh file đó. Không ghi đè history bằng empty template. State writes dùng atomic replacement, nhưng phải có một writer tại một thời điểm và đọc lại state trước khi ghi. Nếu agent không có quyền lưu, trả patch và note đề xuất, nói rõ **chưa ghi vào repo**; chat không thay thế durable state.

## Riêng tư và kiểm chứng
{: #privacy-and-verification }

State, điểm và attempts commit vào public GitHub repo vẫn công khai dù Pages loại trừ chúng. Giữ evidence nhạy cảm ngoài checkout hoặc dùng private profile. Đường dẫn cũng không nên lộ danh tính. Chỉ dùng ví dụ đã loại thông tin riêng tư.

Sau sửa đổi, chạy `python scripts/validate.py` và `python -m unittest discover -s tests -v`. Xem [các commands kiểm tra](../../docs/verification.md) và [hướng dẫn thêm bản dịch](../../docs/localization.md). CI build site, kiểm tra hai ngôn ngữ và lưu screenshots; deployment vẫn theo workflow `main` hiện có.

[Lộ trình](../curriculum/index.md) · [Bài học](../lessons/index.md) · [Skill của agent](../../agent/SKILL.md)
