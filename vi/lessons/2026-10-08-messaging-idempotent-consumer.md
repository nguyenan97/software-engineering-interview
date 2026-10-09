---
layout: lesson
locale: vi
translation_key: 2026-10-08-messaging-idempotent-consumer
lesson_id: 2026-10-08-messaging-idempotent-consumer
topic_id: messaging-idempotent-consumer
canonical_lesson: lessons/2026-10-08-messaging-idempotent-consumer.md
title: 'Một transaction: retry khoản cộng tiền an toàn sau lỗi'
description: Sửa lỗi tách commit của inbox và số dư, kiểm chứng rollback bằng lab Python/SQLite và luyện giải thích bằng English.
primary_objective: Đặt inbox marker và thao tác cộng tiền trong cùng một transaction để lần xử lý bị lỗi vẫn có thể retry an toàn.
prerequisites_note: Biết COMMIT và ROLLBACK cơ bản. Lab dùng Python 3.10+ có sqlite3; SQL Server là phần tùy chọn.
translated_at: '2026-10-09'
---

## A · Xác định mục tiêu — 2 phút
{: #goal }

**Sau bài này, bạn có thể sửa một lỗi retry bằng cách commit inbox marker và khoản cộng tiền cùng nhau, rồi chứng minh cách sửa bằng test có chèn lỗi.**

Hãy hình dung một worker cộng tiền vào tài khoản. Nó ghi “đã xử lý event” rồi dừng trước khi cập nhật số dư. Khi event được gửi lại, worker phải còn khả năng cộng khoản tiền đó. **Inbox marker** là bản ghi bền vững đánh dấu một thao tác logic đã được xử lý; marker chỉ hữu ích khi ý nghĩa của nó khớp với business state đã commit.

| Lesson card | Giá trị |
| --- | --- |
| Topic / lesson | `messaging-idempotent-consumer` / `2026-10-08-messaging-idempotent-consumer` |
| Domain / level / ring | Messaging và event-driven systems / senior / A — từ câu hỏi trong nguồn |
| Nguồn gợi ý | [Message queues và background processing, Q024–Q026](../../sources/04-architecture-distributed-systems.md#q024); [tình huống production](../../sources/04-architecture-distributed-systems.md#production-scenario) |
| Lý do chọn | Nguồn hỏi về lỗi xử lý queue. Bài mẫu đã được thu hẹp quanh một invariant của transaction; bản dịch này **không phải bài mới**. |
| Bài chính / mở rộng | 40 phút, trong đó 28 phút làm lab, kiểm chứng và nhớ lại. Concurrency trên SQL Server nằm ở phần tùy chọn. |
| Chế độ | Full lesson: lời giải đầy đủ có thể mở khi cần. Hãy thử trước. |

Bạn đạt mục tiêu khi có thể (1) vẽ đúng transaction boundary, (2) chứng minh lỗi được chèn vào để lại **không marker và không khoản cộng tiền**, (3) giải thích vì sao retry còn hoạt động. Đây là ba cách kiểm tra **một** mục tiêu. Objectives và fingerprint gốc nằm trong bản English canonical để giữ provenance; phần triển khai SQL Server vẫn được giữ bên dưới.

Dùng môi trường dùng thử. Lab Python/SQLite minh họa cùng invariant của transaction mà stack SQL Server cần bảo vệ. Nó **không** mô phỏng broker hoặc kiểm chứng khóa của SQL Server. Nếu chưa hiểu `COMMIT` và `ROLLBACK`, bắt đầu bằng state trace ở C; nhãn senior không chứng minh bạn đã nắm kiến thức nền.

**Tiếp theo:** [Dự đoán trước khi mở đáp án](#predict).
{: .next-step }

## B · Dự đoán trước — 4 phút
{: #predict }

<div class="task-box" markdown="1">

Chưa chạy code. Ghi dự đoán và một lý do cho mỗi câu.

```text
BEGIN
  insert inbox(event-7, account-42, +100 cents)
COMMIT

BEGIN
  update account balance +100
COMMIT
```

1. Worker dừng giữa hai transaction. Số dư và inbox lúc đó chứa gì?
2. Khi retry, worker thấy `event-7` và bỏ qua khoản cộng tiền. Thao tác đó đã thực sự hoàn tất chưa?
3. Chỉ có một event ID duy nhất có sửa được lỗi này không?

**Thử thách:** Sửa transaction boundary mà vẫn giữ deduplication — khả năng nhận ra event đã xử lý. Số dư ban đầu là `0`. Một lần thành công rồi gửi lại cùng event phải cho số dư `100`; lỗi trước business update phải để số dư `0` **và không có inbox row**.

</div>

Không trả lời được ngay là điểm bắt đầu để học, chưa phải điểm số hoặc bằng chứng bạn yếu. Giữ dự đoán để so với output thật.

**Tiếp theo:** [Hiểu invariant](#model).
{: .next-step }

## C · Hiểu cơ chế — 6 phút
{: #model }

**Vấn đề → nguyên nhân.** Retry có thể làm một khoản cộng tiền xảy ra hai lần. Nhưng ghi “đã xử lý” trước khi khoản cộng tiền commit lại tạo lỗi ngược: thao tác thất bại bị bỏ qua mãi. Marker và số dư phản ánh hai trạng thái không khớp nhau.

**Cơ chế.** Đặt marker và business mutation — thay đổi dữ liệu nghiệp vụ — trong **cùng một database transaction**. Invariant của handler này là: marker đã commit đồng nghĩa khoản cộng tiền của event đó đã commit trong cùng transaction.

```text
New event → BEGIN → insert marker → apply credit → COMMIT → Applied
                        │                 │
                        └── failure ──────┴── ROLLBACK → retry may apply

Same event after commit → validate stored business data → AlreadyProcessed
```

Rollback loại bỏ cả hai thay đổi; commit thành công giữ cả hai. Khi cùng identity và business data được gửi lại, marker giúp bỏ qua mutation. Nếu ID cũ được dùng với dữ liệu khác, phải từ chối thay vì coi đó là retry hợp lệ.

| Lần xử lý | Số dư đã commit | Marker đã commit | Lần gửi lại |
| --- | --- | --- | --- |
| Lỗi sau khi insert marker, trước khoản cộng tiền | 0 | Không có | Có thể thực hiện |
| Cộng tiền thành công | 100 | `event-7` | Bỏ qua cùng khoản cộng tiền |
| Cùng ID nhưng đổi amount | Vẫn 100 | Dữ liệu gốc | Từ chối identity bị tái sử dụng sai |

Lab dùng `BEGIN IMMEDIATE`, `COMMIT`, `ROLLBACK` tường minh của SQLite. SQLite cho phép một write transaction tại một thời điểm; bắt đầu transaction có thể thất bại khi writer khác đang hoạt động. Đây là [semantics của SQLite](https://www.sqlite.org/lang_transaction.html), không phải mô hình khóa SQL Server. Verifier Python đặt `isolation_level=None` để điều khiển transaction bằng SQL tường minh ([tài liệu sqlite3 chính thức](https://docs.python.org/3/library/sqlite3.html)). Bản gốc kiểm tra hai tài liệu này ngày 2026-10-09; việc dịch không thay đổi ngày kiểm tra.

**Giới hạn.** Transaction này bảo vệ một database effect. Nó không commit nguyên tử một HTTP call từ xa hoặc broker acknowledgment. Đừng biến invariant thành lời hứa mọi hành động phân tán đều xảy ra exactly once.

**Tự giải thích:** Nếu marker được commit riêng, tại sao một unique event ID vẫn có thể làm mất khoản cộng tiền?

**Tiếp theo:** [Sửa starter và quan sát lỗi](#practice).
{: .next-step }

## D · Thử làm lab — 16 phút
{: #practice }

**Cần có:** Python 3.10+ với `sqlite3` trong standard library. Không cần database server, pip package, dịch vụ mạng hay credentials. Mỗi test dùng một database in-memory mới.

{% include lab-download.html path='/assets/labs/atomic-inbox.zip' %}

Giải nén, vào thư mục `atomic-inbox/`, chạy `python verify.py`. Nếu đang dùng repo checkout, chạy từ root:

```bash
python labs/atomic-inbox/verify.py
```

`exercise.py` là starter cố ý có lỗi; `verify.py` có năm checks; `solution.py` là lời giải tham khảo. Xem [hướng dẫn lab](../../labs/atomic-inbox/README.md) nếu cần chi tiết. Lab files dùng chung cho cả hai ngôn ngữ.

<div class="task-box" markdown="1">

**Nhiệm vụ:** Chỉ sửa `apply_credit` trong `exercise.py`. Giữ signature và hai kết quả `Applied` / `AlreadyProcessed`. Amount là số nguyên cents dương. Từ chối khi cùng event ID nhưng khác account hoặc amount. Nếu khoản cộng tiền không thực hiện được, rollback phải loại bỏ marker. Không đổi test để chấp nhận lỗi.

1. Chạy starter: happy path retry qua, nhưng injected-failure và missing-account thất bại.
2. Sửa boundary; giải thích những thao tác nào phải nằm bên trong.
3. Chạy lại để cả năm test qua. Giữ output thật và dự đoán ban đầu.

**Câu hỏi về bằng chứng:** Test nào phân biệt một transaction đúng với code chỉ chạy đúng happy path?

</div>

<details markdown="1" data-answer>
<summary>Lời giải đầy đủ — mở sau khi tự thử</summary>

{% include lab-code/atomic-inbox-solution.md %}

`BEGIN` đứng trước lookup và cả hai writes. Một `COMMIT` duy nhất làm marker có ý nghĩa. Nếu update thất bại hoặc có exception được chèn vào, `ROLLBACK` khôi phục cả hai bảng. Marker đã tồn tại được so với business data gốc, tránh nhầm ID reuse với retry hợp lệ.

Chạy reference mà không sửa starter:

```bash
python labs/atomic-inbox/verify.py --solution
```

Trong bản ZIP, dùng `python verify.py --solution`. Reference qua test không chứng minh code bạn sửa đã đúng: hãy chạy default command trên starter của bạn nữa.

</details>

### Biến thể ít gợi ý: giữ chỗ tồn kho

Một handler phải giảm stock khả dụng `2` đơn vị cho một reservation ID. Đổi tình huống cộng tiền thành giữ chỗ tồn kho. Thiết kế transaction và test từ chối khi không đủ stock. Khi từ chối, điều gì phải còn retry được? Dành bốn phút cuối cho state trace hoặc code sketch; chưa cần xây database mới.

<details markdown="1" data-answer>
<summary>Hướng dẫn giải biến thể</summary>

Đặt reservation marker và stock decrement trong cùng transaction. Chỉ update nếu stock ít nhất bằng lượng cần giữ chỗ; nếu không có row đủ điều kiện, rollback marker. Lần bị từ chối phải giữ nguyên stock và không có success marker đã commit. Khi có thêm hàng, retry có thể thành công. Replay của reservation đã commit không được giảm stock thêm lần nữa. So với missing-account test: cùng invariant trong tình huống khác.

</details>

**Tiếp theo:** [So dự đoán với checks](#verify).
{: .next-step }

## E · Kiểm chứng và sửa — 6 phút
{: #verify }

| Check | Kết quả kỳ vọng sau khi sửa | Bằng chứng cần xem |
| --- | --- | --- |
| Lần đầu rồi cùng event | `Applied`, sau đó `AlreadyProcessed`; số dư 100, một marker | Return values và cả hai bảng |
| Lỗi ngay sau marker | Số dư 0, không marker; retry thành công | State sau rollback và sau retry |
| Account không tồn tại | Error; không commit marker | Số inbox rows |
| Cùng ID, business data khác | Error; giữ số dư và marker gốc | Account/amount đã lưu và số dư |
| Amount không hợp lệ | Error; không có writes | 0, số âm, boolean, số có phần thập phân |

**Bằng chứng chuẩn bị bài trong bản gốc, ngày 2026-10-09:** reference qua cả năm test; starter nguyên bản thất bại đúng hai rollback tests. Đây là kiểm tra của người chuẩn bị nội dung, **không phải bài làm của bạn**. Suite này chưa kiểm chứng SQL Server runtime, broker, nhiều worker, process termination hoặc unknown commit outcome.

**Một hiểu lầm quan trọng:** “Retry bình thường qua test là handler đã an toàn.” Starter qua đường đó nhưng làm mất khoản cộng tiền sau failure. So dự đoán B với injected-failure output. Nếu bỏ sót marker còn lại, vẽ hai state đã commit và chạy lại tình huống đó; sau đó giải thích tại sao cách sửa thay đổi kết quả. Agent chỉ nhận xét điểm yếu từ bài làm thật.

### Production twist: commit thành công, acknowledgment thất bại

Sau database commit, broker acknowledgment có thể thất bại và message được gửi lại ([Service Bus settlement, V1](https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement)). Đừng hoàn tác khoản cộng tiền chỉ vì acknowledgment lỗi. Identity ổn định giúp retry trả `AlreadyProcessed`. Database timeout hoặc mất response cũng có thể làm client chưa biết commit thành công hay chưa; hãy retry **cùng identity**, đừng tạo thao tác mới.

| Lựa chọn | Khi phù hợp | Chi phí / giới hạn | Kiểm chứng |
| --- | --- | --- | --- |
| Durable inbox và business transaction | Database mutation không tự idempotent có thể bị retry | Thêm writes, lưu lịch sử, contention; không atomic với remote call | Rollback/replay tests; concurrency và recovery tests trong môi trường thật |
| Update tự idempotent | Gán cùng một giá trị mong muốn là an toàn theo ordering của domain | Event cũ có thể ghi đè state mới nếu thiếu kiểm soát thứ tự | Test out-of-order và replay |

Một tập “seen IDs” trong process không sống qua restart và không phối hợp được replicas. SQL Server locks, concurrent callers và acknowledgment contract cần kiểm chứng thêm ở phần tùy chọn. Những checks portable chỉ chứng minh invariant trong môi trường đã nêu.

Trong production, theo dõi applied/replayed outcomes, identity conflicts và transaction failures. Dùng event identity đã loại thông tin nhạy cảm để đối chiếu inbox với business state. Replay tăng cho thấy nhiều lần thử xử lý hơn, chưa tự chứng minh có khoản cộng tiền trùng. Đo contention trước khi đổi thiết kế.

**Tiếp theo:** [Đóng lời giải và giải thích từ trí nhớ](#recall).
{: .next-step }

## F · Nói lại và nhớ lại — 6 phút
{: #recall }

**Câu hỏi phỏng vấn:** <span lang="en">“How would you stop a retried account-credit event from changing the balance twice?”</span>

**Điều có thể được đánh giá:** Bạn có giải thích được durable invariant, partial failure và phạm vi bảo đảm không? Đây là suy luận từ câu hỏi, không phải rubric chung của mọi interviewer.

Tự nói câu trả lời 30 giây, rồi mở rộng đến 90 giây với một failure timeline, trade-off và test cần chạy. Đo thời gian nói thật. Câu trả lời mẫu giữ English để luyện phỏng vấn; phần hướng dẫn dưới đây giải thích lập luận bằng Vietnamese.

<details markdown="1" data-answer>
<summary>Câu trả lời mẫu 30 giây bằng English</summary>
<div lang="en" markdown="1">

{% include interview/inbox-30s.md %}

</div>

Lập luận có bốn bước: stable ID → commit marker và credit cùng nhau → rollback để retry còn hợp lệ → giới hạn ở database effect. Không cần kể mọi chi tiết implementation ngay trong câu đầu.

</details>

<details markdown="1" data-answer>
<summary>Câu trả lời 90 giây, hai follow-ups và hướng mở chủ đề</summary>
<div lang="en" markdown="1">

{% include interview/inbox-90s.md %}

</div>

Câu dài bổ sung hai failure windows, một test phân biệt đúng/sai, chi phí lưu inbox và giới hạn của bằng chứng SQLite. “I would” và “in this lab” phân biệt kế hoạch kiểm chứng với kinh nghiệm production chưa được cung cấp.

**Follow-up 1:** <span lang="en">“Why is a unique event ID insufficient?”</span> — Nó ngăn marker trùng, nhưng không làm credit atomic với marker. Starter có thể commit marker mà chưa cộng tiền.

**Follow-up 2:** <span lang="en">“What if a timeout happens during commit?”</span> — Mất response chưa chứng minh rollback. Retry cùng ID: marker đã commit thì bỏ qua; chưa có marker đã commit thì có thể thử xử lý. Recovery của connection và retry policy vẫn cần runtime tests.

**Hướng mở, sau khi đã trả lời đủ:** <span lang="en">“If this handler also needs to publish an event, the next question is coordinating that publication through an outbox.”</span> Phải sẵn sàng giải thích giới hạn: outbox ghi publication intent trong database transaction; publisher vẫn có thể retry, nên downstream idempotency còn quan trọng. Trả lời follow-up trực tiếp trước; hướng mở này không bảo đảm interviewer sẽ ngừng hỏi sâu.

</details>

{% include recall-close.html %}

1. Phát biểu invariant liên kết inbox row với khoản cộng tiền.
2. Reservation thất bại vì không đủ stock. Transaction phải để lại gì, và vì sao?
3. Commit thành công nhưng acknowledgment bị mất. Vì sao vẫn cần stable identity?

<details markdown="1" data-answer>
<summary>Đáp án retrieval — mở sau khi trả lời</summary>

1. Marker đã commit đồng nghĩa khoản cộng tiền của event đó đã commit trong cùng transaction.
2. Không success marker, stock không đổi; nếu không, retry có thể bỏ qua reservation chưa từng thành công.
3. Redelivery phải nhận ra cùng thao tác logic để bỏ qua effect đã commit.

</details>

### Bài làm, feedback và phiên sau

Lưu function bạn sửa, test output thật, dự đoán đã sửa và transcript câu trả lời (hoặc một bài viết ngắn). Gửi agent: **“Đánh giá bài làm này; sửa một hiểu lầm rồi cho tôi thử lại.”** Đọc bài hoặc chạy reference chưa phải tín hiệu hoàn thành.

| Rubric | Bằng chứng | Điểm khi cung cấp bài |
| --- | --- | --- |
| Technical | Invariant và phạm vi đúng | `null` |
| Reasoning | Giải thích lỗi hai commits và so sánh lựa chọn khác | `null` |
| Implementation | Code tự sửa và failure test có ý nghĩa | `null` |
| Operations | Retry sau failure và commit/ack gap | `null` |
| Communication | Trả lời thẳng trong 30–90 giây, bảo vệ follow-ups | `null` |

Chỉ dùng [rubric 0–4](../agent/INTERVIEW_METHOD.md#evidence-based-feedback) cho phần đã quan sát được, rồi thử lại điểm còn thiếu. Completion là một phiên có bài làm, không phải chứng nhận đã thành thạo.

Record vẫn là `generated`, tạo ngày `2026-10-08`, `completed_at: null`, mọi điểm null, chưa có evidence hoặc review dates. Refactor và bản dịch ngày `2026-10-09` giữ nguyên lịch sử này. Hai ngôn ngữ có cùng lesson ID; chuyển ngôn ngữ không tạo bài mới. Agent lưu bài làm/cursor; website chỉ lưu lựa chọn ngôn ngữ và vị trí đọc trong trình duyệt. Xem [workflow thật](../docs/workflow.md).

Sau completion có evidence, ôn tại **D+1, D+3, D+7, D+14, D+30**. Dùng một account hoặc inventory example khác, trả lời trước khi mở notes. Agent có thể điều chỉnh lượt chưa ôn dựa trên evidence và lý do; không được ghi review chưa diễn ra. **Tiếp theo:** gửi bài làm hoặc [bắt đầu ôn cùng agent](../practice/review.md).

## Phần mở rộng — ngoài 40 phút

<details markdown="1" data-answer>
<summary>SQL Server: durable uniqueness và concurrent callers</summary>

Phần triển khai gốc được giữ cho stack SQL Server và objectives ban đầu. Cần instance SQL Server dùng thử được hỗ trợ và test bổ sung; **chưa được chạy trong môi trường chuẩn bị bài**. SQLite tests không kiểm chứng các locks này. Trong production, scope inbox identity theo consumer contract và giữ marker cho replay horizon được hỗ trợ.

### Tạo database tables

Dùng database mới có thể bỏ đi. `CREATE OR ALTER PROCEDURE` cần bản SQL Server hỗ trợ cú pháp này. Dùng SSMS hoặc client hiểu `GO`; `GO` là batch separator của client, không phải SQL gửi qua database command.

{% include lab-code/sql-server-setup.md %}

Composite primary key tạo durable uniqueness boundary. Unique constraint cũng có thể biểu đạt quy tắc duy nhất của domain và tạo unique index tương ứng [V4].

### Stored procedure đầy đủ

{% include lab-code/sql-server-procedure.md %}

**Call contract:** gọi bằng command độc lập, không có caller transaction hoặc ambient `TransactionScope`, và tắt implicit transactions. `COMMIT` bên trong không commit transaction bên ngoài [V6]; acknowledgment trước outer commit thật sẽ sai. Guard từ chối caller không được hỗ trợ. Đây không phải procedure dùng savepoint để chạy trong transaction có sẵn. Kiểm tra amount scale ở ingress: chuyển sang `decimal(19,2)` có thể làm tròn phần thập phân trước khi procedure so sánh.

`HOLDLOCK` có semantics `SERIALIZABLE`; `UPDLOCK` giữ update locks đến cuối transaction [V3]. Indexed key cho phép bảo vệ key range khi row chưa có. Lock granularity có thể rộng hơn tùy plan và workload; đừng nói mọi lần chạy chỉ khóa đúng một row khi chưa đo.

Primary key vẫn là uniqueness boundary bền vững. Transaction gắn nó với mutation. Account không có hoặc update lỗi thì inbox insert rollback. `THROW` tuân theo `XACT_ABORT`; xử lý transaction state rõ ràng bảo vệ rollback cho catchable failures [V5]. Mất connection vẫn là unknown outcome, chưa phải bằng chứng rollback.

Test bổ sung cần có: concurrent identical callers chỉ apply một lần; conflicting payload dưới cùng ID bị từ chối; missing account rollback marker; replay sau crash sau commit không cộng thêm. Test deadlocks/transient retries với cùng identity. Timeout chưa xác định outcome; tránh remote calls khi đang giữ transaction.

Với Service Bus worker, chỉ complete broker message sau database commit thật. Source .NET đã kiểm tra hỗ trợ `AutoCompleteMessages = false` [V7]; không vừa manual complete vừa dựa vào automatic completion. Giữ business identity ổn định. Broker duplicate detection có time window và scope riêng [V2], không thay thế atomic consumer effects.

</details>

<details markdown="1">
<summary>Provenance và ngày kiểm chứng</summary>

Nguồn là câu hỏi phỏng vấn, chưa phải lời giải xác minh: [Q024](../../sources/04-architecture-distributed-systems.md#q024), [Q025](../../sources/04-architecture-distributed-systems.md#q025), [Q026](../../sources/04-architecture-distributed-systems.md#q026), [background processing](../../sources/02-aspnet-api-ef.md#background-processing), [large-file scenario](../../sources/02-aspnet-api-ef.md#large-file-processing-scenario).

Bản gốc kiểm tra SQLite/Python ngày **2026-10-09**: [SQLite](https://www.sqlite.org/lang_transaction.html) mô tả explicit transaction và single-writer boundary; [Python sqlite3](https://docs.python.org/3/library/sqlite3.html) mô tả `isolation_level=None`. Lab cần Python 3.10+ có sqlite3, không dùng constructor option `autocommit` mới hơn. Năm runtime checks ở E chỉ là bằng chứng cho lab portable.

Các kiểm tra Microsoft giữ ngày **2026-10-08**. Người chuẩn bị bản gốc đã đọc source chính thức của MicrosoftDocs trên GitHub; dưới đây là documentation verification, không phải execution.

| ID | Nhận định đã kiểm tra trong bản gốc | Tài liệu đọc | Source chính thức |
| --- | --- | --- | --- |
| V1 | Peek-Lock completion/lock operations có thể thất bại; công việc đã xử lý có thể redeliver | [Settlement](https://learn.microsoft.com/en-us/azure/service-bus-messaging/message-transfers-locks-settlement) | [MicrosoftDocs](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/service-bus-messaging/message-transfers-locks-settlement.md) |
| V2 | Broker duplicate detection theo dõi submitted message identity trong time window cấu hình; partitioning ảnh hưởng identity | [Duplicate detection](https://learn.microsoft.com/en-us/azure/service-bus-messaging/duplicate-detection) | [MicrosoftDocs](https://github.com/MicrosoftDocs/azure-docs/blob/main/articles/service-bus-messaging/duplicate-detection.md) |
| V3 | `HOLDLOCK` tương đương `SERIALIZABLE`; `UPDLOCK` giữ update locks đến cuối transaction | [Table hints](https://learn.microsoft.com/en-us/sql/t-sql/queries/hints-transact-sql-table) | [MicrosoftDocs](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/queries/hints-transact-sql-table.md) |
| V4 | Unique constraint ngăn giá trị trùng và tạo unique index tương ứng | [Unique constraints](https://learn.microsoft.com/en-us/sql/relational-databases/tables/create-unique-constraints) | [MicrosoftDocs](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/relational-databases/tables/create-unique-constraints.md) |
| V5 | `THROW` tuân theo `SET XACT_ABORT`; runtime và compile errors được xử lý khác nhau | [XACT_ABORT](https://learn.microsoft.com/en-us/sql/t-sql/statements/set-xact-abort-transact-sql) | [MicrosoftDocs](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/statements/set-xact-abort-transact-sql.md) |
| V6 | Nested `COMMIT` chỉ giảm `@@TRANCOUNT`; outer commit quyết định tính bền vững | [COMMIT](https://learn.microsoft.com/en-us/sql/t-sql/language-elements/commit-transaction-transact-sql) | [MicrosoftDocs](https://github.com/MicrosoftDocs/sql-docs/blob/live/docs/t-sql/language-elements/commit-transaction-transact-sql.md) |
| V7 | .NET Service Bus processor cấu hình được automatic completion qua `AutoCompleteMessages`, mặc định true trong source đã đọc | [Official SDK source](https://github.com/Azure/azure-sdk-for-net/blob/main/sdk/servicebus/Azure.Messaging.ServiceBus/src/Processor/ServiceBusProcessorOptions.cs) | Cùng source chính thức |

SQL Server execution vẫn chưa được xác minh vì môi trường chặn tải container image. Bản dịch không đổi ngày kiểm tra cũ. Đọc documentation và chạy runtime là hai loại bằng chứng khác nhau.

</details>
