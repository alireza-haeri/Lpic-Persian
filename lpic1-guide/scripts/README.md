# Content Pipeline Scripts

این دایرکتوری شامل اسکریپت‌های خودکارسازی برای وارد کردن، پردازش و تبدیل محتوای linux1st.com به دروس LPIC-1 به زبان فارسی است.

## Pipeline Overview

```
linux1st.com/archives.html
         ↓
    fetch_articles.py → linux1st_articles.json
         ↓
    fetch_article_content.py → linux1st_full.json
         ↓
    build_lessons.py → docs/lessons/*.md + lessons_index.json
         ↓
    update_navigation.py → mkdocs.yml (updated)
```

## Scripts

### 1. `fetch_articles.py`
واکشی لیست مقالات از صفحه آرشیو

**Input:** URL مقاله آرشیو  
**Output:** `linux1st_articles.json` - لیست عناوین و URLها

**استفاده:**
```bash
python3 fetch_articles.py
```

### 2. `fetch_article_content.py`
استخراج محتوای کامل هر مقاله

**Input:** `linux1st_articles.json`  
**Output:** `linux1st_full.json` - محتوای کامل مقالات

**استفاده:**
```bash
python3 fetch_article_content.py
```

### 3. `build_lessons.py`
تولید فایل‌های درس به فارسی

**Input:** `linux1st_full.json`  
**Output:** 
- `../docs/lessons/*.md` - فایل‌های درس
- `lessons_index.json` - ایندکس دروس

**ویژگی‌ها:**
- طبقه‌بندی خودکار به موضوعات LPIC-1 (101-110)
- امتیازدهی بر اساس کلیدواژه‌ها
- استخراج دستورات از محتوا
- تولید محتوای ساختاریافته فارسی
- حفظ کدها به صورت LTR

**استفاده:**
```bash
python3 build_lessons.py
```

### 4. `update_navigation.py`
به‌روزرسانی خودکار ناوبری mkdocs.yml

**Input:** `lessons_index.json`  
**Output:** `../mkdocs.yml` (به‌روزشده)

**ویژگی‌ها:**
- سازماندهی بر اساس موضوعات LPIC-1
- حفظ دروس موجود
- گروه‌بندی منطقی

**استفاده:**
```bash
python3 update_navigation.py
```

## اجرای کامل Pipeline

برای اجرای کامل pipeline به صورت دستی:

```bash
cd lpic1-guide/scripts

# مرحله 1: واکشی لیست مقالات
python3 fetch_articles.py

# مرحله 2: واکشی محتوای کامل
python3 fetch_article_content.py

# مرحله 3: ساخت دروس
python3 build_lessons.py

# مرحله 4: به‌روزرسانی ناوبری
python3 update_navigation.py

# مرحله 5: بیلد و پیش‌نمایش
cd ..
mkdocs serve
```

## اجرای خودکار در GitHub Actions

Pipeline به صورت خودکار در GitHub Actions اجرا می‌شود:

- **Trigger:** هر push به main branch
- **محیط:** Ubuntu latest با Python 3.x
- **نتیجه:** دروس جدید در سایت منتشرشده ظاهر می‌شوند

مشاهده: `.github/workflows/deploy-docs.yml`

## Dependencies

```bash
pip install requests beautifulsoup4 lxml pyyaml
```

## LPIC-1 Topics Covered

این سیستم مقالات را به 25+ موضوع LPIC-1 طبقه‌بندی می‌کند:

- **101:** معماری سیستم، نصب و بسته‌ها
- **102:** طراحی دیسک، بوت‌منیجر
- **103-104:** دستورات، فایل‌سیستم‌ها
- **105:** Shell و اسکریپت‌نویسی
- **107:** مدیریت کاربران، وظایف خودکار
- **108:** سرویس‌ها، لاگ‌ها، زمان
- **109:** شبکه، IP، troubleshooting
- **110:** امنیت، رمزنگاری

## توضیحات فنی

### الگوریتم طبقه‌بندی
- امتیازدهی بر اساس تعداد کلیدواژه‌های یافت‌شده
- وزن بیشتر برای کلیدواژه‌های عنوان
- آستانه حداقلی برای فیلتر کردن مقالات غیرمرتبط

### ساختار فایل درس
```markdown
# عنوان درس

**موضوع LPIC-1:** XXX-X - نام موضوع

## خلاصه
...

## توضیح مفصل
...

## دستورات مهم
```bash
...
```

## تمرین پیشنهادی
...
```

### JSON Formats

**linux1st_articles.json:**
```json
[
  {
    "title": "عنوان مقاله",
    "url": "https://..."
  }
]
```

**linux1st_full.json:**
```json
[
  {
    "title": "عنوان",
    "url": "https://...",
    "extracted_title": "عنوان استخراج‌شده",
    "content": "محتوای کامل..."
  }
]
```

**lessons_index.json:**
```json
{
  "created_lessons": [...],
  "by_topic": {
    "101-1": ["file1.md", "file2.md"]
  },
  "total": 42
}
```

## Troubleshooting

### مشکل: دسترسی به linux1st.com
اگر در محیط sandbox دسترسی نداشتید، فایل JSON را به صورت دستی بسازید.

### مشکل: طبقه‌بندی نادرست
کلیدواژه‌های موضوع را در `build_lessons.py` تنظیم کنید.

### مشکل: فرمت YAML
اگر ruamel.yaml نصب نیست، از PyYAML استفاده می‌شود (ممکن است فرمت را تغییر دهد).

## Contributing

برای اضافه کردن موضوعات جدید یا بهبود طبقه‌بندی:

1. `LPIC1_TOPICS` در `build_lessons.py` را ویرایش کنید
2. کلیدواژه‌های جدید اضافه کنید
3. وزن‌ها را تنظیم کنید

---

**نگهداری:** این pipeline به صورت خودکار در GitHub Actions اجرا می‌شود و نیاز به مداخله دستی ندارد.
