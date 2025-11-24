# 102.6 - لینوکس به‌عنوان مهمان مجازی‌سازی (Linux as a Virtualization Guest)

## اهداف یادگیری  

در این فصل با موارد زیر آشنا می‌شوید:  

- درک مفهوم کلی ماشین‌های مجازی و کانتینرها  
- شناخت اجزای رایج ماشین‌های مجازی در محیط‌های IaaS (مثل پردازنده، دیسک بلوکی، شبکه)  
- تغییرات لازم در سیستم لینوکس هنگام کلون‌کردن یا استفاده به‌عنوان Template  
- نحوه استفاده از Imageها برای راه‌اندازی ماشین‌های مجازی، نمونه‌های ابری و کانتینرها  
- آشنایی با ابزارهای یکپارچه‌سازی لینوکس با محصولات مجازی‌سازی (مثل cloud-init)  

## کلیدواژه‌ها  

`Virtual Machine`, `Linux Container`, `Application Container`, `Guest Drivers`, `SSH Host Keys`, `D-Bus Machine ID`  

---

## مقدمه  

ماشین‌های مجازی (VM) شبیه‌سازی کامپیوتر هستند. با استفاده از آن‌ها می‌توان سیستم‌عامل‌های جدید را روی یک ماشین موجود اجرا کرد.  
برای اجرای VMها نیاز به **Hypervisor** داریم.  

### بررسی پشتیبانی CPU از مجازی‌سازی  
```bash
cat /proc/cpuinfo | grep -E "vmx|svm"
lsmod | grep -i kvm
sudo modprobe kvm
```

اگر در `/proc/cpuinfo` عبارت `hypervisor` دیده شود، یعنی سیستم در حال اجرا داخل یک ماشین مجازی است.  

---

## انواع Hypervisor  

### Type 2 Hypervisor  
- اجرا روی سیستم‌عامل میزبان  
- مثال‌ها: **VirtualBox**، **VMware Workstation**  

### Type 1 Hypervisor  
- اجرا مستقیم روی سخت‌افزار (Bare-metal)  
- مثال‌ها: **KVM**، **Xen**، **Hyper-V**  

!!! info "نکته"  
    KVM از نسخه 2.6.20 کرنل لینوکس به‌صورت داخلی وجود دارد.  

---

## ایجاد ماشین مجازی  

روش‌های ایجاد:  
- نصب از CD/DVD یا ISO  
- کلون‌کردن ماشین موجود  
- استفاده از فرمت استاندارد OVF/OVA  
- ساخت Template برای ایجاد ماشین‌های جدید  

برای کنترل بهتر، نصب **Guest Drivers/Additions** توصیه می‌شود (مثل درایورهای گرافیکی VirtualBox یا ابزارهای VMware).  

---

## تنظیمات خاص مهمان (Guest-specific configs)  

هنگام کلون یا استفاده از Template باید تغییر دهید:  
- Hostname  
- MAC Address کارت شبکه  
- IP Address (در صورت عدم استفاده از DHCP)  
- Machine ID (`/etc/machine-id`, `/var/lib/dbus/machine-id`)  
- کلیدهای رمزنگاری (SSH Keys, PGP Keys)  
- UUID دیسک‌ها  

!!! warning "هشدار"  
    اگر این مقادیر تغییر نکنند، ممکن است باعث تداخل در شبکه یا مشکلات امنیتی شوند.  

---

## کانتینرها (Containers)  

- مجازی‌سازی در سطح سیستم‌عامل (OS-level virtualization)  
- ایجاد چند محیط ایزوله در یک کرنل  
- کاربرد: اجرای سرویس‌ها یا تست بخش‌هایی از یک OS  

مثال‌ها: **Docker**, **LXC**  

---

## IaaS (Infrastructure as a Service)  

زیرساخت به‌عنوان سرویس یعنی اجاره منابع از ارائه‌دهندگان ابری.  
نمونه‌ها: **AWS**, **Google Cloud**, **Microsoft Azure**  

### خدمات رایج در IaaS  
- Load Balancing  
- Block Storage  
- Object Storage  
- Elasticity (افزایش/کاهش خودکار منابع)  
- SaaS (نرم‌افزار به‌عنوان سرویس)  

ابزار **cloud-init** برای پیکربندی خودکار ماشین‌های ابری استفاده می‌شود.  

---

## تمرین‌های عملی  

### تمرین 1: بررسی پشتیبانی CPU از مجازی‌سازی  
```bash
cat /proc/cpuinfo | grep -E "vmx|svm"
```

### تمرین 2: بارگذاری ماژول KVM  
```bash
sudo modprobe kvm
```

### تمرین 3: تغییر Machine ID پس از کلون  
```bash
sudo rm /etc/machine-id /var/lib/dbus/machine-id
sudo dbus-uuidgen --ensure
```

### تمرین 4: ایجاد کانتینر ساده با Docker  
```bash
docker run -it ubuntu bash
```

---

## خلاصه  

در این فصل یاد گرفتیم:  

- تفاوت Hypervisor نوع 1 و 2  
- روش‌های ایجاد ماشین مجازی (ISO، کلون، OVF/OVA، Template)  
- تنظیمات خاص مهمان مثل MAC، Hostname، Machine ID و کلیدهای رمزنگاری  
- مفهوم کانتینرها و کاربرد آن‌ها  
- خدمات IaaS و نقش cloud-init در راه‌اندازی ماشین‌های ابری  

!!! example "نکات کلیدی برای آزمون"  
    - تفاوت Hypervisor نوع 1 و 2  
    - نقش KVM در لینوکس  
    - تغییر Machine ID و SSH Keys پس از کلون  
    - مفهوم کانتینرها و تفاوت آن‌ها با VM  
    - آشنایی با IaaS و ابزار cloud-init  
