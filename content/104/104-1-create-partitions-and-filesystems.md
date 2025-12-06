# 104.1 - ایجاد پارتیشن‌ها و فایل‌سیستم‌ها

## وزن

2

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- مدیریت پارتیشن‌های MBR و GPT
- استفاده از دستورات مختلف mkfs برای ایجاد فایل‌سیستم‌های مختلف مانند:
  - ext2/ext3/ext4
  - XFS
  - VFAT
  - exFAT
- دانش پایه ویژگی‌های Btrfs، از جمله فایل‌سیستم‌های چند دستگاهه، فشرده‌سازی و زیرمجموعه‌ها
- fdisk
- gdisk
- parted
- mkfs
- mkswap

## کلیدواژه‌ها

`fdisk`, `gdisk`, `parted`, `mkfs`, `mkswap`, `tune2fs`, `dumpe2fs`

---

## دستگاه‌های بلوکی

دستگاه بلوکی یک دستگاه ذخیره‌سازی غیرفرار است که اطلاعات آن می‌تواند به هر ترتیبی دسترسی پیدا کند؛ مانند دیسک‌های سخت، حافظه‌های USB، دیسک‌های فلاپی و CD-ROM. ما این دستگاه‌ها را به بلوک‌های اندازه ثابت قالب‌بندی می‌کنیم.

می‌توانیم همه دستگاه‌های بلوکی را با دستور `lsblk` بررسی کنیم. علاوه بر این، در فرمت ls طولانی (`-l`)، دستگاه‌های بلوکی با `b` در ستون اول نشان داده می‌شوند:

```bash
jadi@debianamd:~$ ls /dev/ -l | grep "^b"
brw-rw---- 1 root disk 8, 0 Feb 3 2023 sda
brw-rw---- 1 root disk 8, 16 Feb 3 2023 sdb
brw-rw---- 1 root disk 8, 17 Feb 3 2023 sdb1
brw-rw---- 1 root disk 8, 18 Feb 3 2023 sdb2
brw-rw---- 1 root disk 8, 19 Feb 3 2023 sdb3
brw-rw----+ 1 root cdrom 11, 0 Feb 3 2023 sr0
```

ایجاد پارتیشن‌ها روی یک دستگاه بلوکی امکان‌پذیر است و حتی می‌توان آن را تقسیم کرد و به عنوان چندین دیسک استفاده کرد. سیستم‌هایی با بوت لودرهای BIOS قدیمی از روش Master Boot Record (MBR) برای پارتیشن‌بندی استفاده می‌کنند و سیستم‌های UEFI جدیدتر از فرمت GUID Partition Table (GPT) استفاده می‌کنند.

سیستم‌های لینوکس از udev برای اضافه کردن دستگاه‌های بلوکی و پارتیشن‌های آنها به `/dev` در فرم `/dev/sdb1` (دیسک دوم (b) و پارتیشن اول (1)) استفاده می‌کنند.

## ویرایش جداول پارتیشن

### fdisk

fdisk دستور اصلی برای مشاهده/تغییر و ایجاد پارتیشن‌ها روی سیستم‌های MBR است. سوئیچ `-l` پارتیشن‌ها را لیست می‌کند:

```bash
# fdisk -l /dev/sdb
Disk /dev/sdb: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 11D48091-5AA7-422A-85F7-A23F476CDFD7
Device      Start      End  Sectors Size Type
/dev/sdb1    2048  1050623  1048576 512M EFI System
/dev/sdb2 1050624 39942143 38891520  18.5G Linux filesystem
/dev/sdb3 39942144 41940991  1998848 976M Linux swap
```

فلگ Boot نشان می‌دهد کدام پارتیشن در هنگام بوت روی PCهای DOS شروع می‌شود و اهمیت ندارد روی LILO و GRUB.

Start و End نشان می‌دهد پارتیشن کجا روی دیسک قرار دارد.

Size اندازه هر پارتیشن را نشان می‌دهد.

ID فرمت پارتیشن را نشان می‌دهد (82 برای swap، 83 برای داده‌های لینوکس، ... همه را با `l` در حالت تعاملی چک کنید)

همچنین امکان اجرای fdisk در حالت تعاملی وجود دارد. `m` منوی راهنما را نشان می‌دهد:

```bash
~# fdisk /dev/sda
Welcome to fdisk (util-linux 2.36.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0xe2dbaded.

Command (m for help): m

Help:

DOS (MBR)
   a   toggle a bootable flag
   b   edit nested BSD disklabel
   c   toggle the dos compatibility flag
Generic
   d   delete a partition
   F   list free unpartitioned space
   l   list known partition types
   n   add a new partition
   p   print the partition table
   t   change a partition type
   v   verify the partition table
   i   print information about a partition
Misc
   m   print this menu
   u   change display/entry units
   x   extra functionality (experts only)
Script
   I   load disk layout from sfdisk script file
   O   dump disk layout to sfdisk script file
Save & Exit
   w   write table to disk and exit
   q   quit without saving changes
Create a new label
   g   create a new empty GPT partition table
   G   create a new empty SGI (IRIX) partition table
   o   create a new empty DOS partition table
   s   create a new empty Sun partition table

Command (m for help):
```

برای چک کردن لیست پارتیشن فعلی، از دستور `p` (print) استفاده کنید:

```bash
Command (m for help): p

Disk /dev/sdb: 20 GiB, 21474836480 bytes, 41943040 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: gpt
Disk identifier: 11D48091-5AA7-422A-85F7-A23F476CDFD7
Device      Start      End  Sectors Size Type
/dev/sdb1    2048  1050623  1048576 512M EFI System
/dev/sdb2 1050624 39942143 38891520  18.5G Linux filesystem
/dev/sdb3 39942144 41940991  1998848 976M Linux swap
```

شما باید مفاهیم چیدمان دیسک را از فصل 102.1 به یاد داشته باشید. بنابراین بیایید با استفاده از fdisk پارتیشن‌هایی ایجاد کنیم. من از `n` برای جدید استفاده می‌کنم:

```bash
# fdisk /dev/sda
Welcome to fdisk (util-linux 2.36.1).
Changes will remain in memory only, until you decide to write them.
Be careful before using the write command.

Device does not contain a recognized partition table.
Created a new DOS disklabel with disk identifier 0x40bd0f72.

Command (m for help): n
Partition type
   p   primary (0 primary, 0 extended, 4 free)
   e   extended (container for logical partitions)
Select (default p): p
Partition number (1-4, default 1):
First sector (2048-8388607, default 2048):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2048-8388607, default 8388607): +1G

Created a new partition 1 of type 'Linux' and of size 1 GiB.

Command (m for help): p

Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start     End Sectors Size Id Type
/dev/sda1       2048 2099199 2097152   1G 83 Linux
```

بیایید یک پارتیشن Extended اضافه کنیم و یک پارتیشن Linux (83) و یک پارتیشن Swap (82) در آن اضافه کنیم.

```bash
Command (m for help): n
Partition type
   p   primary (1 primary, 0 extended, 3 free)
   e   extended (container for logical partitions)
Select (default p): e
Partition number (2-4, default 2):
First sector (2099200-8388607, default 2099200):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2099200-8388607, default 8388607):

Created a new partition 2 of type 'Extended' and of size 3 GiB.

Command (m for help): p

Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start      End  Sectors Size Id Type
/dev/sda1       2048  2099199  2097152   1G 83 Linux
/dev/sda2    2099200  8388607  6289408   3G  5 Extended
```

```bash
Command (m for help): n
All space for primary partitions is in use.
Adding logical partition 5
First sector (2101248-8388607, default 2101248):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2101248-8388607, default 8388607):

Created a new partition 5 of type 'Linux' and of size 3 GiB.

Command (m for help): p

Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start      End  Sectors Size Id Type
/dev/sda1       2048  2099199  2097152   1G 83 Linux
/dev/sda2    2099200  8388607  6289408   3G  5 Extended
/dev/sda5    2101248  8388607  6287360   3G 83 Linux
```

اووه! فراموش کردم فضای اختصاصی برای پارتیشن swap را اضافه کنم. بیایید قبلی را حذف کنیم و دو پارتیشن جدید اضافه کنیم:

```bash
Command (m for help): d
Partition number (1,2,5, default 5): 5
Partition 5 has been deleted.

Command (m for help): n
All space for primary partitions is in use.
Adding logical partition 5
First sector (2101248-8388607, default 2101248):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (2101248-8388607, default 8388607): +1G

Created a new partition 5 of type 'Linux' and of size 1 GiB.

Command (m for help): p

Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start      End  Sectors Size Id Type
/dev/sda1       2048  2099199  2097152   1G 83 Linux
/dev/sda2    2099200  8388607  6289408   3G  5 Extended
/dev/sda5    2101248  4198399  2097152   1G 83 Linux

Command (m for help): n
All space for primary partitions is in use.
Adding logical partition 6
First sector (4200448-8388607, default 4200448):
Last sector, +/-sectors or +/-size{K,M,G,T,P} (4200448-8388607, default 8388607):

Created a new partition 6 of type 'Linux' and of size 2 GiB.

And now, I have to change the type of the partition 6 to swap:

Command (m for help): t
Partition number (1,2,5,6, default 6): 6
Hex code or alias (type L to list all): L

00 Empty            24 NEC DOS         81 Minix / old Lin bf Solaris
01 FAT12            27 Hidden NTFS Win 82 Linux swap / So c1 DRDOS/sec (FAT-
02 XENIX root       39 Plan 9          83 Linux             c4 DRDOS/sec (FAT-
03 XENIX usr        3c PartitionMagic  84 OS/2 hidden or    c6 DRDOS/sec (FAT-
04 FAT16 <32M       40 Venix 80286     85 Linux extended    c7 Syrinx
05 Extended         41 PPC PReP Boot   86 NTFS volume set   da Non-FS data
06 FAT16            42 SFS             87 NTFS volume set   db CP/M / CTOS / .
07 HPFS/NTFS/exFAT  4d QNX4.x          88 Linux plaintext   de Dell Utility
08 AIX              4e QNX4.x 2nd part 8e Linux LVM         df BootIt
09 AIX bootable     4f QNX4.x 3rd part 93 Amoeba            e1 DOS access
0a OS/2 Boot Manag  50 OnTrack DM      94 Amoeba BBT       e3 DOS R/O
0b W95 FAT32        51 OnTrack DM6 Aux 9f BSD/OS            e4 SpeedStor
0c W95 FAT32 (LBA)  52 CP/M            a0 IBM Thinkpad hi   ea Linux extended
0e W95 FAT16 (LBA)  53 OnTrack DM6 Aux a5 FreeBSD           eb BeOS fs
0f W95 Ext'd (LBA)  54 OnTrackDM6      a6 OpenBSD           ee GPT
10 OPUS             55 EZ-Drive        a7 NeXTSTEP          ef EFI (FAT-12/16/11
11 Hidden FAT12     56 Golden Bow      a8 Darwin UFS        f0 Linux/PA-RISC b
12 Compaq diagnost  5c Priam Edisk     a9 NetBSD            f1 SpeedStor
14 Hidden FAT16 <3  61 SpeedStor       ab Darwin boot       f4 SpeedStor
16 Hidden FAT16     63 GNU HURD or Sys af HFS / HFS+        f2 DOS secondary
17 Hidden HPFS/NTF  64 Novell Netware  b7 BSDI fs           fb VMware VMFS
18 AST SmartSleep   65 Novell Netware  b8 BSDI swap         fc VMware VMKCORE
1b Hidden W95 FAT3  70 DiskSecure Mult bb Boot Wizard hid   fd Linux raid auto
1c Hidden W95 FAT3  75 PC/IX           bc Acronis FAT32 L   fe LANstep
1e Hidden W95 FAT1  80 Old Minix       be Solaris boot      ff BBT
Aliases:
   linux          - 83
   swap           - 82
   extended       - 05
   uefi           - EF
   raid           - FD
   lvm            - 8E
   linuxex        - 85

Hex code or alias (type L to list all): swap
Changed type of partition 'Linux' to 'Linux swap / Solaris'.

Command (m for help): p

Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start      End  Sectors Size Id Type
/dev/sda1       2048  2099199  2097152   1G 83 Linux
/dev/sda2    2099200  8388607  6289408   3G  5 Extended
/dev/sda5    2101248  4198399  2097152   1G 83 Linux
/dev/sda6    4200448  8388607  4188160   2G 82 Linux swap / Solaris
```

راضی شدم! بیایید `v`erify کنیم و سپس `w`rite کنیم:

```bash
Command (m for help): v
No errors detected.
Remaining 4094 unallocated 512-byte sectors.

Command (m for help): w
The partition table has been altered.
Calling ioctl() to re-read partition table.
Syncing disks.
```

```bash
root@debianamd:~$ fdisk -l /dev/sda
Disk /dev/sda: 4 GiB, 4294967296 bytes, 8388608 sectors
Disk model: QEMU HARDDISK
Units: sectors of 1 * 512 = 512 bytes
Sector size (logical/physical): 512 bytes / 512 bytes
I/O size (minimum/optimal): 512 bytes / 512 bytes
Disklabel type: dos
Disk identifier: 0x40bd0f72

Device     Boot Start      End  Sectors Size Id Type
/dev/sda1       2048  2099199  2097152   1G 83 Linux
/dev/sda2    2099200  8388607  6289408   3G  5 Extended
/dev/sda5    2101248  4198399  2097152   1G 83 Linux
/dev/sda6    4200448  8388607  4188160   2G 82 Linux swap / Solaris
```

### gdisk

همانطور که در فصل 102.1 دیدیم، از gdisk روی ماشین‌های GPT استفاده کردیم. خیلی متفاوت از fdisk نیست. بیایید نگاهی به دستورات اصلی آن بیاندازیم:

```bash
root@debianamd:~$ gdisk /dev/sda
GPT fdisk (gdisk) version 1.0.6

Warning: Partition table header claims that the size of partition table entries is 0 bytes, but this program supports only 128-byte entries.
Adjusting accordingly, but partition table may be garbage.

Warning: Partition table header claims that the size of partition table entries is 0 bytes, but this program supports only 128-byte entries.
Adjusting accordingly, but partition table may be garbage.

Partition table scan:
  MBR: MBR only
  BSD: not present
  APM: not present
  GPT: not present

***************************************************************
Found invalid GPT and valid MBR; converting MBR to GPT format
in memory. THIS OPERATION IS POTENTIALLY DESTRUCTIVE! Exit by
typing 'q' if you don't want to convert your MBR partitions
to GPT format!
***************************************************************

Command (? for help): ?
b	back up GPT data to a file
c	change a partition's name
d	delete a partition
i	show detailed information on a partition
l	list known partition types
n	add a new partition
o	create a new empty GUID partition table (GPT)
p	print the partition table
q	quit without saving changes
r	recovery and transformation options (experts only)
s	sort partitions
t	change a partition's type code
v	verify disk
w	write table to disk and exit
x	extra functionality (experts only)
?	print this menu

As you can see, the partition table have to be compatible with your BIOS/UEFI setup.
```

### parted

parted ابزار GNU برای ویرایش پارتیشن‌ها است. مزیت اصلی آن توانایی تغییر اندازه پارتیشن‌های تعریف شده فعلی است اما استفاده از آن کمی پیچیده‌تر از fdisk و gdisk است:

```bash
# parted
GNU Parted 3.4
Using /dev/sda
Welcome to GNU Parted! Type 'help' to view a list of commands.
(parted) help
  align-check TYPE N                     check partition N for TYPE(min|opt) alignment
  help [COMMAND]                        print general help, or help on COMMAND
  mklabel,mktable LABEL-TYPE            create a new disklabel (partition table)
  mkpart PART-TYPE [FS-TYPE] START END  make a partition
  name NUMBER NAME                      name partition NUMBER as NAME
  print [devices|free|list,all|NUMBER]  display the partition table, available devices, free space, all found partitions, or a particular partition
  quit                                 exit program
  rescue START END                     rescue a lost partition near START and END
  resizepart NUMBER END                resize partition NUMBER
  rm NUMBER                            delete partition NUMBER
  select DEVICE                        choose the device to edit
  disk_set FLAG STATE                  change the FLAG on selected device
  disk_toggle [FLAG]                   toggle the state of FLAG on selected device
  set NUMBER FLAG STATE                change the FLAG on partition NUMBER
  toggle [NUMBER [FLAG]]               toggle the state of FLAG on partition NUMBER
  unit UNIT                            set the default unit to UNIT
  version                              display the version number and copyright information of GNU Parted
  hint?                                use gparted

The gparted tool is a graphical tool to manage your partitioned. It has the ability to resize partitions and is super easy to use. Its not part of the LPIC exam but its good to know about it. just in case ;)
gparted.org
```

## قالب‌بندی پارتیشن

### فایل‌سیستم‌ها

پس از پارتیشن‌بندی دستگاه‌های بلوکی، باید آنها را قالب‌بندی کنیم تا برای ذخیره فایل‌ها و دایرکتوری‌ها قابل استفاده شوند. قالب‌بندی یک فایل‌سیستم نقشه‌ای ایجاد می‌کند که مکان و نام فایل‌ها و دایرکتوری‌ها را ذخیره می‌کند و امکان حرکت فایل‌ها بین فولدرها، حذف آنها یا تغییر نام آنها را فراهم می‌کند؛ فکر کنید به آن مانند فهرست یک کتاب.

فایل‌سیستم‌های زیادی در دنیای لینوکس وجود دارد اما این‌ها رایج‌ترین آن‌ها هستند:

فرمت | توضیح
--- | ---
ext2 | سیستم فایل گسترده دوم توسعه یافت تا کمبودهای سیستم فایل قدیمی Unix/Minix استفاده شده در نسخه‌های اولیه لینوکس را برطرف کند. به طور گسترده در لینوکس برای سال‌های زیادی استفاده شده است. journaling در ext2 وجود ندارد و به طور گسترده توسط ext3 و اخیراً ext4 جایگزین شده است.
ext3 | ext2 + journaling، اندازه حداکثر فایل 2TB و اندازه حداکثر فایل‌سیستم 16TB
ext4 | نسخه فعلی ext، اندازه حداکثر فایل 16TB و اندازه حداکثر فایل‌سیستم 1EB (1000*1000TB)
XFS | journaling، کش به RAM، عالی برای تأمین برق بدون وقفه، اندازه حداکثر فایل و فایل‌سیستم 8EB
swap | Swap زمانی استفاده می‌شود که سیستم نیاز به استفاده از رم بیشتری از آنچه دارد داشته باشد. مانند رم اضافی روی دیسک
VFAT | FAT32، بدون journaling، خوب برای تبادل داده با ویندوز، مجوزها را درک نمی‌کند و لینک‌های symbolic
exFAT | Extended FAT. نسخه جدیدتر FAT که عمدتاً برای دستگاه‌های توسعه‌یافته استفاده می‌شود که باید روی همه ماشین‌ها کار کند؛ مانند دیسک‌های USB
btrfs | یک فایل‌سیستم عملکرد بالا جدید. اندازه حداکثر فایل و فایل‌سیستم 16 EB. دارای فرم خود از RAID و LVM و اسنپ‌شات‌های داخلی و تحمل خطا و فشرده‌سازی داده‌ها به صورت زنده.

### ایجاد فایل‌سیستم‌ها

می‌توانید پارتیشن‌های خود را با دستور `mkfs` قالب‌بندی کنید (و `mkswap` برای swap). این یک frontend برای دستوراتی مانند `mkfs.ext3` برای ext3، `mkfs.ext4` برای ext4 و `mkfs.reiserfs` برای ReiserFS است. لیست کاملی از نصب شده روی سیستم شما در اینجا است:

```bash
# ls /sbin/mk*
/sbin/mkdosfs  /sbin/mkexfatfs  /sbin/mkfs.bfs     /sbin/mkfs.exfat  /sbin/mkfs.ext3  /sbin/mkfs.fat    /sbin/mkfs.msdos  /sbin/mkfs.vfat     /sbin/mkinitramfs   /sbin/mkntfs
/sbin/mke2fs   /sbin/mkfs   /sbin/mkfs.cramfs  /sbin/mkfs.ext2   /sbin/mkfs.ext4  /sbin/mkfs.minix  /sbin/mkfs.ntfs   /sbin/mkhomedir_helper  /sbin/mklost+found  /sbin/mkswap
```

اگر از `mkfs` استفاده کنید، سوئیچ اصلی `-type` (یا `-t`) برای مشخص کردن فرمت است:

```bash
# mkfs -t ext4 /dev/sda1
mke2fs 1.46.2 (28-Feb-2021)
Discarding device blocks: done
Creating filesystem with 262144 4k blocks and 65536 inodes
Filesystem UUID: 63625ecd-857a-419f-a300-12395aaad89f
Superblock backups stored on blocks:
	32768, 98304, 163840, 229376
Allocating group tables: done
Writing inode tables: done
Creating journal (8192 blocks): done
Writing superblocks and filesystem accounting information: done
```

```bash
root@debianamd:~$ mkfs.exfat /dev/sda5
mkexfatfs 1.3.0
Creating... done.
Flushing... done.
File system created successfully.
```

اگر نیاز به اختصاص برچسب به پارتیشن دارید، باید از گزینه `-L label_name` استفاده کنید. لطفاً توجه داشته باشید که در سیستم‌های اخیر، مردم به جای برچسب‌ها از UUIDها استفاده می‌کنند. UUID یک دیسک را می‌توان با مشاهده کرد:

```bash
# blkid /dev/sda1
/dev/sda1: UUID="63625ecd-857a-419f-a300-12395aaad89f" BLOCK_SIZE="4096" TYPE="ext4" PARTUUID="40bd0f72-01"
```

و به عنوان آخرین کار، بیایید یک swap روی `/dev/sda6` ایجاد کنیم:

```bash
# mkswap /dev/sda6
Setting up swapspace version 1, size = 2 GiB (2144333824 bytes)
no label, UUID=6a59cf20-8fd6-4d86-b044-89f7bc67993b
```

و سپس:

```bash
# swapon /dev/sda6
```

در فصل 14.3 خواهیم دید چگونه این فایل‌سیستم‌ها را mount/unmount کنیم.

## نکات

- دستگاه‌های بلوکی با `lsblk` لیست می‌شوند و پارتیشن‌ها با fdisk, gdisk یا parted مدیریت می‌شوند.
- fdisk برای MBR، gdisk برای GPT مناسب است.
- parted برای تغییر اندازه پارتیشن‌ها مفید است.
- فایل‌سیستم‌ها با mkfs ایجاد می‌شوند؛ ext4 رایج‌ترین است.
- swap با mkswap تنظیم می‌شود.

## تمرین‌ها

1. با استفاده از fdisk یک پارتیشن جدید روی یک دیسک ایجاد کنید.
2. پارتیشن را با ext4 قالب‌بندی کنید.
3. UUID پارتیشن را با blkid بررسی کنید.
4. یک پارتیشن swap ایجاد و فعال کنید.
5. از parted برای مشاهده پارتیشن‌ها استفاده کنید.

## خلاصه

در این فصل، ایجاد پارتیشن‌ها و فایل‌سیستم‌ها را پوشش دادیم. دستگاه‌های بلوکی را بررسی کردیم و ابزارهای fdisk، gdisk و parted برای مدیریت پارتیشن‌ها معرفی شدند. فایل‌سیستم‌های مختلف مانند ext4، XFS و swap را یاد گرفتیم و نحوه ایجاد آنها با mkfs و mkswap را دیدیم. تمرین‌ها به شما کمک می‌کنند مهارت‌های خود را تقویت کنید.