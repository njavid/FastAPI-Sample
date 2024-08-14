from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .models import *
from .database import SessionLocal, engine
from .auth.auth_bearer import JWTBearer
from .auth.auth_handler import *

from fastapi import FastAPI, File, UploadFile

import polars as pl

import io

from .utils import create_sample_data

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret

@app.post('/login' ,response_model=schemas.TokenSchema)
def login(request: schemas.UserPass, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.hashed_password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)

    token_db = models.TokenTable(user_id=user.id,  access_toke=access, status=True)
    db.add(token_db)
    db.commit()
    db.refresh(token_db)
    return {
        "access_token": access
    }

@app.post("/register", response_model=schemas.User)
def register(user: schemas.UserPass, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)


@app.post('/upload-buy-excel')
async def upload_buy_excel(file: UploadFile, db: Session = Depends(get_db)):

    print(1)
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="Invalid file format.")

    file_content = await file.read()
    print(file_content)
    df = pl.read_excel(io.BytesIO(file_content))

    print(pl.DataFrame([df.columns], schema=df.columns))
    print(df.columns)

    # Check if it has header? -> the first row & second column (product code) has  non-integer value or not.
    
    # if not isinstance(df.columns[1], int): 
    #     print('yess')
    #     df = pl.concat([df,pl.DataFrame([df.columns], schema=df.columns)], how="vertical")
    user = db.query(User).filter(User.email =="user1@example.com").first() # todo get_current_user()

    print(3,df)
    new_rows = []
    # Simple logic to assign each product to a user
    for i,row in enumerate(df.rows()):
        print(f'{i} -- ')
        # row = .to_numpy()
        print(row)
        print('3-------')
        print(int(row[1]))
        product = db.query(Product).filter(Product.id == int(row[1]),Product.measurement_unit==row[3]).first()

        #get current user active basket:
        basket = db.query(BuyBasket).filter(BuyBasket.user_id == user.id, BuyBasket.is_active == True).first()
        
        basket_product = BasketProduct(product_id=product.id,basket_id=basket.id,quantity=row[2])
        db.add(basket_product)
        db.commit()


        # basket.products.append(product)
        # db.commit()


    # Do something with the DataFrame (e.g., print, process, etc.)
    
    
    return {"message": "File processed successfully"}
    
    # except Exception as e:
    #     raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.get('/get-buy-excel')
async def get_buy_excel():

    new_rows = []
    # Simple logic to assign each product to a user
    for i,rows in enumerate(df.rows()):

        # user = users_df.get_row(i % len(users_df))
        # new_row = {
        #     "user_id": user[0],
        #     "email": user[1],
        #     "is_active": user[2],
        #     "product_code": row[0],
        #     "product_type": row[1],
        #     "quantity": row[2]
        # }
        # new_rows.append(new_row)

        # # Convert new_rows to a DataFrame
        # new_rows_df = pl.DataFrame(new_rows)

        return 1
    # return {"data": df.to_dict()}
  
@app.get('/get_user')
def get_current_user(db: Session = Depends(get_db)): #todo 
    user = db.query(User).filter(User.email =="user1@example.com").first()
    return user


@app.get('/get-users2')
def getusers(dependencies=Depends(JWTBearer()),db: Session = Depends(get_db)):
    user = db.query(models.User).all()
    return user


@app.post("/reset-sample-data/")
def reset_sample_data(db: Session = Depends(get_db)):
    create_sample_data()
    product = db.query(models.Product).all()
    print(product)
    return {"message": "Sample data has been inserted."}




#-------------------------------------

# @app.get("/profile/", response_model=schemas.User,dependencies=[Depends(JWTBearer())])
# def get_profile():

#     return current_user

# @app.get("/users/", response_model=List[schemas.User])
# def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     users = crud.get_users(db, skip=skip, limit=limit)
#     return users


# @app.get("/users/{user_id}", response_model=schemas.User)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     db_user = crud.get_user(db, user_id=user_id)
#     if db_user is None:
#         raise HTTPException(status_code=404, detail="User not found")
#     return db_user


# @app.post("/users/{user_id}/items/", response_model=schemas.Item)
# def create_item_for_user(
#     user_id: int, item: schemas.ItemCreate, db: Session = Depends(get_db)
# ):
#     return crud.create_user_item(db=db, item=item, user_id=user_id)


# @app.get("/items/", response_model=List[schemas.Item])
# def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
#     items = crud.get_items(db, skip=skip, limit=limit)
#     return items