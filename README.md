# User Authentication & Authorization API

Cистема аутентификации и авторизации.

## Основные принципы

- Аутентификация: JWT-токен
- Хранение паролей: bcrypt
- Soft-delete пользователей: поле `is_active = False`
- Разграничение доступа: роли + правила на уровне бизнес-сущностей

## Разграничения прав доступа
Правила доступа (AccessRoleRule) содержат 7 булевых флагов:
- read_permission          — читать свои записи
- read_all_permission      — читать все записи
- create_permission        — создавать записи
- update_permission        — редактировать свои записи
- update_all_permission    — редактировать любые записи
- delete_permission        — удалять свои записи
- delete_all_permission    — удалять любые записи
textТекущая логика проверки прав (функция `check_permission` в `access/permissions.py`):

## Доступные эндпоинты

| Метод | Путь                              | Название              | Описание                                                                 | Требуется авторизация | Примечания                                  |
|-------|-----------------------------------|-----------------------|--------------------------------------------------------------------------|------------------------|---------------------------------------------|
| POST  | `/api/auth/register/`            | register             | Регистрация нового пользователя                                          | Нет                   | Обязательные поля: first_name, last_name, email, password |
| POST  | `/api/auth/login/`               | login                | Вход в систему, выдача JWT-токена в cookie                               | Нет                   | Возвращает cookie `access_token`            |
| POST  | `/api/auth/logout/`              | logout               | Выход из системы (удаление cookie)                                       | Да                    | Просто удаляет cookie на клиенте            |
| GET   | `/api/auth/products/`            | products             | Получение списка всех продуктов                                          | Да                    | Проверяет право `read`/`read_all` на элемент "products" |
| POST  | `/api/user/delete/`              | delete               | Soft-delete аккаунта (is_active = False) + удаление токена               | Да                    | После выполнения повторный логин невозможен |
| GET   | `/api/user/profile/`             | update-profile (GET) | Просмотр текущих данных профиля                                          | Да                    | Возвращает first_name, last_name, middle_name, email |
| PUT   | `/api/user/profile/`             | update-profile (PUT) | Обновление профиля (first_name, last_name, middle_name)                  | Да                    | Изменяет только переданные поля             |

**Примечание**:  
Эндпоинт `/api/user/profile/` поддерживает два метода (GET и PUT) в одном представлении (`UpdateProfileView`).

## Запуск
1. Клонировать репозиторий:
    ```sh
    git clone https://github.com/Igor39-dev/task_EM.git
    cd user_auth
    ```

2. Создать и активировать виртуальное окружение:
    ```sh
    python -m venv .venv
    source .venv/bin/activate  # For Unix or MacOS
    .venv\Scripts\activate  # For Windows
    ```

3. Установка зависимостей:
    ```sh
    pip install -r requirements.txt
    ```

4. Применение миграций:
   ```sh
   python manage.py makemigrations
   python manage.py migrate
   ```

5. Запуск сервера:
    ```sh
    python manage.py runserver
    ```

6. Для регистрации тестого пользователя через API перейти на [http://localhost:8000/api/auth/register/](http://localhost:8000/api/auth/register/)

7. Зарегистрировать тестового пользователя(POST):
   ```sh
    {
        "first_name": "user1",
        "last_name": "surname1",
        "middle_name": "midname1",
        "email": "user1@mail.com",
        "password": "123456"
    }
    ```

## Тестовые данные (через shell)
```sh
python manage.py shell:
```

```python
from users.models import User
from access.models import Role, UserRole, BusinessElement, AccessRoleRule
from products.models import Product
import bcrypt

# Роли
for name in ['admin', 'manager', 'user']:
    Role.objects.create(name=name)

admin_role = Role.objects.get(name='admin')
user_role = Role.objects.get(name='user')

# Пользователь (если регистрировали через API)
user = User.objects.get(email="user1@mail.com")

# Присваиваем роль admin этому пользователю
UserRole.objects.create(user=user, role=admin_role)

# Бизнес-элемент "products"
products_elem = BusinessElement.objects.create(code="products")

# Полные права на products для роли admin
AccessRoleRule.objects.create(
    role=admin_role,
    element=products_elem,
    defaults={
        'read_all_permission': True,
        'create_permission': True,
        'update_all_permission': True,
        'delete_all_permission': True,
    }
)

# Тестовые продукты
Product.objects.bulk_create([
    Product(name="product1", price=799.99, owner=user),
    Product(name="product2", price=1199.00, owner=user),
])
```
Для проверки API:

- Зарегистрировать пользователя → [/api/auth/register/](http://localhost:8000/api/auth/register/)
- Залогиниться → [/api/auth/login/](http://localhost:8000/api/auth/login/)
- Посмотреть/Обновить профиль → [/api/user/profile/](http://localhost:8000/api/user/profile/)
- Получить список продуктов → [/api/auth/products/](http://localhost:8000/api/auth/products/)
- Удалить аккаунт → [/api/user/delete/](http://localhost:8000/api/user/delete/)
- Попробовать любой запрос с тем же токеном → должен вернуть 401
 