from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import Product

# Ми імпортуємо лише Product, оскільки Order та OrderItem не потрібні для ініціалізації

# ====================================================================
# ДАНІ АДМІНІСТРАТОРА (ОБОВ'ЯЗКОВО ЗМІНИТИ ПІСЛЯ ПЕРШОГО ВХОДУ!)
# ====================================================================
ADMIN_USERNAME = 'admin'
ADMIN_EMAIL = 'admin@gardencol.ua'
ADMIN_PASSWORD = 'TemporarySecurePassword123!'


# Пароль буде використано для входу після розгортання

class Command(BaseCommand):
    help = 'Initializes the database by creating a superuser and basic products if they do not exist.'

    def handle(self, *args, **options):
        # 1. Створення Суперкористувача
        if not User.objects.filter(username=ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                username=ADMIN_USERNAME,
                email=ADMIN_EMAIL,
                password=ADMIN_PASSWORD
            )
            self.stdout.write(self.style.SUCCESS(f'Successfully created superuser: {ADMIN_USERNAME}'))
        else:
            self.stdout.write(self.style.WARNING('Superuser already exists.'))

        # 2. Додавання тестових товарів у нову базу даних
        if not Product.objects.exists():

            # Товар 1: Кімнатні рослини
            Product.objects.create(
                name="Орхідея Фаленопсис",
                price=550.00,
                description="Елегантна кімнатна рослина з тривалим періодом цвітіння. Потребує яскравого, але розсіяного світла.",
                category='indoor',
                # Тут можна було б додати image=... якщо б був файл
            )

            # Товар 2: Хвойні рослини
            Product.objects.create(
                name="Туя Смарагд",
                price=1200.00,
                description="Стрункий, колоноподібний ялівець, ідеально підходить для вертикального акценту у саду. Морозостійкий.",
                category='conifers',
            )

            # Товар 3: Плодові дерева
            Product.objects.create(
                name="Яблуня Голден Делішес",
                price=320.50,
                description="Осінній сорт яблуні з великими, солодкими та соковитими плодами. Відмінна стійкість до хвороб.",
                category='fruit_trees',
            )

            self.stdout.write(self.style.SUCCESS('Successfully created 3 initial products for catalog.'))
        else:
            self.stdout.write(self.style.WARNING('Initial products already exist.'))