# 102.4 - مدیریت بسته‌ها در Debian (Debian Package Management)

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- نصب، ارتقا و حذف بسته‌های باینری Debian
- جستجوی بسته‌ها و فایل‌های مرتبط
- بررسی اطلاعات بسته‌ها (نسخه، محتوا، وابستگی‌ها، وضعیت نصب)
- آشنایی با apt

## کلیدواژه‌ها

`apt-get`, `apt-cache`, `dpkg`, `/etc/apt/sources.list`, `dpkg-reconfigure`

---

## مفهوم سیستم مدیریت بسته‌ها

برخی فکر می‌کنند که در GNU/Linux باید همه نرم‌افزارها را دستی کامپایل کنیم. این در 99% موارد درست نیست و هرگز در 20 سال گذشته درست نبوده است. GNU/Linux پیشرو چیزی است که امروزه App Store می‌نامیم. همه توزیع‌های بزرگ آرشیوهای بزرگی از نرم‌افزارهای از پیش کامپایل‌شده به نام **repositories** دارند و نوعی نرم‌افزار **package manager** که مسئول جستجو در این repositories، نصب نرم‌افزار از آنها، یافتن وابستگی‌ها، نصب آنها، حل تعارض‌ها و به‌روزرسانی سیستم و نرم‌افزارهای نصب شده است. توزیع‌های مبتنی بر Debian از فایل‌های `.deb` به عنوان "بسته‌ها" استفاده می‌کنند و از ابزارهایی مانند `apt-get`, `dpkg`, `apt` و ابزارهای دیگر برای مدیریت آنها استفاده می‌کنند.

بسته‌های Debian نام‌هایی مانند `NAME-VERSION-RELEASE_ARCHITECTURE.deb` دارند؛ مثلاً `tmux_3.2a-4build1_amd64.deb`.

!!! info "نکته"
    بسته‌های Debian با پسوند `.deb` شناخته می‌شوند.

---

## مخازن (Repositories)

اما این بسته از کجا آمده است؟ چگونه OS می‌داند کجا به دنبال این بسته deb بگردد؟ پاسخ **Repositories** است. هر توزیع repository بسته‌های خود را دارد. می‌تواند روی دیسک، درایو شبکه، مجموعه DVDها یا معمولاً آدرس شبکه روی اینترنت باشد.

در سیستم‌های debian، مکان‌های پیکربندی اصلی عبارتند از:

- `/etc/apt/sources.list`
- `/etc/apt/sources.list.d/`

**نمونه:**

```bash
deb http://us.archive.ubuntu.com/ubuntu/ jammy main restricted
deb http://security.ubuntu.com/ubuntu jammy-security universe
```

### به‌روزرسانی اطلاعات مخازن

```bash
apt-get update
```

- فقط اطلاعات بسته‌ها را به‌روز می‌کند.
- بسته‌ها را ارتقا نمی‌دهد.

!!! tip "نکته"
    این فقط اطلاعات بسته‌ها را به‌روز می‌کند و نه خود بسته‌ها.

---

## نصب بسته‌ها

فرض کنید درباره این multiplexer ترمینال شگفت‌انگیز به نام `tmux` شنیده‌اید و می‌خواهید آن را امتحان کنید.

```bash
$ tmux
The program 'tmux' is currently not installed. You can install it by typing:
sudo apt-get install tmux
$ which tmux
$ type tmux
bash: type: tmux: not found
```

پس بیایید آن را نصب کنیم. اگر در repositories باشد، کافی است به package manager بگویید آن را نصب کند:

```bash
apt-get install tmux
```

توجه کنید که

- apt-get install درخواست تأیید کرد (Y)
- apt-get وابستگی‌ها را حل کرد، می‌داند چه چیزی برای نصب این بسته نیاز است و آنها را نصب می‌کند
- بسته‌های Debian چیزی.deb هستند

اگر فقط می‌خواهید dry-run/simulation:

```bash
apt-get install --dry-run tmux
```

### ارتقا بسته‌ها

برای ارتقا بسته‌ها:

```bash
apt-get upgrade
```

این همه بسته‌های نصب شده را ارتقا می‌دهد اگر نسخه جدیدتری در repositories موجود باشد.

برای ارتقای توزیع:

```bash
apt-get dist-upgrade
```

### حذف بسته‌ها

```bash
apt-get remove tmux
```

برای حذف کامل با فایل‌های پیکربندی:

```bash
apt-get purge tmux
```

یا

```bash
apt-get remove --purge tmux
```

---

## جستجو و اطلاعات بسته‌ها

### جستجوی بسته‌ها

```bash
apt-cache search tmux
```

### نمایش اطلاعات بسته

```bash
apt-cache show tmux
```

این نسخه، وابستگی‌ها، توضیحات و غیره را نشان می‌دهد.

### یافتن بسته‌ای که فایل خاصی را فراهم می‌کند

```bash
apt-file search /bin/tmux
```

یا

```bash
dpkg -S /bin/tmux
```

---

## dpkg

dpkg ابزار سطح پایین‌تر است.

### نصب بسته deb

```bash
dpkg -i package.deb
```

### لیست بسته‌های نصب شده

```bash
dpkg -l
```

### اطلاعات بسته

```bash
dpkg -I package.deb
dpkg -s package_name
```

### حذف بسته

```bash
dpkg -r package_name
```

### لیست فایل‌های بسته

```bash
dpkg -L package_name
```

---

## dpkg-reconfigure

برای پیکربندی مجدد بسته‌ها:

```bash
dpkg-reconfigure tzdata
```

---

## apt

apt نسخه جدیدتر apt-get است.

```bash
apt update
apt install tmux
apt remove tmux
apt search tmux
apt show tmux
```

---

## تمرین‌ها

### تمرین 1: به‌روزرسانی لیست بسته‌ها

```bash
sudo apt-get update
```

### تمرین 2: نصب بسته

```bash
sudo apt-get install htop
```

### تمرین 3: جستجوی بسته

```bash
apt-cache search editor
```

### تمرین 4: بررسی وضعیت بسته

```bash
dpkg -s vim
```

### تمرین 5: حذف بسته

```bash
sudo apt-get remove htop
```

---

## خلاصه

در این فصل یاد گرفتیم:

- مفهوم repositories و بسته‌های .deb
- پیکربندی `/etc/apt/sources.list`
- استفاده از apt-get برای نصب، ارتقا و حذف
- جستجو با apt-cache
- ابزار dpkg برای مدیریت سطح پایین
- تفاوت apt و apt-get

!!! example "نکات کلیدی برای آزمون"
    - ساختار فایل sources.list
    - تفاوت apt-get update و upgrade
    - حل وابستگی‌ها
    - استفاده از dpkg برای بسته‌های محلی
    - جستجوی فایل‌ها در بسته‌ها  

---

## نصب بسته‌ها  

```bash
apt-get install tmux
apt-get install -s tmux          # شبیه‌سازی نصب
apt-get install --download-only tmux
apt-get download tmux
```

!!! tip "نکته"  
    بسته‌ها پس از دانلود در مسیر `/var/cache/apt/archive/` ذخیره می‌شوند.  

---

## حذف بسته‌ها  

```bash
apt-get remove tmux
apt-get autoremove tmux
```

!!! warning "هشدار"  
    حذف یک بسته وابستگی‌هایش را حذف نمی‌کند، مگر با `autoremove`.  

---

## جستجوی بسته‌ها  

```bash
apt-cache search "tiny window"
apt search grub2
```

---

## ارتقا بسته‌ها  

```bash
apt-get upgrade
apt-get dist-upgrade
```

- `upgrade`: ارتقای بسته‌های نصب‌شده  
- `dist-upgrade`: ارتقای نسخه‌ی توزیع  

---

## پیکربندی مجدد بسته‌ها  

```bash
dpkg-reconfigure tzdata
```

---

## کار با dpkg  

```bash
dpkg -i package.deb        # نصب بدون وابستگی‌ها
dpkg -s bzr                # وضعیت بسته
dpkg -L bzr                # فایل‌های نصب‌شده
dpkg -S /path/to/file      # بسته مالک فایل
dpkg --contents package.deb # محتوای بسته
```

---

## گزینه‌های پرکاربرد apt-get  

- `update` → به‌روزرسانی اطلاعات بسته‌ها  
- `upgrade` → ارتقای همه بسته‌ها  
- `install` → نصب یا ارتقا بسته‌ها  
- `remove` → حذف بسته‌ها  
- `dist-upgrade` → ارتقای نسخه توزیع  
- `clean` → پاک‌سازی کش بسته‌ها  

---

## تمرین‌های عملی  

### تمرین 1: نصب یک بسته  
```bash
sudo apt-get install htop
```

### تمرین 2: بررسی فایل‌های یک بسته  
```bash
dpkg -L htop
```

### تمرین 3: جستجوی بسته‌های مرتبط با شبکه  
```bash
apt-cache search network
```

### تمرین 4: پیکربندی مجدد یک بسته  
```bash
dpkg-reconfigure tzdata
```

---

## خلاصه  

در این فصل یاد گرفتیم:  

- مفهوم مخازن و فایل‌های پیکربندی `/etc/apt/sources.list`  
- تفاوت `apt-get update` و `apt-get upgrade`  
- نصب، حذف و جستجوی بسته‌ها با `apt-get` و `apt-cache`  
- استفاده از `dpkg` برای بررسی و مدیریت بسته‌ها  
- پیکربندی مجدد بسته‌ها با `dpkg-reconfigure`  

!!! example "نکات کلیدی برای آزمون"  
    - تفاوت `update` و `upgrade`  
    - مسیرهای پیکربندی مخازن (`/etc/apt/sources.list`)  
    - دستورهای `apt-get`, `apt-cache`, `dpkg`  
    - مفهوم `autoremove` و نقش آن در حذف وابستگی‌ها  
    - ساختار نام بسته‌های Debian با پسوند `.deb`  
