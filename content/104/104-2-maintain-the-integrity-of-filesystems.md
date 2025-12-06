# 104.2 - حفظ یکپارچگی فایل‌سیستم‌ها

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- بررسی و تعمیر فایل‌سیستم‌ها
- استفاده از ابزارهای تشخیصی

## کلیدواژه‌ها

`fsck`, `e2fsck`, `xfs_repair`, `debugfs`

---

## بررسی فایل‌سیستم‌ها

### fsck

```bash
$ fsck /dev/sda1
$ fsck -y /dev/sda1  # پاسخ خودکار yes
```

### e2fsck برای ext

```bash
$ e2fsck /dev/sda1
```

### xfs_repair برای XFS

```bash
$ xfs_repair /dev/sda2
```

### debugfs

```bash
$ debugfs /dev/sda1
debugfs: ls
```