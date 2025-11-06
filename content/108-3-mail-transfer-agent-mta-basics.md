# 108.3 مبانی عامل انتقال ایمیل (MTA)

**وزن:** 3  
**توضیح:** داوطلبان باید از برنامه‌های MTA رایج آگاه باشند و قادر به انجام پیکربندی پایه forward و alias در یک میزبان کلاینت باشند. سایر فایل‌های پیکربندی پوشش داده نمی‌شوند.

## حوزه‌های کلیدی دانش
- ایجاد نام‌های مستعار (alias) ایمیل
- پیکربندی forward ایمیل
- دانش برنامه‌های MTA رایج (postfix، sendmail، exim) (بدون پیکربندی)

## اصطلاحات و ابزارها
- ~/.forward
- sendmail emulation layer commands
- newaliases
- mail
- mailq
- postfix
- sendmail
- exim

## MTA ها (عامل‌های انتقال ایمیل)

ایمیل بخش جدایی‌ناپذیر بسیاری از سیستم‌های GNU/Linux و Unix است. هر کاربر یک صندوق پستی دارد و می‌تواند ایمیل بفرستد/دریافت کند به/از سایر کاربران محلی. این کار از طریق MTA ها (Mail Transfer Agents) انجام می‌شود. به عبارت دیگر، MTA ها برنامه‌هایی هستند که ایمیل‌ها را در سیستم‌عامل شما مدیریت می‌کنند. آنها می‌توانند ایمیل‌ها را به صورت محلی و از طریق شبکه دریافت و ارسال کنند. گزینه‌های مختلفی برای MTA ها وجود دارد. در این بخش یک بررسی سریع از آنها خواهیم داشت و خواهید دید که چگونه می‌توانید ایمیل‌هایی به سایر کاربران (یا از طریق اینترنت) بفرستید و چگونه می‌توانید ایمیل‌های محلی خود را بررسی کنید.

### sendmail

یکی از قدیمی‌ترین گزینه‌های موجود است. بزرگ است و تا حدودی پیکربندی آن دشوار است و چندان امنیت‌محور نیست. به دلیل این موارد، سیستم‌های کمی از آن به عنوان MTA پیش‌فرض خود استفاده می‌کنند.

### exim

هدف آن یک سیستم ایمیل عمومی و انعطاف‌پذیر با امکانات گسترده برای بررسی ایمیل‌های ورودی است. با ACL ها، احراز هویت و بسیاری از ویژگی‌های دیگر پر از امکانات است.

### postfix

این یک جایگزین جدید برای `sendmail` است و از فایل‌های پیکربندی آسان برای درک استفاده می‌کند. از دامنه‌های متعدد، رمزگذاری و غیره پشتیبانی می‌کند. Postfix چیزی است که در بیشتر توزیع‌ها به عنوان MTA پیش‌فرض می‌بینید.

**نکته:** بیشتر توزیع‌های دسکتاپ به طور پیش‌فرض MTA نصب نمی‌کنند. اگر می‌خواهید، پیشنهاد می‌کنم `postfix` (و `mailx` یا `bsd-mailx`) را از طریق مدیر بسته خود نصب کنید.

## لایه شبیه‌سازی sendmail

همانطور که می‌دانید، `sendmail` قدیمی‌ترین MTA زنده است و بنابراین، بسیاری از MTA های دیگر سعی می‌کنند با آن سازگار باشند و یک **لایه شبیه‌سازی sendmail** دارند تا خود را با sendmail سازگار با گذشته نگه دارند. به همین دلیل است که می‌توانید `sendmail` را در هر توزیعی که هستید تایپ کنید یا از `mailq` استفاده کنید و صرف نظر از انتخاب MTA خود، ایمیل خود را بررسی کنید.

## نام‌های مستعار (aliases)

برخی نام‌های مستعار ایمیل در سیستم وجود دارد. در `/etc/aliases` تعریف شده‌اند:

```bash
$ cat /etc/aliases
#
#  Aliases in this file will NOT be expanded in the header from
#  Mail, but WILL be visible over networks or from /bin/mail.
#
#       >>>>>>>>>>      The program "newaliases" must be run after
#       >> NOTE >>      this file is updated for any changes to
#       >>>>>>>>>>      show through to sendmail.
#
# Basic system aliases -- these MUST be present.
mailer-daemon:  postmaster
postmaster:     root
# General redirections for pseudo accounts.
bin:            root
daemon:         root
adm:            root
lp:             root
sync:           root
shutdown:       root
halt:           root
mail:           root
news:           root
uucp:           root
operator:       root
games:          root
www:            webmaster
webmaster:      root
[ .... ]
```

این به سیستم می‌گوید اگر پیامی برای `news` باشد، باید به `root` تحویل داده شود و اگر ایمیل به `www` نوشته شده باشد، باید به `webmaster` تحویل داده شود.

در صورت هرگونه تغییر در این فایل، باید دستور `newaliases` را اجرا کنید.

## ارسال ایمیل

امکان ارسال ایمیل از خط فرمان با استفاده از دستور `mail` وجود دارد:

```bash
[jadi@funlife ~]$ mail news
Subject: Email to news user
hahah.. we know where this will go.
this will go to root and then to jadi!
Hi Jadi!
Cc:
[jadi@funlife ~]$ mail
Mail version 8.1.2 01/15/2001.  Type ? for help.
"/var/mail/jadi": 12 messages 12 new
>N  1 root@funlife       Sat Jan 02 08:50   39/1373  apt-listchanges: news for f
N  2 root@funlife       Sat Jan 02 09:01  165/7438  apt-listchanges: news for f
N  3 jadi@funlife       Sat Jan 02 19:58   18/640   *** SECURITY information fo
N  4 jadi@funlife       Sat Jan 02 20:04   18/631   *** SECURITY information fo
N  5 jadi@funlife       Sun Jan 03 10:15   18/664   *** SECURITY information fo
N  6 root@funlife       Mon Jan 04 12:42   27/941   Cron <jadi@funlife> /home/j
N  7 root@funlife       Mon Jan 04 17:11   26/845   apt-listchanges: news for f
N  8 root@funlife       Tue Jan 05 18:42   27/945   Cron <jadi@funlife> /home/j
N  9 root@funlife       Wed Jan 06 09:17   46/1788  apt-listchanges: news for f
N 10 root@funlife       Thu Jan 07 12:42   27/945   Cron <jadi@funlife> /home/j
N 11 root@funlife       Thu Jan 07 18:42   27/943   Cron <jadi@funlife> /home/j
N 12 jadi@funlife       Thu Jan  7 19:53   17/478   Email to news user
& 12
Message 12:
From jadi@funlife  Thu Jan  7 19:53:08 2016
X-Original-To: news
To: news@funlife
Subject: Email to news user
Date: Thu,  7 Jan 2016 19:53:08 +0330 (IRST)
From: jadi@funlife (jadi)
hahah.. we know where this will go.
this will go to root and then to jadi!
Hi Jadi!
& d
& q
Held 11 messages in /var/mail/jadi
```

## forward های محلی

دیدیم که امکان forward کردن ایمیل‌ها با استفاده از `/etc/aliases` وجود دارد. آن فایل توسط کاربران عادی قابل نوشتن نیست پس یک کاربر عادی مانند `jadi` باید چه کار کند؟

هر کاربر می‌تواند یک فایل `.forward` در دایرکتوری خود ایجاد کند و همه ایمیل‌های هدف‌گذاری شده به آن کاربر به آن آدرس forward می‌شوند.

حتی می‌توانید یک آدرس ایمیل کامل مانند `[email protected]` در فایل `.forward` خود قرار دهید.

همچنین می‌تواند ایمیل را از خط فرمان یا حتی در اسکریپت‌های خود با صادر کردن چیزی شبیه به این ارسال کند:

```bash
echo -e "email content" | mail -s "email subject" "[email protected]"
```

## mailq

این دستور صف ایمیل را لیست می‌کند. هر ورودی شناسه فایل صف، اندازه پیام، زمان ورود، فرستنده و گیرندگانی را که هنوز باید تحویل داده شوند نشان می‌دهد. اگر ایمیل در آخرین تلاش نتواند تحویل داده شود، دلیل شکست نشان داده می‌شود. مدیر سیستم می‌تواند از این دستور برای بررسی وضعیت ایمیل‌هایی که هنوز در صف‌ها هستند استفاده کند.

```bash
$ mailq
-Queue ID- --Size-- ----Arrival Time---- -Sender/Recipient-------
AA52C228E6B      468 Thu Jan  7 19:59:41  jadi@funlife
(connect to alt2.gmail-smtp-in.l.google.com[2404:6800:4003:c01::1a]:25: Network is unreachable)
[email protected]
-- 0 Kbytes in 1 Request.
```

---

**مثال عملی:** برای ارسال سریع یک ایمیل به خودتان:
```bash
echo "این یک تست است" | mail -s "ایمیل تست" $USER
```
سپس با `mail` ایمیل خود را بررسی کنید.

**خلاصه:** MTA ها (Mail Transfer Agents) مانند sendmail، exim و postfix، ایمیل‌ها را در Linux مدیریت می‌کنند. Postfix محبوب‌ترین گزینه مدرن است. نام‌های مستعار در `/etc/aliases` تعریف می‌شوند (نیاز به `newaliases` پس از تغییر). کاربران می‌توانند با فایل `~/.forward` ایمیل‌های خود را هدایت کنند. از دستور `mail` برای ارسال و خواندن ایمیل و از `mailq` برای بررسی صف ایمیل استفاده می‌شود.

---

← 108.2 ثبت رویدادهای سیستم  
**فهرست فصل‌ها**  
108.4 مدیریت چاپگرها و چاپ →

**دسته‌بندی:** LPIC1  
**برچسب‌ها:** 102، LPIC1، LPIC1-102-500  
**تماس**
