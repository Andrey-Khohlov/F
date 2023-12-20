from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
import uvicorn
from fastapi import FastAPI, Cookie, Depends, HTTPException, Response, Form, Request, Header, status
from fastapi.responses import FileResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials, OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models.models import User, User1, User2, Feedback, UserCreate, SearchProducts, User3
from data.fake_db import sample_products, users_db, user_data


title = 'My first App'
app = FastAPI(title=title)


# @app.get("/")
# async def root():
#     return FileResponse('../templates/index.html')


@app.get("/hello")
async def hello():
    return 'Hello World!'


@app.post("/calculate")
def calculate(num1: int, num2: int):
    return {'result': num1 + num2}



# Реализуйте функцию, которая при получении GET-запроса по дополнительному маршруту `/users` возвращала бы JSON
# с данными о пользователе (юзере).

@app.get("/users_1")
def get_user():
    user_data = {
        "id": 1,
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    user = User(**user_data)
    return user


# 2. Создайте новый маршрут `/user`, который принимает запросы POST и принимает полезную нагрузку JSON,
# содержащую пользовательские данные, соответствующие модели `User1`.
# 3. Реализуйте функцию для проверки того, является ли пользователь взрослым (возраст >= 18)
# или несовершеннолетним (возраст < 18).
# 4. Верните пользовательские данные вместе с дополнительным полем `is_adult` в ответе JSON, указывающим,
# является ли пользователь взрослым (True) или несовершеннолетним (False).
@app.post("/user_age")
async def root(user1: User1):
    if user1.age >= 18:
        is_adult = True
    else:
        is_adult = False
    return user1.model_dump() | {'is_adult': is_adult}


@app.post("/user2")
async def root(user2: User2):
    '''тут мы можем с переменной user, которая в себе содержит объект класса User с соответствующими полями (и указанными типами), делать любую логику
    - например, мы можем сохранить информацию в базу данных
    - или передать их в другую функцию
    - или другое'''
    print(
        f'Мы получили от юзера {user2.username} такое сообщение: {user2.message}')  # тут мы просто выведем полученные данные на экран в отформатированном варианте
    return user2  # или можем вернуть обратно полученные данные, как символ того, что данные получили, или другая логика на ваш вкус

# Пример пользовательских данных (для демонстрационных целей)
fake_users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"},
}


# Конечная точка для получения информации о пользователе по ID
@app.get("/users_2/{user_id}")
def read_user(user_id: int):
    if user_id in fake_users:
        return fake_users[user_id]
    return {"error": "User not found"}


@app.get("/users/{user_id}")
def read_users(limit: int = 10):
    return dict(list(fake_users.items())[:limit])

"""
1. Определите Pydantic модель с именем "Feedback" (обратная связь) со следующими полями:
   - `name` (str)
   - `message` (str)

2. Создайте новый маршрут публикации "/feedback", который принимает данные JSON в соответствии с моделью `Feedback`.

3. Реализуйте функцию для обработки входящих данных обратной связи и ответа сообщением об успешном завершении.

4. Сохраните данные обратной связи в списке или хранилище данных, чтобы отслеживать все полученные отзывы.
"""
feedback_fake_db = []


@app.post("/feedback")
async def feedback(fb: Feedback):
    feedback_fake_db.append(fb.model_dump())
    print(feedback_fake_db)
    return {'message': f'Feedback received. Thank you, {fb.username}!'}


# 3.1 Обработка HTTP-запросов (GET, POST, PUT, DELETE и т.д.)
@app.post("/create_user")
async def create_user(user: UserCreate):
    return user


@app.post("/products/search")
async def search_products(query: SearchProducts):
    results = []
    for product in sample_products:
        if query.category is not None and product["category"] != query.category:
            continue
        elif query.keyword in product["name"].lower():
            results.append(product)
    return results[:query.limit] if query.limit is not None else results


@app.get("/product/{product_id}")
async def get_product(product_id: int):
    for product in sample_products:
        if product["product_id"] == product_id:
            return product
    else:
        return {"error": "Product not found"}


# 3.2 Дополнительные типы, асинхронность и параметры Cookie
# Пример валидации учетных данных
async def validate_user(username: str, password: str):
    # Здесь должна быть логика проверки учетных данных
    for user_id, user in users_db.items():
        if user["name"] == username and user["password"] == password:
            return user_id
    return False


@app.post("/login_cookie")
async def login(response: Response, username: str = Form(...), password: str = Form(...)):
    user_id = await validate_user(username, password)
    if user_id is not False:
        # Установка безопасного файла cookie с уникальным значением
        now = datetime.now()
        session_token = now.strftime("%Y%m%d%H%M%S")  # Генерация уникального значения
        response.set_cookie(key="session_token", value=session_token, max_age=60, httponly=True)
        users_db[user_id]['token'] = session_token
        print(now, session_token)
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")

# Пример валидации файла cookie "session_token"
# async def validate_session_token(session_token: str = Cookie(None)):
#     # Здесь должна быть логика проверки файла cookie "session_token"
#     if session_token == "unique_session_token":  # Проверка на уникальное значение
#         return True
#     else:
#         return False


@app.get("/user")
async def get_user_profile(request: Request):
    token = request.cookies.get("session_token")
    print(users_db[6])
    print('token', token)
    if token:
        for user_id, user in users_db.items():  # Возвращение информации профиля пользователя в формате JSON
            try:
                if user['token'] == token:
                    return user
            except KeyError:
                continue
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")


@app.get("/items/")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}
# async def read_items(x_token: Annotated[list[str] | None, Header()] = None):
#     return {"X-Token values": x_token}


@app.get("/")
# def root():
#     data = "Hello from here"
#     return Response(content=data, media_type="text/plain", headers={"Secret-Code": "123459"})
def root(response: Response):
    response.headers["Secret-Code"] = "123459"
    return {"message": "Hello from my api"}


@app.get("/headers")
def get_headers(request: Request):
    if not request.headers.get("User-Agent") or not request.headers.get("Accept-Language"):
        raise HTTPException(status_code=400, detail="Oops! Missing headers")
    return {"User-Agent": request.headers.get("User-Agent"), "Accept-Language": request.headers.get("Accept-Language")},


"""4.1 Реализуйте защищенную базовой аутентификацией конечную точку FastAPI `/login`, которая принимает запросы GET."""

security = HTTPBasic()


# Определите функцию аутентификации
def authenticate_user_basic(credentials: HTTPBasicCredentials = Depends(security)):
    user = get_user_from_db(credentials.username)
    if user is None or user.password != credentials.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Basic"}
                            )
    return user


# Задайте логику получения информации о пользователе и его пароле
def get_user_from_db(username: str):
    for user in user_data:
        if user.username == username:
            return user
    return None


# Защитите конечные точки с помощью аутентификации
@app.get("/login_basic/")
def login_basic(user: User = Depends(authenticate_user_basic)):
    return {"You got my secret, welcome": user}


'''4.2 Аутентификация на основе JWT'''

oath2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

'''
@app.post("/token")
async def tokenize(response: Response, user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    token = create_jwt_token(data={"sub": user.username})
    response.set_cookie("access_token", token, httponly=True)
    return {"access_token": token}


def get_token(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


def get_user_from_token(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # декодируем токен
        return get_user_from_db(payload.get("sub") )# тут мы идем в полезную нагрузку JWT-токена и возвращаем утверждение о юзере (subject); обычно там еще можно взять "iss" - issuer/эмитент, или "exp" - expiration time - время 'сгорания' и другое, что мы сами туда кладем
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Expired Signature", headers={"WWW-Authenticate": "Bearer"})
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token", headers={"WWW-Authenticate": "Bearer"})


def create_jwt_token(data: dict):
    exp = {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=60)}
    return jwt.encode(data | exp, key=SECRET_KEY, algorithm=ALGORITHM)


@app.get("/protected_resource")
async def info_user(request: Request, user: User = Depends(get_user_from_token)):
    access_token = request.cookies.get("access_token")
    if not access_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return user
'''


@app.post("/token")
async def tokenize(user: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Bearer"})
    token = create_jwt_token(data={"sub": user.username})
    return {"access_token": token}


def get_user_from_token(token: str = Depends(oath2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return get_user_from_db(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=403, detail="Expired Signature")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid Token")


def create_jwt_token(data: dict):
    exp = {"exp": datetime.now(tz=timezone.utc) + timedelta(seconds=360)}
    return jwt.encode(data | exp, key=SECRET_KEY, algorithm=ALGORITHM)


@app.get("/protected_resource")
async def info_user(current_user: Annotated[User3, Depends(get_user_from_token)]):
    user = get_user_from_db(current_user.username)
    if user:
        return user
    else:
        raise HTTPException(status_code=401, detail="No Token")


if __name__ == '__main__':
    uvicorn.run(app="app.main:app",
                host='127.0.0.1',
                port=8000,
                reload=True)
