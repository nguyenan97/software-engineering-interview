---
layout: default
locale: vi
translation_key: review
title: Ôn mà không nhìn tài liệu
---

# Ôn mà không nhìn tài liệu

Bắt đầu lượt ôn năm phút bằng trí nhớ, chưa đọc lại bài. Agent kiểm tra ngày đến hạn dựa trên completion thật. Trang công khai này không biết bạn đang đến hạn ôn bài nào.

{% include prompt-box.html kind='review' %}

## Thử một lượt ôn

Nếu đã học bài atomic inbox, đóng lời giải và tự giải thích:

1. Hai writes nào phải nằm trong cùng transaction?
2. Worker lỗi sau khi insert marker nhưng trước account update. Database phải còn gì?
3. Update đã commit nhưng acknowledgment bị mất. Điều gì làm redelivery an toàn?

Phát biểu một invariant, vẽ failure timeline và dùng ví dụ khác, chẳng hạn giữ chỗ tồn kho. Sau đó [đối chiếu đáp án](../lessons/2026-10-08-messaging-idempotent-consumer.md#recall).

Thử ở đây không tự tạo một review đã hoàn thành. Lưu bài làm thật và nhờ agent ghi lượt ôn vào đúng lesson ID. Nếu một câu sai, sửa đúng một hiểu lầm rồi thử lại bằng ví dụ mới. Agent có thể dời một lượt chưa ôn sớm hơn khi có evidence và lý do; không được ghi những lần ôn chưa diễn ra.

Đọc bản English hay Vietnamese đều là cùng bài và cùng lịch ôn. Đổi ngôn ngữ không tính là review.

[Về trang học hôm nay](../index.md) · [Workflow tiến độ](../docs/workflow.md)
