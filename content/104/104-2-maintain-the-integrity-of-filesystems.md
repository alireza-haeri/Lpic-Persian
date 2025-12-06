# 104.2 - حفظ یکپارچگی فایل‌سیستم‌ها

## وزن

2

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- بررسی یکپارچگی فایل‌سیستم‌ها
- نظارت بر فضای آزاد و inodeها
- تعمیر مشکلات ساده فایل‌سیستم
- du
- df
- fsck
- e2fsck
- mke2fs
- tune2fs
- xfs_repair
- xfs_fsr
- xfs_db

---

## du و df

در بسیاری موارد می‌خواهید درباره فضای آزاد دیسک یا اینکه یک دایرکتوری چقدر فضا استفاده می‌کند یا اینکه چند inode باقی مانده است بدانید.

inode (index node) یک ساختار داده در یک فایل‌سیستم سبک Unix است که یک شی فایل‌سیستم مانند یک فایل یا دایرکتوری را توصیف می‌کند. هر inode ویژگی‌های شی را ذخیره می‌کند و مکان‌های بلوک دیسک داده‌های آن را. ویژگی‌های شی فایل‌سیستم ممکن است شامل متادیتا (زمان‌های آخرین تغییر، دسترسی، اصلاح)، و همچنین داده‌های مالکیت و مجوز باشد. یک دایرکتوری لیستی از inodeها با نام‌های اختصاص داده شده آنهاست. لیست شامل ورودی برای خودش، والدش و هر یک از فرزندانش است.

(ویکی‌پدیا)

### df

دستور d isk f ree برای یافتن فضای آزاد و استفاده شده روی فایل‌سیستم‌ها استفاده می‌شود.

```bash
jadi@funlife:~$ df -TH
Filesystem        Type      Size  Used Avail Use% Mounted on
/dev/sda2         ext4       23G   15G  7.7G  65% /
none              tmpfs     4.0K     0  4.0K   0% /sys/fs/cgroup
udev              devtmpfs  3.9G  4.0K  3.9G   1% /dev
tmpfs             tmpfs     788M  1.4M  786M   1% /run
none              tmpfs     5.0M  4.0K  5.0M   1% /run/lock
none              tmpfs     3.9G   19M  3.9G   1% /run/shm
none              tmpfs     100M   28K  100M   1% /run/user
/dev/mapper/chome ext4      243G  229G   14G  95% /home/jadi
/dev/sdb1         vfat      3.7G  7.8M  3.6G   1% /media/jadi/BA82-BECD
```

در اینجا، سوئیچ `-T` به df می‌گوید انواع فایل‌سیستم را نشان دهد و `-H` اعداد را به صورت قابل خواندن انسانی می‌کند (در توان‌های 1000، برای توان‌های 2، از `-h` استفاده کنید).

در برخی فایل‌سیستم‌ها مانند ext2-4، تعداد ثابتی از inodeها داریم، بنابراین ممکن است نیاز به چک کردن تعداد inodeهای باقی‌مانده داشته باشیم. برای انجام این کار، از سوئیچ `-i` استفاده کنید:

```bash
jadi@funlife:~$ df -i
Filesystem          Inodes  IUsed    IFree IUse% Mounted on
/dev/sda2          1531904 458616  1073288   30% /
none               1007533      4  1007529    1% /sys/fs/cgroup
udev               1003703    542  1003161    1% /dev
tmpfs              1007533    644  1006889    1% /run
none               1007533      3  1007530    1% /run/lock
none               1007533    162  1007371    1% /run/shm
none               1007533     33  1007500    1% /run/user
/dev/mapper/chome 16171008 269293 15901715    2% /home/jadi
/dev/sdb1                0      0        0     - /media/jadi/BA82-BECD
```

فرمت فایل vfat inode ندارد؛ هیچ مالکیت یا حقوق دسترسی روی فایل‌های vfat وجود ندارد.

### du

دستور d isk u sage فضای استفاده شده دایرکتوری‌ها و فایل‌ها را نشان می‌دهد. سوئیچ‌های رایج عبارتند از:

سوئیچ | کاربرد
--- | ---
`-h` | اندازه‌ها را در توان‌های 1024 چاپ می‌کند (مثلاً 1023M)
`-H` | اندازه‌ها را در توان‌های 1000 چاپ می‌کند (مثلاً 1.1G)
`-c` | مجموع بزرگ را نشان می‌دهد
`--max-depth 2` | همه را محاسبه می‌کند اما فقط 2 دایرکتوری عمیق نشان می‌دهد
`-s` | فقط خلاصه را نشان می‌دهد و نه همه دایرکتوری‌ها را یکی یکی

```bash
jadi@funlife:~/w/lpic$ du
16    ./101
701456    ./done
701464    ./Logo/chert
704588    ./Logo
12    ./data
12    ./100
9432884    .
jadi@funlife:~/w/lpic$ du -c
16    ./101
701456    ./done
701464    ./Logo/chert
704588    ./Logo
12    ./data
12    ./100
9432884    .
9432884    total
jadi@funlife:~/w/lpic$ du -hs
9.0G    .
```

در بسیاری موارد وقتی می‌خواهم ببینم چه چیزی فضای سرورهایم را استفاده می‌کند، از چیزی مانند `$ sudo du /home -h --max-depth 1` استفاده می‌کنم.

## بررسی فایل‌سیستم‌ها

### fsck

اگر چیزی بد برای فایل‌سیستم شما اتفاق بیفتد (بگویید برق ناگهان قطع شود) فایل‌سیستم خراب خواهید داشت. دستور عمومی برای رفع این مشکل fsck است. از نظر فنی این دستور یک frontend برای بسیاری دستورات است:

```bash
jadi@funlife:~$ ls /sbin/*fsck*
/sbin/dosfsck       /sbin/fsck.ext2     /sbin/fsck.fat     /sbin/fsck.vfat
/sbin/e2fsck       /sbin/fsck.ext3     /sbin/fsck.minix
/sbin/fsck       /sbin/fsck.ext4     /sbin/fsck.msdos
/sbin/fsck.cramfs  /sbin/fsck.ext4dev  /sbin/fsck.nfs
```

برخی از این‌ها فقط hardlink به e2fsck هستند.

یک سوئیچ رایج در هنگام بوت `-A` است که به fsck می‌گوید همه فایل‌سیستم‌ها را در /etc/fstab بر اساس passno در آن فایل چک کند که فیلد 6 است (فایل‌سیستم‌ها با passno برابر با 0 در هنگام بوت چک نمی‌شوند.

```bash
root@funlife:~# fsck /dev/sdb
fsck from util-linux 2.25.1
e2fsck 1.42.10 (18-May-2014)
/dev/sdb is in use.
e2fsck: Cannot continue, aborting.
root@funlife:~# umount /dev/sdb
umount: /dev/sdb: not mounted
root@funlife:~# umount /dev/sdb1
root@funlife:~# fsck /dev/sdb
fsck from util-linux 2.25.1
e2fsck 1.42.10 (18-May-2014)
ext2fs_open2: Bad magic number in super-block
fsck.ext2: Superblock invalid, trying backup blocks...
fsck.ext2: Bad magic number in super-block while trying to open /dev/sdb
The superblock could not be read or does not describe a valid ext2/ext3/ext4
filesystem.  If the device is valid and it really contains an ext2/ext3/ext4
filesystem (and not swap or ufs or something else), then the superblock
is corrupt, and you might try running e2fsck with an alternate superblock:
    e2fsck -b 8193 <device>
or
    e2fsck -b 32768 <device>
```

همچنین می‌توانید فایل‌سیستم‌ها را با UUID چک کنید (آنها را با دستور blkid پیدا کنید یا با برچسب‌ها):

```bash
root@funlife:~# fsck LABEL=movies
fsck from util-linux 2.25.1
root@funlife:~# fsck UUID="BA82-BECD"
fsck from util-linux 2.25.1
fsck.fat 3.0.26 (2014-03-07)
/dev/sdb1: 14 files, 1972/945094 clusters
```

از `-N` برای دیدن اینکه چه دستوری/تستی اجرا خواهد شد بدون اجرای واقعی استفاده کنید:

```bash
root@funlife:~# fsck -N UUID="BA82-BECD"
fsck from util-linux 2.25.1
[/sbin/fsck.vfat (1) -- /dev/sdb1] fsck.vfat /dev/sdb1
```

اگر بخواهید یک فایل‌سیستم XFS را چک کنید، باید از دستور `xfs_check` استفاده کنید.

برخی نسخه‌ها `-a` برای تعمیر خودکار همه مسائل یافت شده دارند اما توصیه نمی‌شود.

### e2fsck

e2fsck برای چک کردن خانواده فایل‌سیستم‌های ext2/ext3/ext4 استفاده می‌شود. برای فایل‌سیستم‌های ext3 و ext4 که از journal استفاده می‌کنند، اگر سیستم به طور غیرمنتظره خاموش شده باشد بدون هیچ خطایی، معمولاً پس از بازپخش تراکنش‌های committed در journal، فایل‌سیستم به عنوان پاک علامت‌گذاری می‌شود. بنابراین، برای فایل‌سیستم‌هایی که از journaling استفاده می‌کنند، e2fsck معمولاً journal را بازپخش می‌کند و خارج می‌شود، مگر اینکه superblock آن نشان دهد که چک کردن بیشتر لازم است.

device یک دستگاه بلوکی است (مثل /dev/sdc1) یا فایلی حاوی فایل‌سیستم.

توجه داشته باشید که در عمومی امن نیست e2fsck را روی فایل‌سیستم‌های mounted اجرا کنید. تنها استثنا اگر گزینه `-n` مشخص شده باشد، و گزینه‌های `-c`، `-l` یا `-L` مشخص نشده باشند. اما حتی اگر امن باشد، نتایج چاپ شده توسط e2fsck اگر فایل‌سیستم mounted باشد معتبر نیستند. اگر e2fsck بپرسد آیا باید یک فایل‌سیستم mounted را چک کند، پاسخ صحیح همیشه "no" است. فقط کارشناسان که واقعاً می‌دانند چه کار می‌کنند ممکن است در نظر گرفتن پاسخ دادن به این سوال در هر راه دیگری داشته باشند.

اگر e2fsck در حالت تعاملی اجرا شود (به معنای اینکه هیچ‌کدام از `-y`، `-n` یا `-p` مشخص نشده باشند)، برنامه از کاربر می‌پرسد که هر مشکل یافت شده در فایل‌سیستم را رفع کند. پاسخ `y` مشکل را رفع می‌کند؛ `n` مشکل را رفع نشده رها می‌کند؛ و `a` مشکل را رفع می‌کند و همه مشکلات بعدی را. فشار دادن Enter با پاسخ پیش‌فرض ادامه می‌دهد، که قبل از علامت سوال چاپ می‌شود. فشار دادن Control-C e2fsck را فوراً خاتمه می‌دهد.

### mke2fs

mke2fs برای ایجاد یک فایل‌سیستم ext2، ext3 یا ext4 استفاده می‌شود، معمولاً در یک پارتیشن دیسک. device فایل ویژه مربوط به دستگاه است (مثل /dev/hdXX). blocks-count تعداد بلوک‌ها روی دستگاه است. اگر حذف شود، mke2fs به طور خودکار اندازه فایل‌سیستم را محاسبه می‌کند. اگر به عنوان mkfs.ext3 فراخوانی شود، یک journal ایجاد می‌شود گویی گزینه `-j` مشخص شده است.

defaults پارامترهای فایل‌سیستم تازه ایجاد شده، اگر توسط گزینه‌های زیر override نشده باشند، توسط فایل پیکربندی /etc/mke2fs.conf کنترل می‌شوند. برای جزئیات بیشتر به صفحه دستی mke2fs.conf(5) مراجعه کنید.

### tune2fs

این یک دستور برای تنظیم فایل‌سیستم‌های ext است. می‌تواند اطلاعات را نشان دهد و بسیاری گزینه‌ها را تنظیم کند. گزینه `-l` configs فعلی را لیست می‌کند:

```bash
jadi@funlife:~$ sudo tune2fs -l /dev/sda2
tune2fs 1.42.10 (18-May-2014)
Filesystem volume name:   <none>
Last mounted on:          /
Filesystem UUID:          1651a94e-0b4e-47fb-aca0-f77e05714617
Filesystem magic number:  0xEF53
Filesystem revision #:    1 (dynamic)
Filesystem features:      has_journal ext_attr resize_inode dir_index filetype needs_recovery extent flex_bg sparse_super large_file huge_file uninit_bg dir_nlink extra_isize
Filesystem flags:         signed_directory_hash
Default mount options:    user_xattr acl
Filesystem state:         clean
Errors behavior:          Continue
Filesystem OS type:       Linux
Inode count:              1531904
Block count:              6123046
Reserved block count:     306152
Free blocks:              2302702
Free inodes:              1073461
First block:              0
Block size:               4096
Fragment size:            4096
Reserved GDT blocks:      1022
Blocks per group:         32768
Fragments per group:      32768
Inodes per group:         8192
Inode blocks per group:   512
Flex block group size:    16
Filesystem created:       Mon Dec  1 10:21:42 2014
Last mount time:          Sat Jan 31 17:21:51 2015
Last write time:          Sat Jan 31 17:21:51 2015
Mount count:              32
Maximum mount count:      -1
Last checked:             Mon Dec  1 10:21:42 2014
Check interval:           0 (<none>)
Lifetime writes:          103 GB
Reserved blocks uid:      0 (user root)
Reserved blocks gid:      0 (group root)
First inode:              11
Inode size:              256
Required extra isize:     28
Desired extra isize:      28
Journal inode:            8
First orphan inode:       786620
Default directory hash:   half_md4
Directory Hash Seed:      16c38a41-e709-4e04-b1c2-8a79d71ea7e8
Journal backup:           inode blocks
```

### debugfs

این یک ابزار تعاملی برای debug یک فایل‌سیستم ext است. فایل‌سیستم را در حالت فقط خواندنی باز می‌کند مگر اینکه به آن بگوییم نکنیم (با گزینه `-w`). می‌تواند فایل‌ها و دایرکتوری‌ها را un-delete کند..

```bash
root@funlife:~# debugfs /dev/sda2
debugfs 1.42.10 (18-May-2014)
debugfs:  cd /etc/        <-- cd
debugfs:  pwd            <-- show were am I
[pwd]   INODE: 524289  PATH: /etc
[root]  INODE:      2  PATH: /
debugfs:  stat passwd        <-- show data on one file
Inode: 527187   Type: regular    Mode:  0644   Flags: 0x80000
Generation: 1875144872    Version: 0x00000000:00000001
User:     0   Group:     0   Size: 2145
File ACL: 0    Directory ACL: 0
Links: 1   Blockcount: 8
Fragment:  Address: 0    Number: 0    Size: 0
ctime: 0x548d4241:a7b196fc -- Sun Dec 14 11:24:41 2014
atime: 0x54cc635b:6acfc148 -- Sat Jan 31 08:38:43 2015
mtime: 0x548d4241:a01076f8 -- Sun Dec 14 11:24:41 2014
crtime: 0x548d4241:9f1c52f8 -- Sun Dec 14 11:24:41 2014
Size of extra inode fields: 28
EXTENTS:
(0):2188172
debugfs:  ncheck 527187        <-- node check an inode
Inode    Pathname
527187    /etc/passwd
debugfs:  q            <-- quit
```

### Superblock

سیستم‌های Unix از superblockها برای ذخیره metadata فایل‌سیستم استفاده می‌کنند. بیشتر اوقات این بلوک در ابتدای فایل‌سیستم قرار دارد و روی مکان‌های دیگر نیز تکرار می‌شود. گزینه `-n` mke2fs مکان‌های superblock را نمایش می‌دهد

```bash
# mke2fs -n /dev/sda7
mke2fs 1.41.9 (22-Aug-2009)
Filesystem label=
OS type: Linux
Block size=4096 (log=2)
Fragment size=4096 (log=2)
7159808 inodes, 28637862 blocks
1431893 blocks (5.00%) reserved for the super user
First data block=0
Maximum filesystem blocks=4294967296
874 block groups
32768 blocks per group, 32768 fragments per group
8192 inodes per group
Superblock backups stored on blocks:
32768, 98304, 163840, 229376, 294912, 819200, 884736, 1605632, 2654208,
4096000, 7962624, 11239424, 20480000, 23887872
```

## ابزارهای xfs

توجه: در برخی توزیع‌ها، ابزارهای xfs به طور پیش‌فرض نصب نیستند و ممکن است نیاز به نصب بسته xfsprogs داشته باشید.

این همان tune2fs است اما برای فایل‌سیستم‌های xfs.

xfs_info باید روی فایل‌سیستم‌های mounted استفاده شود

دستور | کاربرد
--- | ---
`xfs_info` | نمایش اطلاعات
`xfs_growfs` | گسترش فایل‌سیستم
`xfs_admin` | تغییر پارامترها روی فایل‌سیستم‌های XFS
`xfs_repair` | تعمیر مشکلات. لطفاً توجه داشته باشید که فایل‌سیستم تحت تعمیر باید unmounted باشد
`xfs_db` | چک و debug فایل‌سیستم. xfs_db برای بررسی یک فایل‌سیستم XFS استفاده می‌شود. در شرایط نادر ممکن است برای تغییر یک فایل‌سیستم XFS نیز استفاده شود، اما این کار معمولاً به xfs_repair یا اسکریپت‌هایی مانند xfs_admin که xfs_db را اجرا می‌کنند واگذار می‌شود.
`xfs_fsr` | سازمان‌دهنده فایل‌سیستم برای XFS. وقتی بدون آرگومان فراخوانی شود، xfs_fsr همه فایل‌های منظم را در همه فایل‌سیستم‌های mounted سازمان‌دهی می‌کند. xfs_fsr چندین چرخه روی /etc/mtab انجام می‌دهد، هر بار یک گذر روی هر فایل‌سیستم XFS. هر گذر از طریق فایل‌ها می‌رود و فایل‌هایی را انتخاب می‌کند که تعداد زیادی extent دارند. سعی می‌کند 10% برتر این فایل‌ها را در هر گذر defragment کند.

## تعمیر

ما از fsck برای نمایش اطلاعات فایل‌سیستم استفاده کردیم اما طراحی شده برای fix فایل‌سیستم‌ها نیز هست. اگر چک بوت مشکل پیدا کند، شما به یک خط فرمان برای رفع مشکلات منتقل خواهید شد.

در فایل‌سیستم‌های بدون journaling (ext2) fsck بسیاری سؤال درباره هر بلوک خواهد کرد و باید بگویید y اگر بخواهید آن را رفع کند. در فایل‌سیستم‌های journaling (ext3&4, xfs, ..) fsck کارهای کمتری برای انجام دارد.

برای فایل‌سیستم‌های xfs، ما دستور `xfs_check` داریم

یک سوئیچ مهم `-n` است که باعث می‌شود این دستورات چیزی را fix نکنند و فقط نشان دهند چه کاری انجام خواهد شد.

## ابزارهای دیگر

برای امتحان LPIC، خوب است این دستورات را بدانید.

فایل‌سیستم | دستور | کاربرد
--- | --- | ---
ext | tune2fs | نمایش یا تنظیم پارامترهای ext2 و ext3 یا حتی تنظیم گزینه‌های journaling
ext | dumpe2fs | super block و block group descriptor information را برای یک فایل‌سیستم ext2 یا ext3 چاپ می‌کند.
ext | debugfs | یک debugger فایل‌سیستم تعاملی است. برای بررسی یا تغییر وضعیت یک فایل‌سیستم ext2 یا ext3 استفاده می‌شود.
reiserfs | reiserfstune | نمایش و تنظیم پارامترها
reiserfs | debugreiserfs | super block و block group descriptor information را برای یک فایل‌سیستم ext2 یا ext3 چاپ می‌کند.
XFS | xfs_info | نمایش اطلاعات
XFS | xfs_growfs | گسترش فایل‌سیستم
XFS | xfs_admin | تغییر پارامترها روی فایل‌سیستم‌های XFS
XFS | xfs_repair | تعمیر مشکلات
XFS | xfs_db | چک و debug فایل‌سیستم

## نکات

- df فضای آزاد را نشان می‌دهد و du فضای استفاده شده را.
- fsck یکپارچگی فایل‌سیستم را چک می‌کند و می‌تواند تعمیر کند.
- e2fsck مخصوص ext است و tune2fs برای تنظیم پارامترها.
- ابزارهای xfs مانند xfs_repair برای XFS هستند.

## تمرین‌ها

1. فضای آزاد دیسک را با df چک کنید.
2. فضای استفاده شده یک دایرکتوری را با du بررسی کنید.
3. یک فایل‌سیستم را با fsck چک کنید.
4. اطلاعات یک فایل‌سیستم ext را با tune2fs مشاهده کنید.
5. از debugfs برای بررسی یک inode استفاده کنید.

## خلاصه

در این فصل، حفظ یکپارچگی فایل‌سیستم‌ها را پوشش دادیم. ابزارهای df و du برای نظارت بر فضای دیسک و inodeها معرفی شدند. fsck، e2fsck و ابزارهای xfs برای چک و تعمیر فایل‌سیستم‌ها استفاده می‌شوند. tune2fs و debugfs برای مدیریت فایل‌سیستم‌های ext مفید هستند. تمرین‌ها به شما کمک می‌کنند مهارت‌های خود را تقویت کنید.