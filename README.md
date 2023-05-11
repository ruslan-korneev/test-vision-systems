## Установка
```bash
git clone 
cd test-vision-systems
docker-compose up -d
```

## Использование
### Endpoint 1 - `/api/v1/face/detection`
request:
```bash
curl -X POST -F \
    "image=@/home/user/image.jpg" \
    http://0.0.0.0:5000/api/v1/face/detection
```
response - HTTP 200 OK
```json
[
    {
        "bounding_box": [0, 0, 100, 100],
        "landmarks": [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
        ]
    },
    {
        "bounding_box": [0, 0, 100, 100],
        "landmarks": [
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0],
            [0, 0]
        ]
    }
]
```
### Endpoint 2 - `/api/v1/face/comparison`
request:
```bash
curl -X POST -F \
    "image=@/home/user/image.jpg" \
    http://0.0.0.0:5000/api/v1/face/comparison
```
response - HTTP 200 OK
```json
{
    "faces": 2,
    "matches": 1
}
```
