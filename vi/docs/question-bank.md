---
layout: default
title: Cấu trúc bộ câu hỏi
locale: vi
translation_key: question-bank-guide
---

# Cấu trúc bộ câu hỏi

[Bộ câu hỏi](../questions/index.md) diễn giải nguồn trên curriculum hiện có. English và Vietnamese dùng chung danh tính và provenance; trang hiển thị câu hỏi dễ đọc với hướng dẫn thu gọn, chưa phải lời giải kỹ thuật đã xác minh. [Coverage](../questions/coverage.md) cho phép truy ngược từng đơn vị nguồn.

## Mỗi loại dữ liệu có một nơi quản lý

| Dữ liệu | Nơi quản lý chính | Quy tắc |
| --- | --- | --- |
| Câu hỏi phỏng vấn gốc | `sources/*.md` | Giữ nguyên nội dung, IDs, URLs và anchors; không khôi phục bối cảnh riêng tư đã bỏ |
| Domain, group ID, level, prerequisite | `curriculum/catalog.json` | Group ID là topic ID có sẵn; không tạo taxonomy cạnh tranh |
| Inventory và các cặp gộp ý | `_data/question_bank/inventory.json` | Schema 1; đơn vị nguồn, mapping canonical, nguyên văn, mười lý do gộp EN/VI, vai trò/hash tài liệu trước chỉnh sửa |
| Diễn giải từng câu | `_data/question_bank/questions/s01.json` … `s06.json` | Một annotation cho mỗi canonical ID; nội dung EN/VI và phase/order/version flag dùng chung |
| Group cards | `_data/question_bank/groups/s01.json` … `s06.json` | Group/representative IDs dùng chung; mục tiêu, 2–4 năng lực, dẫn nhập, bài production bổ sung và rubric song ngữ |
| Nhãn hiển thị | `_data/question_bank/labels.json` | Nhãn EN/VI tương đương và tên domain, không đổi slugs |
| Trang xuất bản | `questions/`, `vi/questions/` | Sinh từ `scripts/question_bank.py`; sửa data, regenerate rồi commit cả hai bản |
| Tiến độ học | `learning/state.json` hoặc private profile | Lifecycle riêng; công cụ question bank không đọc/ghi tiến độ hoặc suy ra completion |

## Inventory và danh tính

Một đơn vị nguồn có `source_id`, `source_ref` chính xác, `kind` (`numbered` hoặc `source-scenario`), `original`, `group_id`, `original_group_id`, `canonical_id`. Câu canonical có `question_id`, `group_id` chính, toàn bộ `source_ids`/`source_refs`, `kind`, `merge_rationale` nếu gộp và `related_group_ids`. Mỗi ID nguồn được mapping đúng một lần; ID nguồn nhỏ nhất đặt tên câu sau gộp. Alias vẫn là anchor trên cả hai trang ngôn ngữ.

Bốn scenario chưa đánh số nhận IDs biên tập `S02-SC001`, `S03-SC001`, `S04-SC001`, `S06-SC001`. Các bullet là ràng buộc của một scenario, không phải câu hỏi phỏng vấn bổ sung. Phần cấu trúc trả lời của S06 vẫn là lời khuyên. Snapshot 62 file trước chỉnh sửa phân loại hướng dẫn, curriculum, bài generated, templates, labs và ví dụ dùng chung, tránh đếm câu luyện tập phát triển thêm vào coverage nguồn.

`algorithms-department-headcount` là group tập trung đã có cho S03-Q032. Liên kết nguồn cũ tới SQL-relations rộng hơn vẫn hoạt động. `algorithms-collection-reasoning` tiếp tục là thực hành Ring B mở rộng trong catalog 47 topic nên không có group câu nguồn canonical riêng. Các quyết định này đổi đường học, không đổi IDs nguồn hoặc mục tiêu học tập trong catalog.

## Schema diễn giải và mạch câu hỏi

Mỗi câu có `question_id`, `phase`, `order` số nguyên, `version_sensitive` boolean và hai object `en`/`vi` đầy đủ:

- `question`: cách hỏi tự nhiên, tập trung, không đưa sẵn lời giải.
- `explanation`, `intent`, `scope`: điều cần làm rõ, năng lực quan sát được suy luận từ câu hỏi và giả định quan trọng.
- `senior_signals`: hai tiêu chí cụ thể; `pitfalls`: ít nhất một hiểu nhầm hoặc cách trả lời hời hợt liên quan.
- `followups`: một hoặc hai câu hỏi liên quan, được ghi rõ là agent bổ sung.

Phase chính được sắp theo `foundation → mechanism → application → failure → tradeoff → production`, sau đó `order` và ID. Chỉ hiển thị phase có câu nguồn thực tế. Một câu tiêu biểu giới thiệu group trước mạch chi tiết. Rubric gồm `basic`, `senior`, `evidence_missing`; không tự chấm điểm. Tính đúng kỹ thuật của bản dịch và mạch prerequisite cần review nội dung cùng kiểm tra cấu trúc.

Framing nguồn, tiêu chí biên tập và lời giải đã xác minh là ba loại bằng chứng khác nhau. Bộ này chưa đưa ra model answers phụ thuộc phiên bản. Version flags yêu cầu xác định runtime, framework/provider thực tế và kiểm tra tài liệu chính thức khi dạy hoặc trả lời. Bài học sau phải ghi nhận định, phạm vi áp dụng, URL chính thức trực tiếp và ngày kiểm tra thật theo skill; render câu hỏi không tạo ngày xác minh giả.

## Cập nhật và kiểm tra

```sh
python scripts/question_bank.py
python scripts/question_bank.py --check
python scripts/validate.py
python -m unittest discover -s tests -v
python scripts/check_site.py _site
python tests/questions_browser_check.py --site _site --axe work/browser-checks/node_modules/axe-core/axe.min.js
```

Cài requirements hiện có và build Jekyll trước khi kiểm tra site/browser; xem [hướng dẫn kiểm chứng English](../../docs/verification.md). Generator không tải tài liệu và không ghi state. `--check` từ chối coverage thiếu, alias sai, trang cũ chưa regenerate, metadata ngôn ngữ lệch và hash nguồn bị đổi. Thay nguồn cần inventory migration được review và đọc lại nguồn đầy đủ; không chỉ thay hash để vượt kiểm tra.

Regenerate cả khi xuất bản hoặc dịch một bài học: liên kết bài liên quan được suy ra từ metadata bài công khai. Làm mới liên kết không tạo record hoặc completion. Group là mạch nhiều câu có thể học qua nhiều buổi; mỗi bài hằng ngày chỉ chọn một mục tiêu tập trung.

Hằng ngày chọn một câu, tự thử trước khi mở hướng dẫn, giải thích cơ chế, kiểm tra một trường hợp đổi/thất bại, sửa một điểm còn thiếu rồi nói câu trả lời trực tiếp. Khi cần bài đầy đủ, dùng [daily skill](../../agent/SKILL.md). Có trang đã generated hoặc đã review biên tập không chứng minh bạn đã học xong.
