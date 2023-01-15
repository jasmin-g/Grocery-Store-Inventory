from models import (Base, session, Brands, Product, engine)
import csv
import datetime
import time


def menu():
    while True:
        print('''
        \rWelcome to the Grocery Store Inventory\n
        \rHere are your choices:\n
        \rN) Add new Product
        \rV) View a Product by ID
        \rA) Procuct Analysis
        \rB) Backup Database
        \rQ) Quit
        ''')
        choice = input('What would you like to do? ')
        if choice.upper() in ['N', 'V', 'A', 'B', 'Q']:
            return choice 
        else:
            input('''
            \rThis is not a valid option.
            \rPlease select from the following option: N, V, A, B, Q
            \rPress enter to try again.
            ''')    

def submenu():
  while True:
    print('''
    \r1) Edit
    \r2) Delete
    \r3) Return to main menu''')
    choice = input('What would you like to do? ')
    if choice in ['1', '2', '3']:
      return choice
    else:
      input('''
      \rPlease choose one of the option above.
      \rA number from 1-3.
      \rPress enter to try again. ''')


def clean_qty(qty_str):
    try:
        qty_int = int(qty_str)
    except ValueError:
        input('''
        \n****** QANTITY ERROR ******
        \rThe quantity should be a integer.
        \rPress enter to try again.
        \r************************''')
    else:
        return qty_int


def clean_price(price_str): 
    try: 
        float_price = float(price_str)
        return int(float_price * 100)
    except ValueError:
        input('''
        \n****** PRICE ERROR ******
        \rThe price should be a number without a currency symbol.
        \rEx: 10.99
        \rPress enter to try again.
        \r************************''')
    else:
        return int(float_price * 100)


def clean_date(date_str):
    split_date = date_str.split('/')
    try:
        month = int(split_date[0])
        day = int(split_date[1])
        year = int(split_date[2])
        return_date = datetime.date(year, month, day)
    except ValueError:
        input('''
        \n****** DATE ERROR ******
        \rThe date format should be MM/DD/YYYY
        \rPress enter to try again.
        \r************************''')
        return
    else:
        return return_date


def clean_id(id_str, options):
  try:
    product_id = int(id_str)
  except ValueError:
     input('''
    \n****** ID ERROR ******
    \rThe ID should be a number.
    \rPress enter to try again.
    \r************************''')
     return
  else:
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n****** ID ERROR ******
            \rOptions: {options} 
            \rPress enter to try again.
            \r************************''')
            return


def add_brands_csv():
  with open('brands.csv') as csvfile:
    data = csv.reader(csvfile)
    next(data)
    for row in data:
         brand_in_db = session.query(Brands).filter(Brands.brand_name==row[0]).one_or_none()
         if brand_in_db == None:
            brand_name = row[0]
            new_brand = Brands(brand_name=brand_name)
            session.add(new_brand)
    session.commit()


def add_inventory_csv():
  with open('inventory.csv') as csvfile:
    data = csv.reader(csvfile) 
    next(data)
    for row in data:
        product_in_db = session.query(Product).filter(Product.product_name==row[0]).one_or_none()
        if product_in_db == None:
            product_name = row[0]
            product_price = row[1]
            product_price = product_price.split('$')
            product_price = product_price[1]
            product_price = clean_price(product_price)
            product_quantity = clean_qty(row[2])
            date_updated = clean_date(row[3])
            brand_name = row[4]
            get_brand_id = session.query(Brands).filter(Brands.brand_name==row[4]).first()
            brand_id = get_brand_id.brand_id
            new_product = Product(product_name=product_name, product_price=product_price,  
                                  product_quantity=product_quantity, date_updated=date_updated, brand_name=brand_name, brand_id=brand_id)
            session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()

        if choice.upper() == 'N':
            product_name = input('Product Name: ')

            price_error = True
            while price_error:
                product_price = input('Product Price (Ex: 10.99): ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False

            qty_error = True
            while qty_error:
                product_quantity = input('Quantity: ')
                product_quantity = clean_qty(product_quantity)
                if type(product_quantity) == int:
                    qty_error = False

            date_error = True
            while date_error:
                date_updated = input('Date updated (MM/DD/YYYY): ')
                date_updated = clean_date(date_updated)
                if type(date_updated) == datetime.date:
                    date_error = False

            brand_name = input('Brand name: ')
            brand_id = session.query(Brands).filter(Brands.brand_name == brand_name).first().brand_id
            new_product = Product(product_name=product_name, product_price=product_price,
                                product_quantity=product_quantity, date_updated=date_updated,
                                brand_id=brand_id)
            session.add(new_product)
            session.commit()
            print('Product added!')
            time.sleep(1.5)
        

        elif choice.upper() == 'V':
            id_options = []
            for product in session.query(Product):
                id_options.append(product.product_id)
            id_error = True
            while id_error:
                id_choice = input(f'''
                \nId Options: {id_options}
                \rProduct id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            sel_product = session.query(Product).filter(Product.product_id==id_choice).first()
            print(f'''
            \nProduct Name: {sel_product.product_name}
            \rProduct Quantity: {sel_product.product_quantity}
            \rProduct Price: {sel_product.product_price}
            \rDate Updated: {sel_product.date_updated}
            \rBrand ID: {sel_product.brand_id}
            ''')
            input('\nPress ENTER to continue')


        elif choice.upper() == 'A':
            exp_product = session.query(Product).order_by(Product.product_price.desc()).first()
            cheap_product = session.query(Product).order_by(Product.product_price).first()
            most_products = []
            for brand in session.query(Product.brand_id).all():
                most_products.append(brand)
            most_brands = max(most_products, key=most_products.count)
            most_brands = most_brands[0]
            most_brands = session.query(Brands).filter(Brands.brand_id == most_brands).first()
            print(f'''
            \n***** INVENTORY ANALYSIS *****
            \rMost expensive product: {exp_product}
            \rCheapest product: {cheap_product}
            \rBrand with most products: {most_brands}
            \r****************************
            ''')
            input('\nPress enter to return to the main menu')
            

        elif choice.upper() == 'B':
            with open('backup_inventory.csv', 'a') as csvfile: 
                header = ['product_id','product_name','product_price','product_quantity','date_updated','brand_id']
                writer = csv.DictWriter(csvfile, fieldnames = header)

                writer.writeheader()
                for product in session.query(Product):
                    writer.writerow({'product_id': product.product_id,
                                    'product_name': product.product_name,
                                    'product_price': product.product_price,
                                    'product_quantity':product.product_quantity,
                                    'date_updated': product.date_updated,
                                    'brand_id': product.brand_id})
                
            print('\nBackup File Created!')
            time.sleep(1.5)

        else:
            print('GOODBYE')
            app_running = False


if __name__ == "__main__":
    Base.metadata.create_all(engine)

    add_brands_csv()
    add_inventory_csv()
    app()
    


        