---
layout: default
locale: vi
translation_key: curriculum
title: Lộ trình ôn phỏng vấn hằng ngày
---

# Lộ trình ôn phỏng vấn hằng ngày

Lộ trình dựa trên nguồn phỏng vấn Software Engineering. Catalog là chỉ mục câu hỏi; bài học giải thích và kiểm chứng lời giải. Một chủ đề catalog có thể rộng: agent thu hẹp một mục tiêu thực hành cho phiên 30–45 phút.

[Skill](../../agent/SKILL.md) · [Taxonomy](../../agent/TOPIC_TAXONOMY.md) · [Source coverage và gaps](../../curriculum/source-coverage.md) · [Catalog dùng chung](../../curriculum/catalog.json)

## Chọn bài phù hợp

Agent đọc history trước khi chọn: ưu tiên mục tiêu chưa học có câu hỏi trong nguồn, kiểm tra prerequisite, luân phiên domain khi hợp lý và chọn lab đủ nhỏ. Bài đã tạo vẫn có thể đọc; completion/review chỉ dựa trên evidence. Bản dịch không là một topic mới.

Foundation xây mental model; senior áp dụng vào failure, concurrency và evidence; architect xét system boundaries và vận hành. Level độc lập với source ring:

- **A:** câu hỏi/tình huống có trực tiếp trong corpus.
- **B:** thực hành hoặc kiến thức hỗ trợ cho câu hỏi có trong nguồn.
- **C:** mở rộng kiến trúc từ nguồn, thêm phạm vi hệ thống.

Catalog hiện có 47 topics. Ring A vẫn có thể ở mức architect nếu câu hỏi nguồn vốn thuộc mức đó.

## Các domain

Các route chuyên sâu và nguồn chưa dịch đầy đủ vẫn mở đúng bản English, có thông báo rõ; không tạo trang Vietnamese rỗng.

| Domain | Foundation | Senior | Architect | Nguồn |
| --- | ---: | ---: | ---: | --- |
| [Kiến trúc và hệ thống phân tán](../../curriculum/domains/architecture-distributed.md) | 0 | 4 | 2 | 01, 04, 05 |
| [C# và .NET Runtime](../../curriculum/domains/dotnet-runtime.md) | 4 | 4 | 0 | 01 |
| [ASP.NET Core và API](../../curriculum/domains/aspnet-api.md) | 2 | 2 | 0 | 02, 04, 05 |
| [EF Core và LINQ](../../curriculum/domains/ef-linq.md) | 1 | 2 | 0 | 01, 02 |
| [SQL Server và dữ liệu](../../curriculum/domains/sql-data.md) | 2 | 3 | 0 | 02, 03 |
| [Messaging và event-driven systems](../../curriculum/domains/messaging-event-driven.md) | 1 | 2 | 1 | 04, 05 |
| [Azure và cloud architecture](../../curriculum/domains/azure-cloud.md) | 0 | 1 | 1 | 05 |
| [Security và identity](../../curriculum/domains/security-identity.md) | 1 | 1 | 1 | 05 |
| [Observability, performance, reliability](../../curriculum/domains/observability-reliability.md) | 0 | 2 | 0 | 01, 04, 05, 06 |
| [DevOps, containers, delivery](../../curriculum/domains/devops-delivery.md) | 1 | 1 | 0 | 05 |
| [Angular, TypeScript và frontend](../../curriculum/domains/frontend-typescript.md) | 1 | 2 | 0 | 06 |
| [Algorithms, coding, debugging](../../curriculum/domains/algorithms-debugging.md) | 3 | 0 | 0 | 01, 03 |
| [Quy trình và giao tiếp kỹ thuật](../../curriculum/domains/engineering-communication.md) | 0 | 2 | 0 | 04, 06 |

## Phạm vi nguồn và lời giải

Source files giữ câu hỏi đã chuẩn hóa, constraints và hướng dẫn cấu trúc trả lời. Chúng không chứng nhận một technical solution. Source IDs/anchors ổn định; grouping chỉ sắp xếp learning route, vẫn giữ những khác biệt có ý nghĩa.

Mỗi bài phân biệt source framing, official-documentation verification và lab assumptions. Không khôi phục danh tính, employer hoặc context riêng tư đã bị xóa. Claims về runtime/framework/database/broker/browser phụ thuộc version phải kiểm tra tài liệu chính thức khi tạo bài.

## Catalog contract

`catalog.json` có `schema_version: 1` và `topics`: stable topic ID, title, domain, level, ring, 2–4 objectives, 3–7 fingerprint concepts, source refs và prerequisite topic IDs. Metadata này dùng chung bằng English; không dịch IDs hoặc đổi objective chỉ để có phiên bản Vietnamese.

Fingerprint chung là gợi ý cần đối chiếu objectives, chưa chứng minh trùng bài. API request idempotency và atomic consumer processing có contract và failure window khác nhau.

## Một số nhánh bắt đầu

- Request pipeline → background jobs → idempotent import submission.
- LINQ execution → loading performance hoặc DbContext concurrency.
- Index design → query optimization dựa trên evidence.
- Delivery/recovery → idempotent consumer → outbox → distributed compensation.
- Token lifecycle → service identity; TypeScript semantics → Angular hoặc HTTP interceptors.

Topic idempotent consumer không có catalog prerequisite để bài mẫu tự đủ kiến thức bắt đầu; phần dự đoán/model giới thiệu transaction và delivery assumptions cần thiết.
