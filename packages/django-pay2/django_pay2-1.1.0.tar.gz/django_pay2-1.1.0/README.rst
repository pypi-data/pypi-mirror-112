=============================
DjangoPay2
=============================

.. image:: https://travis-ci.org/la1t/django_pay2.svg?branch=master
    :target: https://travis-ci.org/la1t/django_pay2

Интеграция платежных систем для Django

Quickstart
----------

Установите DjangoPay2::

    pip install django_pay2

Добавьте приложение в `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'django_pay2',
        ...
    )

Добавьте Django Pay's URLы в urlpatterns:

.. code-block:: python


    urlpatterns = [
        ...
        path('payments/', include('django_pay2.urls')),
        ...
    ]

Платежи
-----------------

Любой платеж создается методом create_<название-платежной-системы>_payment. Метод возвращает объект типа PaymentMethod. Существует два типа
PaymentMethod — PaymentForm и RedirectMethod. Первый должен сериализовываться и отправляться на front. Второй можно либо также сериализовать
и отправить на фронт, либо возвратить редирект.

Так же метод создает объект типа Payment. Эта модель отвечает за сохранение информации о платеже, а так же об объекте-инициаторе платежа. 
После успешной оплаты он отправляет сигнал `payment_received` привязанному объекту. 

TODO
--------

- [*] Сериализаторы для PaymentForm и RedirectMethod
- [ ] Интеграция с free_kassa
- [ ] `handle_form_debug` проверяет, что ему пришла валидная форма
- [*] Переписывание тестов на pytest
- [ ] Инструкция по написанию собственных провайдеров
- [ ] Инструкция по добавлению и настройке каждого провайдера
- [ ] Более подробная инструкция по использованию
- [ ] Инструкция по увеличению версии


Разработка
----------

Установка development зависимостей

::
  pip install -r requirements_dev.txt

Запуск тестов

::
  tox
