CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(60) NOT NULL,
    role ENUM('admin', 'user') NOT NULL DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inventory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL, -- не UNIQUE потому что один и тот-же вид предмета может быть в разных состояниях
    amount INT NOT NULL,
    item_condition ENUM('new', 'used', 'broken') NOT NULL DEFAULT 'new',
    owned_by INT DEFAULT NULL,
    FOREIGN KEY (owned_by) REFERENCES users(id)
);



