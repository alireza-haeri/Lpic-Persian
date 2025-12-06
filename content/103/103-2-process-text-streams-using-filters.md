# 103.2 - پردازش جریان‌های متنی با استفاده از فیلترها

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- ارسال فایل‌های متنی و جریان‌های خروجی از طریق فیلترهای ابزار متنی برای تغییر خروجی با استفاده از دستورات استاندارد UNIX موجود در بسته GNU textutils

## کلیدواژه‌ها

`bzcat`, `cat`, `cut`, `head`, `less`, `md5sum`, `nl`, `od`, `paste`, `sed`, `sha256sum`, `sha512sum`, `sort`, `split`, `tail`, `tr`, `uniq`, `wc`, `xzcat`, `zcat`

---

## جریان‌ها (Streams)

در دنیای UNIX، بسیاری از داده‌ها به صورت TEXT هستند. فایل‌های log، تنظیمات، داده‌ها و غیره. **فیلترینگ** این داده‌ها به معنای گرفتن یک جریان ورودی متنی و انجام برخی تبدیل‌ها روی متن قبل از ارسال آن به یک جریان خروجی است. در این زمینه، یک **جریان** چیزی جز "یک دنباله از بایت‌ها که می‌تواند با استفاده از توابع کتابخانه‌ای که جزئیات دستگاه زیرین را از برنامه پنهان می‌کنند، خوانده یا نوشته شود" نیست.

به عبارت ساده، یک جریان متنی ورودی متنی از صفحه کلید، یک فایل، یک دستگاه شبکه و غیره است که می‌تواند از طریق دستورات ابزار متنی مشاهده، تغییر، بررسی و غیره شود.

محیط‌های برنامه‌نویسی مدرن و پوسته‌ها (شامل bash) از سه جریان I/O استاندارد استفاده می‌کنند:

- **stdin** جریان ورودی استاندارد است که ورودی را به دستورات فراهم می‌کند.
- **stdout** جریان خروجی استاندارد است که خروجی دستورات را نمایش می‌دهد.
- **stderr** جریان خطای استاندارد است که خروجی خطا از دستورات را نمایش می‌دهد.

در اینجا ما در مورد **stdin** صحبت می‌کنیم و نحوه مشاهده یا دستکاری آن از طریق دستورات و ابزارهای مختلف را خواهیم دید. در فصل 103.4 بیشتر در مورد این جریان‌ها خواهید دید و خواهید دید چگونه می‌توانیم دستورات را ترکیب کنیم تا ورودی‌ها و خروجی‌های دستورات مختلف را PIPE کنیم.

## دستورات مشاهده (Viewing commands)

### cat

این دستور به سادگی جریان ورودی خود را خروجی می‌دهد (یا نام فایلی که به آن می‌دهید). همانطور که در بخش قبلی دیدید. مانند اکثر دستورات، اگر ورودی به آن ندهید، داده‌ها را از صفحه کلید می‌خواند.

```bash
jadi@funlife:~/w/lpic/101$ cat > mydata
test
this is the second line
bye
jadi@funlife:~/w/lpic/101$ cat mydata
test
this is the second line
bye
```

!!! note "نکته"
    هنگام وارد کردن ورودی از طریق صفحه کلید، `ctrl+d` جریان را پایان می‌دهد.

می‌توانید بیش از یک نام فایل ورودی ارائه دهید:

```bash
jadi@funlife:~/w/lpic/101$ cat mydata directory_data
test
this is the second line
bye
total 0
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:33 12
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:33 62
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:33 neda
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:33 jadi
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:33 you
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:34 amir
-rw-rw-r-- 1 jadi jadi 0 Jan  4 17:37 directory_data
```

برخی سوئیچ‌های رایج cat عبارتند از `-n` برای نمایش شماره خطوط، `-s` برای فشرده‌سازی خطوط خالی، `-T` برای نمایش تب‌ها، و `-v` برای نمایش کاراکترهای غیر قابل چاپ.

### bzcat, xzcat, zcat, gzcat

این‌ها برای `cat` مستقیم فایل‌های فشرده bz، xz، و Z & gz استفاده می‌شوند. این‌ها به شما اجازه می‌دهند محتوای فایل‌های فشرده را بدون باز کردن آنها ببینید.

### less

این یک ابزار قدرتمند برای مشاهده فایل‌های متنی بزرگ‌تر است. می‌تواند صفحه‌بندی کند، جستجو کند و در فایل‌های متنی حرکت کند.

!!! note "نکته"
    یک دستور دیگر به نام `more` وجود دارد. این برای افرادی که از محیط DOS می‌آیند آشنا‌تر است و در دنیای لینوکس رایج نیست. از آن استفاده نکنید. به یاد داشته باشید: `less` بیشتر از `more` است.

برخی دستورات کمتر رایج less به شرح زیر است.

| Command | Usage |
|---------|-------|
| q | خروج |
| /foo | جستجو برای foo |
| n | بعدی (جستجو) |
| N | قبلی (جستجو) |
| ?foo | جستجو به عقب برای foo |
| G | رفتن به انتها |
| nG | رفتن به خط n |
| PageUp, PageDown, UpArrow, DownArrow | حدس بزنید! |

### od

این دستور فایل‌ها را در فرمت‌هایی غیر از متن _dump_ می‌کند (فایل‌ها را در پایه 8 نشان می‌دهد):

```bash
jadi@funlife:~/w/lpic/101$ od mydata
0000000 062564 072163 072012 064550 020163 071551 072040 062550
0000020 071440 061545 067543 062156 066040 067151 005145 074542
0000040 005145
0000042
```

برای انسان‌های عادی کافی نیست. بیایید از برخی سوئیچ‌ها استفاده کنیم:

- **-t** فرمت چاپ را مشخص می‌کند:
  - `-t a` برای نمایش فقط کاراکترهای نام‌گذاری شده
  - `-t c` برای نمایش کاراکترهای escaped.
  می‌توانید دو مورد بالا را به `-a` و `-c` خلاصه کنید
- **-A** برای انتخاب نحوه ارائه فیلد offset:
  - `-A d` برای دهدهی
  - `-A o` برای octal
  - `-A x` برای hex
  - `-A n` برای هیچ

!!! note "نکته"
    `od` برای یافتن مشکلات در فایل‌های متنی شما بسیار مفید است - مثلاً پیدا کردن اینکه آیا از تب استفاده می‌کنید یا پایان خطوط صحیح.

## انتخاب قسمت‌هایی از فایل‌ها (Choosing parts of files)

### split

فایل‌ها را تقسیم می‌کند. برای انتقال فایل‌های HUGE روی رسانه‌های کوچک‌تر بسیار مفید است (مثل تقسیم یک فایل 3TB به قسمت‌های 8GB و انتقال آنها به ماشین دیگری با دیسک USB).

```bash
jadi@funlife:~/w/lpic/101$ cat mydata
hello
this is the second line
but as you can see we are
still writing
and this is getting longer
.
.
and longer
and longer!
jadi@funlife:~/w/lpic/101$ ls
mydata
jadi@funlife:~/w/lpic/101$ split -l 2 mydata
jadi@funlife:~/w/lpic/101$ ls
mydata    xaa  xab  xac  xad  xae
jadi@funlife:~/w/lpic/101$ cat xab
but as you can see we are
still writing
```

- به طور پیش‌فرض، split از xaa, xab, xac, ... برای نام فایل‌های خروجی استفاده می‌کند. می‌توان آن را با `split -l 2 mydata output` تغییر داد که mydata را به outputaa, outputab, ... تقسیم می‌کند؛ 2 خط در هر فایل.
- `-l 2` هر 2 خط را تقسیم می‌کند. امکان استفاده از `-b 42` برای تقسیم هر 42 بایت یا حتی `-n 5` برای اجبار 5 فایل خروجی وجود دارد.
- اگر می‌خواهید خروجی عددی (x00, x01, ..) داشته باشید، از گزینه `-d` استفاده کنید.

!!! note "نکته"
    نیاز به پیوستن این فایل‌ها دارید؟ آنها را با `cat x* > originalfile` cat کنید.

### head و tail

ابتدا (head) یا انتها (tail) فایل‌های متنی را نمایش می‌دهند. به طور پیش‌فرض، 10 خط نمایش می‌دهند اما می‌توانید با `-n20` یا `-20` تغییر دهید.

!!! note "نکته"
    `tail -f` خطوط جدیدی را که در انتهای فایل نوشته می‌شوند دنبال می‌کند. بسیار مفید.

### cut

دستور `cut` یک یا چند ستون را از یک فایل _برش_ می‌دهد. برای جدا کردن فیلدها خوب است:

بیایید _اولین فیلد_ یک فایل را برش دهیم.

```bash
jadi@funlife:~/w/lpic/101$ cat howcool
jadi    5
sina    6
rubic    2
you     12
jadi@funlife:~/w/lpic/101$ cut -f1 howcool
jadi
sina
rubic
you
```

!!! note "نکته"
    جداکننده پیش‌فرض TAB است. از `-dx` برای تغییر به "x" یا `-d' '` برای تغییر به space استفاده کنید.

همچنین امکان _برش_ فیلدهای 1، 2 و 3 با `-f1-3` یا فقط کاراکترهای با ایندکس 4، 5، 7، 8 از هر خط `-c4,5,7,8` وجود دارد.

## تغییر جریان‌ها (Modifying streams)

### nl

این دستور برای نمایش شماره خطوط است.

```bash
jadi@funlife:~/w/lpic/101$ nl mydata  | head -3
     1    hello
     2    this is the second line
     3    but as you can see we are
```

!!! note "نکته"
    `cat -n` نیز خطوط را شماره‌گذاری می‌کند.

### sort و uniq

ورودی(های) خود را مرتب می‌کنند.

```bash
jadi@funlife:~/w/lpic/101$ cat uses
you fedora
jadi ubuntu
rubic windows
neda mac
jadi@funlife:~/w/lpic/101$ cat howcool
jadi    5
sina    6
rubic    2
you     12
jadi@funlife:~/w/lpic/101$ sort howcool uses
jadi    5
jadi ubuntu
neda mac
rubic    2
rubic windows
sina    6
you     12
```

اگر می‌خواهید مرتب‌سازی معکوس داشته باشید، از سوئیچ `-r` استفاده کنید.

!!! note "نکته"
    اگر می‌خواهید NUMERICALLY مرتب کنید (پس 9 پایین‌تر از 19 است)، از `-n` استفاده کنید.

و `uniq` ورودی تکراری را از ورودی خود حذف می‌کند. رفتار عادی حذف فقط خطوط تکراری است اما می‌توانید رفتار آن را تغییر دهید، مثلاً سوئیچ `-f1` آن را مجبور می‌کند اولین فیلد را بررسی نکند.

```bash
jadi@funlife:~/w/lpic/101$ uniq what_i_have.txt
laptop
socks
tshirt
ball
socks
glasses
jadi@funlife:~/w/lpic/101$ sort what_i_have.txt | uniq
ball
glasses
laptop
socks
tshirt
jadi@funlife:~/w/lpic/101$
```

!!! note "نکته"
    همانطور که می‌بینید، ورودی باید مرتب باشد تا uniq کار کند.

uniq سوئیچ‌های عالی دارد:

```bash
jadi@funlife:~/w/lpic/101$ cat what_i_have.txt
laptop
socks
tshirt
ball
socks
glasses
jadi@funlife:~/w/lpic/101$ sort what_i_have.txt  | uniq -c  #show count of each item
      1 ball
      1 glasses
      1 laptop
      2 socks
      1 tshirt
jadi@funlife:~/w/lpic/101$ sort what_i_have.txt  | uniq -u #show only non-repeated items
ball
glasses
laptop
tshirt
jadi@funlife:~/w/lpic/101$ sort what_i_have.txt  | uniq -d #show only repeated items
socks
```

### paste

دستور paste خطوط از دو یا چند فایل را کنار هم می‌چسباند! شما نمی‌توانید این کار را در یک ویرایشگر متنی عمومی به راحتی انجام دهید!

```bash
jadi@funlife:~/w/lpic/101$ cat howcool
jadi    5
sina    6
rubic    2
you     12
jadi@funlife:~/w/lpic/101$ cat uses
you fedora
jadi ubuntu
rubic windows
neda mac
jadi@funlife:~/w/lpic/101$ paste howcool uses
jadi    5    you fedora
sina    6    jadi ubuntu
rubic    2    rubic windows
you     12    neda mac
```

### tr

دستور `tr` کاراکترها را در جریان _ترجمه_ می‌کند. مثلاً `tr 'ABC' '123'` A را با 1، B را با 2 و C را با 3 در جریان ارائه شده جایگزین می‌کند. این یک فیلتر خالص است و نام فایل ورودی را نمی‌پذیرد. اگر نیاز باشد می‌توانید cat را با آن pipe کنید (فصل 103.4 را ببینید).

```bash
jadi@funlife:~/w/lpic/101$ cat mydata
hello
this is the second line
but as you can see we are
still writing
and this is getting longer
.
.
and longer
and longer!
jadi@funlife:~/w/lpic/101$ cat mydata | tr 'and' 'AND'
hello
this is the second liNe
but As you cAN see we Are
still writiNg
AND this is gettiNg loNger
.
.
AND loNger
AND loNger!
```

!!! note "نکته"
    همه 'a'ها با 'A' جایگزین شده‌اند.

### sed

sed ویرایشگر جریان است. قدرتمند است و می‌تواند چیزهایی نزدیک به جادویی انجام دهد! درست مانند اکثر ابزارهایی که تا کنون دیده‌ایم، sed می‌تواند به عنوان فیلتر کار کند یا ورودی از یک فایل بگیرد. sed یک ابزار عالی برای جایگزینی متن با استفاده از **عبارات منظم** است. اگر نیاز به جایگزینی A با B فقط یک بار در هر خط در یک جریان دارید، فقط `sed 's/A/B/'` صادر کنید:

```bash
jadi@funlife:~/w/lpic/101$ cat uses
you fedora
jadi ubuntu
rubic windows
neda mac
jadi@funlife:~/w/lpic/101$ sed 's/ubuntu/debian/' uses
you fedora
jadi debian
rubic windows
neda mac
jadi@funlife:~/w/lpic/101$
```

الگوی تغییر EVERY رخداد A به B در یک خط `sed 's/A/B/g'` است.

کاراکترهای escape را به یاد دارید؟ آنها نیز اینجا کار می‌کنند و این هر new line را از یک فایل حذف می‌کند و آن را با space جایگزین می‌کند:

```bash
jadi@funlife:~/w/lpic/101$ cat mydata
hello
this is the second line
but as you can see we are
still writing
and this is getting longer
.
.
and longer
and longer!
jadi@funlife:~/w/lpic/101$ sed 's/ /\t/g' mydata > mydata.tab
jadi@funlife:~/w/lpic/101$ cat mydata.tab
hello
this    is the second    line
but    as    you    can    see    we    are
still    writing
and    this    is    getting    longer
.
.
and    longer
and    longer!
```

## گرفتن آمار (Getting stats)

### wc

`wc` شمارش کلمه است. خطوط، کلمات و بایت‌ها را در جریان ورودی شمارش می‌کند.

```bash
jadi@funlife:~/w/lpic/101$ wc mydata
  9  25 121 mydata
```

!!! note "نکته"
    بسیار رایج است که شماره خطوط را با سوئیچ `-l` شمارش کنید.

### -

باید بدانید که اگر `-` را به جای نام فایل قرار دهید، داده‌ها از pipe (یا stdin صفحه کلید) جایگزین می‌شوند.

```bash
jadi@funlife:~/w/lpic/101$ wc -l mydata | cat mydata - mydata  
hello
this is the second line
but as you can see we are
still writing
and this is getting longer
.
.
and longer
and longer!
9 mydata
hello
this is second line
but as you can see we are
still writing
and this is getting longer
.
.
and longer
and longer!
```

## هشینگ (Hashing)

یک تابع هش هر تابعی است که می‌تواند داده‌های اندازه دلخواه را به مقادیر اندازه ثابت نگاشت کند. هش‌های مختلفی وجود دارند و از آنها برای اهداف مختلف استفاده می‌کنیم. مثلاً یک سایت ممکن است رمز عبور شما را در پایگاه داده خود هش کند تا امن نگه دارد (و هش رمز عبور ارائه شده را با هشی که قبلاً در DB دارد در طول ورودها بررسی کند) یک سایت ممکن است هش یک فایل را ارائه دهد تا مطمئن شوید فایل صحیح را دانلود کرده‌اید و ...

الگوریتم‌های هشینگ پوشش داده شده در LPIC1 عبارتند از:

- md5sum
- sha256sum
- sha512sum

می‌توانید هر فایل (یا هش جریان‌های ورودی) را با چیزی شبیه به این بررسی کنید:

```bash
jadi@ocean:~$ md5sum /tmp/myfile.txt
8183aa57a23658efe7ba7aebe60816bc  /tmp/myfile.txt
jadi@ocean:~$ sha256sum /tmp/myfile.txt
7ddcfda184b55ee06b0c81e0ad136b1aa4a86daeb1078bcaeccc246eb2c8693b  /tmp/myfile.txt
jadi@ocean:~$ sha512sum /tmp/myfile.txt
79e5d789528e5e55fc1bddcb381afd56e896b1b452347a76777fb38d76c9754278700036f35df2a53c4d53d3e3623538a8b9ed155a3fd5275e667bdbf3c0b359  /tmp/myfile.txt
```

همانطور که می‌بینید، `sha512sum` یک هش طولانی‌تر ایجاد می‌کند که امن‌تر است.

## تمرین‌ها

1. محتوای یک فایل را با `cat` نمایش دهید.
2. 10 خط اول یک فایل را با `head` ببینید.
3. 10 خط آخر یک فایل را با `tail` ببینید.
4. خطوط یک فایل را مرتب کنید و تکراری‌ها را حذف کنید.
5. تعداد خطوط، کلمات و کاراکترهای یک فایل را شمارش کنید.
6. فیلد اول فایل `/etc/passwd` را استخراج کنید.
7. محتوای یک فایل را به حروف بزرگ تبدیل کنید.
8. خطوط یک فایل را شماره‌گذاری کنید.
9. از `sed` برای جایگزینی یک کلمه در یک فایل استفاده کنید.
10. دو فایل را با `paste` کنار هم قرار دهید.
11. هش MD5 یک فایل را محاسبه کنید.
12. یک فایل بزرگ را با `split` تقسیم کنید و سپس دوباره جمع کنید.

## خلاصه

در این فصل با پردازش جریان‌های متنی با استفاده از فیلترها آشنا شدیم. جریان‌ها ورودی‌ها و خروجی‌های استاندارد هستند که می‌توانیم آنها را دستکاری کنیم. ابزارهای مهمی مانند `cat`, `head`, `tail`, `sort`, `uniq`, `wc`, `cut`, `paste`, `tr`, `sed`, `nl`, `od`, `split`, `bzcat`, `xzcat`, `zcat`, `less` و ابزارهای هشینگ مانند `md5sum`, `sha256sum`, `sha512sum` را آموختیم. این ابزارها برای مشاهده، تغییر و تحلیل داده‌های متنی در خط فرمان ضروری هستند.
