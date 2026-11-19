# Контракт REST API (ЛР7, итоговый — сверено с request_service.py)

## Реализуемые эндпоинты

| Метод | Путь | Назначение | Кто может | Успех | Ошибки |
|---|---|---|---|---|---|
| GET | /requests | Список заявок (фильтры status_id, category_id) | admin/operator — все; executor — только свои; applicant — только свои | 200 | 400, 403, 422 |
| GET | /requests/{id} | Карточка заявки | admin/operator — любую; executor — назначенную; applicant — свою | 200 | 403, 404, 422 |
| POST | /requests | Создать заявку | admin, operator, applicant | 201 | 400, 403, 404, 422 |
| POST | /requests/{id}/assign | Назначить исполнителя | admin, operator | 200 | 400, 403, 404, 409, 422 |
| PATCH | /requests/{id}/status | Сменить статус | admin/operator — любые по таблице; executor — только свои и допустимые | 200 | 400, 403, 404, 409, 422 |
| GET | /requests/{id}/comments | Комментарии заявки | admin/operator — любую; executor — назначенную; applicant — свою | 200 | 403, 404 |
| POST | /requests/{id}/comments | Добавить комментарий | admin/operator — любую; executor — назначенную; applicant — свою | 201 | 400, 403, 404, 422 |
| GET | /categories | Справочник категорий | все авторизованные | 200 | 401 |
| GET | /statuses | Справочник статусов | все авторизованные | 200 | 401 |
| GET | /users | Список пользователей (для выбора исполнителя) | admin, operator | 200 | 403 |
| GET | /users/me | Текущий пользователь | все авторизованные | 200 | 401 |

## Аутентификация (упрощённая, учебная)
Заголовок `X-User-Id: <int>`. Сервер ищет в Users, берёт role. Нет заголовка / нет пользователя → 401. Подделка тривиальна — для учебного проекта допустимо, в проде заменить на токен.

## Отклонено / не реализовано (вне объёма ЛР6)
- POST /requests для executor — отклонено: `CAN_CREATE` без executor.
- PATCH /requests/{id}, DELETE /requests/{id} — нет методов в сервисе ЛР6.
- CRUD /categories, /statuses — нет методов; оставлены только GET-справочники.
- Фильтр по чужим id в GET /requests — реализуем «тихое сужение» по роли, а не 403.
