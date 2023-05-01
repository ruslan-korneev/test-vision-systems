Тестовое задание для компании "Vision Systems"
===============================================
## Задание
Необходимо разработать web-сервис (REST API) на flask, который реализует два эндпоинта (endpoint). Интерфейсы и реализация на ваше усмотрение.
Первый эндпоинт осуществляет получение изображений из вне, анализирует наличие лиц на нем, и каждый запрос к нему формирует историю запросов
в sqlite БД. Для взаимодействия с БД использовать SQLAlchemy. Второй эндпоинт позволяет понять были в истории запросы с такими же лицами.

Результатом выполнения работы должен быть архив/git-репозиторий, который должен содержать Dockerfile, чтобы проверяющий мог собрать докер-
образ и запустить web-сервис. В README должен быть описан формат запросов в стиле curl. Можно добавить docker-compose.yaml .

## Endpoint 1
**Входные данные:** запрос с изображением (jpeg).
**Выходные данные:** информация об окаймляющем прямоугольнике (bounding box) и координатах пяти лицевых точек для каждого лица на изображении.
ML часть сервиса должна использовать две функции из библиотеки dlib: get_frontal_face_detector и shape_predictor . Примерный код:
```python
face_detector = dlib.get_frontal_face_detector()
dets = face_detector(image, 1)
predictor = dlib.shape_predictor(model_path) # model_path - путь к модели, которую надо скачать
for d in dets:
    shape = predictor(image, d)
    for i in range(shape.num_parts):
        p = shape.part(i) # точка на лице
```
Модель определения точек на лице надо скачать [отсюда](https://github.com/davisking/dlib-models/blob/master/shape_predictor_5_face_landmarks.dat.bz2). Ссылки на python [примеры](https://www.programcreek.com/python/example/103113/dlib.get_frontal_face_detector). Ссылка на С++ код с [примером](http://dlib.net/face_detector.py.html). [Документация](http://dlib.net/imaging.html#get_frontal_face_detector) у dlib "чудесная", но с
этим приходится работать в реальности. Внутри вы можете найти код на на C++, иногда на python, но я не нашел описание параметров функций.
Рекомендуется найти docker-image, в котором уже установлен dlib и его использовать.


Формирование истории необходимо сделать самописное, т.е. не использовать стандартные инструменты логирования. После обработки запроса
необходимо сохранить входное изображение на диск и в БД sqlite сохранять информацию о пути к этому изображению, а также другие атрибуты
необходимые для работы второго эндпоинта.

## Endpoint 2
**Входные данные:** запрос с изображением (jpeg).
**Выходные данные:** два целых числа. Первое - количество лиц на переданном изображении. Второе - количество совпадений лиц на этом изображении с
лицами уже ранее просмотренными этим сервисом. Два лица считаются совпадающими, если положения соответствующих точек этих лиц отличаются
не более чем на 10 по стандартной (евклидовой) метрике расстояния.

## Установка
```bash
git clone 
cd vision_systems_test_task
docker-compose up -d
```

## Использование
### Endpoint 1 - `/api/v1/face_detection`
request:
```bash
curl -X POST -F \
    "image=@/home/user/image.jpg" \
    http://localhost:5000/api/v1/face/detection
```
response - HTTP status code 200 if faces found, 404 if not found:
```json
{
    "faces": [
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
}
```
### Endpoint 2 - `/api/v1/face_comparison`
request:
```bash
curl -X POST -F \
    "image=@/home/user/image.jpg" \
    http://localhost:5000/api/v1/face/comparison
```
response - HTTP status code 200 if faces found, 404 if not found:
```json
{
    "faces": 2,
    "matches": 1
}
```