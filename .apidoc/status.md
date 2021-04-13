# Get a status report

A status report that show the total/free/reserved parking spots per level per vehicle type

**URL** : `/status/`

**Method** : `GET`

## Success Response

**Code** : `200 OK`

**Content examples**

```json
{
  "status": "Success",
  "data": {
    "1": {
      "Car": {
        "all": 3, 
        "free": 0, 
        "taken": 3
      }, 
      "Motorbike": {
        "all": 2, 
        "free": 1, 
        "taken": 1
      }
    }
  }
}
```
