Анализ перехваченного трафика через функционал скрипта на примере 40 сообщений
=============================================================================================

1. В ходе выполнения задания был произведён перехват и анализ HTTP‑трафика веб‑приложения
Google Gruyere с использованием библиотеки Scapy. Анализ выполнялся на основе ранее сохранённого
файла сетевого трафика (griko_xss.pcap).
2. В результате анализа было обнаружено 42 HTTP‑сообщения, включающие:
HTTP‑запросы клиента (методы GET)
HTTP‑ответы сервера (200 OK, 302 Found)
Трафик соответствует типичному взаимодействию браузера с веб‑приложением и включает загрузку
HTML‑страниц, изображений и выполнение переходов.
3. В перехваченном трафике были зафиксированы следующие типы запросов:
загрузка основной страницы приложения:
GET /<session_id>/snippets.gtl
запросы дополнительных ресурсов (изображения, элементы интерфейса):
GET /<session_id>/0
GET /<session_id>/nonexistent.jpg
запросы с пользовательскими параметрами, передаваемыми через URL:
GET /newsnippet2?snippet=<payload>
GET /saveprofile?action=update&...&private_snippet=<payload>
Часть параметров передавалась в URL‑кодированном виде, что характерно для GET‑запросов.
4. Ответы сервера имеют следующие характеристики:
Код ответа:
200 OK — успешная обработка запроса
302 Found — перенаправление пользователя
Тип содержимого:
Content-Type: text/html
Используемое сжатие:
Content-Encoding: gzip
Применение gzip‑сжатия указывает на оптимизацию передачи данных между сервером и клиентом.
4.1 Несмотря на наличие заголовка Content-Encoding: gzip, тело HTTP‑ответов не всегда может
быть корректно распаковано средствами Scapy.
Причина заключается в том, что:
HTTP‑ответы передаются фрагментированно, по протоколу TCP
тело gzip‑сообщения разбивается на несколько TCP‑сегментов
Scapy анализирует пакеты по отдельности, без автоматической сборки TCP‑потока
!!! Извините, не смог победить данный формат, если подскажете как это сделать, буду благодарен!!
5. В анализируемом трафике были обнаружены признаки межсайтового скриптинга (XSS):
Пример 1 — отражённый XSS через параметр snippet:
<script>alert('XSS')</script>
Передача полезной нагрузки осуществлялась в URL‑кодированном виде:
%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E
Пример 2 — XSS через HTML‑атрибут:
<img src="nonexistent.jpg" onerror="alert('XSS')">
Данные конструкции были зафиксированы в GET‑запросах и предназначались для внедрения в
HTML‑контент страницы.
6. После отправки запросов с XSS‑полезной нагрузкой сервер:
возвращал HTTP‑ответ с кодом 302 Found
перенаправлял пользователя на основную страницу приложения
Это свидетельствует о наличии частичных защитных механизмов, однако сам факт отражения
пользовательского ввода указывает на потенциальную уязвимость приложения.
7. В результате анализа перехваченного трафика можно сделать следующие выводы:
Веб‑приложение активно использует HTTP‑запросы с передачей параметров через URL
Ответы сервера сжимаются с использованием gzip
В трафике присутствуют признаки отражённых XSS‑атак
Приложение Google Gruyere демонстрирует уязвимости, характерные для учебных веб‑платформ

Заключение:
Перехват и анализ сетевого трафика позволил выявить структуру HTTP‑взаимодействия веб‑приложения,
особенности передачи данных и наличие XSS‑уязвимостей. Полученные результаты подтверждают
возможность использования анализа сетевого трафика как метода выявления потенциальных проблем
безопасности веб‑приложений.

P.S. А вообще очень интересные материалы и хотелось бы, чтобы их разбор был более глубоким и
практичным, спасибо.

===========================================================================================
(.venv) andrey@MacBook-Air-andrey topic_9_www % python HW_8.py --analyze griko_xss.pcap
Анализ трафика из файла: griko_xss.pcap
Найдено HTTP-сообщений: 42

HTTP-сообщение 1
GET /541816364936026820920854899500429118802/snippets.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: text/

HTTP-сообщение 2
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: f901951f62e9968b406fd65bbce1a1bc
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:26 GMT
server: Google Frontend
Content-Length: 1108

HTTP-сообщение 3
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml

HTTP-сообщение 4
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: a8a5ddb8703df469406fd65bbce1a2f7
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:26 GMT
server: Google Frontend
Content-Length: 946


HTTP-сообщение 5
GET /541816364936026820920854899500429118802/newsnippet.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: tex

HTTP-сообщение 6
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 877f7355c6023551406fd65bbce1af95;o=1
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:27 GMT
server: Google Frontend
Content-Length: 1138



HTTP-сообщение 7
GET /541816364936026820920854899500429118802/newsnippet2?snippet=%3Cscript%3Ealert%28%27XSS%27%29%3C%2Fscript%3E HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, li

HTTP-сообщение 8
HTTP/1.1 302 Found
cache-control: no-cache
location: http://google-gruyere.appspot.com/541816364936026820920854899500429118802/snippets.gtl
pragma: no-cache
content-type: text/html
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: fe281be08bbb41447dbaaae34a69e0d5
vary: Accept

HTTP-сообщение 9
GET /541816364936026820920854899500429118802/snippets.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: text/

HTTP-сообщение 10
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 4479def388ea216f7dbaaae34a69ebcc
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:39 GMT
server: Google Frontend
Content-Length: 1267


HTTP-сообщение 11
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml

HTTP-сообщение 12
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: dcd09a193ecafad37dbaaae34a69eee5
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:39 GMT
server: Google Frontend
Content-Length: 946


HTTP-сообщение 13
GET /541816364936026820920854899500429118802/snippets.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Sa

HTTP-сообщение 14
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 342732f29e6317a17dbaaae34a69e01f
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:43 GMT
server: Google Frontend
Content-Length: 1267


HTTP-сообщение 15
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml

HTTP-сообщение 16
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: a68cbe21caac543b7dbaaae34a69e338;o=1
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:43 GMT
server: Google Frontend
Content-Length: 946



HTTP-сообщение 17
GET /541816364936026820920854899500429118802/newsnippet.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: tex

HTTP-сообщение 18
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: aefe41ec8aa8131b7dbaaae34a69e00b
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:46 GMT
server: Google Frontend
Content-Length: 1138



[Т

HTTP-сообщение 19
GET /541816364936026820920854899500429118802/newsnippet2?snippet=%3Cimg+src%3D%22nonexistent.jpg%22+onerror%3D%22alert%28%27XSS%27%29%22%3E HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Ap

HTTP-сообщение 20
HTTP/1.1 302 Found
cache-control: no-cache
location: http://google-gruyere.appspot.com/541816364936026820920854899500429118802/snippets.gtl
pragma: no-cache
content-type: text/html
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 4f9527fba4f8bc27b13c41ef60332b13
vary: Accept

HTTP-сообщение 21
GET /541816364936026820920854899500429118802/snippets.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: text/

HTTP-сообщение 22
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 016274f7c50bd402b13c41ef60332836
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:54 GMT
server: Google Frontend
Content-Length: 1313


HTTP-сообщение 23
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml

HTTP-сообщение 24
GET /541816364936026820920854899500429118802/nonexistent.jpg HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng

HTTP-сообщение 25
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: d747b45820f9c6c8b13c41ef60332928;o=1
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:54 GMT
server: Google Frontend
Content-Length: 946



HTTP-сообщение 26
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 270538244cf6b23da1326e6a4d3f5cde
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:54 GMT
server: Google Frontend
Content-Length: 956


HTTP-сообщение 27
GET /541816364936026820920854899500429118802/editprofile.gtl HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: te

HTTP-сообщение 28
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: f2b4f132028aee5ba1326e6a4d3f57c3
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:31:58 GMT
server: Google Frontend
Content-Length: 1370



[Т

HTTP-сообщение 29
GET /541816364936026820920854899500429118802/saveprofile?action=update&name=Nomad55&oldpw=&pw=&icon=0&web_site=&color=&private_snippet=%3Cimg+src%3D%22nonexistent.jpg%22+onerror%3D%22alert%28%27XSS%27%29%22%3E HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Reque

HTTP-сообщение 30
HTTP/1.1 302 Found
cache-control: no-cache
location: http://google-gruyere.appspot.com/541816364936026820920854899500429118802/
pragma: no-cache
content-type: text/html
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: caa29649f3e3320baf4fe65e2eabe1ee
vary: Accept-Encoding
d

HTTP-сообщение 31
GET /541816364936026820920854899500429118802/ HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: text/html,applica

HTTP-сообщение 32
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 1f66543d97c864a2af4fe65e2eabe79c
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:32:03 GMT
server: Google Frontend
Content-Length: 1494



[Т

HTTP-сообщение 33
GET /541816364936026820920854899500429118802/nonexistent.jpg HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng

HTTP-сообщение 34
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml

HTTP-сообщение 35
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: 2cb8821073eb0df9ae6010c4ba9f289d
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:32:04 GMT
server: Google Frontend
Content-Length: 946


HTTP-сообщение 36
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: c95175173727aa5aaf4fe65e2eabeb86
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:32:04 GMT
server: Google Frontend
Content-Length: 956


HTTP-сообщение 37
GET /541816364936026820920854899500429118802/ HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: text/html,applica

HTTP-сообщение 38
HTTP/1.1 200 OK
cache-control: no-cache
content-type: text/html
pragma: no-cache
x-xss-protection: 0
content-encoding: gzip
x-cloud-trace-context: aca3c4d566acf8b3af4fe65e2eabed12
vary: Accept-Encoding
date: Sat, 07 Feb 2026 13:32:09 GMT
server: Google Frontend
Content-Length: 1494


HTTP-сообщение 39
GET /541816364936026820920854899500429118802/nonexistent.jpg HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng

HTTP-сообщение 40
GET /541816364936026820920854899500429118802/0 HTTP/1.1
Host: google-gruyere.appspot.com
Connection: keep-alive
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36
Accept: image/avif,image/webp,image/apng,image/svg+xml
(.venv) andrey@MacBook-Air-andrey topic_9_www %