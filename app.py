from flask import Flask ,request,render_template,redirect,url_for,flash,session,Response
from otp import genotp
from cmail import send_mail
from stoken import entoken,dtoken
from flask_session import Session
import mysql.connector
import bcrypt
from mysql.connector import (connection)
import os
import razorpay
import re
import pdfkit
app=Flask(__name__)
app.config['SESSION_TYPE']='filesystem'
Session(app)
config=pdfkit.configuration(wkhtmltopdf=r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe')
app.secret_key='codegnan@123'
mydb=mysql.connector.connect(user='root',host='localhost',password='prasad',db='ecom')
client=razorpay.Client(auth=("rzp_test_FSOeGXmMmvG5cj", "LVGwV75n2bygfag7nsDhOYVc"))

@app.route('/')
def home():
    return render_template("welcome.html") 

@app.route('/index')
def index():
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items')
        itemsdata=cursor.fetchall()
                 
    except Exception as e:
        print(f'error {e}')
        flash('could not fetch items data')
        return redirect(url_for('home'))
    else:
        return render_template("index.html",itemsdata=itemsdata)

@app.route('/admincreate',methods=['GET','POST'])
def admincreate():
    if request.method=='POST':
        username=request.form['username']
        useremail=request.form['email']
        password=request.form['password']
        address=request.form['address']
        agreed=request.form['agree']
        otp=genotp()
        admindata={'username':username,'useremail':useremail,'password':password,'address':address,'agree':agreed,'otp':otp}
        subject=f'OTP for Ecom admincreate'
        body=f'use the otp {otp}'
        send_mail(to=useremail,body=body,subject=subject)
        flash(f'OTP has sent given mail{useremail}')
        return redirect(url_for('otpverify',enddata=entoken(data=admindata)))
    return render_template('admincreate.html')

@app.route('/otpverify/<enddata>' ,methods=['GET','POST'])
def otpverify(enddata):
    try:
        ddata=dtoken(data=enddata)
    except Exception as e:
        print(f'Error in dcode admindata')
        flash ('could not verify otp')
        return redirect(url_for(admincreate))
    else:
        if request.method=='POST':
            uotp=request.form['otp']
            if uotp==ddata['otp']:
                salt=bcrypt.gensalt()
                hash=bcrypt.hashpw(ddata['password'].encode('utf-8'),salt)
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into admindata(username,adminemail,password,address,agree) values(%s,%s,%s,%s,%s)',[ddata['username'],ddata['useremail'],hash,ddata['address'],ddata['agree']])
                    mydb.commit()

                except Exception as e:
                    print(f'Error is {e}')
                    flash('could not store data')
                    return redirect(url_for('admincreate'))
                else:
                    flash(f'{ddata["useremail"]} successfully registered')
                    return redirect(url_for('adminlogin'))
            else:
                flash('otp wrong')
                return redirect(url_for('otpverify',enddata=enddata))
            
        return render_template('adminotp.html')
    
    
@app.route('/adminlogin',methods=['GET','POST'])
def adminlogin():
    if not session.get('admin'):
        if request.method=='POST':
            useremail=request.form['email']
            password=request.form['password']
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select count(*) from admindata where adminemail=%s',[useremail])
                email_count=cursor.fetchone()
                if email_count[0]==1:
                    cursor.execute('select password from admindata where adminemail=%s',[useremail])
                    stored_password=cursor.fetchone()
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password[0].encode('utf-8')):

                        session['admin']=useremail
                        print(session)
                        return redirect(url_for('adminpanel'))
                    else:
                        flash('password wrong')
                        return redirect(url_for('adminlogin'))
                else:
                    flash('Email not found')
                    return redirect(url_for('adminlogin'))
            except Exception as e:
                print(f'ERROR in login validation {e}')
        return render_template('adminlogin.html')
    else:
        return redirect(url_for('adminpanel'))

@app.route('/adminpanel')
def adminpanel():
    return render_template('adminpanel.html')


@app.route('/additem',methods=['GET','POST'])
def additem():
    if session.get('admin'): 
        if request.method=='POST':
            try:
                print('hi')
                title=request.form['title']
                Description=request.form['Description']
                quantity=request.form['quantity']
                price=request.form['price']
                item_category=request.form['category']
                imgdata=request.files['file']
                filename=genotp()+'.'+imgdata.filename.split('.')[-1]
                path=os.path.abspath(__file__)
                print(path)
                dirpath=os.path.dirname(path)
                print(dirpath)
                static_path=os.path.join(dirpath,'static')
                print(static_path)
                imgdata.save(os.path.join(static_path,filename))
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('insert into items(itemid,itemname,Description,quantity,cost,category,imagename,added_by) values(uuid_to_bin(uuid()),%s,%s,%s,%s,%s,%s,%s)',[title,Description,quantity,price,item_category,filename,session.get('admin')])
                    mydb.commit()
                    cursor.close()
                except Exception as e:
                    print(f'error in mysql{e}')
                    flash("could not save item data")
                    return redirect(url_for('additem'))
                else:
                    flash(f'{title[:10]}added successfully')
                    return redirect(url_for('additem'))
            except Exception as e:
                print(e)
                return redirect(url_for('adminpanel'))
        return render_template('additem.html')
    return redirect(url_for('adminlogin'))

@app.route('/viewallitems')
def viewallitems():
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where added_by=%s',[session.get('admin')])
            itemsdata=cursor.fetchall()
        except Exception as e:
            print(f'error {e}')
            flash('could not fetch items data')
            return redirect(url_for('adminpanel'))
        else:
            return render_template('viewall_items.html',itemsdata=itemsdata)
    else:
        flash(f'pls login first')
        return redirect(url_for('adminlogin'))
    
@app.route('/viewitem/<itemid>')
def viewitem(itemid):
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where itemid=uuid_to_bin(%s) and added_by=%s',[itemid,session.get('admin')])
            itemdata=cursor.fetchone()
        except Exception as e:
            print(e)
            flash(f'could not fetch items data')
            return redirect(url_for('adminpanel'))
        else:
            return render_template('view_item.html',itemdata=itemdata)
    else:
        flash(f'pls login first')
        return redirect(url_for('adminlogin'))
    
@app.route('/update/<itemid>', methods=['GET', 'POST'])
def update(itemid):
    if not session.get('admin'):
        flash("Please login first.")
        return redirect(url_for('adminlogin'))

    cursor = mydb.cursor(buffered=True)
    cursor.execute('SELECT bin_to_uuid(itemid), itemname, description, quantity, cost, category, imagename FROM items WHERE itemid=uuid_to_bin(%s) AND added_by=%s', [itemid, session['admin']])
    item = cursor.fetchone()

    if request.method == 'POST':
        name = request.form['title']
        desc = request.form['Description']
        qty = request.form['quantity']
        cost = request.form['price']
        cat = request.form['category']
        file = request.files['file']

        if file and file.filename != '':
            filename = genotp() + '.' + file.filename.split('.')[-1]
            filepath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', filename)
            file.save(filepath)
        else:
            filename = item[6] 
        cursor.execute('UPDATE items SET itemname=%s, description=%s, quantity=%s, cost=%s, category=%s, imagename=%s WHERE itemid=uuid_to_bin(%s) AND added_by=%s',
                       [name, desc, qty, cost, cat, filename, itemid, session['admin']])
        mydb.commit()
        flash("Item updated successfully.")
        return redirect(url_for('viewitem', itemid=itemid))

    return render_template('update_item.html', item_data=item)

    
@app.route('/delete/<itemid>')
def delete(itemid):
    if not session.get('admin'):
        flash("Please login first.")
        return redirect(url_for('adminlogin'))

    try:
        cursor = mydb.cursor(buffered=True)
        cursor.execute('DELETE FROM items WHERE itemid = uuid_to_bin(%s) AND added_by = %s', [itemid, session['admin']])
        mydb.commit()
        flash("Item deleted successfully.")
    except Exception as e:
        print(f"Delete error: {e}")
        flash("Could not delete item.")
    return redirect(url_for('viewallitems'))

    
@app.route('/adminprofile',methods=['GET','POST'])
def adminprofile():
    if session.get('admin'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select username,address,phone_no,profilepic from admindata where adminemail=%s',[session.get('admin')])
            stored_details=cursor.fetchone()
        except Exception as e:
            print(e)
            flash('could not fetch stored details')
            return redirect(url_for('adminpanel'))
        else:
            if request.method=='POST':
                username=request.form['adminname']
                address=request.form['address']
                phone_no=request.form['ph_no']
                profile_pic=request.files['file']
                if profile_pic.filename!='':
                    filename=genotp()+'.'+profile_pic.filename.split('.')[-1]
                    path=os.path.abspath(__file__)
                    print(path)
                    dirpath=os.path.dirname(path)
                    print(dirpath)
                    static_path=os.path.join(dirpath,"static")
                    print(static_path)
                    profile_pic.save(os.path.join(static_path,filename))
                elif profile_pic.filename=='':
                    filename=stored_details[3]
                cursor.execute('update admindata set username=%s,address=%s,phone_no=%s,profilepic=%s where adminemail=%s',[username,address,phone_no,filename,session.get('admin')])
                mydb.commit()
                flash('successfully updated')
                return redirect(url_for('adminprofile'))
            return render_template('adminupdate.html',admin_data=stored_details)
    else:
        flash(f'pls login first')
        return redirect(url_for('adminlogin'))
    

@app.route('/usercreate',methods=['GET','POST'])
def usercreate():
    if request.method=='POST':
        username=request.form['name']
        useremail=request.form['email']
        password=request.form['password']
        address=request.form['address']
        gender=request.form['usergender']
        otp=genotp()
        userdata={'username':username,'useremail':useremail,'password':password,'address':address,'gender':gender,'otp':otp}
        subject=f'OTP for Ecom usercreate'
        body=f'use the otp {otp}'
        send_mail(to=useremail,body=body,subject=subject)
        flash(f'OTP has sent given mail{useremail}')
        return redirect(url_for('userotpverify',endata=entoken(data=userdata)))
    return render_template('usersignup.html')

@app.route('/userotpverify/<endata>', methods=['GET', 'POST'])
def userotpverify(endata):
    try:
        ddata=dtoken(data=endata)
    except Exception as e:
        print(f'Error in dcode admindata {e}')
        flash('could not verify otp')
        return redirect(url_for('usercreate'))
    else:
        if request.method=='POST':
            uotp=request.form['otp']
            if uotp==ddata['otp']:
                salt=bcrypt.gensalt()
                hash=bcrypt.hashpw(ddata['password'].encode('utf-8'), salt)
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('Insert into users(username,useremail,address,password,gender) values(%s,%s,%s,%s,%s)',[ddata['username'], ddata['useremail'],ddata['address'],hash,ddata['gender']])
                    mydb.commit()
                except Exception as e:
                    print(f'Error is {e}')
                    flash('could not store data')
                    return redirect(url_for('usercreate'))
                else:
                    flash(f'{ddata["useremail"]} successfully registerd')
                    return redirect(url_for('userlogin'))
            else:
                flash('otp wrong')
                return redirect(url_for('userotpverify',endata=endata))

        
        return render_template('userotp.html')                  


            
@app.route('/userlogin',methods=['GET','POST'])
def userlogin():
    if not session.get('user'):
        if request.method=='POST':
            useremail=request.form['email']
            password=request.form['password'].encode('utf-8')
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select count(*) from users where useremail=%s',[useremail])
                email_count=cursor.fetchone()
                if email_count[0]==1:
                    cursor.execute('select password from users where useremail=%s',[useremail])
                    stored_password=cursor.fetchone()
                    if bcrypt.checkpw(password,stored_password[0]):
                        print(session)
                        session['user']=useremail
                        if not session.get(useremail):
                            session[useremail]={}
                        print(session)
                        return redirect(url_for('index'))
                    else:
                        flash('password wrong')
                        return redirect(url_for('userlogin'))
                else:
                    flash('Email not found')
                    return redirect(url_for('userlogin'))
            except Exception as e:
                print(f'ERROR in login validation {e}')
        return render_template('userlogin.html')

    else:
        return redirect(url_for('index'))
    
@app.route('/category/<ctype>')
def category(ctype):
    try:
        cursor=mydb.cursor(buffered=True)
        cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where category=%s',[ctype])
        items=cursor.fetchall()
    except Exception as e:
        print(e)
        flash ('could not fetch category items')
        return redirect(url_for('index'))
    else:
        return render_template('daashboard.html',items=items)
    
@app.route('/addcart/<itemid>')
def addcart(itemid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where bin_to_uuid(itemid)=%s',[itemid])
            item_data=cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not fetch category items')
            return redirect(url_for('index'))
        else:
            print(session)
            if itemid not in session[session.get('user')]:
                session[session.get('user')][itemid]=[item_data[1],item_data[2],1,item_data[4],item_data[5],item_data[6]]
                session.modified=True
                print(session)
                flash(f'{item_data[1]} added toi cart')
                return redirect(url_for('index'))
            else:
                session[session.get('user')][itemid][2]+=1
                session.modified=True
                return redirect(url_for('index'))
    else:
        flash('pls login to addcart')
        return redirect(url_for('userlogin'))
    
@app.route('/userlogout')
def userlogout():
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('userlogin'))
    else:
        flash(f'pls login first')
        return redirect(url_for('userlogin'))
    
@app.route('/adminlogout')
def adminlogout():
    if session.get('admin'):
        session.pop('admin')
        return redirect(url_for('adminlogin'))
    else:
        flash(f'pls login frst')
        return redirect(url_for(adminlogin))
    
@app.route('/viewcart')
def viewcart():
    if session.get('user'):
        items=session[session.get('user')]
        if items:
            return render_template('cart.html',items=items)
        else:
            flash('No items added to cart')
            return redirect(url_for('index'))
    else:
        flash(f'pls login frst ')
        return redirect(url_for('userlogin'))

@app.route('/removecart/<itemid>')
def removecart(itemid):
    if session.get('user'):
        try:
            session[session.get('user')].pop(itemid)
            session.modified=True

        except Exception as e:
            print(e)
            flash('can not remove item')
            return redirect(url_for('viewcart'))
        else:
            flash(f'{itemid} removed from cart')
            return redirect(url_for('viewcart'))
    else:
        flash('pls login  first')
        return redirect(url_for('userlogin'))


@app.route('/description/<itemid>')
def description(itemid):
    cursor=mydb.cursor(buffered=True)
    cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where bin_to_uuid(itemid)=%s',[itemid])
    item=cursor.fetchone()
    cursor.close()
    return render_template('description.html',item=item)

@app.route('/pay/<itemid>/<dqyt>/<float:price>',methods=['GET','POST'])
def pay(itemid,dqyt,price):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where bin_to_uuid(itemid)=%s',[itemid])
            item=cursor.fetchone()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not fetch details')
            return redirect(url_for('index'))
        else:
            if request.method=='POST':
                qyt=int(request.form['qyt'])
                price=price*100 #convert into paise
                amount=price * qyt
                print(amount,qyt,price)
                print(f' creating payment for item :{item[1]}, with {amount}')
                order=client.order.create({
                    "amount":amount,
                    "currency":"INR",
                    "payment_capture":"1"})
                print(f'order created ,{order}')
                return  render_template('pay.html',order=order,amount=amount,itemid=itemid,name=item[1],qyt=qyt)      
    else:
        flash('pls login first')
        return redirect(url_for('userlogin'))
    
@app.route('/success',methods=['GET','POST'])
def success():
    if request.method=='POST':
        payment_id=request.form["razorpay_payment_id"]
        order_id=request.form['razorpay_order_id']
        order_signature=request.form['razorpay_signature']
        item_id=request.form['itemid']
        name=request.form['name']
        item_qyt=request.form['quantity']
        total_amount=request.form['total_amount']
        params_dict={
            'razorpay_payment_id': payment_id,
            'razorpay_order_id': order_id,
            'razorpay_signature': order_signature
        }
        try:
            client.utility.verify_payment_signature(params_dict)
        except razorpay.errors.SignatureVerificationError:
            return 'Payment verification failed', 400
        else:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select bin_to_uuid(itemid), itemname,description, quantity, cost, category, imagename from items where bin_to_uuid(itemid)=%s', [item_id])
            item=cursor.fetchone()
            new_quantity=item[3]-int(item_qyt)
            cursor.execute('update items set quantity=%s where itemid=uuid_to_bin(%s)', [new_quantity, item_id])
            mydb.commit()
            cursor.execute("select * from users where useremail=%s", [session.get("user")])
            userdata=cursor.fetchone()
            cursor.execute("insert into orders(item_name,total_amount,quantity,payment_by,address) values (%s,%s,%s,%s,%s)", [name,
            total_amount,item_qyt,session.get("user"),userdata[2]])
            mydb.commit()
            cursor.close()
            flash("order placed successfully")
            return "order"


@app.route('/logout')
def logout():
    print(session)
    if session.get('user'):
        session.pop('user')
        return redirect(url_for('index'))
    else:
        flash('pls login first')
        return redirect(url_for('index'))
    
@app.route('/myorders')
def myorders():
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select * from orders where payment_by=%s',[session.get['user']])
            myorder=cursor.fetchall()
            cursor.close()
        except Exception as e:
            print(e)
            flash('could not fetch orders')
            return redirect(url_for('index'))
        else:
            return render_template('order.html',myorder=myorder)
    else:
        flash('pls login first')
        return redirect(url_for('userlogin'))

@app.route('/addreview/<itemid>',methods=['GET','POST'])
def addreview(itemid):
    if request.method=='POST':
        review=request.form['review']
        rating=request.form['rate']
        cursor=mydb.cursor(buffered=True)
        cursor.execute('insert into reviews(review,rating,itemid,user) values(%s,%s,uuid_to_bin(%s),%s)',[review,rating,itemid,session.get('user')])
        mydb.commit()
        cursor.close()
        flash('review added successfully')
    return render_template('review.html')

@app.route('/searchdata',methods=['GET','POST'])
def searchdata():
    if request.method=='POST':
        sdata=request.form['search']
        strg=['A-Za-z0-9']
        MATCHING_STRG=re.compile(f'^{strg}',re.IGNORECASE)
        if MATCHING_STRG.search(sdata):
            try:
                cursor=mydb.cursor(buffered=True)
                cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where itemname like %s or description like %s cost like %s category like %s',['%'+sdata+'%','%'+sdata+'%','%'+sdata+'%','%'+sdata+'%'])
                items=cursor.fetchall()
                cursor.close()
            except Exception as e:
                print(e)
                flash ('could not fetch search items')
                return redirect(url_for('index'))
            else:
                return render_template('dashboard.html',items=items)
        
        else:
            flash ('invalid search data pls enter some value')
            return redirect(url_for('index'))
        

@app.route('/invoice/<ordid>')
def invoice(ordid):
    if session.get('user'):
        try:
            cursor=mydb.cursor(buffered=True)
            cursor.execute('select order_id,item_name,total_amount,quantity,order_date,payment_by from orders where order_id=%s and payment_by=%s', [ordid, session.get('user')])
            order_details=cursor.fetchone()
            cursor.execute('select username,useremail,address from users where useremail=%s', [session.get('user')])
            user_details=cursor.fetchone()
            html=render_template('bill.html',order_details=order_details,user_details=user_details)
            pdf=pdfkit.from_string(html,False,configuration=config)
            response=Response(pdf,content_type='application/pdf')
            response.headers['Content-Disposition']='inline; filename=output.pdf'
            return response
        except Exception as e:
            print(e)
            flash('could not generate pdf')
            return redirect(url_for('myorders'))
    else:
        return redirect(url_for('index'))
    
@app.route('/adminsearch',methods=['GET','POST'])
def adminsearch():
    if session.get('admin'):
        if request.method=='POST':
            sdata=request.form['search']
            strg=['A-Za-z0-9']
            matching_strg=re.compile(f'^{strg}',re.IGNORECASE)
            if matching_strg.search(sdata):
                try:
                    cursor=mydb.cursor(buffered=True)
                    cursor.execute('select bin_to_uuid(itemid),itemname,description,quantity,cost,category,imagename from items where (itemname like %s or description like %s or cost like %s or category like %s) and added_by=%s',['%'+sdata+'%','%'+sdata+'%','%'+sdata+'%','%'+sdata+'%',session.get('admin')])
                    items=cursor.fetchall()
                    cursor.close()
                except Exception as e:
                    print(e)
                    flash('could not fetch category items')
                    return redirect(url_for('index'))
                else:
                    return render_template('viewall_items.html',itemsdata=items)
            else:
                flash('invalid search data pls enter some value')
                return redirect(url_for('index'))
    else:
        flash('pls login first')
        return redirect(url_for('adminlogin'))
    

    


app.run(debug=True,use_reloader=True)
