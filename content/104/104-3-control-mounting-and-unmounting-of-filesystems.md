# 104.3 - کنترل mount و unmount فایل‌سیستم‌ها

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- mount و unmount فایل‌سیستم‌ها
- مدیریت /etc/fstab
- درک نقاط mount

## کلیدواژه‌ها

`mount`, `umount`, `/etc/fstab`, `/etc/mtab`, `/proc/mounts`

---

## mount

```bash
$ mount /dev/sda1 /mnt
$ mount -t ext4 /dev/sda1 /mnt
$ mount -o ro /dev/sda1 /mnt  # read-only
```

## unmount

```bash
$ umount /mnt
$ umount /dev/sda1
```

## /etc/fstab

فایل تنظیمات mount خودکار.

فرمت: device mountpoint fstype options dump pass

مثال:

```
/dev/sda1 / ext4 defaults 0 1
```

## نمایش mountها

```bash
$ mount
$ cat /etc/mtab
$ cat /proc/mounts
```