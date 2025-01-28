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

Возвращает закреплённый за пользователем инвентарь

**Методы**: GET

**Роль**: user, admin

**Возвращает**:

- Успех:

   код 200

   список списков [ [id1,name1,amount1,itemCondition1], [id2,name2,amount2,itemCondition2] ]

```json
[
  [
    1,
    "boots",
    3,
    "new"
  ],
  [
    2,
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

## /api/getInventoryAdmin
**Методы**: GET

**Роль**: admin

**Возвращает**:

- Успех:

   код 200

   список списков [ [id1, name1,amount1,itemCondition1, ownedBy1], [id2, name2,amount2,itemCondition2, ownedBy2] ]


```json
[
  [
    1,
    "item1",
    3,
    "new",
    "user1"
  ],
  [
    2,
    "item2",
    3,
    "used",
    "user2"
  ]
]
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```


## /api/addItem

Добавляет позицию инвентаря в БД

**Методы**: POST

**Роль**: admin

**Принимает:**  

```json
{
  "item_name": "string",
  "amount": 3 ,
  "owned_by": "string"
}
```

**Возвращает**:

- Успех:

   код 200


```json
{
  "message":"Item added Successfully!"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```

- Неправильный json

   код 400

```json
{
  "error": "Invalid json provided"
}
```

- Неправильное название

   код 400

```json
{
  "error": "Invalid or missing name"
}
```

- Неправильное количество

   код 400

```json
{
  "error": "Invalid or missing amount"
}
```

- Неизвестная ошибка

   код 500

```json
{
  "error": "Unexpected error"
}
```


## /api/changeItem

изменяет предмет инвентаря по id

**Методы**: POST

**Роль**: admin

**Принимает**:
```json
{
  "item_id": 1,
  "item_name": "bats",
  "amount": 42,
  "condition": "used",
  "owned_by": "user1"
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Item changed successfully"
}
```

- Предмет не существует

   код 400

```json
{
  "error":"Item does not exist"
}
```

- Ошибки валидации

   код 400

```json
{
  "error": "Invalid or missing <field_name>"
}
```

- Пользователь не существует

   код 400

```json
{
  "error": "User does not exist"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```

- Неизвестная ошибка

   код 500

```json
{
  "error": "Unexpected error"
}
```

## /api/deleteItem

удаляет предмет по id

**Методы**: POST

**Роль**: admin

**Принимает**:

```json
{
  "item_id":1
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Item deleted successfully"
}
```

- Предмет не существует

   код 400
  
```json
{
  "error":"item does not exist"
}
```

- Ошибки валидации

   код 400

```json
{
  "error":"Invalid or missing item_id"
}
```

- Не авторизован

   код 401

```json
{
  "error":"No admin rights"
}
```

## /api/requestFix

создаёт запрос на починку инвентаря

**Методы**: POST

**Роль**: user, admin

**Принимает:**  

```json
{
  "item_id": 1,
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Request created"
}
```

- Ошибки валидации

   код 400

```json
{
  "error": "Invalid or missing <field_name>"
}
```

- Предмета не существует или вы не владелец предмета

   код 400

```json
{
  "error": "Item does not exist or you are not the owner"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "Unauthorized"
}
```

## /api/approveFixRequest

принять запрос на починку инвентаря

**Методы**: POST

**Роль**: admin

**Принимает:**  

```json
{
  "request_id": 1,
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Request approved"
}
```

- запрос уже принят/отклонён или его не cуществует

   код 400

```json
{
  "error": "Request does not exist or already approved/denied"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```


## /api/denyFixRequest

отклонить запрос на починку инвентаря

**Методы**: POST

**Роль**: admin

**Принимает:**  

```json
{
  "request_id": 1,
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Request denied"
}
```

- запрос уже принят/отклонён или его не cуществует

   код 400

```json
{
  "error": "Request does not exist or already approved/denied"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```


## /api/getFixRequests

возвращает запросы на починку со статусом 'pending'

**Методы**: GET

**Роль**: admin

**Возвращает**:

- Успех:

   код 200

   список списков [ [id1,username1,itemId1,status1], [id2,username2,itemId2,status2] ]

```json
[
  [
    1,
    "user1",
    3,
    "pending"
  ],
  [
    2,
    "user2",
    4,
    "pending"
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


## /api/createOrder

добавляет закупку в план

**Методы**: POST

**Роль**: admin

**Принимает:**  

```json
{
  "item_name": "item1",
  "amount": 1,
  "price": 1,
  "supplier": "supplier1"
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Order created"
}
```

- Ошибки валидации

   код 400

```json
{
  "error": "Invalid or missing <field_name>"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```


## /api/changeOrder

изменяет план закупок по id

**Методы**: POST

**Роль**: admin

**Принимает**:
```json
{
  "item_id": 1,
  "item_name": "item1",
  "amount": 42,
  "supplier": "supplier1"
}
```

**Возвращает**:

- Успех:

   код 200

```json
{
  "message":"Order changed"
}
```

- Ошибки валидации

   код 400

```json
{
  "error": "Invalid or missing <field_name>"
}
```

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```


## /api/generateReport

создает xlsx файл с текущим состоянием инвентаря

**Методы**: GET

**Роль**: admin

**Возвращает**:

- Успех:

   код 200

   xlsx файл

- Не авторизован:

   код 401

```json
{
  "error": "No admin rights"
}
```