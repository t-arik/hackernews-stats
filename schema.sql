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
    id INTEGER,
    captured_at TEXT,
    title TEXT,
    link TEXT,
    description TEXT NOT NULL,
    points INTEGER NOT NULL,
    user TEXT NOT NULL,
    comment_count INTEGER NOT NULL,
    PRIMARY KEY(id, captured_at)
);

CREATE TABLE IF NOT EXISTS comment (
    id INTEGER NOT NULL,
    idx INTEGER NOT NULL,
    indent INTEGER NOT NULL,
    user TEXT NOT NULL,
    timestamp TEXT NOT NULL,
    age TEXT NOT NULL,
    contents TEXT NOT NULL,
    PRIMARY KEY(id)
);
