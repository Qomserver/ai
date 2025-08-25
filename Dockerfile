FROM python:3.9-slim

# تنظیم متغیرهای محیطی
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# نصب وابستگی‌های سیستم
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# تنظیم دایرکتوری کاری
WORKDIR /app

# کپی فایل requirements
COPY requirements.txt .

# نصب وابستگی‌های Python
RUN pip install --no-cache-dir -r requirements.txt

# کپی کدهای پروژه
COPY . .

# ایجاد دایرکتوری‌های مورد نیاز
RUN mkdir -p logs data

# تغییر مجوزها
RUN chmod +x main.py

# پورت
EXPOSE 8000

# اجرای برنامه
CMD ["python", "main.py"]