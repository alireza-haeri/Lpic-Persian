# 102.5 - مدیریت بسته‌ها با RPM و YUM

## اهداف یادگیری  

در این فصل با موارد زیر آشنا می‌شوید:  

- نصب، بازنصب، ارتقا و حذف بسته‌ها با استفاده از RPM، YUM و Zypper  
- دریافت اطلاعات بسته‌ها (نسخه، وضعیت، وابستگی‌ها، امضاها و صحت)  
- یافتن فایل‌های ارائه‌شده توسط یک بسته یا تشخیص بسته‌ی مالک یک فایل خاص  
- آشنایی با ابزارهای `dnf` در سیستم‌های جدید  

## کلیدواژه‌ها  

`rpm`, `yum`, `zypper`, `rpm2cpio`, `/etc/yum.conf`, `/etc/yum.repos.d/`  

---

## معرفی  

در توزیع‌های مبتنی بر RedHat (مثل Fedora، RHEL، CentOS) مدیریت بسته‌ها با **RPM** و **YUM** انجام می‌شود.  
- **RPM (RedHat Package Manager):** مدیریت مستقیم فایل‌های `.rpm`  
- **YUM (Yellowdog Updater, Modified):** مدیریت بسته‌ها از طریق مخازن و وابستگی‌ها  
- **Zypper:** ابزار مدیریت بسته در openSUSE و SUSE Linux  

!!! info "نکته"  
    در Fedora ابزار پیش‌فرض **dnf** است که دستورات `yum` را به معادل‌های خود ترجمه می‌کند.  

---

## پیکربندی YUM  

- فایل اصلی: `/etc/yum.conf`  
- فایل‌های مخزن: `/etc/yum.repos.d/`  

**نمونه:**  
```bash
cat /etc/yum.conf
[main]
cachedir=/var/cache/yum/$basearch/$releasever
gpgcheck=1
plugins=1
installonly_limit=3
```

---

## دستورات پرکاربرد YUM  

- `yum install PACKAGE` → نصب بسته  
- `yum update` → به‌روزرسانی بسته‌ها  
- `yum remove PACKAGE` → حذف بسته  
- `yum info PACKAGE` → نمایش اطلاعات بسته  
- `yum search KEYWORD` → جستجو در مخازن  
- `yum provides /path/to/file` → یافتن بسته‌ی مالک یک فایل  
- `yum groupinstall "KDE Plasma Workspaces"` → نصب گروهی بسته‌ها  

!!! tip "ترفند"  
    گزینه‌ی `-y` برای پاسخ خودکار "Yes" به پرسش‌ها استفاده می‌شود.  

---

## ابزار yumdownloader  

دانلود بسته‌ها بدون نصب:  
```bash
yumdownloader --resolve PACKAGE
```

---

## مدیریت بسته‌ها با RPM  

فرمت کلی:  
```bash
rpm ACTION [OPTIONS] package.rpm
```

### دستورات مهم  
- `rpm -i` → نصب بسته  
- `rpm -U` → نصب یا ارتقا  
- `rpm -e` → حذف بسته  
- `rpm -q` → پرس‌وجو وضعیت بسته  
- `rpm -V` → بررسی صحت نصب  
- `rpm -K` → بررسی امضای بسته  

!!! warning "هشدار"  
    استفاده از گزینه‌های `--nodeps` یا `--force` فقط در شرایط خاص توصیه می‌شود.  

---

## پرس‌وجو با RPM  

- `rpm -q PACKAGE` → بررسی نصب بودن بسته  
- `rpm -qi PACKAGE` → اطلاعات کامل بسته  
- `rpm -ql PACKAGE` → لیست فایل‌های نصب‌شده  
- `rpm -qf /path/to/file` → یافتن بسته‌ی مالک فایل  
- `rpm -qR PACKAGE` → نمایش وابستگی‌ها  

---

## بررسی و صحت بسته‌ها  

```bash
rpm -V tmux
```

خروجی نشان‌دهنده‌ی تغییرات در اندازه، مجوزها، هش و مالکیت فایل‌هاست.  

---

## استخراج فایل‌های RPM  

```bash
rpm2cpio package.rpm > package.cpio
cpio -idv < package.cpio
```

---

## مدیریت بسته‌ها با Zypper  

- `zypper install PACKAGE` → نصب بسته  
- `zypper remove PACKAGE` → حذف بسته  
- `zypper search KEYWORD` → جستجو  
- `zypper info PACKAGE` → اطلاعات بسته  
- `zypper update` → ارتقا بسته‌ها  
- `zypper lr` → نمایش مخازن  

---

## تمرین‌های عملی  

### تمرین 1: نصب یک بسته با YUM  
```bash
sudo yum install nano
```

### تمرین 2: پرس‌وجو فایل‌های یک بسته با RPM  
```bash
rpm -ql nano
```

### تمرین 3: جستجوی بسته با Zypper  
```bash
zypper se tmux
```

### تمرین 4: بررسی صحت یک بسته  
```bash
rpm -V nano
```

---

## خلاصه  

در این فصل یاد گرفتیم:  

- تفاوت ابزارهای RPM، YUM و Zypper  
- ساختار فایل‌های پیکربندی YUM و مخازن  
- دستورات پرکاربرد برای نصب، حذف، ارتقا و جستجوی بسته‌ها  
- بررسی وابستگی‌ها و صحت بسته‌ها با `rpm`  
- استخراج فایل‌های RPM با `rpm2cpio`  
- استفاده از Zypper در openSUSE  

!!! example "نکات کلیدی برای آزمون"  
    - تفاوت RPM و YUM  
    - مسیرهای پیکربندی YUM (`/etc/yum.conf`, `/etc/yum.repos.d/`)  
    - دستورات `rpm -i`, `rpm -U`, `rpm -e`, `rpm -q`  
    - نقش `yum provides` در یافتن بسته‌ی مالک فایل  
    - دستورات اصلی Zypper (`install`, `remove`, `search`)  
