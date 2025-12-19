# 104.3 - کنترل mount و unmount فایل‌سیستم‌ها

## اهداف یادگیری

در این درس یاد می‌گیرید چگونه فایل‌سیستم‌ها را به‌صورت دستی mount و unmount کنید، ماندگار کردن mount در بوت را پیکربندی کنید، و از UUID/Label برای شناسایی پایدار فایل‌سیستم‌ها استفاده کنید.

## کلیدواژه‌ها

`mount`, `umount`, `/etc/fstab`, `blkid`, `lsblk`, `findmnt`, `swapon`, `swapoff`, `x-systemd.automount`, `UUID`, `LABEL`

---

## ایدهٔ کلی و دستورهای پایه

برای دسترسی به محتوای یک پارتیشن آن را به یک دایرکتوری وصل می‌کنیم (mount point):

```bash
sudo mount -t ext4 /dev/sda3 /mnt/mydisk
```

با اجرای `mount` بدون پارامتر می‌توانید همهٔ mountهای فعلی را ببینید؛ برای باز کردن فایل ایزو از `-o loop` استفاده کنید:

```bash
sudo mount -o loop ~/image.iso /mnt/iso
```

برای جدا کردن از `umount` (دوست اشتباه‌گیر) استفاده کنید:

```bash
sudo umount /mnt/mydisk
```

---

## خطاهای رایج و راه‌حل‌ها (مسئله → رفع)

### مشکل: umount: target is busy

دلایل: باین‌برنامه/شل یا پروسه‌ای در آن دایرکتوری فعال است.

رفع:

- با `lsof +f -- /mnt/mydisk` یا `fuser -v /mnt/mydisk` ببینید چه فرایندهایی باز هستند.
- در صورت امکان فرایندها را ببندید یا با `sudo kill PID` خاتمه دهید.
- اگر نیاز به جدا کردن بدون بستن فرایندها دارید، از "lazy" unmount استفاده کنید: `sudo umount -l /mnt/mydisk` (با احتیاط).

!!! warning "هشدار: استفادهٔ نامناسب از unmount -l یا -f"
    `umount -l` و `umount -f` ممکن است داده‌ها را در شرایط خاص از بین ببرد یا وضعیت فایل‌سیستم را نامعلوم بگذارد؛ ابتدا تلاش کنید فرایندهای باز را ببندید و فقط در شرایط اضطراری از گزینه‌های اجباری استفاده کنید.

---

## استفاده از UUID / LABEL و `fstab`

برای جلوگیری از مشکل تغییر نام دستگاه‌ها (مثلاً /dev/sdb → /dev/sdc) بهتر است در `/etc/fstab` از `UUID=` یا `LABEL=` استفاده کنید. UUID دستگاه را با `blkid` یا `lsblk -o NAME,UUID,MOUNTPOINT` بیابید.

مثال یک سطر در `/etc/fstab`:

```fstab
UUID=4c1a51e6-47bf-4a34-84a2-87027c91e14a /data ext4 defaults 0 2
```

ستون‌ها معمولاً به‌صورت: device | mountpoint | type | options | dump | pass هستند.

!!! note "نکتهٔ عملی"
    پس از ویرایش `/etc/fstab` آن را با `sudo systemctl daemon-reload` و سپس `sudo mount -a` تست کنید؛ اگر خطایی وجود داشت از ورود اشتباه جلوگیری می‌شود. به‌جای `mount -a` می‌توانید فقط سطر جدید را `mount /mountpoint` کنید.

---

## گزینه‌های پرکاربرد mount و کاربردشان

- `-o remount,ro` — تغییر حالت (مثلاً readonly) بدون unmount مجدد
- `noauto` — مانع mount خودکار در بوت می‌شود
- `user` — اجازهٔ mount به کاربران غیر-root می‌دهد (با محدودیت‌ها)
- `users` — هر کاربری می‌تواند unmount کند
- `noexec`, `nosuid`, `nodev`, `noatime` — گزینه‌های امنیتی/عملیاتی

!!! tip "نکته"
    اگر می‌خواهید یک فایل‌سیستم شبکه‌ای به محض ضرورت mount شود، از option `x-systemd.automount` در `fstab` استفاده کنید تا systemd آن را روی‌درخواست mount کند و مشکلات زمان بوت با منابع شبکه‌ای را کاهش دهد.

---

## مدیریت swap

فضای swap با `mkswap` ایجاد و با `swapon` فعال می‌شود؛ برخلاف فایل‌سیستم‌ها، swap در `fstab` با نوع `swap` ثبت می‌شود:

```fstab
UUID=6a59cf20-8fd6-4d86-b044-89f7bc67993b none swap sw 0 0
```

برای غیرفعال‌کردن موقت swap: `sudo swapoff /dev/sda6` و برای فعال‌سازی دوباره `sudo swapon /dev/sda6`.

---

## ابزارهای بررسی و تایید

- `lsblk -f` و `blkid` برای پیدا کردن UUID/TYPE/LABEL
- `findmnt` برای دیدن درختی mountها و `findmnt --verify` برای بررسی `/etc/fstab`
- `mount -o remount,ro` برای تغییر حالت و `mount -a` برای تلاش mount همه‌ی سطرهای `fstab`

---

## چک‌لیست عملی

1. دستگاه را با `lsblk`/`blkid` شناسایی کنید.
2. اگر نیاز به فرمت یا ایجاد swap دارید، قبل از عملیات پشتیبان تهیه کنید و مطمئن شوید که target صحیح است.
3. برای mount دائمی از `UUID` در `/etc/fstab` استفاده کنید.
4. پس از ویرایش `fstab`: `sudo systemctl daemon-reload` و `sudo mount -a` یا `findmnt --verify` را اجرا کنید.
5. در صورت مواجهه با `target is busy`، از `lsof`/`fuser` برای پیدا کردن فرایندها استفاده کنید.

---

## تمرین‌ها

1. یک فایل ایمیج 100MiB بسازید و با `mke2fs` آن را فرمت کنید؛ سپس آن را با `-o loop` mount کرده و محتوا را بررسی کنید.
2. یک ورودی در `/etc/fstab` با استفاده از `UUID` اضافه کنید، `systemctl daemon-reload` و `mount -a` را اجرا کنید و صحت کار را با `findmnt` بررسی کنید.

---

## خلاصه

این درس چگونگی mount و unmount فایل‌سیستم‌ها، کار با `/etc/fstab`، استفاده از UUID/LABEL و راه‌حل‌های خطاهای رایج مثل "target is busy" را پوشش داد. همیشه قبل از تغییرات حیاتی از داده‌ها پشتیبان تهیه کنید و تنظیمات `fstab` را پیش از reboot اعتبارسنجی کنید.

!!! example "نکات کلیدی برای آزمون"
    - دستورهای پایه: `mount`, `umount`, `mount -o loop`, `swapon`/`swapoff`
    - `fstab` ستون‌ها: device | mountpoint | type | options | dump | pass
    - استفاده از `UUID` یا `LABEL` برای پایداری در /etc/fstab
    - نحوهٔ مقابله با خطای "target is busy": `lsof` / `fuser`، سپس unmount یا `umount -l` (با احتیاط)
    - تفاوت `user` و `users` در options و کاربرد `x-systemd.automount` برای mount روی‌درخواست
