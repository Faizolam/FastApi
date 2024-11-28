from passlib.context import CryptContext

# we're telling passlib, what is the default hashing algorithm or what hashing algorithm do we want to use? In this case, we want use bcrypt.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hash the password
def hash(password: str):
    return pwd_context.hash(password)

#compare two hash to validate
def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)