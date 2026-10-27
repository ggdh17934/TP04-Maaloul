FROM python:3.12-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
COPY requirements.txt ./
COPY vendor/linux-wheels/ /wheels/
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels
COPY app/ ./app/
EXPOSE 8000
CMD ["python", "app/analyze.py"]
