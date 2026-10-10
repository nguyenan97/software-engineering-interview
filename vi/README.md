---
layout: default
locale: vi
translation_key: repo-guide
title: Hướng dẫn repository
---

# Ôn phỏng vấn Software Engineering

Curriculum dựa trên nguồn cho senior software engineers hướng đến solution architecture. Học quyết định kỹ thuật và giải thích rõ ràng; chọn English hoặc Vietnamese cho bài học, giữ English để luyện câu trả lời phỏng vấn mặc định.

## Bắt đầu mỗi ngày

Mở [trang học hôm nay](index.md), hoặc mở repo trong agent và gửi:

> **Viết bài học hôm nay bằng tiếng Việt.**

[Daily Interview Mastery](../agent/SKILL.md) đọc source prompts, curriculum và learning history; tự chọn mục tiêu mới, kiểm tra claims phụ thuộc version, viết Full lesson và đăng ký generated. Generated chưa phải completion. Không có background job tự tạo bài theo lịch.

| Yêu cầu | Kết quả |
| --- | --- |
| `Viết bài học hôm nay` | Full lesson theo preference đã lưu, mặc định English |
| `Viết bài học hôm nay bằng tiếng Việt` | Bài đầy đủ bằng Vietnamese, có English model answers |
| `Write today’s lesson in English` | Bài English |
| `Chuyển bài đang học sang tiếng Việt` | Cùng lesson ID và cursor, không tạo record mới |
| `Học interactive bằng tiếng Việt` | Hỏi thử thách và chờ attempt trước lời giải |
| `Tiếp tục bài đang học` | Resume session note và lesson ID đã lưu |
| `Ôn tập hôm nay bằng tiếng Việt` | Due retrieval, tách khỏi bài mới |
| `Mock interview bằng English, feedback bằng tiếng Việt` | Hỏi English từng câu, nhận xét từ answers thật |
| `Đánh giá bài làm này và cập nhật tiến độ` | Rubric và bookkeeping dựa trên evidence |

Agent tự chọn topic; explicit topic/language request ưu tiên default. Khi thiếu prerequisite đã hoàn thành, resume hoặc dạy prerequisite, không tự coi bài generated là learned.

## Học ít nhưng chắc

Mỗi bài một mục tiêu, 30–45 phút, ít nhất một nửa active. Theo **A mục tiêu → B dự đoán → C cơ chế → D thực hành → E kiểm chứng/sửa → F nói/nhớ lại**. Lời giải và optional depth thu gọn. Lab có happy path, meaningful failure và transfer ít hints hơn.

Review D+1/3/7/14/30 từ completion thật. Retrieval, spacing, worked examples và explanatory questions có nghiên cứu trong [phương pháp học](agent/INTERVIEW_METHOD.md); lịch cụ thể và domain rotation là lựa chọn curriculum.

Trả lời trực tiếp, giải thích cơ chế bằng ví dụ, nêu trade-off/evidence rồi mới bridge sang chủ đề liên quan. Không có script bảo đảm interviewer hài lòng hoặc ngừng hỏi sâu; không bịa experience, số đo hoặc certainty.

## Hai ngôn ngữ, một lịch sử học

English giữ URL cũ, Vietnamese ở `/vi/`. Hai bản cùng lesson ID/topic ID/fingerprint và một canonical learning record. Có thể đổi ngôn ngữ ở cùng bước; dictionary UI và layouts dùng chung. Source corpus/IDs không bị dịch hoặc tái tạo riêng để tránh mất provenance.

Website tĩnh không tạo bài, đọc state cá nhân hay ghi completion lên GitHub. Ngôn ngữ và vị trí đọc chỉ lưu trong browser. Agent dùng session note và state CLI để lưu bền vững. Thiếu translation có thông báo và mở đúng English content. Có thể đọc và chuyển ngôn ngữ bằng liên kết khi tắt JavaScript.

## Nội dung và cấu trúc

Corpus có 234 numbered prompts, bốn scenario/request-flow sections, tổ chức thành 47 topics thuộc 13 domains. Stable source IDs giữ traceability; những contract khác nhau không bị gộp chỉ vì dùng cùng thuật ngữ.

- [Lộ trình](curriculum/index.md), [taxonomy English](../agent/TOPIC_TAXONOMY.md), [source coverage English](../curriculum/source-coverage.md).
- [Bài đã xuất bản](lessons/index.md) và [bài mẫu atomic inbox](lessons/2026-10-08-messaging-idempotent-consumer.md).
- [Workflow tiến độ](docs/workflow.md) và [cách thêm bản dịch](../docs/localization.md).

`agent/` chứa skill/templates; `curriculum/` catalog dùng chung; `sources/` giữ nguồn đã loại thông tin riêng tư; `lessons/` bài English canonical; `vi/` nội dung Vietnamese; `_data/i18n/` chuỗi UI; `_includes/` và `_layouts/` render chung; `labs/` code thật; `learning/` state/schema; `scripts/` bookkeeping/validation; `tests/` kiểm tra fixture và browser.

Bài mẫu vẫn generated ngày gốc 2026-10-08, chưa có score/completion. SQLite suite đã được chạy trong quá trình chuẩn bị; SQL Server optional chưa có execution evidence. Cả hai bản ghi rõ phạm vi kiểm chứng, không đổi ngày cũ khi dịch.

## Kiểm tra và state

```sh
python -m pip install -r requirements.txt
python scripts/learning.py next --date 2026-10-09 --language vi
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/package_labs.py --check
python scripts/render_lesson_code.py --check
python labs/atomic-inbox/verify.py --solution
```

Thay bằng ngày địa phương. `next` là heuristic, agent phải đối chiếu semantic objectives. State được schema-validate và atomic replacement; dùng một writer, giữ history. Agent không ghi được phải trả proposed patch và nói chưa lưu. Xem [workflow](docs/workflow.md) cho preference, completion, review và private profile.

CI kiểm tra metadata, links, state, translation keys/identity, lab, Jekyll và browser flow cả hai ngôn ngữ. Test dependencies không ship lên website. Screenshots ở artifact CI; Pages deployment vẫn theo `main`.

## Ngôn ngữ, riêng tư, bằng chứng

Giữ thuật ngữ `Dependency Injection`, `ThreadPool`, `Deadlock`, `Idempotency`, `Eventual Consistency` khi giúp hiểu. Vietnamese diễn giải tự nhiên, không lặp cả bài hai lần. Source questions chỉ định framing; official sources xác nhận behavior. Documentation check không phải runtime execution.

Không khôi phục identities hoặc confidential context đã loại bỏ. State/evidence bị loại khỏi Pages nhưng commit public GitHub vẫn công khai. Giữ attempts nhạy cảm ngoài checkout hoặc private profile; không tạo điểm, completion hay experience tưởng tượng.
