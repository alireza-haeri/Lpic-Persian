# 102.4 - مدیریت بسته‌ها در Debian (Debian Package Management)

## اهداف یادگیری  

در این فصل با موارد زیر آشنا می‌شوید:  

- نصب، ارتقا و حذف بسته‌های باینری Debian  
- جستجوی بسته‌ها و فایل‌های مرتبط  
- بررسی اطلاعات بسته‌ها (نسخه، وابستگی‌ها، وضعیت نصب)  
- آشنایی با ابزارهای `apt` و `dpkg`  

## کلیدواژه‌ها  

`apt-get`, `apt-cache`, `dpkg`, `/etc/apt/sources.list`, `dpkg-reconfigure`  

---

## مفهوم سیستم مدیریت بسته‌ها  

در لینوکس نیازی به کامپایل دستی همه نرم‌افزارها نیست. توزیع‌های بزرگ دارای **مخازن نرم‌افزاری (Repositories)** هستند که شامل بسته‌های از پیش کامپایل‌شده‌اند. ابزارهای مدیریت بسته مانند `apt-get` و `dpkg` وظیفه‌ی نصب، ارتقا، بررسی وابستگی‌ها و رفع تعارض‌ها را بر عهده دارند.  

!!! info "نکته"  
    بسته‌های Debian با پسوند `.deb` شناخته می‌شوند. مثال:  
    ```
    tmux_3.2a-4build1_amd64.deb
    ```

---

## فایل‌های پیکربندی مخازن  

- `/etc/apt/sources.list`  
- `/etc/apt/sources.list.d/`  

**نمونه:**  
```bash
deb http://us.archive.ubuntu.com/ubuntu/ jammy main restricted
deb http://security.ubuntu.com/ubuntu jammy-security universe
```

---

## به‌روزرسانی اطلاعات مخازن  

```bash
apt-get update
```

- فقط اطلاعات بسته‌ها را به‌روز می‌کند.  
- بسته‌ها را ارتقا نمی‌دهد.  

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
