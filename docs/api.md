# API documentation

## /api/login
**Методы:** POST  
**Принимает:**  
```json
{
  "username": "string",
  "password": "string"
}
```

**Возвращает:**

- успешный логин

    код 200
```json
{
  "message": "Login successful"
}
```

- ошибка авторизации

   код 401
```json
{
  "error": "Invalid username or password"
}
```

## /api/register
**Методы:** POST  
**Принимает:**  
```json
{
  "username": "string",
  "password": "string"
}
```

**Возвращает:**

- успешная регистрация

    код 201
```json
{
  "message": "Registration successful"
}
```

- пользователь уже существует

   код 409
```json
{
  "error": "User already exists"
}
```

- Юзернейм или пароль не соответствует требованиям

   код 400
```json
{
  "error": "Invalid username" // или "Invalid password"
}
```

## /api/logout
**Методы**: GET

**Возвращает:**

- Успешный выход:

   код 200
   
```json
{
  "message": "Logged out successfully"
}
```
