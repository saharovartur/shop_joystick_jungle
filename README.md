shop_joystick_jungle

## Проект Django: shop_joystick_jungle

Интернет-магазин для геймеров: JoyStick Jungle

## Технологии:

Backend: Django: 4.1, Python: 3.10, Celery, RabbitMQ, Flower
База данных: PostgreSQL,
Frontend: HTML/CSS, SVGBox, Boxicons, Pay: Stripe

## Описание функциональности

1. Разработал вывод списка товаров по категориям на главной странице.
   1.1 Разработал блок с категориями товаров:
   ![image](https://github.com/user-attachments/assets/ea84b521-d915-4ec6-8af4-25a403c7ea52)
   1.2 Разработал страницу с карточкой товара:
   ![image](https://github.com/user-attachments/assets/2273fcef-d121-40a5-a0d5-95f6f1ac9673)

2. Разработал корзину товаров. Товары можно добавлять в корзину с помощью кнопки на странице карточки с товаром.

3. Разработана возможность оформить заказ заполнив форму, данные о заказах хранятся в БД. Асинхронно отправляется
   уведомление на почту о совершенном заказе.
4. Разработана возможность оплатить заказ, настроена интеграция с Stripe(https://stripe.com/)
    1. Страница заказа --> страница подтверждения оплаты --> ввод данных карты:
       ![image](https://github.com/user-attachments/assets/dca2c7e4-65ee-4cbf-930f-1b234715d9c0)
       --> страница об успехе или отказе.
       Настроки stripe локализованы под рубли.
    2. Разработан веб-хук для изменения статуса заказа на "оплачен" если оплата была успешно совершена.
5. Доработана админская часть: добавлена возможность просмотра деталей заказа на отдельной странице + выгрузка
   счет-фактуры в формате PDF.

## Установка

1.Клонируйте репозиторий.
2.Перейдите в директорию проекта.
3.Установки зависимости: pip install -r requirements.txt
4.Настройте базу данных в файле settings.py.
5.Выполните миграции: py manage.py makemigrations > python manage.py migrate
6.Запустите сервер: py manage.py runserver

## Настройка окружения

Убедитесь, что у вас установлен Python версии [3.10].

## Лицензия

Проект распространяется под лицензией MIT.

## Контакты

Разработчик: Артур Сахаров
Telegram: grizz_dev
