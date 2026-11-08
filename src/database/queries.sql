-- SELECT с WHERE (3 штуки)
SELECT * FROM Users WHERE role = 'executor';
SELECT * FROM Requests WHERE status_id = 1;
SELECT * FROM Requests WHERE applicant_id = 1;

-- SELECT с JOIN (2 штуки)
SELECT r.id, r.title, s.name AS status, c.name AS category FROM Requests r JOIN Statuses s ON r.status_id = s.id JOIN Categories c ON r.category_id = c.id;
SELECT u.full_name AS applicant, r.title FROM Requests r JOIN Users u ON r.applicant_id = u.id;

-- UPDATE (2 штуки)
UPDATE Requests SET status_id = 3 WHERE id = 4;
UPDATE Users SET full_name = 'Смирнов А.А.' WHERE id = 5;
