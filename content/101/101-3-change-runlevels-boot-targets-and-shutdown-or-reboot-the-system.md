

# 101.3 - تغییر runlevelها / boot targets و خاموش یا ریبوت کردن سیستم

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- تغییر runlevel در SysVinit یا boot target در systemd  
- ورود به حالت تک‌کاربره (single-user mode)  
- خاموش و ریبوت کردن سیستم از خط فرمان  
- اطلاع‌رسانی به کاربران قبل از تغییر runlevel یا boot target  
- خاتمه صحیح پردازش‌ها هنگام تغییر سطح اجرا  
- تنظیم runlevel یا boot target پیش‌فرض  
- آشنایی با Upstart به عنوان جایگزین SysVinit یا systemd  
- آگاهی از ACPI برای مدیریت توان سیستم  

## کلیدواژه‌ها

`/etc/inittab`, `shutdown`, `init`, `/etc/init.d/`, `telinit`, `systemd`, `systemctl`, `/etc/systemd/`, `/usr/lib/systemd/`, `wall`, `runlevels`, `acpi`

---

## Runlevels

Runlevelها مشخص می‌کنند سیستم در چه حالت یا مرحله‌ای قرار دارد. می‌توانید آن را مثل "سطوح مختلف زنده بودن" سیستم در نظر بگیرید.

---

## Systemd Targets

در systemd به جای runlevelها از **targets** استفاده می‌شود که گروهی از سرویس‌ها هستند.

**لیست targets:**

```bash
systemctl list-units --type=target
```

نمونه خروجی روی Debian:

- `graphical.target` → رابط گرافیکی  
- `multi-user.target` → حالت چندکاربره با شبکه  
- `rescue` → حالت تعمیر با فایل‌سیستم محلی، بدون شبکه  
- `emergency` → فقط root filesystem به صورت read-only، بدون شبکه  
- `halt` → توقف پردازش‌ها و CPU  
- `poweroff` → مشابه halt اما با ارسال سیگنال ACPI برای خاموشی کامل  

**بررسی target پیش‌فرض:**

```bash
systemctl get-default
```

**تغییر target:**

```bash
systemctl isolate emergency
```

---

## SysV Runlevels

در سیستم‌های مبتنی بر SysV، runlevelها به شکل زیر تعریف می‌شوند:

- **Red Hat:**  
  - 0: خاموش  
  - 1: تک‌کاربره (S یا s)  
  - 2: چندکاربره بدون شبکه  
  - 3: چندکاربره با شبکه  
  - 4: قابل تنظیم توسط مدیر سیستم  
  - 5: چندکاربره با شبکه و گرافیک  
  - 6: ریبوت  

- **Debian:**  
  - 0: خاموش  
  - 1: تک‌کاربره  
  - 2: چندکاربره با گرافیک  
  - 6: ریبوت  

**بررسی runlevel فعلی:**

```bash
runlevel
```

**تغییر runlevel:**

```bash
telinit 5
```

**خاموش کردن سیستم:**

```bash
init 0
```

---

## فایل inittab

فایل `/etc/inittab` در SysVinit برای تعریف runlevel پیش‌فرض و رفتار init استفاده می‌شود.  

نمونه:

```bash
id:5:initdefault:
```

فرمت خطوط:

```
id:runlevels:action:process
```

- `id`: شناسه کوتاه  
- `runlevels`: سطح اجرا  
- `action`: نوع اجرا (respawn, wait, once, initdefault, ctrlaltdel)  
- `process`: دستور یا سرویس  

---

## مدیریت سرویس‌ها در SysVinit

فایل‌های کنترل سرویس‌ها در `/etc/init.d/` قرار دارند.  

**مثال:**

```bash
/etc/init.d/sshd start
/etc/init.d/sshd stop
/etc/init.d/sshd restart
```

یا با دستور `service`:

```bash
service sshd status
```

---

## خاموش و ریبوت کردن سیستم

روش ترجیحی استفاده از دستور `shutdown` است. این دستور:

- به کاربران هشدار می‌دهد (با `wall`)  
- ورود کاربران جدید غیر از root را مسدود می‌کند  
- سیگنال `SIGTERM` به پردازش‌ها می‌فرستد  
- پس از تأخیر مشخص، سیگنال `SIGKILL` ارسال می‌کند  

**مثال‌ها:**

```bash
shutdown -r now        # ریبوت فوری
shutdown -h +5 "System will halt"  # خاموشی در 5 دقیقه
shutdown -c            # لغو خاموشی
```

گزینه‌ها:  
- `-h` → خاموش  
- `-r` → ریبوت  
- `-t60` → تأخیر 60 ثانیه بین SIGTERM و SIGKILL  

---

## دستورات halt, reboot, poweroff

- `halt` → توقف پردازش‌ها  
- `poweroff` → توقف و ارسال سیگنال ACPI برای خاموشی کامل  
- `reboot` → توقف و راه‌اندازی مجدد  

در اکثر توزیع‌ها این دستورات لینک‌هایی به `systemctl` هستند.

---

## ACPI (Advanced Configuration and Power Interface)

ACPI استانداردی برای مدیریت توان و سخت‌افزار است.  
- مدیریت خواب سخت‌افزار  
- Plug and Play و hot-swap  
- مانیتورینگ وضعیت سیستم  
- ارسال سیگنال خاموشی از طریق دستوراتی مثل `shutdown`  

---

## اطلاع‌رسانی به کاربران

ابزارهای اطلاع‌رسانی:

- `wall` → ارسال پیام به همه کاربران وارد شده  
- `/etc/issue` → پیام قبل از ورود در ترمینال محلی  
- `/etc/issue.net` → پیام قبل از ورود در ترمینال راه دور  
- `/etc/motd` → پیام روز پس از ورود  
- `mesg` → کنترل دریافت پیام‌های wall (اما پیام‌های shutdown همیشه ارسال می‌شوند)  
- `systemctl` → ارسال پیام‌های wall هنگام emergency, halt, reboot, rescue  

---

## تمرین‌های عملی

### تمرین 1: بررسی runlevel یا target
```bash
runlevel
systemctl get-default
```

### تمرین 2: تغییر سطح اجرا
```bash
telinit 3
systemctl isolate multi-user.target
```

### تمرین 3: خاموش و ریبوت
```bash
shutdown -r now
shutdown -h +10 "System will halt in 10 minutes"
```

### تمرین 4: اطلاع‌رسانی به کاربران
```bash
wall "System maintenance in 5 minutes"
```

---

## خلاصه

در این فصل یاد گرفتیم:

- تفاوت runlevel در SysVinit و target در systemd  
- نحوه تغییر سطح اجرا و ورود به حالت تک‌کاربره  
- استفاده از `shutdown`, `halt`, `reboot`, `poweroff`  
- نقش ACPI در مدیریت توان و خاموشی سیستم  
- اطلاع‌رسانی به کاربران با ابزارهایی مثل `wall`, `/etc/motd`  
- ساختار فایل `/etc/inittab` و جایگزینی آن با systemd  

!!! example "نکات کلیدی برای آزمون"
    - تفاوت runlevelهای SysVinit و targetهای systemd  
    - دستورهای `shutdown` و گزینه‌های آن  
    - نقش ACPI در خاموشی سیستم  
    - ابزارهای اطلاع‌رسانی به کاربران  
    - PID فرآیند init همیشه 1 است  
؟
