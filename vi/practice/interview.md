---
layout: default
locale: vi
translation_key: interview
title: Luyện trả lời phỏng vấn
---

# Luyện trả lời phỏng vấn

Trả lời câu hỏi trước. Giải thích cơ chế, nêu failure case rồi nói điều kiện nào sẽ làm bạn chọn phương án khác.

{% include prompt-box.html kind='interview' %}

## Thử ngay — năm phút

**Câu hỏi:** <span lang="en">“How would you stop a retried message from crediting an account twice?”</span>

1. Nói bằng English trong 30 giây: direct answer → mechanism → boundary.
2. Mở rộng đến 90 giây với một failure timeline cụ thể và cách kiểm chứng.
3. Bảo vệ lập luận: <span lang="en">“Why not save the processed marker in its own transaction?”</span>
4. Bảo vệ giới hạn: <span lang="en">“Does this also guarantee exactly one external payment?”</span>

Sau khi trả lời đầy đủ, có thể mở hướng: <span lang="en">“If the handler also publishes an event, the related boundary is the transactional outbox.”</span> Chuẩn bị giải thích chủ đề đó trước khi đề nghị. Câu hỏi sâu giúp thể hiện reasoning; phương pháp này không hứa tránh được việc bị hỏi sâu.

Chỉ [mở câu trả lời mẫu](../lessons/2026-10-08-messaging-idempotent-consumer.md#recall) sau khi thử. Ghi lời bạn thực sự nói; ví dụ trau chuốt không phải bằng chứng về performance của bạn. Agent feedback bằng Vietnamese, nhưng không đánh đồng độ trôi chảy English với tính đúng của kỹ thuật.

[Về trang học hôm nay](../index.md) · [Phương pháp trả lời](../agent/INTERVIEW_METHOD.md)
