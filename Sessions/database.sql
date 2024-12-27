CREATE TABLE IF NOT EXISTS receipts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    payment_receipt TEXT NOT NULL,  -- Store file path or URL here
    file_type TEXT NOT NULL,        -- 'image' or 'pdf'
    FOREIGN KEY (user_id) REFERENCES users (id)
)
