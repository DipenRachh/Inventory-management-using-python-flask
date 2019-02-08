from flask import Flask,render_template,redirect, url_for
from flask import request
import sqlite3 as sql


con = sql.connect("database.db",check_same_thread=False)
con.row_factory = sql.Row
cur = con.cursor()

app = Flask(__name__)

@app.route('/')
def root():
   return redirect(url_for('home'))


@app.route("/home")
def home():
    return render_template('home.html')
    #stock balance
@app.route("/stockbalance")
def stockbalance():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   return  render_template('stock.html',rows = rows) 


                                  #Product Page
@app.route("/Product")
def Product():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from Product")
   
   rows = cur.fetchall();
   return  render_template('Product.html',rows = rows) 

                                #ADD Product
@app.route('/addProduct',methods = ['POST'])
def addProduct():
   if request.method == 'POST':
      try:
         pn = request.form['pn']
         pd = request.form['pd']
         pq = request.form['pq']
        
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO Product (productName,productDescription,QTY) VALUES (?,?,?)",(pn,pd,pq) )
            
            con.commit()
            msg = "Record added"
      except:
         con.rollback()
         msg = "error in  operation"
      
      finally:
         
         return redirect(url_for('Product')+"?msg="+msg)
         con.close()
                                  #Edit Product
@app.route('/editProduct',methods = ['POST'])
def editProduct():
   if request.method == 'POST':
      try:
         productID = request.form['ProductID']
         productName = request.form['NEWProductName']
         productDescription=request.form['NEWProductDescription']
         ProductQty=request.form['NEWProductQty']
         cur.execute("UPDATE Product SET productName = ?,productDescription = ?, QTY = ? WHERE productID = ?",(productName,productDescription,ProductQty,productID) )
         
         con.commit()
         msg = "Product Edited "
      except:
         con.rollback()
         msg = "error in operation"
      
      finally:
         return redirect(url_for('Product')+"?msg="+msg)
         con.close()

                                #Delete Product
@app.route('/deleteProduct/<productID>')
def deleteProduct(productID):
      try:
            cur.execute("DELETE FROM Product WHERE productID = ?",(productID,))
            
            con.commit()
            msg = "Product Deleted"
      except:
            con.rollback()
            msg = "error in operation"
   
      finally:
            return redirect(url_for('Product')+"?msg="+msg)
            con.close()
                                #Location Page
@app.route("/Location")
def Location():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   
   cur = con.cursor()
   cur.execute("select * from locations")
   
   rows = cur.fetchall();
   return  render_template('Location.html',rows = rows) 
                                  #ADD Locations
@app.route('/addlocation',methods = ['POST'])
def addlocation():
   if request.method == 'POST':
      try:
         ln = request.form['ln']

         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO locations (locationName) VALUES (?)",(ln,))
            
            con.commit()
            msg = "successfully added"
      except:
            con.rollback()
            msg = "error in operation"
      
      finally:
            return redirect(url_for('Location')+"?msg="+msg)
            con.close()
                              # Edit Location
@app.route('/editlocation',methods = ['POST'])
def editlocation():
   if request.method == 'POST':
      try:
         locationID = request.form['locationID']
         locationName = request.form['NEWLocationName']
         cur.execute("UPDATE locations SET locationName = ? WHERE locationID = ?",(locationName,locationID) )
         
         con.commit()
         msg = "location Edit Successfully"
      except:
         con.rollback()
         msg = "error operation"
      
      finally:
         return redirect(url_for('Location')+"?msg="+msg)
         con.close()
                            # Delete Location
@app.route('/deletelocation/<locationID>')
def deletelocation(locationID):
      try:
            cur.execute("DELETE FROM locations WHERE locationID = ? ",(locationID))
            
            con.commit()
            msg = "location Delete Successfully"
      except:
            con.rollback()
            msg = "error operation"
   
      finally:
            return redirect(url_for('Location')+"?msg="+msg)
            con.close()

@app.route('/ProductMovement')
def ProductMovement():
   cur.execute("select * from product_movement")
   
   rows = cur.fetchall()

   cur.execute("select * from products")
   productRows = cur.fetchall()

   cur.execute("select * from locations")
   locationRows = cur.fetchall()

   for pr in productRows:
      for lr in locationRows:
         cur.execute("SELECT * FROM Balance WHERE locationName = ? AND productName = ? ",(lr["locationName"],pr["productName"]))
         data = cur.fetchall()

         if len(data) == 0:
            cur.execute("INSERT INTO Balance (locationName, productName, qty)VALUES (?,?,?)",(lr["locationName"],pr["productName"],0))
            con.commit()
            

   return render_template('ProductMovement.html',rows = rows,  productRows =  productRows, locationRows = locationRows)

              # ADD ProductMovement

@app.route('/addProductMovement',methods = ['POST'])
def addProductMovement():
   if request.method == 'POST':
      try:
         pn = request.form['pn']
         datetime = request.form['datetime']
         fromlocation = request.form['fromlocation']
         tolocation = request.form['tolocation']
         pq =request.form['pq']
        
         
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("INSERT INTO product_movement (productName,Timing,fromlocation,tolocation,QTY) VALUES (?,?,?,?,?)",(pn,datetime,fromlocation,tolocation,pq) )
            
            con.commit()
            msg = "Record added"
      except:
         con.rollback()
         msg = "error in  operation"
      
      finally:
          return redirect(url_for('ProductMovement')+"?msg="+msg)
          con.close()
                #Edit ProductMovement 
@app.route('/editProductMovement',methods = ['POST'])
def editProductMovement():
   if request.method == 'POST':
      try:
         movementID = request.form['movementID']
         ProductName = request.form['NEWProductName']
         datetime = request.form['NEWDateTime']
         fromlocation = request.form['NEWfromlocation']
         tolocation = request.form['NEWtolocation']
         qty=request.form['NEWProductQty']
         cur.execute("UPDATE product_movement SET productName = ?,Timing = ?,fromlocation = ?,tolocation = ?,QTY = ? WHERE movementID = ?",(ProductName,datetime,fromlocation,tolocation,qty,movementID),)
         
         con.commit()
         msg = " movement Edit Successfully"
      except:
         con.rollback()
         msg = "error operation"
      
      finally:
         return redirect(url_for('ProductMovement')+"?msg="+msg)
         con.close()
            #Delete Product Movement
@app.route('/deleteprouctmovement/<movementID>')
def deleteprouctmovement(movementID):
      try:
            cur.execute("DELETE FROM product_movement WHERE movementID = ? ",(movementID))
            
            con.commit()
            msg = "movement Delete Successfully"
      except:
            con.rollback()
            msg = "error operation"
   
      finally:
            return redirect(url_for('ProductMovement')+"?msg="+msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)