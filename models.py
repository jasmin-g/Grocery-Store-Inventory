from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine("sqlite:///inventory.db", echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Brands(Base):
    __tablename__ = "brands"

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column('Brand Name', String)
    products =  relationship("Product", back_populates="brand")

    def __repr__(self):
        return f"""
        \nBrand {self.brand_id}
        \rBrand Name = {self.brand_name}\r
        """

class Product(Base):
    __tablename__ = "product"

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', DateTime)  
    brand_id = Column('Brand ID', Integer, ForeignKey("brands.brand_id"))
    brand =  relationship("Brands", back_populates="products")

    def __repr__(self):
        return f"""
        \nProduct: {self.product_id}
        \rProduct Name: {self.product_name} 
        \rProduct Quantity: {self.product_quantity} 
        \rProduct Price: {self.product_price} 
        \rDate Updated: {self.date_updated}
        \rBrand ID: {self.brand_id}
        """



    