import os
import django
from django.conf import settings

# Налаштування змінної середовища для налаштувань Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Замість config.settings вкажіть шлях до вашого модуля налаштувань

# Ініціалізація Django
django.setup()

# Тепер можна звертатися до налаштувань
import boto3

s3_client = boto3.client(
    's3',
    region_name='fra1',  # Вкажіть свій регіон
    endpoint_url=settings.AWS_S3_ENDPOINT_URL,
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
)

# Спробуйте отримати список об'єктів у бакеті
try:
    s3_client.head_bucket(Bucket=settings.AWS_STORAGE_BUCKET_NAME)
    print("Бакет існує.")
except s3_client.exceptions.NoSuchBucket:
    print("Бакет не знайдено.")
except Exception as e:
    print(f"Помилка доступу: {e}")