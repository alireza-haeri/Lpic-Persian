# 102.2 - نصب Boot Manager

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- فراهم کردن مکان‌های بوت جایگزین و گزینه‌های بوت پشتیبان
- نصب و پیکربندی یک بوت لودر مانند GRUB Legacy
- انجام تغییرات پیکربندی پایه برای GRUB 2
- تعامل با بوت لودر

## کلیدواژه‌ها

`menu.lst`, `grub.cfg`, `grub.conf`, `grub-install`, `grub-mkconfig`, `MBR`, `chainloader`

---

## مرور فرآیند بوت

اکثر سیستم‌ها از BIOS یا UEFI استفاده می‌کنند. در BIOS، سیستم یک تست خودکار به نام POST (Power-On Self-Test) انجام می‌دهد. سپس کنترل بوت را به اولین سکتور Master Boot Record (MBR) که track (Cylinder) 0، side (Head) 0 و Sector 1 اولین دیسک است، منتقل می‌کند.

MBR فقط 512 بایت است، بنابراین نیاز به یک **بوت لودر هوشمند** داریم تا بوت لودرهای بزرگ‌تر و حتی سیستم‌های چندگانه را مدیریت کند. برخی از این بوت لودرها LILO، GRUB و GRUB2 هستند.

اگر سیستم از UEFI استفاده کند، سخت‌افزار مراحل UEFI را دنبال می‌کند. آنها با یک مرحله امنیتی شروع می‌شوند و تا مرحله پایانی ادامه می‌دهند که UEFI به دنبال یک EFI System Partition می‌گردد، که فقط یک پارتیشن FAT32 است (معمولاً اولین، اما تعریف پیاده‌سازی است) با اجرایی‌های PE و آنها را اجرا می‌کند.

در هر دو حالت، باینری بوت لودر را شروع می‌کند. ممکن است یک بوت لودر کامل روی `/boot/efi/` کامپیوتر شما باشد یا یک لودر کوچک برای grub اصلی روی MBR یا یک لودر ویندوز یا حتی یک chainloader.

!!! note "نکته"
    Chain Loading زمانی است که یک بوت لودر، بوت لودر دیگری را بارگذاری می‌کند. این زمانی انجام می‌شود که یک بوت لودر لینوکس نیاز به شروع یک سیستم ویندوز دارد.

---

## GRUB

**GRUB** (**GR**and **U**nified **B**ootloader) شروع به جایگزینی LILO قدیمی کرد. نسخه اول (1) Grub Legacy نامیده می‌شود و از 1999 شروع شد. نسخه دوم از 2005 شروع شد و بازنویسی کامل نسخه 1 است.

این یک سیستم مبتنی بر منو است که می‌توانید انتخاب کنید کدام کرنل یا chainloader بوت شود. همچنین امکان ویرایش منوها در لحظه یا دادن دستورات مستقیم از خط فرمان وجود دارد.

### Grub Legacy

معمولاً GRUB v1 (در واقع 0.9) در `/boot/grub` نصب می‌شود. پیکربندی اصلی آن در `/boot/grub/menu.lst` است اما امروزه برخی توزیع‌ها (شامل RedHat Based) این را به `/boot/grub/grub.conf` لینک می‌کنند.

یک نمونه فایل `menu.lst` / `grub.conf` برای GRUB legacy شامل دو بخش است. بخش اول شامل پیکربندی‌های جهانی است و بخش دوم گزینه‌های مختلف کرنل/initram یا chainloader را تعریف می‌کند.

پیکربندی‌های جهانی عبارتند از:

| پیکربندی | توضیح |
|-----------|-------|
| # | کامنت |
| color | رنگ‌های پیش‌زمینه و پس‌زمینه برای آیتم‌های عادی و فعال |
| default | کدام آیتم منوی بوت پیش‌فرض است |
| fallback | کدام منوی بوت باید استفاده شود اگر default شکست خورد |
| hiddenmenu | پنهان کردن گزینه‌های منو |
| splashimage | نمایش این تصویر در پس‌زمینه! |
| timeout | این مقدار صبر کن و سپس پیش‌فرض را شروع کن |
| password | امنیت مهم است! این رمز عبور را می‌پرسد |
| savedefault | آخرین آیتم بوت شده را به یاد بسپار |

در بخش دوم پیکربندی، این‌ها داریم:

| پیکربندی | توضیح |
|-----------|-------|
| title | نام بخش را تعریف می‌کند |
| root | دیسک و پارتیشن که دایرکتوری `/boot` در آن است. به شکل (hddrive, partition)، مانند (hd0, 0) یا (hd0, msdos0) |
| kernel | نام فایل تصویر کرنل در `/boot` |
| initrd | فایل Initramfs در `/boot` |
| rootnoverify | یک پارتیشن root غیر-لینوکس تعریف می‌کند |
| chainloader | بوت لودر دیگری را بارگذاری می‌کند |

### نصب Grub Legacy

برای نصب GRUB Legacy روی MBR:

```bash
grub-install /dev/sda
```

این دستور فایل‌های GRUB را در `/boot/grub` کپی می‌کند و مرحله 1 را در MBR نصب می‌کند.

### GRUB 2

GRUB 2 (که اکنون فقط GRUB نامیده می‌شود) پیچیده‌تر است اما انعطاف‌پذیرتر. پیکربندی اصلی در `/boot/grub/grub.cfg` است، اما این فایل توسط اسکریپت‌ها تولید می‌شود و نباید مستقیماً ویرایش شود.

پیکربندی واقعی در `/etc/default/grub` و فایل‌های `/etc/grub.d/` است.

برای تولید `grub.cfg`:

```bash
grub-mkconfig -o /boot/grub/grub.cfg
```

یا در برخی توزیع‌ها:

```bash
update-grub
```

### تعامل با GRUB

در منوی GRUB، می‌توانید:

- کلیدهای جهت‌دار برای انتخاب
- 'e' برای ویرایش آیتم انتخاب شده
- 'c' برای خط فرمان GRUB

در خط فرمان GRUB، دستوراتی مانند `ls`, `set`, `linux`, `initrd`, `boot` وجود دارد.

### گزینه‌های بوت پشتیبان

برای فراهم کردن گزینه‌های پشتیبان، می‌توانید چندین ورودی در منوی GRUB داشته باشید، مانند کرنل‌های مختلف یا chainloader برای ویندوز.

همچنین می‌توانید از `grub-install` برای نصب روی چندین دیسک استفاده کنید.

### مثال‌ها

#### نصب GRUB 2

```bash
# نصب روی MBR
grub-install /dev/sda

# تولید پیکربندی
grub-mkconfig -o /boot/grub/grub.cfg
```

#### ویرایش /etc/default/grub

```bash
GRUB_DEFAULT=0
GRUB_TIMEOUT=5
GRUB_CMDLINE_LINUX_DEFAULT="quiet splash"
```

#### Chainloading ویندوز

در `grub.cfg`:

```
menuentry "Windows" {
    insmod ntfs
    set root=(hd0,1)
    chainloader +1
}
```

### نکات برای آزمون

- تفاوت GRUB Legacy و GRUB 2
- فایل‌های پیکربندی
- دستورات نصب و تولید پیکربندی
- تعامل با منوی GRUB
- Chainloading

!!! tip "نکته"
    همیشه پس از تغییر پیکربندی GRUB، `grub-mkconfig` را اجرا کنید تا `grub.cfg` به‌روزرسانی شود.  
- فایل پیکربندی: `menu.lst` یا `grub.conf`  

### تنظیمات عمومی

| گزینه | توضیح |
|-------|-------|
| `color` | رنگ متن و پس‌زمینه |
| `default` | آیتم پیش‌فرض بوت |
| `fallback` | آیتم جایگزین در صورت شکست بوت |
| `hiddenmenu` | مخفی کردن منو |
| `splashimage` | تصویر پس‌زمینه |
| `timeout` | زمان انتظار قبل از بوت پیش‌فرض |
| `password` | رمز عبور برای امنیت |
| `savedefault` | ذخیره آخرین آیتم بوت شده |

### تنظیمات بخش کرنل/Chainloader

| گزینه | توضیح |
|-------|-------|
| `title` | نام بخش |
| `root` | دیسک و پارتیشن `/boot` |
| `kernel` | فایل کرنل در `/boot` |
| `initrd` | فایل initramfs |
| `rootnoverify` | پارتیشن غیر لینوکسی |
| `chainloader` | اجرای Bootloader دیگر (مثلاً ویندوز) |

### نصب GRUB Legacy

```bash
grub-install /dev/sda
grub-install '(fd0)'
```

!!! warning "هشدار"
    اگر GRUB را خارج از MBR نصب کنید، باید از chainloader برای اشاره به آن استفاده کنید.

### تعامل با GRUB Legacy

- کلید `e`: ویرایش آیتم انتخابی  
- کلید `c`: ورود به خط فرمان GRUB  
- دستورات: `root`, `kernel`, `initrd`, `boot`  

---

## GRUB2

- مسیر نصب:  
  - BIOS: `/boot/grub/` یا `/boot/grub2/`  
  - UEFI: `/boot/efi/EFI/<distro>/`  

- فایل پیکربندی: `grub.cfg`  

### نمونه ساده grub.cfg

```bash
set default="0"
menuentry "Fedora" {
  set root=(hd0,1)
  linux /boot/vmlinuz-5.10.0-9-arm64 ro quiet
  initrd /boot/initrd.img-5.10.0-9-arm64
}
menuentry "Windows" {
  chainloader (hd1,msdos2)+1
}
```

### گزینه‌های مهم

| گزینه | توضیح |
|-------|-------|
| `menuentry` | تعریف آیتم منو |
| `set root` | محل `/boot` |
| `linux`, `linux16` | کرنل لینوکس در BIOS |
| `linuxefi` | کرنل لینوکس در UEFI |
| `initrd`, `initrdefi` | فایل initramfs |

### نصب و پیکربندی GRUB2

```bash
grub-install /dev/sda
grub2-mkconfig -o /boot/grub2/grub.cfg
```

یا:

```bash
update-grub
```

!!! info "نکته"
    `update-grub` در واقع یک frontend برای `grub-mkconfig` است.

### تعامل با GRUB2

- کلید `c`: ورود به خط فرمان GRUB  
- دستورات مشابه GRUB Legacy (`root`, `linux`, `initrd`, `boot`)  

---

## پارامترهای کرنل

نمونه:

```bash
linux /boot/vmlinuz-5.10.0-9-arm64 root=/dev/sda1 ro quiet
```

گزینه‌های رایج:

| گزینه | توضیح |
|-------|-------|
| `console=` | تعیین کنسول |
| `debug` | حالت اشکال‌زدایی |
| `init=` | اجرای برنامه خاص به جای init پیش‌فرض |
| `ro` | mount ریشه به صورت read-only |
| `rw` | mount ریشه به صورت read-write |
| `root=` | تعیین فایل‌سیستم ریشه |
| `selinux` | غیرفعال کردن SELinux |
| `single` یا `S` یا `1` | بوت در حالت تک‌کاربره |
| `systemd.unit=` | بوت در target مشخص systemd |

---

## تمرین‌های عملی

### تمرین 1: نصب GRUB Legacy
```bash
grub-install /dev/sda
```

### تمرین 2: بررسی فایل پیکربندی GRUB Legacy
```bash
cat /boot/grub/menu.lst
```

### تمرین 3: نصب GRUB2
```bash
grub-install /dev/sda
grub2-mkconfig -o /boot/grub2/grub.cfg
```

### تمرین 4: تغییر پارامترهای کرنل
```bash
linux /boot/vmlinuz root=/dev/sda1 ro single
```

---

## خلاصه

در این فصل یاد گرفتیم:

- تفاوت فرآیند بوت در BIOS و UEFI  
- نقش MBR و ESP در بوت  
- ساختار و تنظیمات GRUB Legacy (`menu.lst`, `grub.conf`)  
- نصب و پیکربندی GRUB2 (`grub.cfg`)  
- تعامل با Bootloader از طریق منو و خط فرمان  
- ارسال پارامترهای کرنل در زمان بوت  

!!! example "نکات کلیدی برای آزمون"
    - تفاوت GRUB Legacy و GRUB2  
    - مسیرهای نصب در BIOS و UEFI  
    - دستورات `grub-install`, `grub-mkconfig`, `update-grub`  
    - پارامترهای کرنل مانند `ro`, `rw`, `single`  
    - مفهوم chainloader برای بوت ویندوز  
