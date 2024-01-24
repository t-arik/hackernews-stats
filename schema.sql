CREATE TABLE IF NOT EXISTS news_page (
    id INTEGER NOT NULL,
    captured_at TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    rank INTEGER NOT NULL,
    title TEXT NOT NULL,
    site TEXT NOT NULL,
    age TEXT NOT NULL,
    points INTEGER,
    author TEXT,
    comments INTEGER,
    PRIMARY KEY(id, captured_at)
);

CREATE TABLE IF NOT EXISTS item_page (
    id INTEGER NOT NULL,
    captured_at TEXT,
    title TEXT,
    link TEXT,
    description TEXT,
    points INTEGER,
    user TEXT,
    comment_count INTEGER,
    PRIMARY KEY(id, captured_at)
);

CREATE TABLE IF NOT EXISTS comment (
    id INTEGER NOT NULL,
    captured_at INT NOT NULL,
    idx INTEGER NOT NULL,
    indent INTEGER NOT NULL,
    user TEXT,
    timestamp TEXT NOT NULL,
    age TEXT NOT NULL,
    content TEXT,
    item_id INT NOT NULL,
    PRIMARY KEY(id, captured_at)
    FOREIGN KEY(item_id) REFERENCES item_page(id)
);
