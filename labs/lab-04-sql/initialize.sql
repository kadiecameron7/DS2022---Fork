DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    users_id INT PRIMARY KEY, 
    username VARCHAR(30),
    email VARCHAR(50),
    created_at DATETIME
);

CREATE TABLE posts ( 
    post_id INT PRIMARY KEY, 
    users_id INT, 
    content TEXT, 
    posted_at DATETIME, 
    FOREIGN KEY (users_id) REFERENCES users(users_id)
);

INSERT INTO users (users_id, username, email, created_at) 
VALUES (123, 'kc123', 'kc123@gmail.com', '2026-06-12 09:30:00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (101, 123, 'yay!', '2026-08-16 10:15:00');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (124, 'kr124', 'kr124@gmail.com', '2026-01-15 09:45:00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (102, 124, 'lets go', '2026-07-01 08:13:00');

INSERT INTO users (users_id, username, email, created_at) VALUES (125, 'tc125', 'tc125@gmail.com', '2026-07-11 12-07-00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (103, 125, 'wow', '2026-07-12 08-44-00');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (126, 'hannah126', 'hannah126@gmail.com', '2026-09-14 09-07-00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (104, 126, 'hannah', '2026-07-11 04-13-00');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (127, 'vivian127', 'vivian127@gmail.com', '2027-08-14 06-12-00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (105, 127, 'vivian', '2027-09-01 00-14-00');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (128, 'kennedy128', 'kennedy128@gmail.com', '2023-01-09 09-08-00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (106, 128, 'kennedy', '2024-09-02 03-44-00');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (129, 'brett129', 'brett129@gmail.com', '2024-09-08 07-09-00');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (107, 129, 'brett', '2022-02-02 03-03-03');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (130, 'suzie130', 'suzie130@gmail.com', '08-08-08 06-06-06');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (108, 130, 'suzie', '05-05-05 05-05-05');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (131, 'pam131', 'pam131@gmail.com', '2007-07-07 09-09-09');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (109, 131, 'pam', '2029-09-08 07-06-55');

INSERT INTO users (users_id, username, email, created_at) 
VALUES (132, 'm132', 'm132@gmail.com', '2005-09-08 04-33-22');

INSERT INTO posts (post_id, users_id, content, posted_at) 
VALUES (110, 132, 'm', '2004-09-07 09-08-03');