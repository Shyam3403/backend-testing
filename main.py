from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from jose import jwt, JWTError

app = FastAPI()

SECRET_KEY = "mysecretkey"

security = HTTPBearer()

fake_user = {
    "username": "shyam",
    "password": "1234"
}


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/login")
async def login(user: dict):

    if (
        user["username"] == fake_user["username"]
        and user["password"] == fake_user["password"]
    ):

        token = jwt.encode(
            {"username": user["username"]},
            SECRET_KEY,
            algorithm="HS256"
        )

        return {
            "access_token": token
        }

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials"
    )


@app.get("/profile")
async def profile(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=["HS256"]
        )

        return {
            "message": "Protected route",
            "user": payload
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )