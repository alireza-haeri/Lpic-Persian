# 104.5 - مدیریت مجوزهای فایل و مالکیت

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- تغییر مجوزها و مالکیت فایل‌ها
- درک بیت‌های ویژه مانند SUID، SGID، sticky

## کلیدواژه‌ها

`chmod`, `chown`, `chgrp`, `umask`, `suid`, `sgid`, `sticky bit`

---

## مجوزها

- r: خواندن (4)
- w: نوشتن (2)
- x: اجرا (1)

برای کاربر، گروه، دیگران.

### chmod

```bash
$ chmod 755 file
$ chmod u+x file
$ chmod g-w file
```

### chown

```bash
$ chown user file
$ chown user:group file
```

### chgrp

```bash
$ chgrp group file
```

### umask

```bash
$ umask 022
```

### بیت‌های ویژه

- SUID: اجرا به عنوان مالک
- SGID: اجرا به عنوان گروه
- Sticky: فقط مالک می‌تواند حذف کند

```bash
$ chmod u+s file  # SUID
$ chmod g+s file  # SGID
$ chmod +t dir    # Sticky
```