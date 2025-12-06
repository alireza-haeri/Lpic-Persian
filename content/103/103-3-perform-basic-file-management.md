# 103.3 - انجام مدیریت پایه فایل‌ها

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- کپی، جابجایی و حذف فایل‌ها و دایرکتوری‌ها به صورت جداگانه
- کپی چندین فایل و دایرکتوری به صورت بازگشتی
- حذف فایل‌ها و دایرکتوری‌ها به صورت بازگشتی
- استفاده از مشخصات wildcard ساده و پیشرفته در دستورات
- استفاده از find برای یافتن و عمل بر روی فایل‌ها بر اساس نوع، اندازه یا زمان
- استفاده از tar، cpio و dd

## کلیدواژه‌ها

`cp`, `find`, `mkdir`, `mv`, `ls`, `rm`, `rmdir`, `touch`, `tar`, `cpio`, `dd`, `file`, `gzip`, `gunzip`, `bzip2`, `bunzip2`, `xz`

---

## Wildcards و file globbing

File globbing قابلیتی در پوسته است که به شما اجازه می‌دهد چیزهایی مانند همه فایل‌ها، همه چیزهایی که با A شروع می‌شوند، همه فایل‌های سه حرفی که با A یا B یا C پایان می‌یابند و غیره را بیان کنید.

برای انجام این کار، باید با این کاراکترها آشنا باشید:

- `*` به معنای هر رشته‌ای است
- `?` به معنای هر کاراکتر واحدی است
- `[ABC]` با A، B یا C مطابقت دارد
- `[a-k]` با a، b، c، ...، k مطابقت دارد (هر دو کوچک و بزرگ)
- `[0-9a-z]` با همه ارقام و اعداد مطابقت دارد
- `[!x]` به معنای NOT X است.

با دانستن این‌ها، می‌توانید الگوهای خود را ایجاد کنید. مثلاً:

| command | meaning |
|---------|---------|
| rm * | همه فایل‌ها را در این دایرکتوری حذف می‌کند |
| ls A*B | همه فایل‌هایی که با A شروع می‌شوند و با B پایان می‌یابند را نمایش می‌دهد |
| cp ???.* /tmp | همه فایل‌هایی با 3 کاراکتر، سپس یک نقطه، سپس هر چیزی (حتی هیچ) را به /tmp کپی می‌کند |
| rmdir [a-z]* | همه دایرکتوری‌های خالی که با یک حرف شروع می‌شوند را حذف می‌کند |

## دستورات عمومی

### لیست کردن با `ls`

`ls` برای لیست کردن دایرکتوری‌ها و فایل‌ها استفاده می‌شود. می‌توانید یک مسیر مطلق یا نسبی ارائه دهید؛ اگر حذف شود، "." به عنوان هدف استفاده می‌شود.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
```

!!! note "نکته"
    اولین فیلد نشان می‌دهد که آیا این یک فایل (`-`) یا دایرکتوری (`d`) است.

برخی سوئیچ‌های رایج عبارتند از:

- `-l` برای long (اطلاعات بیشتر برای هر فایل)
- `-1` برای چاپ یک فایل در هر خط
- `-t` بر اساس تاریخ تغییر مرتب می‌کند
- `-r` جستجو را معکوس می‌کند (پس `-tr` فایل‌های جدیدتر را در پایین نشان می‌دهد).

!!! note "نکته"
    می‌توانید سوئیچ‌ها را ترکیب کنید. یکی از معروف‌ها `-ltrh` است (long + human readable sizes + reverse time).

## کپی (`cp`)، جابجایی (`mv`) و حذف (`rm`)

### `cp`

این فایل‌ها را از یک مکان/نام به مکان/نام دیگری کپی می‌کند. اگر هدف یک دایرکتوری باشد، همه منابع در آن کپی می‌شوند.

```bash
cp source destination
```

یک سوئیچ رایج `-r` (یا `-R`) است که به صورت بازگشتی کپی می‌کند (دایرکتوری‌ها و محتویات آنها). پس برای کپی کردن یک دایرکتوری به نام `A` به `/tmp/` می‌توانید `cp -r A /tmp/` صادر کنید.

### `mv`

جابجایی یا تغییر نام فایل‌ها یا دایرکتوری‌ها. مانند دستور `cp` کار می‌کند. اگر یک فایل را در همان فایل سیستم جابجا کنید، inode تغییر نمی‌کند.

به طور کلی:

- اگر هدف یک دایرکتوری موجود باشد، سپس همه منابع در هدف کپی می‌شوند
- اگر دایرکتوری هدف وجود نداشته باشد، سپس منبع باید فقط یک دایرکتوری باشد که به دایرکتوری هدف تغییر نام می‌دهد.
- اگر هدف یک فایل باشد، سپس منبع باید فقط یک فایل باشد تا تغییر نام اتفاق بیفتد.

این‌ها مانند "فرمول‌ها" هستند اما منطقی هستند!

### `rm`

فایل‌ها را حذف (Deletes) می‌کند. می‌توانید با سوئیچ `-r` به صورت بازگشتی حذف کنید یا با سوئیچ `-f` (force) از بررسی تأیید جلوگیری کنید. پس `rm -rf /` به معنای "همه چیز را از فایل سیستم حذف کن" است.

### نکات

به طور معمول، دستور cp فایل را روی کپی موجود کپی می‌کند، اگر فایل موجود قابل نوشتن باشد. از طرف دیگر، `mv` یک فایل را جابجا یا تغییر نام نمی‌دهد اگر هدف وجود داشته باشد. اگرچه این کاملاً به پیکربندی سیستم شما بستگی دارد. اما در همه موارد، می‌توانید با سوئیچ `-f` غلبه کنید.

- `-f` (--force) باعث می‌شود cp سعی کند روی هدف بازنویسی کند.
- `-i` (--interactive) سؤال Y/N را می‌پرسد (حذف / بازنویسی).
- `-b` (--backup) پشتیبان‌هایی از فایل‌های بازنویسی شده ایجاد می‌کند
- `-p` ویژگی‌ها را حفظ می‌کند.

## ایجاد (mkdir) و حذف (rmdir) دایرکتوری‌ها

دستور `mkdir` دایرکتوری‌ها را ایجاد می‌کند.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 20K
-rw-rw-r-- 1 jadi jadi  207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi   29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi   24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi  116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 04:57 new_dir
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ mkdir -p 1/2/3 
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ tree
.
├── 1
│   └── 2
│       └── 3
├── data.txt
├── info.txt
├── new_dir
├── note_to_self
└── tasks.txt

0 directories, 4 files
```

اگر می‌خواهید یک درخت دایرکتوری ایجاد کنید، می‌توانید از سوئیچ `-p` استفاده کنید تا `mkdir` دایرکتوری‌های والد را در صورت نیاز ایجاد کند.

اگر نیاز به حذف یک دایرکتوری دارید، دستور `rmdir` است و همچنین می‌توانید از `-p` برای حذف تو در تو استفاده کنید:

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ rmdir -p 1/2/3
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ rmdir new_dir
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ tree
.
├── data.txt
├── info.txt
├── note_to_self
└── tasks.txt

0 directories, 4 files
```

!!! warning "هشدار"
    اگر از `rmdir` برای حذف یک دایرکتوری استفاده می‌کنید، باید EMPTY باشد! به همین دلیل بسیاری از افراد از `rm -rf directory_name` برای حذف دایرکتوری غیر خالی و هر چیزی که در آن است استفاده می‌کنند.

### `touch`

`touch` یک فایل خالی ایجاد می‌کند (اگر وجود نداشته باشد) یا تاریخ تغییر یک فایل موجود را به‌روزرسانی می‌کند. زمان پیش‌فرض "حالا" است اما می‌توانید زمان‌های دیگر را نیز مشخص کنید.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ touch new_file
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
-rw-rw-r-- 1 jadi jadi   0 Aug 14 05:08 new_file
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ touch note_to_self
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi   0 Aug 14 05:08 new_file
-rw-rw-r-- 1 jadi jadi 116 Aug 14 05:08 note_to_self
```

یا می‌توانید زمان‌ها را مشخص کنید. امکان استفاده از `-d` و دادن تاریخ‌ها یا استفاده از `-t` و دادن یک timestamp در قالب `[[CC]YY]MMDDhhmm[.ss]` وجود دارد.

```bash
$ touch -t 200908121510.59 file1
$ touch -d 11am file2
$ touch -d "last fortnight" file3
$ touch -d "yesterday 6am" file4
$ touch -d "2 days ago 12:00" file5
$ touch -d "tomorrow 02:00" file6
$ touch -d "5 Nov" file3
$ ls -ltrh file?
-rw-rw-r-- 1 jadi jadi 0 Aug 12  2009 file1
-rw-rw-r-- 1 jadi jadi 0 Aug 12 12:00 file5
-rw-rw-r-- 1 jadi jadi 0 Aug 13 06:00 file4
-rw-rw-r-- 1 jadi jadi 0 Aug 14  2022 file2
-rw-rw-r-- 1 jadi jadi 0 Aug 15  2022 file6
-rw-rw-r-- 1 jadi jadi 0 Nov  5  2022 file3
```

همچنین امکان استفاده از زمان فایل دیگری با سوئیچ `-r` (برای --reference) وجود دارد:

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -l /etc/debian_version
-rw-r--r-- 1 root root 13 Aug 22  2021 /etc/debian_version
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ touch -r /etc/debian_version file1
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 20K
-rw-rw-r-- 1 jadi jadi   0 Aug 22  2021 file1
```

### `file`

برای تعیین نوع یک فایل، از دستور `file` استفاده کنید. به داخل فایل نگاه می‌کند و نوع آن را تعیین می‌کند.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ file file1
file1: empty
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ file note_to_self
note_to_self: ASCII text
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ file /bin/bash
/bin/bash: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=33a5554034feb2af38e8c75872058883b2988bc5, for GNU/Linux 3.2.0, stripped
```

!!! note "نکته"
    سوئیچ `-i` فرمت mime را چاپ می‌کند.

### `dd`

دستور `dd` داده‌ها را از ورودی خود به خروجی کپی می‌کند (بگویید فایل‌ها یا دستگاه‌ها). می‌توانید مانند کپی از آن استفاده کنید:

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ dd if=note_to_self of=new_file
0+1 records in
0+1 records out
116 bytes copied, 0.00141561 s, 81.9 kB/s
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ cat new_file
I will continue learning... and if I get confused, I'll repeat the last section once more till everything is clear!
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$
```

- `if` فایل ورودی است
- `of` فایل خروجی است

اما معمولاً مردم از آن برای خواندن/نوشتن از دستگاه‌های بلوکی استفاده می‌کنند. مثلاً این همه سکتورها را از `/dev/sdb` می‌خواند و آنها را در یک فایل به نام `backup.dd` می‌نویسد. بعداً می‌توانید این پشتیبان را با تعویض `if` و `of` و نوشتن از `backup.dd` به `/dev/sdb` بازیابی کنید.

```bash
# dd if=/dev/sda of=backup.dd bs=4096
```

یا حتی:

```bash
# dd if=/dev/sda2 | gzip > backup.dd.gzip
```

همچنین برای ایجاد فایل‌هایی با اندازه‌های خاص استفاده می‌شود:

```bash
dd if=/dev/zero of=1g.bin bs=1G count=1
```

یا حتی نوشتن فایل‌های iso شما به یک USB disk برای داشتن یک USB bootable زنده:

```bash
sudo dd if=ubuntu.iso of=/dev/sdc bs=2048
```

!!! warning "هشدار"
    در اینجا مستقیماً روی یک دستگاه بلوکی می‌نویسید. اگر چیزی اشتباه کنید... دیسک شما خراب می‌شود و نیاز به فرمت مجدد دارد.

### `find`

دستور `find` به ما کمک می‌کند فایل‌ها را بر اساس معیارهای مختلف پیدا کنیم. به این نگاه کنید:

```bash
$ find . -iname "[a-j]*"
./howcool.sort
./alldata
./mydir/howcool.sort
./mydir/newDir/insideNew
./howcool
```

- پارامتر اول جایی است که باید جستجو کنیم (شامل زیر دایرکتوری‌ها).
- سوئیچ `-name` معیار را نشان می‌دهد (در اینجا `iname` به معنای جستجوی فایل‌ها با این نام و نادیده گرفتن حروف کوچک و بزرگ است).

یک سوئیچ رایج دیگر `-type` برای نشان دادن نوع جستجو است (`f` برای فایل‌های منظم، `d` برای دایرکتوری‌ها، `l` برای لینک‌های نمادین):

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ find . -type d -iname "[a-j]*"
./directory
./directory/innder_one
```

اگر می‌خواهید بر اساس اندازه فایل جستجو کنید:

| command | meaning |
|---------|---------|
| -size 100c | فایل‌هایی که دقیقاً 100 کاراکتر/بایت هستند (می‌توانید از `b` نیز استفاده کنید) |
| -size +100k | فایل‌هایی که بیش از 100 کیلوبایت هستند |
| -size -20M | فایل‌هایی که کمتر از 20 مگابایت هستند |
| -size +2G | فایل‌هایی که بیش از 2 گیگابایت هستند |

پس این همه فایل‌هایی را که با *tmp پایان می‌یابند و اندازه بین 1M و 100M در دایرکتوری /var/ پیدا می‌کند:

```bash
find /var -iname '*tmp' -size +1M -size -100M
```

!!! note "نکته"
    می‌توانید همه فایل‌های خالی را با `find . -size 0b` یا `find . -empty` پیدا کنید.

یک معیار جستجوی مفید دیگر زمان است. برخی از گزینه‌ها:

| switch | meaning | samples |
|--------|---------|---------|
| -amin | Access Minutes | `-amin 40` به معنای فایل‌هایی که دقیقاً 40 دقیقه پیش دسترسی شده‌اند یا `-amin +40` فایل‌هایی که بیش از 40 دقیقه پیش دسترسی شده‌اند و `-amin -40` به معنای فایل‌هایی که کمتر از 40 دقیقه پیش دسترسی شده‌اند |
| -cmin | Status Change Min | `-cmin +60` وضعیت فایل قبل از ساعت گذشته تغییر کرده است |
| -mmin | Modified Minutes | `-mmin -60` فایل‌هایی که در ساعت گذشته تغییر کرده‌اند |
| -atime | access time in days | `-atime +1` به معنای فایل‌هایی که "بیش از 1 روز پیش" دسترسی شده‌اند (یعنی 2 روز و بیشتر) |
| -ctime | Status Changed in Days |  |
| -mtime | Modified days |  |
| -newer | Newer than reference | `-newer file1` فایل‌هایی که جدیدتر از file1 هستند |

!!! note "نکته"
    اگر `-daystart` را به -mtime یا -atime اضافه کنید، به معنای این است که می‌خواهیم روزها را به عنوان روزهای تقویم در نظر بگیریم، از نیمه شب شروع می‌شود.

### Acting on files

می‌توانیم دستورات یا اقدامات دیگری را روی فایل‌ها با سوئیچ‌های مختلف اجرا کنیم:

| switch | meaning |
|--------|---------|
| -ls | `ls -dils` را روی هر فایل اجرا می‌کند |
| -print | نام کامل فایل‌ها را روی هر خط چاپ می‌کند |

اما بهترین راه برای اجرای دستورات روی فایل‌های یافت شده سوئیچ `-exec` است. می‌توانید به فایل با `'{}'` یا `{}` اشاره کنید و دستور خود را با `\;` پایان دهید.

مثلاً این همه فایل‌های خالی را در این دایرکتوری و زیر دایرکتوری‌های آن حذف می‌کند:

```bash
find . -empty -exec rm '{}' \;
```

یا این همه فایل‌های htm را به html تغییر نام می‌دهد

```bash
find . -name "*.htm" -exec mv '{}' '{}l' \;
```

!!! note "نکته"
    از آنجایی که حذف فایل‌های یافت شده یک کار رایج است، سوئیچ `-delete` برای آن وجود دارد.

## فشرده‌سازی

### `gzip` و `gunzip`

ساده و سرراست، یکی فایل‌ها را gzip می‌کند و دیگری unzip می‌کند؛ در جای خود:

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ gzip tasks.txt
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
-rw-rw-r-- 1 jadi jadi 171 Aug 14 04:43 tasks.txt.gz
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ gunzip tasks.txt.gz
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 16K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
```

- gzip زمان را حفظ می‌کند
- gzip فایل فشرده جدید را با نام ورودی + .gz ایجاد می‌کند
- gzip فایل ورودی را پس از ایجاد فایل فشرده حذف می‌کند (می‌توانید فایل ورودی را با سوئیچ `-k` نگه دارید)

### `bzip2` و `bunzip2`

`bzip2` ابزار فشرده‌سازی دیگری است. درست مانند `gzip` و `bzip2` کار می‌کند اما با الگوریتم فشرده‌سازی متفاوت.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ bzip2 tasks.txt
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 20K
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
-rw-rw-r-- 1 jadi jadi 172 Aug 14 04:43 tasks.txt.bz2
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ bunzip2 tasks.txt.bz2
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls
data.txt  directory  info.txt  new_file  note_to_self  tasks.txt
```

### `xz` و `unxz`

ابزار فشرده‌سازی/باز کردن فشرده‌سازی دیگری درست مانند `gzip` و `bzip2`.

```bash
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ xz tasks.txt
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 24K
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
-rw-rw-r-- 1 jadi jadi 224 Aug 14 04:43 tasks.txt.xz
-rw-rw-r-- 1 jadi jadi 116 Aug 14 07:51 new_file
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ unxz tasks.txt.xz
jadi@lpicjadi:~/lpic1-practice-iso/100/103.3$ ls -ltrh
total 24K
-rw-rw-r-- 1 jadi jadi 207 Aug 14 04:43 tasks.txt
-rw-rw-r-- 1 jadi jadi  29 Aug 14 04:43 info.txt
-rw-rw-r-- 1 jadi jadi  24 Aug 14 04:44 data.txt
-rw-rw-r-- 1 jadi jadi 116 Aug 14 04:44 note_to_self
drwxrwxr-x 2 jadi jadi 4.0K Aug 14 05:20 directory
-rw-rw-r-- 1 jadi jadi 116 Aug 14 07:51 new_file
```

لطفاً توجه کنید که فشرده‌سازی یک فایل متنی کوچک باعث بزرگتر شدن آن می‌شود. این در فایل‌های کوچک طبیعی است زیرا همه هدرها و metadata.

!!! note "نکته"
    در برخی موارد، دستوراتی مانند `unxz` فقط فراخوانی‌هایی به `xz --decompress` هستند.

## بایگانی با tar و cpio

بعضی اوقات نیاز به ایجاد یک فایل کانتینر آرشیو از بسیاری از فایل‌های دیگر داریم. این عملیات با فشرده‌سازی متفاوت است، فایل‌ها را در یک فایل ترکیب می‌کند و بعداً دوباره استخراج می‌کند. بایگانی بیشتر در پشتیبان‌گیری‌ها، انتقال فایل‌ها به مکان جدید (بگویید از طریق ایمیل)، و غیره استفاده می‌شود. این کار با `cpio` و `tar` انجام می‌شود.

### `tar`

TapeARchive یا tar رایج‌ترین ابزار بایگانی است. به طور خودکار یک فایل آرشیو از یک دایرکتوری و همه زیر دایرکتوری‌های آن ایجاد می‌کند.

سوئیچ‌های رایج عبارتند از:

| switch | meaning |
|--------|---------|
| -cf `myarchive.tar` | فایل با نام myarchive.tar ایجاد می‌کند |
| -xf `myarchive.tar` | فایل با نام myarchive.tar را استخراج می‌کند |
| -z | آرشیو را با gzip پس از ایجاد فشرده می‌کند |
| -j | آرشیو را با bzip2 پس از ایجاد فشرده می‌کند |
| -v | verbose! داده‌های زیادی درباره آنچه در حال انجام است چاپ می‌کند |
| -r | فایل‌های جدید را به آرشیو موجود اضافه می‌کند |

!!! note "نکته"
    اگر مسیرهای مطلق صادر کنید، tar برای ایمنی اسلش شروع (/) را حذف می‌کند هنگام ایجاد آرشیو. اگر می‌خواهید لغو کنید، از گزینه `-p` استفاده کنید.

!!! note "نکته"
    tar می‌تواند با نوارها و ذخیره‌های دیگر کار کند. به همین دلیل از `-f` استفاده می‌کنیم تا به آن بگوییم با فایل‌ها کار می‌کنیم.

### `cpio`

یک لیست از فایل‌ها دریافت می‌کند و یک آرشیو (یک فایل) ایجاد می‌کند. این فایل بعداً می‌تواند برای استخراج فایل‌های اصلی استفاده شود.

```bash
$ ls | cpio -o > allfilesls.cpio
3090354 blocks
```

- `-o` به cpio می‌گوید از ورودی خود خروجی ایجاد کند

لطفاً توجه کنید که `cpio` به داخل پوشه‌ها نگاه نمی‌کند. پس بیشتر اوقات از آن با find استفاده می‌کنیم:

```bash
find . -name "*" | cpio -o > myarchivefind.cpio
```

برای استخراج فایل‌های اصلی:

```bash
mkdir extract
mv myarchivefind.cpio extract
cd extract
cpio -id < myarchivefind.cpio
```

- `-d` پوشه‌ها را ایجاد می‌کند
- `-i` برای استخراج است

## تمرین‌ها

1. لیست فایل‌ها در دایرکتوری فعلی را نمایش دهید.
2. یک دایرکتوری جدید ایجاد کنید و سپس آن را حذف کنید.
3. یک فایل را کپی کنید و سپس تغییر نام دهید.
4. فایل‌هایی را که با "test" شروع می‌شوند پیدا کنید.
5. یک فایل را با gzip فشرده کنید و سپس باز کنید.
6. یک آرشیو tar از چندین فایل ایجاد کنید و سپس استخراج کنید.
7. از dd برای ایجاد یک فایل با اندازه خاص استفاده کنید.
8. فایل‌هایی را که در 7 روز گذشته تغییر کرده‌اند پیدا کنید.

## خلاصه

در این فصل با انجام مدیریت پایه فایل‌ها آشنا شدیم. ابزارهای مهمی مانند `ls`, `cp`, `mv`, `rm`, `mkdir`, `rmdir`, `touch`, `file`, `dd`, `find`, `gzip`, `bzip2`, `xz`, `tar` و `cpio` را آموختیم. این دستورات پایه‌ای برای مدیریت فایل‌ها و دایرکتوری‌ها در سیستم لینوکس هستند و شامل عملیات‌هایی مانند لیست کردن، کپی کردن، جابجایی، حذف، فشرده‌سازی و بایگانی می‌شوند. همچنین با wildcards و جستجوی پیشرفته فایل‌ها آشنا شدیم.
