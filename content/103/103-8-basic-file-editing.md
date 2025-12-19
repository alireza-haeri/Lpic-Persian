# 103.8 - ویرایش پایه فایل‌ها

## وزن

3

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- پیمایش سند با استفاده از vi
- درک و استفاده از حالت‌های vi
- درج، ویرایش، حذف، کپی و یافتن متن در vi
- آگاهی از Emacs، nano و vim
- پیکربندی ویرایشگر استاندارد

## کلیدواژه‌ها

`vi`, `vim`, `modes`, `insert`, `edit`, `delete`, `copy`, `find`, `Emacs`, `nano`, `vim`, `EDITOR`

---

## vi

به عنوان یک ابزار دیگر، ما طیف گسترده‌ای از انتخاب‌ها در ویرایشگرهای متنی داریم. یکی از رایج‌ترین و قدرتمندترین انتخاب‌ها ویرایشگر `vi` است. این ویرایشگر در تمام توزیع‌های اصلی لینوکس از پیش نصب شده است و دانستن آن به شما اجازه می‌دهد فایل‌های خود را در تمام محیط‌ها ویرایش کنید، چه سرور راه دور از طریق SSH، چه محیط کدگذاری روی دسکتاپ یا یک CyberDeck با صفحه کلید حداقل. تنها نقطه ضعف احتمالی آن منحنی یادگیری نسبتاً کند است اما مطمئنم پس از یک جلسه 1 ساعته با آن، راه خود را در `vi` پیدا خواهید کرد.

نسخه بهبود یافته `vi` که به عنوان `VIMproved` یا `vim` شناخته می‌شود. گاهی اوقات این چیزی است که روی سیستم خود پیدا می‌کنید و گاهی دستور `vi` به `vim` مستعار یا پیوند داده شده است. بیایید این را روی سیستم خود بررسی کنیم (Ubuntu 22.04):

```bash
jadi@funlife:~$ whatis vi
vi (1) - Vi IMproved, a programmer's text editor
jadi@funlife:~$ whereis vi
vi: /usr/bin/vi /usr/share/man/man1/vi.1.gz
jadi@funlife:~$ whatis vim
vim (1) - Vi IMproved, a programmer's text editor
jadi@funlife:~$ whereis vim
vim: /usr/bin/vim /etc/vim /usr/share/vim /usr/share/man/man1/vim.1.gz
jadi@funlife:~$ vi --version
VIM - Vi IMproved 9.0 (2022 Jun 28, compiled Aug 23 2022 20:18:58)
Included patches: 1-242
Modified by team+vim@tracker.debian.org
Compiled by team+vim@tracker.debian.org
Huge version without GUI.  Features included (+) or not (-):
+acl               +file_in_path      +mouse_urxvt       -tag_any_white
+arabic            +find_in_path      +mouse_xterm       -tcl
+autocmd           +float             +multi_byte        +termguicolors
+autochdir         +folding           +multi_lang        +terminal
-autoservername    -footer            -mzscheme          +terminfo
-balloon_eval      +fork()            +netbeans_intg     +termresponse
+balloon_eval_term +gettext           +num64             +textobjects
-browse            -hangul_input      +packages          +textprop
++builtin_terms    +iconv             +path_extra        +timers
+byte_offset       +insert_expand     -perl              +title
+channel           +ipv6              +persistent_undo   -toolbar
+cindent           +job               +popupwin          +user_commands
-clientserver      +jumplist          +postscript        +vartabs
-clipboard         +keymap            +printer           +virtualedit
+cmdline_compl     +lambda            +profile           +vim9script
+cmdline_hist      +langmap           -python            +viminfo
+cmdline_info      +libcall           +python3           +virtualedit
+comments          +linebreak         +quickfix          +visual
+conceal           +lispindent        +reltime           +visualextra
+cryptv            +listcmds          +rightleft         +vreplace
+cscope            +localmap          -ruby              +wildignore
+cursorbind        -lua               +scrollbind        +wildmenu
+cursorshape       +menu              +signs             +windows
+dialog_con        +mksession         +smartindent       +writebackup
+diff              +modify_fname      +sodium            -X11
+digraphs          +mouse             -sound             -xfontset
-dnd               -mouseshape        +spell             -xim
-ebcdic            +mouse_dec         +startuptime       -xpm
+emacs_tags        +mouse_gpm         +statusline        -xsmp
+eval              -mouse_jsbterm     -sun_workshop      -xterm_clipboard
+extra_search      +mouse_netterm     +syntax            -xterm_save
+extra_search      +mouse_sgr         +tag_binary        -farsi
-farsi             -mouse_sysmouse    -tag_old_static    system vimrc file: "/etc/vim/vimrc"
user vimrc file: "$HOME/.vimrc"
2nd user vimrc file: "~/.vimrc"
user exrc file: "$HOME/.exrc"
default vimrc file: "$VIMRUNTIME/defaults.vim"
fall-back for $VIM: "/usr/share/vim"
Compilation: gcc -c -I. -Iproto -DHAVE_CONFIG_H -Wdate-time -g -O2 -ffile-prefix-map=/build/vim-Oy69Mt/vim-9.0.0242=. -flto=auto -ffat-lto-objects -flto=auto -ffat-lto-objects -fstack-protector-strong -Wformat -Werror=format-security -DSYS_VIMRC_FILE=\"/etc/vim/vimrc\" -DSYS_GVIMRC_FILE=\"/etc/vim/gvimrc\" -D_REENTRANT -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=1
Linking: gcc -Wl,-Bsymbolic-functions -flto=auto -ffat-lto-objects -flto=auto -Wl,--as-needed -o vim -lm -ltinfo -lselinux -lsodium -lacl -lattr -lgpm -L/usr/lib/python3.10/config-3.10-x86_64-linux-gnu -lpython3.10 -lcrypt -ldl -lm -lm
```

برای ویرایش یک فایل با vi، فقط نام فایل را به آن بدهید:

```bash
$ vi file.txt
```

## حالت‌های vi

vi در دو حالت کار می‌کند:

- **حالت فرمان (Command mode)**: جایی که در فایل حرکت می‌کنید، متن را جستجو می‌کنید، متن را حذف می‌کنید، کپی پیست می‌کنید، جایگزین می‌کنید، ... و دستورات دیگر را به vi می‌دهید. برخی دستورات با `:` شروع می‌شوند و برخی فقط یک کلید هستند.

- **حالت درج (Insert mode)**: جایی که آنچه تایپ می‌کنید در موقعیت مکان‌نما در فایل قرار می‌گیرد.

برای تغییر به حالت فرمان، کلید ESC را فشار دهید. برای بازگشت به حالت درج، می‌توانید از چندین دستور استفاده کنید اما یکی از رایج‌ترین آنها فشار دادن کلید `i` است.

## حرکت در فایل

برای حرکت در یک فایل متنی، از این کلیدها در حالت فرمان استفاده کنید:

کلید | عملکرد
--- | ---
`h` | یک کاراکتر به چپ (فقط خط فعلی)
`j` | یک خط پایین
`k` | یک خط بالا
`l` | یک کاراکتر به راست (فقط خط فعلی)
`w` | کلمه بعدی در خط فعلی
`e` | پایان کلمه بعدی در خط فعلی
`b` | ابتدای کلمه قبلی در خط فعلی
`Ctrl-f` | اسکرول به جلو یک صفحه
`Ctrl-b` | اسکرول به عقب یک صفحه

تایپ کردن یک عدد قبل از اکثر دستورات آن دستور را آن تعداد بار تکرار می‌کند (یعنی `6h` شش کاراکتر به چپ حرکت می‌کند).

## پرش در فایل

کلید | عملکرد
--- | ---
`G` | بدون عدد، به انتها پرش می‌کند و 10G به خط 10 پرش می‌کند
`H` | 5H به خط 5 از بالای صفحه پرش می‌کند
`L` | 3L مکان‌نما را به خط 3 از آخرین خط صفحه منتقل می‌کند

## ویرایش متن

این دستورات در حالت فرمان به شما کمک می‌کنند تا متن را وارد، ویرایش، جایگزین کنید:

کلید | عملکرد
--- | ---
`i` | وارد حالت درج شوید
`a` | وارد حالت درج بعد از موقعیت فعلی مکان‌نما شوید
`r` | فقط یک کاراکتر را جایگزین کنید
`o` | یک خط جدید زیر مکان‌نما باز کنید و به حالت درج بروید
`O` | یک خط جدید بالای مکان‌نما باز کنید و به حالت درج بروید
`c` | پاک کنید تا مکانی و به حالت درج بروید تا جایگزین کنید و سپس درج عادی ( `cw` کلمه فعلی را جایگزین می‌کند)
`d` | حذف. می‌توانید با w ترکیب کنید (`dw`) برای حذف یک کلمه. همان cw اما dw به حالت درج نمی‌رود
`dd` | خط فعلی را حذف کنید
`x` | کاراکتر در موقعیت مکان‌نما را حذف کنید
`p` | متن حذف شده اخیر را بعد از مکان‌نما چسبانید
`P` | متن حذف شده اخیر را قبل از مکان‌نما چسبانید
`xp` | کاراکتر در موقعیت مکان‌نما را با کاراکتر سمت راست آن جابجا می‌کند

## جستجو

کلید | عملکرد
--- | ---
`/` | جستجو به جلو (`/happiness` عبارت بعدی happiness را پیدا می‌کند)
`?` | جستجو به عقب
`n` | جستجوی قبلی را تکرار کنید. همچنین می‌توانید `/` و `?` را بدون پارامتر استفاده کنید)

جستجو در صورت رسیدن به انتهای فایل به بالای فایل می‌پیچد.

## خروج

همیشه خنده‌دار است وقتی کسی وارد vi می‌شود و نمی‌داند چگونه خارج شود! این‌ها را یاد بگیرید و خنده را جلوگیری کنید:

کلید | عملکرد
--- | ---
`:q!` | ویرایش را بدون ذخیره متوقف کنید = پس از هر اشتباه فرار کنید
`:w!` | فایل را بنویسید (خواه تغییر کرده باشد یا نه). تلاش برای بازنویسی فایل‌های موجود یا فقط خواندنی یا غیرقابل نوشتن
`:w myfile.txt` | به نام جدید بنویسید
`ZZ` | فایل را اگر تغییر کرده باشد ذخیره کنید و خارج شوید
`:e!` | فایل را از دیسک دوباره بارگذاری کنید
`:!` | یک دستور shell اجرا کنید

ورود دو نقطه (`:`) در حالت فرمان مکان‌نما را به پایین صفحه منتقل می‌کند و vi منتظر دستورات شما می‌شود. کلید ESC را فشار دهید تا به حالت فرمان عادی برگردید.

علامت تعجب در اکثر دستورات می‌گوید "من می‌دانم چه کار می‌کنم" و فایل‌های فقط خواندنی را اگر دسترسی داشته باشید می‌نویسد و بدون پرسیدن خارج می‌شود.

امکان ترکیب دستورات وجود دارد. به عنوان مثال می‌توانید `:w` و `:q` را ترکیب کنید و فقط `:wq` بگویید (نوشتن و خروج).

## راهنما

می‌توانید همیشه با `:help` یا `:help subject` برای راهنما بپرسید. این راه vi یک متن راهنما باز می‌کند که می‌توانید مانند هر متن دیگر از آن استفاده کنید / جستجو کنید. با دستور `:q` ببندید.

## ویرایشگرهای دیگر

می‌توانید از ویرایشگرهای دیگر نیز استفاده کنید اگر بخواهید. یک گزینه آسان برای استفاده و رایج nano است و گزینه‌های دیگری مانند micro، emacs (با ویژگی کامل) و neovim (به‌روزرسانی vim) وجود دارد.

## ویرایشگر پیش‌فرض

ویرایشگر پیش‌فرض در bash با استفاده از متغیر محیطی `EDITOR` تنظیم می‌شود. می‌توانید آن را با تغییر دهید:

```bash
$ export EDITOR='vim'
```

یا این خط را به فایل `.bashrc` اضافه کنید. در فصل‌های بعدی در مورد این‌ها جزئیات بیشتری خواهیم دید.

## نکات

- vi یک ویرایشگر قدرتمند است که در تمام سیستم‌های لینوکس موجود است.
- یادگیری حالت‌های vi ضروری است: فرمان برای دستورات، درج برای تایپ.
- دستورات حرکت مانند h, j, k, l برای ناوبری کارآمد هستند.
- برای ویرایش پیشرفته، vim را امتحان کنید که ویژگی‌های بیشتری دارد.

## تمرین‌ها

1. یک فایل جدید با vi ایجاد کنید و متن ساده‌ای تایپ کنید.
2. در حالت فرمان، از دستورات حرکت برای پیمایش استفاده کنید.
3. یک کلمه را با استفاده از `cw` جایگزین کنید.
4. یک خط را کپی کرده و در جای دیگری چسبانید.
5. فایل را جستجو کنید و یک الگو را پیدا کنید.
6. فایل را ذخیره کرده و خارج شوید.
7. ویرایشگر پیش‌فرض خود را به vim تغییر دهید و تأیید کنید.

## خلاصه

در این فصل، ویرایش پایه فایل‌ها با vi را پوشش دادیم. vi یک ویرایشگر استاندارد لینوکس است که در دو حالت فرمان و درج کار می‌کند. دستورات حرکت، ویرایش، جستجو و خروج را یاد گرفتیم. همچنین با ویرایشگرهای دیگر مانند nano و emacs آشنا شدیم و نحوه پیکربندی ویرایشگر پیش‌فرض را دیدیم. تمرین‌ها به شما کمک می‌کنند مهارت‌های خود را تقویت کنید.

!!! example "نکات کلیدی برای آزمون"
	- درک حالت‌های `vi`: تفاوت بین حالت فرمان و حالت درج
	- حرکات پایه: `h`, `j`, `k`, `l`, `w`, `b`, `G`, `H`, `L` و استفاده از اعداد برای تکرار
	- ویرایش و جایگزینی: `i`, `a`, `o`, `dd`, `dw`, `cw`, `p`, `x`
	- خروج و ذخیره: `:w`, `:q`, `:wq`, `:q!`, `ZZ`
	- پیکربندی ویرایشگر پیش‌فرض با متغیر `EDITOR` و آگاهی از گزینه‌های دیگر مثل `nano`, `emacs`, `vim`

ویرایشگر ساده‌تر.

```bash
$ nano file.txt
```

کنترل‌ها در پایین نمایش داده می‌شوند. Ctrl+X برای خروج.
 
 