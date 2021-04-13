# Checkout a vehicle

Remove a vehicle from the garage (assign a checkout time for it)

**URL** : `/checkout/`

**Method** : `POST`

**Request Body** : 

```json
{
    "vehicleId": "The licence number (string)",
}
```

## Success Response

**Code** : `200 OK`

**Content examples**

When the vehicle is not in the garage, the response will be

```json
{
    "status": "error",
    "data": "The vehicle is not in the garage"
}
```
