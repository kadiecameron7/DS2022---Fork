SELECT users.username, posts.content, posts.posted_at
FROM posts
JOIN users ON posts.users_id = users.users_id
WHERE posts.posted_at > '2026-06-01 00:00:00';

