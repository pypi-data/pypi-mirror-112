# Утилитарный пакет для работы с django

## Добавление бекенда аутентификации через Keycloak

В настройки django добавьте переменную AUTHENTICATION_BACKENDS с указанием класса 'KeycloakBackend'

```
AUTHENTICATION_BACKENDS = (
    'vtb_django_utils.backends.KeycloakBackend',
    'django.contrib.auth.backends.ModelBackend',
)
```

## Добавление возможности аутентификации с токеном Keycloak
Обратите внимание, что если токен "протух", то выдается ошибка 403. 
Если вы используете пакет межсервисного взаимодействия vtb-http-interaction, 
то в нем не предусмотрено получение нового токена при ошибке 403, только 401. Неправильно делать вызовы сервис->сервис. 
Запрос должен идти через Kong с использованием плагина jwt-keycloak.
```
authentication_classes = (SessionAuthentication, KeycloakAuthentication)
```