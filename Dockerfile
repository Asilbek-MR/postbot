# Python 3.9 imijidan foydalanamiz
FROM python:3.9-slim

# Ishchi katalogni yaratamiz
WORKDIR /app

# Ishchi katalogga `requirements.txt` faylini nusxalab olamiz
COPY requirements.txt .

# Kutubxonalarni o'rnatamiz
RUN pip install --no-cache-dir -r requirements.txt

# Bot kodini ishchi katalogga nusxalab olamiz
COPY main.py .

# Konteyner ichida botni ishga tushiramiz
CMD ["python3", "main.py"]
