# 102.5 - استفاده از مدیریت بسته‌های RPM و YUM

## اهداف یادگیری

در این فصل با موارد زیر آشنا می‌شوید:

- نصب، ارتقا و حذف بسته‌های RPM
- دریافت اطلاعات بسته‌های RPM مانند نسخه، وضعیت، وابستگی‌ها، یکپارچگی و امضاها
- تعیین فایل‌هایی که یک بسته ارائه می‌دهد و همچنین یافتن بسته‌ای که یک فایل خاص از آن آمده است

## کلیدواژه‌ها

`rpm`, `rpm2cpio`, `yum`, `zypper`, `/etc/yum.conf`, `/etc/yum.repos.d/`

---

## مقدمه

**RedHat Package Manager (RPM)** و **YellowDog Update Manager (YUM)** برای مدیریت بسته‌ها در توزیع‌هایی مانند Fedora، RedHat، RHEL، CentOS، RocksOS و غیره استفاده می‌شوند. فرمت بسته RPM نامیده می‌شود و می‌توان آن را با ابزارهای `rpm` مدیریت کرد اما اگر بخواهید از repositories برای نصب، به‌روزرسانی، جستجو و غیره بسته‌ها استفاده کنید یا حتی کل سیستم را ارتقا دهید، می‌توانید از دستور `yum` استفاده کنید. برای درک عمیق‌تری از repositories، به بخش قبلی (102.4) مراجعه کنید؛ در اینجا فرض می‌کنم با مفهوم آشنا هستید.

## YUM

`yum` مدیر بسته‌ای است که توسط سیستم‌های مبتنی بر RedHat استفاده می‌شود. فایل‌های پیکربندی آن در `/etc/yum.conf` و `/etc/yum.repos.d/` قرار دارند. در زیر نمونه‌ای آورده شده است.

```bash
# cat /etc/yum.conf
[main]
cachedir=/var/cache/yum/$basearch/$releasever
keepcache=0
debuglevel=2
logfile=/var/log/yum.log
exactarch=1
obsoletes=1
gpgcheck=1
plugins=1
installonly_limit=3
```

و در اینجا نمونه‌ای از یک فایل Repo واقعی در سیستم Fedora آورده شده است:

```bash
# cat /etc/yum.repos.d/fedora.repo
[fedora]
name=Fedora $releasever - $basearch
#baseurl=http://download.example/pub/fedora/linux/releases/$releasever/Everything/$basearch/os/
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-$releasever&arch=$basearch
enabled=1
countme=1
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-debuginfo]
name=Fedora $releasever - $basearch - Debug
#baseurl=http://download.example/pub/fedora/linux/releases/$releasever/Everything/$basearch/debug/tree/
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-debug-$releasever&arch=$basearch
enabled=0
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False

[fedora-source]
name=Fedora $releasever - $basearch - Source
#baseurl=http://download.example/pub/fedora/linux/releases/$releasever/Everything/source/tree/
metalink=https://mirrors.fedoraproject.org/metalink?repo=fedora-source-$releasever&arch=$basearch
enabled=0
metadata_expire=7d
repo_gpgcheck=0
type=rpm
gpgcheck=1
gpgkey=file:///etc/pki/rpm-gpg/RPM-GPG-KEY-fedora-$releasever-$basearch
skip_if_unavailable=False
```

از `yum` مانند `yum [OPTIONS] [COMMAND] [PACKAGE_NAME]` استفاده می‌کنیم.

یکی از مهم‌ترین گزینه‌ها `-y` است که به معنای "بله" به سؤالات Y/N است.

و در اینجا برخی از دستورات آورده شده است:

| Command      | Description |
|--------------|-------------|
| update       | به‌روزرسانی repositories و به‌روزرسانی نام بسته‌ها، یا همه اگر چیزی نام‌گذاری نشده باشد |
| install      | نصب یک بسته |
| reinstall    | نصب مجدد یک بسته |
| list         | نمایش لیست بسته‌ها |
| info         | نمایش اطلاعات یک بسته |
| remove       | حذف بسته نصب‌شده |
| search       | جستجو در repositories برای بسته‌ها |
| provides     | بررسی بسته‌هایی که فایل خاصی را ارائه می‌دهند |
| upgrade      | ارتقا بسته‌ها و حذف بسته‌های منسوخ |
| localinstall | نصب از فایل rpm محلی |
| localupdate  | به‌روزرسانی از فایل rpm محلی |
| check-update | بررسی repositories برای به‌روزرسانی بسته‌های نصب‌شده |
| deplist      | نمایش وابستگی‌های یک بسته |
| groupinstall | نصب یک گروه، مانند "KDE Plasma Workspaces" |
| history      | نمایش تاریخچه استفاده |

این نمونه‌ای از نصب است:

```bash
# yum install bzr
Last metadata expiration check: 0:00:47 ago on Tue 21 Jun 2022 06:38:00 PM +0430.
Dependencies resolved.
=====================================================================================================================
 Package                                  Architecture       Version                       Repository           Size
=====================================================================================================================
Installing:
 breezy                                   x86_64             3.2.1-3.fc36                  fedora              6.0 M
Installing dependencies:
 libsodium                                x86_64             1.0.18-9.fc36                 fedora              163 k
 python3-bcrypt                           x86_64             3.2.2-1.fc36                  updates              43 k
 python3-certifi                          noarch             2021.10.8-1.fc36              fedora               15 k
 python3-configobj                        noarch             5.0.6-27.fc36                 fedora               63 k
 python3-cryptography                     x86_64             36.0.0-3.fc36                 fedora              1.0 M
 python3-dulwich                          x86_64             0.20.32-1.fc36                fedora              408 k
 python3-httplib2                         noarch             0.20.3-2.fc36                 fedora              122 k
 python3-jeepney                          noarch             0.7.1-2.fc36                  fedora              324 k
 python3-jwt                              noarch             2.4.0-1.fc36                  updates              41 k
 python3-jwt+crypto                       noarch             2.4.0-1.fc36                  updates             8.9 k
 python3-keyring                          noarch             23.6.0-1.fc36                 updates              78 k
 python3-launchpadlib                     noarch             1.10.15.1-2.fc36              fedora              167 k
 python3-lazr-restfulclient               noarch             0.14.4-2.fc36                 fedora               84 k
 python3-lazr-uri                         noarch             1.0.6-2.fc36                  fedora               33 k
 python3-oauthlib                         noarch             3.0.2-12.fc36                 fedora              169 k
 python3-oauthlib+signedtoken             noarch             3.0.2-12.fc36                 fedora              8.5 k
 python3-paramiko                         noarch             2.11.0-1.fc36                 updates             303 k
 python3-patiencediff                     x86_64             0.2.2-4.fc36                  fedora               45 k
 python3-pynacl                           x86_64             1.4.0-5.fc36                  fedora              108 k
 python3-secretstorage                    noarch             3.3.1-4.fc36                  fedora               35 k
 python3-wadllib                          noarch             1.3.6-2.fc36                  fedora               60 k
Installing weak dependencies:
 python3-jwt+crypto                       noarch             2.4.0-1.fc36                  updates             8.9 k
 python3-launchpadlib                     noarch             1.10.15.1-2.fc36              fedora              167 k
 python3-oauthlib+signedtoken             noarch             3.0.2-12.fc36                 fedora              8.5 k
 python3-pyasn1                           noarch             0.4.8-8.fc36                  fedora              134 k

Transaction Summary
=====================================================================================================================
Install  23 Packages

Total download size: 9.4 M
Installed size: 44 M
Is this ok [y/N]: y
Downloading Packages:
(1/23): python3-certifi-2021.10.8-1.fc36.noarch.rpm                                  1.8 kB/s |  15 kB     00:08
(2/23): libsodium-1.0.18-9.fc36.x86_64.rpm                                            15 kB/s | 163 kB     00:10
(3/23): python3-configobj-5.0.6-27.fc36.noarch.rpm                                    10 kB/s |  63 kB     00:06
(4/23): breezy-3.2.1-3.fc36.x86_64.rpm                                               262 kB/s | 6.0 MB     00:23
(5/23): python3-dulwich-0.20.32-1.fc36.x86_64.rpm                                     47 kB/s | 408 kB     00:08
(6/23): python3-cryptography-36.0.0-3.fc36.x86_64.rpm                                 77 kB/s | 1.0 MB     00:13
(7/23): python3-httplib2-0.20.3-2.fc36.noarch.rpm                                     105 kB/s | 122 kB     00:01
(8/23): python3-jeepney-0.7.1-2.fc36.noarch.rpm                                       259 kB/s | 324 kB     00:01
(9/23): python3-launchpadlib-1.10.15.1-2.fc36.noarch.rpm                              74 kB/s | 167 kB     00:02
(10/23): python3-lazr-restfulclient-0.14.4-2.fc36.noarch.rpm                          36 kB/s |  84 kB     00:02
(11/23): python3-lazr-uri-1.0.6-2.fc36.noarch.rpm                                     15 kB/s |  33 kB     00:02
(12/23): python3-oauthlib+signedtoken-3.0.2-12.fc36.noarch.rpm                       4.2 kB/s | 8.5 kB     00:02
(13/23): python3-oauthlib-3.0.2-12.fc36.noarch.rpm                                    58 kB/s | 169 kB     00:02
(14/23): python3-patiencediff-0.2.2-4.fc36.x86_64.rpm                                 15 kB/s |  45 kB     00:02
(15/23): python3-pyasn1-0.4.8-8.fc36.noarch.rpm                                       61 kB/s | 134 kB     00:02
(16/23): python3-pynacl-1.4.0-5.fc36.x86_64.rpm                                       36 kB/s | 108 kB     00:03
(17/23): python3-secretstorage-3.3.1-4.fc36.noarch.rpm                                12 kB/s |  35 kB     00:02
(18/23): python3-wadllib-1.3.6-2.fc36.noarch.rpm                                      24 kB/s |  60 kB     00:02
(19/23): python3-bcrypt-3.2.2-1.fc36.x86_64.rpm                                       16 kB/s |  43 kB     00:02
(20/23): python3-jwt+crypto-2.4.0-1.fc36.noarch.rpm                                  3.2 kB/s | 8.9 kB     00:02
(21/23): python3-jwt-2.4.0-1.fc36.noarch.rpm                                          16 kB/s |  41 kB     00:02
(22/23): python3-keyring-23.6.0-1.fc36.noarch.rpm                                     18 kB/s |  78 kB     00:04
(23/23): python3-paramiko-2.11.0-1.fc36.noarch.rpm                                    38 kB/s | 303 kB     00:08
---------------------------------------------------------------------------------------------------------------------
Total                                                                                177 kB/s | 9.4 MB     00:54
Running transaction check
Transaction check succeeded.
Running transaction test
Transaction test succeeded.
Running transaction
  Preparing        :                                                                                             1/1
  Installing       : python3-cryptography-36.0.0-3.fc36.x86_64                                                  1/23
  Installing       : python3-lazr-uri-1.0.6-2.fc36.noarch                                                       2/23
  Installing       : python3-jeepney-0.7.1-2.fc36.noarch                                                        3/23
  Installing       : python3-httplib2-0.20.3-2.fc36.noarch                                                      4/23
  Installing       : python3-secretstorage-3.3.1-4.fc36.noarch                                                  5/23
  Installing       : python3-keyring-23.6.0-1.fc36.noarch                                                       6/23
  Installing       : python3-wadllib-1.3.6-2.fc36.noarch                                                        7/23
  Installing       : python3-jwt-2.4.0-1.fc36.noarch                                                            8/23
  Installing       : python3-jwt+crypto-2.4.0-1.fc36.noarch                                                     9/23
  Installing       : python3-oauthlib-3.0.2-12.fc36.noarch                                                     10/23
  Installing       : python3-oauthlib+signedtoken-3.0.2-12.fc36.noarch                                         11/23
  Installing       : python3-lazr-restfulclient-0.14.4-2.fc36.noarch                                           12/23
  Installing       : python3-launchpadlib-1.10.15.1-2.fc36.noarch                                              13/23
  Installing       : python3-bcrypt-3.2.2-1.fc36.x86_64                                                        14/23
  Installing       : python3-pyasn1-0.4.8-8.fc36.noarch                                                        15/23
  Installing       : python3-patiencediff-0.2.2-4.fc36.x86_64                                                  16/23
  Installing       : python3-configobj-5.0.6-27.fc36.noarch                                                    17/23
  Installing       : python3-certifi-2021.10.8-1.fc36.noarch                                                   18/23
  Installing       : python3-dulwich-0.20.32-1.fc36.x86_64                                                     19/23
  Installing       : libsodium-1.0.18-9.fc36.x86_64                                                            20/23
  Installing       : python3-pynacl-1.4.0-5.fc36.x86_64                                                        21/23
  Installing       : python3-paramiko-2.11.0-1.fc36.noarch                                                     22/23
  Installing       : breezy-3.2.1-3.fc36.x86_64                                                                23/23
  Running scriptlet: breezy-3.2.1-3.fc36.x86_64                                                                23/23
  Verifying        : breezy-3.2.1-3.fc36.x86_64                                                                 1/23
  Verifying        : libsodium-1.0.18-9.fc36.x86_64                                                             2/23
  Verifying        : python3-certifi-2021.10.8-1.fc36.noarch                                                    3/23
  Verifying        : python3-configobj-5.0.6-27.fc36.noarch                                                     4/23
  Verifying        : python3-cryptography-36.0.0-3.fc36.x86_64                                                  5/23
  Verifying        : python3-dulwich-0.20.32-1.fc36.x86_64                                                      6/23
  Verifying        : python3-httplib2-0.20.3-2.fc36.noarch                                                      7/23
  Verifying        : python3-jeepney-0.7.1-2.fc36.noarch                                                        8/23
  Installing       : python3-launchpadlib-1.10.15.1-2.fc36.noarch                                               9/23
  Verifying        : python3-lazr-restfulclient-0.14.4-2.fc36.noarch                                           10/23
  Verifying        : python3-lazr-uri-1.0.6-2.fc36.noarch                                                      11/23
  Verifying        : python3-oauthlib+signedtoken-3.0.2-12.fc36.noarch                                         12/23
  Verifying        : python3-oauthlib-3.0.2-12.fc36.noarch                                                     13/23
  Verifying        : python3-patiencediff-0.2.2-4.fc36.x86_64                                                  14/23
  Verifying        : python3-pyasn1-0.4.8-8.fc36.noarch                                                        15/23
  Verifying        : python3-pynacl-1.4.0-5.fc36.x86_64                                                        16/23
  Verifying        : python3-secretstorage-3.3.1-4.fc36.noarch                                                 17/23
  Verifying        : python3-wadllib-1.3.6-2.fc36.noarch                                                       18/23
  Verifying        : python3-bcrypt-3.2.2-1.fc36.noarch                                                        19/23
  Verifying        : python3-jwt+crypto-2.4.0-1.fc36.noarch                                                    20/23
  Verifying        : python3-jwt-2.4.0-1.fc36.noarch                                                           21/23
  Verifying        : python3-keyring-23.6.0-1.fc36.noarch                                                      22/23
  Verifying        : python3-paramiko-2.11.0-1.fc36.noarch                                                     23/23

Installed:
  breezy-3.2.1-3.fc36.x86_64                                 libsodium-1.0.18-9.fc36.x86_64
  python3-bcrypt-3.2.2-1.fc36.x86_64                         python3-certifi-2021.10.8-1.fc36.noarch
  python3-configobj-5.0.6-27.fc36.noarch                     python3-cryptography-36.0.0-3.fc36.x86_64
  python3-dulwich-0.20.32-1.fc36.x86_64                      python3-httplib2-0.20.3-2.fc36.noarch
  python3-jeepney-0.7.1-2.fc36.noarch                        python3-jwt-2.4.0-1.fc36.noarch
  python3-jwt+crypto-2.4.0-1.fc36.noarch                     python3-keyring-23.6.0-1.fc36.noarch
  python3-launchpadlib-1.10.15.1-2.fc36.noarch               python3-lazr-restfulclient-0.14.4-2.fc36.noarch
  python3-lazr-uri-1.0.6-2.fc36.noarch                       python3-oauthlib-3.0.2-12.fc36.noarch
  python3-oauthlib+signedtoken-3.0.2-12.fc36.noarch          python3-paramiko-2.11.0-1.fc36.noarch
  python3-patiencediff-0.2.2-4.fc36.x86_64                   python3-pynacl-1.4.0-5.fc36.x86_64
  python3-secretstorage-3.3.1-4.fc36.noarch                  python3-wadllib-1.3.6-2.fc36.noarch

Complete!
```

!!! info "نکته جالب"
    Fedora Linux از `dnf` به عنوان مدیر بسته استفاده می‌کند و دستورات `yum` شما را به معادل‌های `dnf` ترجمه می‌کند.

## yumdownloader

این ابزار بسته‌های rpm را از repositories بدون نصب دانلود می‌کند. اگر نیاز به دانلود همه وابستگی‌ها دارید، از گزینه `--resolve` استفاده کنید:

```bash
yumdownloader --resolve bzr
```

## RPM

دستور `rpm` می‌تواند ACTIONهایی را روی فایل‌های RPM فردی اجرا کند. می‌توانید از آن مانند `rpm ACTION [OPTION] rpm_file.rpm` استفاده کنید.

یکی از گزینه‌های رایج `-v` برای خروجی verbose و این ACTIONهای رایج هستند:

| Short Form | Long Form     | Description |
|------------|---------------|-------------|
| -i         | --install     | نصب بسته |
| -e         | --erase       | حذف بسته |
| -U         | --upgrade     | نصب/ارتقا بسته |
| -q         | --query       | بررسی نصب بسته |
| -F         | --freshen     | فقط ارتقا اگر قبلاً نصب شده باشد |
| -V         | --verify      | بررسی یکپارچگی نصب |
| -K         | --checksig    | بررسی یکپارچگی بسته rpm |

!!! note "نکته"
    هر Action در `rpm` ممکن است گزینه‌های مخصوص به خود داشته باشد؛ همیشه `man` مربوطه را برای هر Action خاص بررسی کنید.

### نصب و ارتقا

در اکثر موارد، از `-U` استفاده می‌کنیم که بسته را نصب یا ارتقا می‌دهد.

- RPM پایگاه داده‌ای از نصب بسته خودکار ندارد، بنابراین نمی‌تواند وابستگی‌های خودکار نصب‌شده را حذف کند.

اگر rpm با همه وابستگی‌های خود دارید، می‌توانید آنها را با `rpm -Uvh *.rpm` نصب کنید. این به rpm می‌گوید که در مورد وابستگی‌ها اگر در فایل‌های دیگر ارائه شده باشد، شکایت نکند. `-h` در اینجا 50 علامت هش برای نشان دادن پیشرفت ایجاد می‌کند.

در برخی موارد - اگر بدانید چه کاری انجام می‌دهید - می‌توانید از `--nodeps` برای جلوگیری از بررسی وابستگی‌ها استفاده کنید یا حتی از `--force` برای اجبار نصب/ارتقا علی‌رغم همه مسائل و شکایات استفاده کنید.

### پرس و جو (Query)

پرس و جوی معمولی مانند این است:

```bash
[root@fedora tmp]# rpm -q breezy-3.2.1-3.fc36.x86_64.rpm
breezy-3.2.1-3.fc36.x86_64
[root@fedora tmp]# rpm -q breezy
breezy-3.2.1-3.fc36.x86_64
[root@fedora tmp]# rpm -q emacs
package emacs is not installed
```

و می‌توانید از این گزینه‌ها برای بهبود آن استفاده کنید:

| Short | Long          | Description |
|-------|---------------|-------------|
| -c    | --configfiles | نمایش فایل‌های پیکربندی بسته |
| -i    | --info        | اطلاعات دقیق بسته |
| -a    | --all         | نمایش همه بسته‌های نصب‌شده |
|       | --whatprovides| نمایش بسته‌هایی که این فایل را ارائه می‌دهند |
| -l    | --list        | پرس و جو لیست فایل‌هایی که بسته نصب می‌کند |
| -R    | --requires    | نمایش وابستگی‌های بسته |
| -f    | --file        | پرس و جو بسته مالک فایل |

### تأیید (Verify)

می‌توانید بسته‌های خود را تأیید کنید و ببینید آیا به درستی نصب شده‌اند یا نه. می‌توانید از گزینه `-Vv` برای خروجی verbose استفاده کنید یا فقط از `-V` برای تأیید و دیدن فقط مسائل استفاده کنید. این خروجی پس از ویرایش دستی `/bin/tmux` است:

```bash
[root@fedora tmp]# rpm -V tmux
S.5....T.    /usr/bin/tmux
```

و این بخشی از بخش `-V` `man rpm` است:

```bash
    S Size differs
    M Mode differs (includes permissions and file type)
    5 digest (formerly MD5 sum) differs
    D Device major/minor number mismatch
    L readLink(2) path mismatch
    U User ownership differs
    G Group ownership differs
    T mTime differs
    P caPabilities differ
```

همچنین می‌توانید یکپارچگی بسته rpm را با `-K` بررسی کنید:

```bash
# rpm -Kv breezy-3.2.1-3.fc36.x86_64.rpm
breezy-3.2.1-3.fc36.x86_64.rpm:
    Header V4 RSA/SHA256 Signature, key ID 38ab71f4: OK
    Header SHA256 digest: OK
    Header SHA1 digest: OK
    Payload SHA256 digest: OK
    V4 RSA/SHA256 Signature, key ID 38ab71f4: OK
    MD5 digest: OK
```

خروجی بالا نشان می‌دهد که این فایل معتبر است.

### حذف

```bash
[root@fedora tmp]# rpm -e tmux
error: Failed dependencies:
    tmux is needed by (installed) anaconda-install-env-deps-36.16.5-1.fc36.x86_64
```

- rpm بسته را بدون پرسیدن حذف می‌کند!
- rpm بسته‌ای را که توسط بسته دیگری نیاز است حذف نمی‌کند

### استخراج فایل‌های RPM

#### rpm2cpio

**cpio** یک فرمت آرشیو است (مانند zip یا rar یا tar). می‌توانید از دستور `rpm2cpio` برای تبدیل فایل‌های RPM به **cpio** و سپس از ابزار `cpio` برای استخراج آنها استفاده کنید:

```bash
[root@fedora tmp]# rpm2cpio breezy-3.2.1-3.fc36.x86_64.rpm > breezy.cpio
[root@fedora tmp]# cpio -idv < breezy.cpio
./usr/bin/brz
./usr/bin/bzr
./usr/bin/bzr-receive-pack
./usr/bin/bzr-upload-pack
./usr/bin/git-remote-brz
./usr/bin/git-remote-bzr
[...]
```

## Zypper

SUSE Linux و خواهرش openSUSE از ZYpp به عنوان موتور مدیر بسته خود استفاده می‌کنند. می‌توانید از ابزارهای YaST یا Zypper برای ارتباط با آن استفاده کنید.

این دستورات اصلی استفاده شده در `zypper` هستند:

| Command      | Description |
|--------------|-------------|
| help         | راهنمایی عمومی |
| install      | نصب بسته |
| info         | نمایش اطلاعات بسته |
| list-updates | نمایش به‌روزرسانی‌های موجود |
| lr           | نمایش اطلاعات repository |
| packages     | لیست همه بسته‌های موجود یا بسته‌ها از یک repo خاص |
| what-provides| نمایش مالک فایل |
| refresh      | تازه‌سازی اطلاعات repositories |
| remove       | حذف بسته از سیستم |
| search       | جستجو برای بسته |
| update       | بررسی repositories و به‌روزرسانی بسته‌های نصب‌شده |
| verify       | بررسی بسته و وابستگی‌های آن |

!!! info "نکته"
    می‌توانید هنگام استفاده از `zypper` دستور را کوتاه کنید، بنابراین `zypper se tmux` برای جستجو برای tmux خواهد بود.

## ابزارهای دیگر

YUM و RPM مدیران بسته اصلی در Fedora، RHEL و CentOS هستند اما ابزارهای دیگری نیز موجود هستند. همانطور که ذکر شد، SUSE از `YaST` استفاده می‌کند، و برخی دسکتاپ‌های مدرن (KDE و Gnome) از `PackageKit` که یک ابزار گرافیکی است استفاده می‌کنند. همچنین خوب است بدانید که مجموعه `dnf` نیز در حال محبوبیت است و در سیستم‌های Fedora از پیش نصب شده است.

## تمرین‌ها

1. بسته `vim` را با استفاده از `yum` نصب کنید.
2. اطلاعات بسته `vim` را با استفاده از `rpm -qi vim` نمایش دهید.
3. فایل‌هایی که بسته `vim` نصب می‌کند را لیست کنید.
4. بسته `vim` را با استفاده از `rpm` حذف کنید.
5. یک بسته rpm را دانلود کرده و محتوای آن را استخراج کنید.

## خلاصه

در این فصل، با مدیریت بسته‌های RPM و YUM آشنا شدیم. RPM برای مدیریت بسته‌های فردی استفاده می‌شود، در حالی که YUM برای مدیریت بسته‌ها از repositories استفاده می‌شود. همچنین با Zypper برای SUSE آشنا شدیم. ابزارهای مختلفی برای نصب، ارتقا، حذف و پرس و جو بسته‌ها وجود دارد که هر کدام کاربردهای خاص خود را دارند.

!!! example "نکات کلیدی برای آزمون"
    - تفاوت `rpm` (مدیریت بستهٔ محلی) و `yum`/`dnf` (مدیر بسته مبتنی بر repo)
    - دستورات مهم: `yum install`, `yum update`, `rpm -q`, `rpm -U`, `yumdownloader --resolve`
    - بررسی یکپارچگی و امضای بسته‌ها: `rpm -V` و `rpm -Kv`
    - توجه: `rpm` وابستگی‌ها را خودکار حذف/نصب نمی‌کند؛ برای مدیریت وابستگی‌ها از `yum`/`dnf` استفاده کنید
