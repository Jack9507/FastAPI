from fastapi import FastAPI, HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr, Field
from typing import Annotated
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta

#below secret is going to be used to sign the JWT token, the key acts as the servers private key. generated using: openssl rand -hex 32
SECRET_KEY = "d901b66be8490489cd25f4e73184e053256de7f1c77f606383a1980b92831579"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme= OAuth2PasswordBearer(tokenUrl="/api/v1/login")

app = FastAPI()

users_db = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class UserDetails(BaseModel):
    username: str
    email: EmailStr
    password: str
    age: Annotated[int, Field(gt=18)]
    disabled: bool

def get_password_hash(incoming_password: str):
    return pwd_context.hash(incoming_password)
def verify_password(username, password):
    return pwd_context.verify(password, users_db[username].password)
def create_JWT_token(username: str):
    expiry = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": username,
        "exp": expiry
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token
def get_current_user(jwtoken: str = Security(oauth2_scheme)):
    try:
        payload = jwt.decode(jwtoken, SECRET_KEY,  algorithms=[ALGORITHM] )
        username: str = payload.get("sub")
        if username is None or username not in users_db:
            raise HTTPException(status_code=401, detail="Invalid Credentials.")
        return users_db[username]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token Expired.")
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid Token")


@app.get("/")
def root():
    return {"message": "welcome to FASTAPI... mate."}

@app.post("/api/v1/signup")
def user_signup(payload: UserDetails):
    # now before storing in DB make sure to update the password to its hash and then store
    payload.username = payload.username.lower()   
    payload.password = get_password_hash(payload.password)
    users_db[payload.username] = payload
    return {"message": f"User {payload.username} signed up successfully."}

@app.post("/api/v1/login")
def user_login(username: str, password: str):
    # first check if user exists i.e. user has already signed up 
    if username.lower() in users_db:
        # now check that the user has given correct creds
        if(verify_password(username.lower(), password)):
            #here generate JWT and return
            jwt_token= create_JWT_token(username)
            print(f"YOUR JWT: {jwt_token}")
            return {"message":  f"Login Success!!!  From now on please use JWT: {jwt_token}"}
        else:
            return HTTPException(401, f"User: {username} Unauthorised, Incorrect username or password.")
    else:
        return HTTPException(404, f"User: {username} not found. Please signup first.")

    
@app.get("/api/v1/getUser")
def get_user(user: str):
    if user in users_db:
        return users_db[user]
    else:
        return {f"404, Sorry User: {user} not found."}

@app.get("/api/v1/users/all")
def get_all_users():
    return users_db

@app.get("/api/v1/protected")
def protected_route(current_user: Annotated[UserDetails, Security(get_current_user)]):
    return {"messsage": f"Hello {current_user.username} !. This is protected route."}