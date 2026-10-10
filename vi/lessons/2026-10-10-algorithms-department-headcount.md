---
layout: lesson
locale: vi
translation_key: 2026-10-10-algorithms-department-headcount
lesson_id: 2026-10-10-algorithms-department-headcount
topic_id: algorithms-department-headcount
canonical_lesson: lessons/2026-10-10-algorithms-department-headcount.md
title: Đếm đúng nhân viên, không đếm nhầm dòng sau JOIN
primary_objective: Viết và kiểm chứng truy vấn đếm đúng nhân viên, với mỗi dòng kết
  quả đại diện cho một phòng ban.
prerequisites_note: Biết bảng và SELECT cơ bản. JOIN, nhóm và NULL được giải thích
  trong bài. Lab cần Python 3.10+ có sqlite3; SQL Server là tùy chọn.
translated_at: '2026-10-10'
---

## A · Chốt mục tiêu — 2 phút
{: #goal }

**Một mục tiêu:** viết và kiểm chứng truy vấn đếm đúng nhân viên theo từng phòng ban. Một số tổng trên dashboard chỉ đáng tin khi mỗi dòng kết quả đại diện đúng thực thể và biểu thức đếm đúng thứ cần đếm.

| Lesson card | Nội dung |
| --- | --- |
| Topic / lesson | `algorithms-department-headcount` / `2026-10-10-algorithms-department-headcount` |
| Domain / level / ring | Algorithms, coding và debugging / foundation / A |
| Câu hỏi nguồn | [S03-Q032: tìm phòng ban có hơn ba nhân viên](../../sources/03-sql-data-performance.md#q032) |
| Lý do chọn | Mục tiêu nền tảng mới từ câu hỏi nguồn, không có prerequisite trong catalog; luân phiên domain sau messaging. Tách một phần nhỏ của chủ đề SQL rộng để học trong một buổi. |
| Đối chiếu bài cũ | Đã so sánh objectives, fingerprint và nội dung với toàn bộ lịch sử: hiện chỉ có `messaging-idempotent-consumer`. Đếm nhóm khác mục tiêu xử lý inbox nguyên tử. Bài cũ vẫn `generated`; cùng dùng SQL không chứng minh bạn đã học xong. |
| Chế độ / thời lượng | Full lesson; 40 phút: A 2, B 4, C 6, D 16, E 6, F 6. D–F có 28 phút thực hành, kiểm chứng và nhớ lại. |

Ba tiêu chí phục vụ cùng mục tiêu: không gộp phòng ban trùng tên; đếm cả nhân viên thiếu tên và giữ số 0 khi yêu cầu báo cáo cần; kiểm chứng các biên 0/3/4 và tên `NULL`. Hiện chưa có review đến hạn. Chỉ cần học một bản ngôn ngữ.

**Giả định:** mỗi nhân viên thuộc một phòng ban; ID nhân viên duy nhất và không `NULL`; tên phòng ban có thể trùng. Câu hỏi nguồn đếm **tất cả** nhân viên. Báo cáo nhân viên active và phòng ban có số 0 bên dưới là bài tập chuyển giao, không phải câu hỏi bổ sung trong nguồn.

**Tiếp theo:** [Dự đoán kết quả](#predict).

## B · Dự đoán trước — 4 phút
{: #predict }

<div class="task-box" markdown="1">

Viết dự đoán trước khi chạy hoặc mở lời giải.

| DepartmentId | Name | Số nhân viên | Số tên nhân viên khác NULL |
| --- | --- | ---: | ---: |
| 10 | Platform | 4 | 3 |
| 20 | Platform | 3 | 3 |
| 30 | Support | 0 | 0 |

Truy vấn ban đầu:

{% include lab-code/department-headcount-exercise.md %}

1. Truy vấn trả những dòng nào, số đếm bao nhiêu? Vì sao?
2. “Hơn ba” có bao gồm phòng ban có đúng ba nhân viên không?
3. Nếu đổi sang nhóm theo ID nhưng giữ `COUNT(e.Name)`, phòng ban 10 đã đúng chưa?

**Thử thách thực tế:** sửa truy vấn để trả `(DepartmentId, Name, EmployeeCount)`, sắp xếp theo ID; với dữ liệu trên, kết quả phải **chỉ có** `(10, 'Platform', 4)`. Giữ dự đoán để đối chiếu ở E.

</div>

**Tiếp theo:** [Hiểu cơ chế](#model).

## C · Hiểu cơ chế — 6 phút
{: #model }

Hãy hình dung `GROUP BY` chia những dòng đã JOIN vào các giỏ có nhãn. **Aggregation grain** là thứ một giỏ đại diện: ở đây là một ID phòng ban. Nhãn hiển thị không phải danh tính; hai phòng ban cùng tên vẫn phải ở hai giỏ khác nhau. Hình ảnh này giải thích việc nhóm, không mô tả execution plan vật lý của database.

JOIN ghép dòng nhân viên với phòng ban tương ứng. INNER JOIN giữ những dòng ghép được. LEFT JOIN còn giữ phòng ban không ghép được, bằng một dòng có các cột phía nhân viên là `NULL`. `NULL` biểu thị thiếu/chưa biết, không phải số 0.

| DepartmentId sau JOIN | EmployeeId | Tên nhân viên |
| --- | --- | --- |
| 10 | 101 | A |
| 10 | 102 | B |
| 10 | 103 | C |
| 10 | 104 | NULL |
| 20 | 201 / 202 / 203 | D / E / F — ba dòng riêng biệt |
| 30 | NULL | NULL — một dòng giữ chỗ của LEFT JOIN |

Dòng phòng ban 20 được viết gọn, thực tế là ba dòng sau JOIN. Dòng giữ chỗ của phòng ban 30 biểu thị “có phòng ban, chưa có nhân viên”; nó không phải một người.

| Biểu thức trong từng nhóm phòng ban | Phòng ban 10 | Phòng ban 20 | Phòng ban 30 với LEFT JOIN |
| --- | ---: | ---: | ---: |
| `COUNT(*)`: đếm dòng, kể cả dòng chứa NULL | 4 | 3 | 1 |
| `COUNT(e.Name)`: đếm tên khác NULL | 3 | 3 | 0 |
| `COUNT(e.EmployeeId)`: đếm ID nhân viên thực, khác NULL | 4 | 3 | 0 |

**Luồng logic:** ghép dòng (`FROM` / `ON` / `JOIN`) → lọc dòng (`WHERE`, nếu có) → chia nhóm phòng ban (`GROUP BY`) → tính số đếm từng nhóm → giữ nhóm có số đếm > 3 (`HAVING`) → chọn cột (`SELECT`) → sắp xếp (`ORDER BY`). Đây là cách hiểu ý nghĩa truy vấn và phạm vi tên cột, không phải thứ tự chạy vật lý bắt buộc. SQL Server có thể chọn physical plan khác.

Tại sao dùng `HAVING`? `WHERE` chọn từng dòng đầu vào; `HAVING` chọn nhóm sau khi tổng hợp. Với quy tắc binding của SQL Server, viết biểu thức COUNT trong HAVING thay vì alias được tạo ở SELECT. Đưa cả hai cột không tổng hợp cần trả (`DepartmentId`, `Name`) vào GROUP BY để phù hợp cú pháp SQL Server đã đối chiếu.

**Bất biến cần giữ:** mỗi dòng kết quả là một danh tính phòng ban; mỗi ID nhân viên khác NULL được đếm tương ứng một nhân viên thuộc nhóm. Điều này đúng với một phép JOIN một–nhiều trong lab. Nếu JOIN thêm bảng một–nhiều khác, một nhân viên có thể bị nhân dòng; ID khác NULL khi đó chưa đảm bảo đếm mỗi người đúng một lần.

Với điều kiện **> 3**, INNER JOIN đủ: phòng ban không có nhân viên không thể đạt điều kiện. LEFT JOIN cùng `COUNT(e.EmployeeId) > 3` trả cùng các phòng ban đạt điều kiện dưới giả định này. Chọn LEFT JOIN khi hợp đồng báo cáo cần giữ số 0; không kết luận kiểu JOIN nào luôn nhanh hơn.

**Tiếp theo:** [Tự sửa và chạy](#practice).

## D · Thực hành — 16 phút
{: #practice }

**Môi trường:** SQLite trong bộ nhớ qua Python 3.10+; không cần tài khoản, thư viện pip hay database lưu lâu dài. SQL dùng cú pháp phù hợp stack SQL Server của project. Chạy SQLite kiểm chứng kết quả quan hệ của các ví dụ nhỏ; **không** kiểm chứng runtime SQL Server, collation, execution plan, hiệu năng hoặc hành vi cập nhật đồng thời.

{% include lab-download.html path='/assets/labs/department-headcount.zip' %}

Từ thư mục gốc repo, chạy bản ban đầu một lần:

```sh
python labs/department-headcount/verify.py
```

Lệnh cố ý trả exit code khác 0. Chỉ sửa `labs/department-headcount/exercise.sql`, giữ nguyên sáu checks. Nếu tải ZIP: giải nén, vào `department-headcount/`, dùng `python verify.py`.

**Đầu vào:** [setup SQL](../../labs/department-headcount/setup.sql) tạo đúng dữ liệu ở bảng trên. Nhân viên 104 có `Name = NULL`, `IsActive = 0`; sáu người còn lại active. ID 101–104 thuộc phòng ban 10, 201–203 thuộc phòng ban 20. Mỗi check dựng lại dữ liệu riêng.

**Tự làm — 10 phút:** chọn khóa nhóm, biểu thức đếm và điều kiện lọc nhóm; thêm ID vào kết quả và sắp xếp theo ID. Chạy lại. Giải thích thay đổi nào sửa lỗi gộp phòng ban, thay đổi nào sửa đếm thiếu. Không giải bằng cách đổi tên phòng ban hoặc điền tên còn thiếu.

**Câu hỏi về bằng chứng:** kết quả hay test thất bại nào hỗ trợ kết luận của bạn? Giữ truy vấn tự sửa, output, dự đoán ban đầu và một đoạn giải thích.

<details markdown="1" data-answer>
<summary>Lời giải đầy đủ — mở sau khi tự thử</summary>

{% include lab-code/department-headcount-solution.md %}

Nhóm theo danh tính ngăn gộp phòng ban; thêm Name vào GROUP BY để có thể chọn cột đó. `COUNT(e.EmployeeId)` đếm đủ bốn người ở phòng ban 10 dù một tên bị thiếu. `HAVING ... > 3` loại phòng ban 20. INNER JOIN loại phòng ban 30 rỗng; phòng ban này vốn không thể đạt ngưỡng. Câu hỏi nguồn không có điều kiện active.

Sau khi thử, kiểm tra bản tham chiếu:

```sh
python labs/department-headcount/verify.py --solution --extensions
```

Kỳ vọng: sáu core checks đều pass. Kết quả dữ liệu gốc: `(10, 'Platform', 4)`. Bản tham chiếu không phải bài làm của bạn; output của nó là bằng chứng tác giả chạy kiểm tra.

Nếu cần báo cáo mọi phòng ban, bỏ HAVING và giữ cả phòng ban không có nhân viên:

{% include lab-code/department-headcount-all.md %}

Số đếm kỳ vọng: `4 / 3 / 0`. Dùng `COUNT(*)` sẽ cho `4 / 3 / 1`; đây là lỗi đúng/sai thực sự của báo cáo số 0. Với yêu cầu gốc > 3, lỗi này không làm phòng ban rỗng vượt ngưỡng, nên không phóng đại tác động của nó.

</details>

**Biến thể — 6 phút, ít gợi ý hơn:** trả **mọi phòng ban**, đếm **chỉ nhân viên active**, kể cả số 0. Sau đó chuyển toàn bộ nhân viên phòng ban 20 thành inactive. Tự viết truy vấn và dự đoán cả hai kết quả mà không nhìn lại. Yêu cầu báo cáo thay đổi, mục tiêu đếm đúng vẫn giữ nguyên.

<details markdown="1" data-answer>
<summary>Lời giải biến thể và cách kiểm chứng</summary>

{% include lab-code/department-headcount-transfer.md %}

Đặt `e.IsActive = 1` trong ON: giới hạn nhân viên được ghép, đồng thời giữ mọi phòng ban bên trái. Nếu đặt trong WHERE, dòng giữ chỗ NULL bị loại; phòng ban chỉ có nhân viên inactive cũng biến mất. `WHERE e.IsActive = 1 OR e.EmployeeId IS NULL` vẫn không sửa trường hợp chỉ có inactive: nhân viên đã ghép được trước khi lọc, nên không có dòng NULL giữ chỗ để nhánh OR cứu lại.

Ban đầu: `(10, 'Platform', 3)`, `(20, 'Platform', 3)`, `(30, 'Support', 0)`. Sau khi đổi toàn bộ nhân viên ở 20 thành inactive: số đếm `3 / 0 / 0`. Lọc active trong WHERE làm mất phòng ban 20 và phòng ban 30 rỗng. Lệnh kiểm tra extension xác nhận ba tình huống báo cáo bằng các file tham chiếu. Để kiểm tra biến thể tự viết, thay SELECT của transfer trong một bản sao lab dùng thử rồi chạy extension checks; không lấy kết quả bản tham chiếu làm bằng chứng truy vấn của mình đúng.

</details>

**Tiếp theo:** [Đối chiếu bằng chứng](#verify).

## E · Kiểm chứng và sửa — 6 phút
{: #verify }

| Trường hợp | Kết quả kỳ vọng | Bằng chứng quan sát |
| --- | --- | --- |
| Dữ liệu gốc: phòng ban trùng tên, tên nhân viên NULL | Chỉ phòng ban 10, số đếm 4 | Check trùng tên và check tên NULL |
| Mỗi phòng ban có nhân viên đều có đúng ba người | Không có phòng ban đạt điều kiện | Xóa nhân viên 104; check đúng ngưỡng |
| Phòng ban rỗng / xóa mọi nhân viên / cả hai bảng rỗng | Không phòng ban nào đạt điều kiện | Hai checks dữ liệu rỗng |
| Thêm nhân viên 204 vào phòng ban 20 | Hai phòng ban 10 và 20 riêng biệt, mỗi nơi 4 người | Check phòng ban khác vượt ngưỡng |
| Báo cáo mọi phòng ban | Số đếm 4/3/0 | Một extension assertion |
| Báo cáo active, rồi phòng ban 20 chỉ còn inactive | Số đếm 3/3/0, rồi 3/0/0 | Hai extension assertions |

**Đã thực sự chạy ngày 2026-10-10:** `python labs/department-headcount/verify.py` cho **bốn failures, hai passes**; số đếm sau khi gộp tên là 6, và trường hợp chỉ còn phòng ban có tên nhân viên NULL không trả dòng nào. `python labs/department-headcount/verify.py --solution --extensions` pass **sáu core tests và ba extension assertions**, trên SQLite **3.53.1**. Đây là lần chạy của tác giả, không phải bằng chứng bạn hoàn thành. **Chưa chạy SQL Server hoặc đo hiệu năng.** Quy tắc ổn định về COUNT/JOIN/nhóm đã được đối chiếu tài liệu chính thức; không khẳng định hành vi riêng của phiên bản mới.

So với B: bản ban đầu trả `('Platform', 6)` vì gộp hai ID phòng ban và đếm sáu tên khác NULL. Sửa một hiểu nhầm cụ thể: đếm khóa của người, không đếm thuộc tính có thể thiếu. Thử lại bằng cách đổi *mọi* tên nhân viên thành NULL. Báo cáo mọi phòng ban vẫn phải cho số đếm 4/3/0; truy vấn gốc > 3 vẫn chỉ trả phòng ban 10 với số đếm 4. Nếu lệch, quay lại C; chưa gọi đây là điểm yếu của bạn khi chưa có bài làm được gửi.

**Production twist:** API JOIN thêm `EmployeeSkill` một–nhiều để hiển thị kỹ năng. Người có hai kỹ năng xuất hiện hai lần. Chốt grain trước khi tối ưu; xem các ID sau JOIN rồi đối chiếu với số đếm chỉ từ Employee. Đây là tình huống thiết kế, chưa được chạy trong lab.

| Phương án | Khi phù hợp | Trade-off / giới hạn | Kiểm chứng |
| --- | --- | --- | --- |
| Đếm ở truy vấn chỉ có nhân viên; tổng hợp trước JOIN làm nhân dòng | Headcount không phụ thuộc kỹ năng | Thêm query/subquery; JOIN phía sau vẫn phải giữ grain đã chọn | Dữ liệu một người có hai kỹ năng, một người không có kỹ năng |
| `COUNT(DISTINCT e.EmployeeId)` với JOIN giữ đúng tập nhân viên cần đếm | Metric chính xác là số người khác nhau | Khử trùng có thể tốn tài nguyên; DISTINCT không khôi phục người đã bị INNER JOIN hoặc filter loại | Kiểm tra ID thiếu/trùng và tập người; đo plan, logical reads thực tế |

Nếu chỉ cần phòng ban có kỹ năng khớp điều kiện, tập người được chọn thay đổi có chủ đích; hỏi rõ hợp đồng đó trước. Bài này chưa đo lợi thế tốc độ của phương án nào.

**Tiếp theo:** [Đóng ghi chú và nói lại](#recall).

## F · Nói lại và nhớ lại — 6 phút
{: #recall }

**Interview question:** “Given Department and Employee in a one-to-many relationship, return departments having more than three employees.”

**Ý định đánh giá có thể có — đây là suy luận:** chuyển quan hệ dữ liệu thành nhóm đúng, giải thích NULL/ngưỡng, kiểm tra kết quả. Viết truy vấn trước; cấu trúc nói không thay thế SQL chạy đúng.

Tự nói trước rồi mới so sánh. Nhắm 30/90 giây; bấm giờ thực tế, không coi nhãn bên dưới là thời lượng đã đo.

<details markdown="1" data-answer>
<summary>Câu trả lời mẫu 30/90 giây, follow-ups và hướng mở</summary>

**Mẫu hướng tới 30 giây**

<div lang="en" markdown="1">
{% include interview/department-headcount-30s.md %}
</div>

**Mẫu hướng tới 90 giây**

<div lang="en" markdown="1">
{% include interview/department-headcount-90s.md %}
</div>

**Lập luận:** trả lời cách giải ngay, bảo vệ khóa nhóm và biểu thức đếm, rồi đưa biên và kế hoạch kiểm chứng. “I would” không bịa kinh nghiệm production. Câu trả lời senior thêm cách xác nhận và giới hạn hiệu năng rõ ràng, không cần liệt kê nhiều thuật ngữ.

**Follow-up 1:** “Why not COUNT(*)?”

<div lang="en" markdown="1">
“With the inner join in the original task and this one-to-many relationship, COUNT(*) is valid because each matched row is an employee. With a left join that includes empty departments, it counts the placeholder as one. COUNT(e.EmployeeId) remains zero for that placeholder.”
</div>

Lý do: tính đúng/sai phụ thuộc dạng dữ liệu sau JOIN. Không học thuộc “COUNT(*) luôn sai”.

**Follow-up 2:** “Why put the active filter in ON?”

<div lang="en" markdown="1">
“The report must preserve every department. ON restricts which employees match before the left join preserves departments with no qualifying match. WHERE filters joined rows and drops the empty or inactive-only department.”
</div>

Lý do: điều kiện active quyết định người được ghép; hợp đồng vẫn yêu cầu giữ phòng ban không có người đáp ứng.

**Hướng mở, sau khi trả lời đầy đủ:**

<div lang="en" markdown="1">
“That covers correctness at the department grain. If this query is slow on SQL Server, I would next inspect the actual plan and logical reads before choosing an index.”
</div>

Chuẩn bị giới hạn: index bắt đầu bằng `Employee.DepartmentId` là ứng viên cho cách truy cập đó, chưa chắc cải thiện. So sánh workload đại diện và tính cả chi phí ghi. Bài này chưa chạy plan hay benchmark SQL Server. Trả lời follow-up trực tiếp trước khi mở chủ đề; câu trả lời gọn không đảm bảo tránh bị hỏi sâu.

</details>

{% include recall-close.html %}

Không nhìn ghi chú:

1. Vì sao hai phòng ban cùng tên Platform có thể thành một dòng? Sửa thế nào?
2. Ba biểu thức COUNT cho phòng ban rỗng sau LEFT JOIN bằng bao nhiêu? Vì sao?
3. Đếm active nhưng giữ phòng ban chỉ có inactive thế nào? Vì sao WHERE thêm “OR child ID IS NULL” vẫn sai?

<details markdown="1" data-answer>
<summary>Đáp án retrieval — mở sau khi trả lời</summary>

1. Nhóm theo tên hiển thị gộp hai danh tính. Nhóm theo ID phòng ban và tên không tổng hợp cần trả.
2. COUNT(*) = 1, COUNT(tên nhân viên) = 0, COUNT(ID nhân viên) = 0: một dòng giữ chỗ có các cột phía nhân viên NULL, không có thuộc tính nhân viên khác NULL.
3. LEFT JOIN với điều kiện active trong ON, rồi đếm ID nhân viên. Phòng ban chỉ có inactive đã ghép được trước WHERE; không tạo dòng NULL để nhánh OR giữ lại.

</details>

### Bằng chứng, rubric và learning record

Gửi SQL tự viết, output kiểm tra, dự đoán đã sửa và giải thích không nhìn ghi chú. Dùng [rubric dựa trên bằng chứng 0–4](../../agent/INTERVIEW_METHOD.md#evidence-based-feedback): 0 sai cơ chế quan trọng; 1 biết thuật ngữ nhưng cần nhiều trợ giúp; 2 đúng trường hợp cơ bản; 3 xử lý biên và có bằng chứng; 4 tự bảo vệ lựa chọn, phương án khác và failure cases. Chiều chưa quan sát giữ null.

| Chiều đánh giá | Bằng chứng cần có trong bài này | Điểm lúc tạo bài |
| --- | --- | --- |
| Technical | Giải thích đúng grain, COUNT và > 3 | `null` |
| Reasoning | Bảo vệ INNER/LEFT và vị trí điều kiện active | `null` |
| Implementation | Truy vấn tự viết và output ở các biên có ý nghĩa | `null` |
| Operations | Phát hiện nhân dòng, đề xuất cách kiểm tra phân biệt | `null` |
| Communication | Trả lời English trực tiếp, bảo vệ hai follow-ups | `null` |

**Bản đã lưu:** English canonical và Vietnamese hoàn chỉnh dùng chung ID này, objectives trong catalog, fingerprint, code và nguồn. Chỉ đăng ký một record trong `learning/state.json`: `status: generated`, `created_at: 2026-10-10`, `completed_at: null`, cả năm điểm null, `weak_points: []`, `evidence: []`, `review_due: []`. Lịch sử trước giữ nguyên. Mở đáp án hoặc bookmark trình duyệt không cập nhật completion.

**Kế hoạch ôn sau khi hoàn thành có evidence:** D+1 giải thích số đếm từ trí nhớ; D+3 sửa báo cáo active; D+7 đổi sang customer/order; D+14 chẩn đoán JOIN làm nhân dòng; D+30 trả lời và kiểm chứng dữ liệu mới không nhìn ghi chú. D là ngày hoàn thành thực tế, không phải hôm nay. Chưa tạo ngày đến hạn hoặc review event nào.

**Tiếp theo:** gửi bằng chứng bài làm đã bỏ thông tin riêng tư hoặc làm theo [workflow lưu trạng thái](../docs/workflow.md). Completion ghi nhận đã thực hành có bằng chứng, không tự động khẳng định thành thạo.

## Nguồn và ngày đối chiếu

<details markdown="1">
<summary>Provenance, phạm vi và kiểm tra thực tế</summary>

| Nội dung / nguồn ý tưởng | Nguồn | Phạm vi / ngày kiểm tra | Trạng thái |
| --- | --- | --- | --- |
| Câu hỏi phỏng vấn | [S03-Q032](../../sources/03-sql-data-performance.md#q032) | Đọc 2026-10-10 | Câu hỏi nguồn, không phải lời giải đã xác minh |
| COUNT(*) đếm dòng; COUNT(expression) đếm giá trị khác NULL | [Trang COUNT](https://learn.microsoft.com/en-us/sql/t-sql/functions/count-transact-sql); [Markdown chính thức](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/functions/count-transact-sql.md) | Tổng hợp cơ bản SQL Server; kiểm tra 2026-10-10 | Đã đọc nguồn tài liệu chính thức |
| Cột nhóm, HAVING và WHERE | [Trang GROUP BY](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-group-by-transact-sql); [Markdown chính thức](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-group-by-transact-sql.md) | Quy tắc nhóm SQL Server; kiểm tra 2026-10-10 | Đã đọc nguồn tài liệu chính thức |
| Thứ tự binding logic khác thực thi vật lý | [Trang SELECT](https://learn.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql); [Markdown chính thức](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/select-transact-sql.md) | Ý nghĩa truy vấn và phạm vi alias; kiểm tra 2026-10-10 | Đã đọc nguồn tài liệu chính thức |
| LEFT JOIN tạo NULL; khác biệt ON/WHERE | [Trang FROM](https://learn.microsoft.com/en-us/sql/t-sql/queries/from-transact-sql); [Markdown chính thức](https://github.com/MicrosoftDocs/sql-docs/blob/main/docs/t-sql/queries/from-transact-sql.md) | Ngữ nghĩa JOIN SQL Server; kiểm tra 2026-10-10 | Đã đọc nguồn tài liệu chính thức |
| Kết quả lab | [Lab chạy được](../../labs/department-headcount/README.md) | SQLite 3.53.1, chạy 2026-10-10 | Sáu reference tests và ba extension assertions pass; starter có bốn failures đúng dự kiến |

Môi trường đọc được các file ở `raw.githubusercontent.com/MicrosoftDocs/sql-docs/main/`, không truy cập trực tiếp website Learn. File COUNT tải về có `ms.date: 07/24/2017`; đó là ngày tài liệu, không phải ngày đối chiếu hôm nay. Kiểm tra nguồn chính thức này hỗ trợ các quy tắc quan hệ ổn định; không chứng minh hành vi optimizer phiên bản hiện tại hoặc việc chạy SQL Server. Không khẳng định default riêng phiên bản, benchmark hay bảo đảm concurrency. Dữ liệu thực hành và yêu cầu biến thể do bài này thiết kế, không phải dữ kiện phỏng vấn gốc.

</details>
