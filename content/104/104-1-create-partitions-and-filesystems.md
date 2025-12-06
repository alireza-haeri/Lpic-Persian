# 104.1 - ایجاد پارتیشن‌ها و فایل‌سیستم‌ها

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- مدیریت پارتیشن‌های MBR و GPT
- ایجاد فایل‌سیستم‌های مختلف
- درک ساختار دیسک و پارتیشن‌بندی

## کلیدواژه‌ها

`fdisk`, `gdisk`, `parted`, `mkfs`, `mkswap`, `tune2fs`, `dumpe2fs`

---

## پارتیشن‌بندی

### ابزارها

- `fdisk`: برای MBR
- `gdisk`: برای GPT
- `parted`: پیشرفته

### ایجاد پارتیشن

```bash
$ fdisk /dev/sda
```

داخل fdisk: n برای جدید، p برای primary، اندازه، w برای نوشتن.

### فایل‌سیستم‌ها

```bash
$ mkfs.ext4 /dev/sda1
$ mkfs.xfs /dev/sda2
$ mkswap /dev/sda3
$ swapon /dev/sda3
```

### تنظیمات فایل‌سیستم

```bash
$ tune2fs -l /dev/sda1  # اطلاعات
$ dumpe2fs /dev/sda1
```