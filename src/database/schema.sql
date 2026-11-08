CREATE TABLE Statuses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE Categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
);
CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    role TEXT NOT NULL CHECK(role IN ('admin', 'operator', 'executor', 'applicant'))
);
CREATE TABLE Requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    applicant_id INTEGER NOT NULL,
    executor_id INTEGER,
    status_id INTEGER NOT NULL,
    category_id INTEGER NOT NULL,
    FOREIGN KEY (applicant_id) REFERENCES Users(id),
    FOREIGN KEY (executor_id) REFERENCES Users(id),
    FOREIGN KEY (status_id) REFERENCES Statuses(id),
    FOREIGN KEY (category_id) REFERENCES Categories(id)
);
CREATE TABLE Comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    request_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (request_id) REFERENCES Requests(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES Users(id)
);
