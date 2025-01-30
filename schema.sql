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

CREATE TABLE IF NOT EXISTS orders (
    -- планирование и управление закупками инвентаря
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(128) NOT NULL,
    amount INT NOT NULL,
    price INT NOT NULL,
    supplier VARCHAR(128) NOT NULL
);

CREATE TABLE IF NOT EXISTS inventory_requests (
    -- заявки на получение инвентаря
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    message VARCHAR(512) DEFAULT NULL,
    request_status ENUM('pending','approved','declined') NOT NULL DEFAULT 'pending', -- отслеживание статуса заявок на получение инвентаря
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
);

CREATE TABLE IF NOT EXISTS fix_requests (
    -- заявки о необходимости ремонта или замены инвентаря;
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    item_id INT NOT NULL,
    request_status ENUM('pending','approved','declined') NOT NULL DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    FOREIGN KEY (item_id) REFERENCES inventory(id) ON DELETE CASCADE
);
