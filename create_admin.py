import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "GardenCol_Project.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = "Yuliia"
password = "Ulia@2007"
email = "yuliia@example.com"

# Якщо користувач уже існує — змінюємо пароль
if User.objects.filter(username=username).exists():
    user = User.objects.get(username=username)
    user.set_password(password)
    user.save()
    print(f"Password for {username} has been updated.")
else:
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f"Superuser {username} has been created.")
