from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from b1.db import Base, engine, get_db
from b1.model import Product
from b1.schemas import ProductCreate, ProductUpdate, ProductOut

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.get("/products", response_model=list[ProductOut])
def get_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/products/{product_id}", response_model=ProductOut)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return product

@app.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED)
def create_product(product_in: ProductCreate, db: Session = Depends(get_db)):
    product = Product(name=product_in.name, price=product_in.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

@app.put("/products/{product_id}", response_model=ProductOut)
def update_product(product_id: int, product_in: ProductUpdate, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    product.name = product_in.name
    product.price = product_in.price
    db.commit()
    db.refresh(product)
    return product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    db.delete(product)
    db.commit()
