INSERT INTO Statuses (name) VALUES ('Новая'), ('В работе'), ('Выполнена'), ('Закрыта');
INSERT INTO Categories (name) VALUES ('Оборудование'), ('Доступы'), ('Программное обеспечение');
INSERT INTO Users (full_name, email, role) VALUES 
('Иванов Иван', 'ivanov@example.com', 'applicant'),
('Петров Петр', 'petrov@example.com', 'executor'),
('Сидорова Анна', 'sidorova@example.com', 'operator'),
('Админов Админ', 'admin@example.com', 'admin');
INSERT INTO Requests (title, description, applicant_id, executor_id, status_id, category_id) VALUES 
('Не работает принтер', 'Принтер в 304 кабинете выдает ошибку.', 1, 2, 2, 1),
('Восстановить пароль', 'Забыл пароль от учетной записи.', 1, NULL, 1, 2),
('Установить Excel', 'Нужен Excel для работы.', 1, 2, 3, 3);
INSERT INTO Comments (request_id, user_id, text) VALUES 
(1, 2, 'Выехал на место, смотрю принтер.'),
(1, 1, 'Спасибо, жду.'),
(2, 3, 'Пароль сброшен, проверьте почту.');
