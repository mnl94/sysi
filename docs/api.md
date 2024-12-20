# API documentation

## /api/login
**Методы:** POST  

**Роль**: Любая

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

- ошибка

   код 401
```json
{
  "error": "Login Failed"
}
```

## /api/register
**Методы:** POST
  
**Роль**: Любая

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
  "error": "Invalid username"
}
```

- Непредвиденная ошибка

   код 500 
```json
{
  "error": "Unexpected error"
}
```

## /api/logout
**Методы**: GET

**Роль**: Любая

**Возвращает:**

- Успешный выход:

   код 200
   
```json
{
  "message": "Logged out successfully"
}
```


## /api/getInventoryUser
**Методы**: GET

**Роль**: user

**Возвращает**:

- Успех:

   код 200

   список списков [ [name1,amount1,itemCondition1], [name2,amount2,itemCondition2] ]

```json
[
  [
    "boots",
    3,
    "new"
  ],
  [
    "bat",
    3,
    "used"
  ]
]
```

- Не авторизован:

   код 401

```json
{
  "error": "Unauthorized"
}
```
