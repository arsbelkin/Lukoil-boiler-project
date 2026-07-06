# Документация к API

**API** *(Application Programming Interface)* - это набор правил и инструкций, который позволяет разным компьютерным программам общаться между собой. Он, служит "переводчиком" или мостом, позволяя одному приложению запрашивать данные или функции у другого, не вникая в его внутреннее устройство.


## Запросы и ответы

- Главная страничка `GET /`

Response example:
  - headers :
```json
{
    "content-type" : "text/html",
}
```


- Получение данных `GET /api/v1/data`

Response example:
  - headers :
```json
{
    "content-type" : "application/json",
}
```

  - body :
```json
{
    "inputHotTemp" : "float",
    "inputColdTemp" : "float",
    "outputTemp" : "float",
    "waterLevel" : "float",
    "outputTemp" : "float",
    "valveHot" : "float",
    "valveCold" : "float",
    "valveOut" : "float",
}
```


- Установка значений `POST /api/v1/data`

Request example:
  - headers :
```json
{
    "content-type" : "application/json",
}
```

  - body :
```json
{
    "name" : "string",
    "value" : "float",
}
```

Response example: *statusCode*


- График `GET /api/v1/graph`

Response example:
  - headers :
```json
{
    "content-type" : "application/json",
}
```

  - body :
```json
{
    "tempGraph" : "string",
    "waterLevelGraph" : "string",
}
```
