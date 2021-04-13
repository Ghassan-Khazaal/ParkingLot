# Reserve a parking spot

Resrve a parking spot for a vehicle.

**URL** : `/resrve/`

**Method** : `POST`

**Request Body** : 

```json
{
    "vehicleId": "The licence number (string)",
    "vehicleType": "id (int)"
}
```

## Success Response

**Code** : `200 OK`

**Content examples**

After reserving the first car, the first parking spot in the first level will get reserved, and the response will have the level number and the spot label

```json
{
    "status": "success",
    "data": {
        "level": 1,
        "label": "C1"
    }
}
```

When the garage is full for the vehicle type, the reponse will be

```json
{
    "status": "error",
    "data": "The garage is full"
}
```

When the vehicle is already in the garage, the reponse will be

```json
{
    "status": "error",
    "data": "The vehicle is already in the garage"
}
```

When the vehicle type is not in the db, the response will be

```json
{
    "status": "error",
    "data": "Wrong vehicle type"
}
```
