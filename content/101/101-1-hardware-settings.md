# 101.1 - تشخیص و پیکربندی تنظیمات سخت‌افزار

**وزن:** 2

---

## اهداف درس

در این درس یاد می‌گیریم:

- چطور peripheral های یکپارچه رو فعال/غیرفعال کنیم
- تفاوت انواع دستگاه‌های ذخیره‌سازی
- چطور منابع سخت‌افزاری رو تشخیص بدیم
- ابزارهای مهم مثل `lsusb`, `lspci`, `lsmod`

---

## مفاهیم کلیدی

- `lsusb` - لیست دستگاه‌های USB
- `lspci` - لیست دستگاه‌های PCI
- `lsmod` - لیست ماژول‌های کرنل
- `modprobe` - مدیریت ماژول‌ها
- `sysfs`, `udev`, `dbus`
- مسیرهای `/sys`, `/proc`, `/dev`

---

## توضیحات

### سیستم عامل چیست؟

سیستم عامل (Operating System) نرم‌افزاری است که:

- منابع سخت‌افزاری رو مدیریت می‌کنه
- واسط بین برنامه‌ها و سخت‌افزار هست
- خدمات مشترک به برنامه‌ها ارائه می‌ده

---

### Firmware

Firmware نرم‌افزاری هست که روی سخت‌افزار اجرا میشه. مثل یه سیستم عامل کوچک برای خود سخت‌افزار.

**انواع Firmware:**

1. **BIOS** - قدیمی و منسوخ شده
2. **UEFI** - استاندارد جدید

---

### دستگاه‌های جانبی (Peripheral Devices)

#### PCI
رابط اتصال قطعات جانبی. اکثر سرورها از PCIe استفاده می‌کنند.

#### هارد دیسک داخلی
- **PATA** - قدیمی
- **SATA** - سریال، تا 4 دستگاه
- **SCSI** - موازی، تا 8 دستگاه

#### USB
Universal Serial Bus - رابط سریال با اتصالات کمتر.

**نسخه‌ها:**
- USB 1: 12Mbps
- USB 2: 480Mbps  
- USB 3: 5-40Gbps

---

## دستورات مهم

### lspci - نمایش دستگاه‌های PCI

نمایش دستگاه‌های PCI متصل به کامپیوتر:

    lspci

**خروجی نمونه:**

    00:00.0 Host bridge: Intel Corporation 2nd Generation...
    00:02.0 VGA compatible controller: Intel Corporation...
    00:19.0 Ethernet controller: Intel Corporation 82579LM...

---

### lsusb - نمایش دستگاه‌های USB

نمایش تمام دستگاه‌های USB:

    lsusb

**خروجی نمونه:**

    Bus 002 Device 003: ID 1c4f:0026 SiGma Micro Keyboard
    Bus 001 Device 005: ID 04f2:b217 Chicony Electronics Camera

---

### lsmod - لیست ماژول‌های کرنل

نمایش ماژول‌های بارگذاری شده در کرنل:

    lsmod

**خروجی نمونه:**

    Module                  Size  Used by
    bluetooth             446190  22
    uvcvideo               81065  0
    iwlwifi               183038  1

---

### modprobe - مدیریت ماژول‌ها

**بارگذاری ماژول:**

    modprobe iwlwifi

**حذف ماژول:**

    modprobe -r iwlwifi

**حذف اجباری:**

    modprobe -rf iwlwifi

---

### lsblk - لیست Block Devices

نمایش دستگاه‌های بلوکی:

    lsblk

---

## مسیرهای مهم

### /sys - Sysfs

سیستم فایل مجازی که اطلاعات کرنل و سخت‌افزار رو نگه می‌داره.

    ls /sys

**محتویات:**
- `block` - دستگاه‌های بلوکی
- `bus` - دستگاه‌های PCI, USB, ...
- `class` - کلاس‌بندی دستگاه‌ها

---

### /proc - Process Information

اطلاعات کرنل و پروسس‌ها:

    ls /proc

**فایل‌های مهم:**
- `/proc/cpuinfo` - اطلاعات CPU
- `/proc/meminfo` - اطلاعات حافظه
- `/proc/modules` - ماژول‌های بارگذاری شده

**مثال:**

    cat /proc/cpuinfo

---

### /dev - Device Files

فایل‌های دستگاه:

    ls /dev

**مثال‌ها:**
- `/dev/sda` - اولین هارد دیسک
- `/dev/sda1` - اولین پارتیشن
- `/dev/tty1` - ترمینال اول

---

## udev

مدیریت‌کننده دستگاه‌ها در فضای کاربری (userspace).

**وظایف:**
- مدیریت `/dev`
- بارگذاری firmware
- اجرای قوانین هنگام اتصال دستگاه

---

## مثال‌های عملی

### مثال ۱: بررسی CPU

    cat /proc/cpuinfo

### مثال ۲: بررسی حافظه

    cat /proc/meminfo

### مثال ۳: بررسی پورت‌های I/O

    cat /proc/ioports

### مثال ۴: بررسی ماژول خاص

    modinfo iwlwifi

---

## تمرین‌ها

1. لیست تمام دستگاه‌های PCI متصل به سیستم
2. بررسی اطلاعات CPU از `/proc/cpuinfo`
3. یک ماژول کرنل رو حذف و دوباره اضافه کن
4. بررسی کن چند پورت USB داری
5. پیدا کن هارد دیسک اصلی سیستمت چیه

---

## نکات امتحانی

- **وزن:** 2
- **موضوعات کلیدی:** `lspci`, `lsusb`, `lsmod`, `modprobe`
- **مسیرهای مهم:** `/sys`, `/proc`, `/dev`
- **مفاهیم:** BIOS vs UEFI, USB versions, PCI

---

## منابع

- [LPIC-1 Official Site](https://www.lpi.org)
- [Linux Kernel Documentation](https://kernel.org/doc)
- [LPIC-1 Book](https://lpic1book.github.io)

---

**نویسنده:** Alireza Haeri  
**آخرین به‌روزرسانی:** 2025