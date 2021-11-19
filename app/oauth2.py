from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from . import config, database, models, schemas

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=config.settings.access_token_expire_minutes)
    to_encode.update({'exp': expire})

    return jwt.encode(to_encode, config.settings.secret_key, algorithm=config.settings.algorithm)


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, config.settings.secret_key, algorithms=[
                             config.settings.algorithm])
        id = payload.get('user_id')

        if id is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail='Could not validate credentials', headers={'WWW-Authenticate': 'Bearer'})

    token = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
