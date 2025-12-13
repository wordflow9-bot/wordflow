CREATE TABLE IF NOT EXISTS words (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    word TEXT NOT NULL,
    translation TEXT NOT NULL,
    total_cnt INTEGER, 
    correct_cnt INTEGER,
    mastery_level INTEGER NOT NULL DEFAULT 0 -- в перспективе mastery level зависит не только от total_cnt и correct_cnt, но и от времени с последнего правильного ответа/теста со словом
    -- created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    -- updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
