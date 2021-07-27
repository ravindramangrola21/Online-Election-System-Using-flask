from itertools import count
from logging import fatal
import re
from MySQLdb import connections, cursors
from flask import Flask,render_template,request,session,redirect,url_for,flash
from flask_mysqldb import MySQL
import datetime
import json
from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage
import os
import uuid
from time import gmtime, strftime


app = Flask(__name__)

jsonfiles = open('static\jsonfile.json','r')
data = jsonfiles.read()
load = json.loads(data)

app.config['SECRET_KEY']='secretkey'
app.config['MYSQL_HOST']='localhost'
app.config["MYSQL_USER"]='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='online_election'

db = MySQL(app)

now=datetime.datetime.now()

variable=False

@app.route('/',methods=['POST','GET'])
def hello():
    var=None
    cur = db.connection.cursor()
    cur.execute('SELECT * FROM release_election')
    fetchdata = cur.fetchone()
    count=cur.rowcount
    cur.close()
    if count>0:
        if now < fetchdata[3]:
            var = 'notice'
            return render_template("homepage.html",data=fetchdata,var=var)

        elif(now >= fetchdata[3] and now <= fetchdata[4]):
            var = 'candidate_list'
            list=db.connection.cursor()
            list.execute('SELECT ID,Fname,Lname,Profile_pic FROM candidate_registration WHERE Status=%s',('Approved',))
            retrieve=list.fetchall()
            list.close()
            #return("candidate list is to be uploaded")
            return render_template('homepage.html' ,data=retrieve,var=var)
        elif(now > fetchdata[4] and now < fetchdata[5]):
            var ='voting'
            list=db.connection.cursor()
            list.execute('SELECT ID,Fname,Lname,Profile_pic FROM candidate_registration WHERE Status=%s',('Approved',))
            retrieve=list.fetchall()
            list.close()
            return render_template('homepage.html', data=retrieve, var=var)
        elif now >= fetchdata[5] and now < fetchdata[6]:
            var='result_wait'
            return render_template('homepage.html', var=var)
        elif(now >= fetchdata[6]):
            var='result'
            rslt1=db.connection.cursor()
            rslt1.execute('SELECT ID,Profile_pic ,Fname,Lname,Email,VoteCount FROM shortlist_candidate')
            rsltdata1=rslt1.fetchall()
            rslt1.close()
            rslt2=db.connection.cursor()
            rslt2.execute('SELECT Max(VoteCount) FROM shortlist_candidate')
            rsltdata2=rslt2.fetchone()
            rslt2.close()
            max=rsltdata2[0]
            rslt2=db.connection.cursor()
            if max!=None:
                rslt2.execute("SELECT ID,Profile_pic ,Fname, Lname, Email,VoteCount FROM shortlist_candidate WHERE VoteCount ='%d'"%(max))
                rsltdata2=rslt2.fetchone()
                rslt2.close()
            return render_template('homepage.html',data1=rsltdata1,data2=rsltdata2,var=var) 
    else:
        var='NoElection'
        return render_template("homepage.html",var=var)          

@app.route('/dashboard', methods=['GET','POST'])
def Dashboard():

    if ('user' in session and session['user'] == load['Admin_username']):
        cur = db.connection.cursor()
        cur.execute('SELECT EID, ETitle FROM release_election')
        fetchdata = cur.fetchone()
        cur.close()
        return render_template ("admin_protected.html",data=fetchdata)
    else:    
        if request.method=='POST':
            Username = request.form.get('username')
            Password = request.form.get('password')
        
            if (Username == load['Admin_username'] and Password == load['Admin_password']):
                session['user'] = Username
                cur = db.connection.cursor()
                cur.execute('SELECT * FROM release_election')
                fetchdata = cur.fetchone()
                cur.close()
                return render_template ('admin_protected.html',data=fetchdata)
            else:
                flash('Invalid username or password')
                return render_template('admin_login.html')
        return render_template('admin_login.html')


@app.route('/logout')
def Logout():
    if 'user' in session:
        session.pop('user',None)
        flash('Admin Logged Out successfully')
        return redirect('/dashboard')
    else:
        return('Requested Url not found')

@app.route('/logout1')
def Logout1():
    if 'user1' in session:
        session.pop('user1',None)
        flash("Logged out")
        return redirect('/clogin')
    else:
        return('Requested Url not found')

@app.route('/logout2')
def Logout2():
    if 'user3' in session:
        session.pop('user3',None)
        flash("Logged out")
        return redirect('/vlogin')
    else:
        return('Requested Url not found')

@app.route('/release', methods=['GET','POST'])
def Adde():
    if 'user' in session:
        add=db.connection.cursor()
        add.execute('SELECT EID FROM release_election')
        count = add.rowcount

        if count>0:
            bool=False
            return render_template('add_election.html',bool=bool)

        else :
            bool=True
            if request.method=='POST':
                etitle = request.form['ename']
                rstart = request.form['sdate']
                rend = request.form['edate']
                vstart = request.form['vstart']
                vend = request.form['vend']
                rdeclare = request.form['rdate']
                about = request.form['about']
    
                cur = db.connection.cursor()
                cur.execute("INSERT INTO release_election(ETitle,Cstart,Cend,Vstart,Vend,Rdeclare,About) VALUES (%s,%s,%s,%s,%s,%s,%s)",(etitle,rstart,rend,vstart,vend,rdeclare,about))
                db.connection.commit()
                flash('Election Released successfully')
                return redirect('/release')
            return render_template('add_election.html' , bool=bool)
    else:
        return("Requested Url Not found")

@app.route('/Candidates')
def Registrations():
    if 'user' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration')
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("verifyCandidates.html" ,data=fetchdata)
    else:
        return('Requested Url not found')
    
@app.route('/Voters')
def vRegistrations():
    if 'user' in session:
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration')
        fetchdata = cur.fetchall()
        cur.close()
        return render_template("verifyVoters.html" ,data=fetchdata)
    else:
        return('Requested Url Not found')
    
@app.route('/cregister' ,methods=['GET','POST'])
def Cregister():
    curl = db.connection.cursor()
    curl.execute('SELECT Cstart,Cend FROM release_election')
    fetchdate = curl.fetchone()
    count1=curl.rowcount
    curl.close()
    
    if count1==1:
        bool=False
        if now >= fetchdate[0] and now <= fetchdate[1]:
            bool=True
        if request.method=='POST':
            Email=request.form['email']
            exist=db.connection.cursor()
            exist.execute('SELECT * FROM candidate_registration WHERE Email=%s',(Email,))
            count=exist.rowcount
            exist.close()
            if count==0:
                Cfname=request.form['fname']
                Clname=request.form['lname']
                Dob=request.form['dob']
                Mobile=request.form['phone']
                Gender=request.form['gender']
                Password=request.form['password']
                Intro = request.form['intro']
        
                cur = db.connection.cursor()
                cur.execute('INSERT INTO candidate_registration(Fname,Lname,Dob,Mobile_NO,Gender,Email,Password,Introduction) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)' ,(Cfname,Clname,Dob,Mobile,Gender,Email,Password,Intro))
                cur.execute('INSERT INTO shortlist_candidate(Fname,Lname,Dob,Email,Gender) VALUES(%s,%s,%s,%s,%s)',(Cfname,Clname,Dob,Email,Gender))
                db.connection.commit()
                flash('Registered successfully')
                return redirect("/cregister")
            else:
                flash("Candidate with email "+Email+" already registered")
        return render_template('c_register.html',bool=bool)
    else:
        return render_template('c_register.html',data=fetchdate)

@app.route('/vregister' ,methods=['GET','POST'])
def Vregister():
    curl = db.connection.cursor()
    curl.execute('SELECT Cstart,Cend FROM release_election')
    fetchdata = curl.fetchall()
    count1=curl.rowcount
    curl.close()
    if count1==1:
        if request.method=='POST':
            Email=request.form['email']
            exist=db.connection.cursor()
            exist.execute('SELECT * FROM voter_registration WHERE Email=%s',(Email,))
            count=exist.rowcount
            exist.close()
            if count==0:
                Vfname=request.form['Fname']
                Vlname=request.form['Lname']
                Dob=request.form['dob']
                Mobile=request.form['phone']
                Gender=request.form['gender']
                Password=request.form['password']
        
                cur = db.connection.cursor()
                cur.execute('INSERT INTO voter_registration(Fname,Lname,Dob,Mobile_NO,Gender,Email,Password) VALUES(%s,%s,%s,%s,%s,%s,%s)' ,(Vfname,Vlname,Dob,Mobile,Gender,Email,Password))
                cur.execute('INSERT INTO due_voters(fname,lname,Email) VALUES (%s,%s,%s)',(Vfname,Vlname,Email))
                db.connection.commit()
                flash('Registered Successfully')
                return redirect("/vregister")
            else:
                flash("Voter with email "+Email+" already registered")
        return render_template('v_register.html')
    else:
        return render_template("v_register.html",data=fetchdata)

@app.route('/clogin',methods=['GET','POST'])
def Clogin():
    if request.method=='POST':
        clogin=request.form
        email=clogin['email']
        password=clogin['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration WHERE Email=%s AND Password=%s',(email,password))
        fetchdata = cur.fetchall()
        count=cur.rowcount
        cur.close()
        if count==1:
            session['user1'] = email
            return render_template('candidate_profile.html',data=fetchdata)
        else:
            flash("Invalid Email or Password")
            return render_template('c_login.html')

    return render_template('c_login.html')

@app.route('/vlogin',methods=['GET','POST'])
def Vlogin():
    if request.method=='POST':
    
        email=request.form['email']
        password=request.form['password']
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration WHERE Email=%s AND Password=%s',(email,password))
        fetchdata = cur.fetchall()
        count=cur.rowcount
    
        if count==1:
            session['user3'] = email
            return render_template('voter_profile.html',data=fetchdata)
        else:
            flash("Invalid Email or Password")
            return render_template('v_login.html')
    return render_template('v_login.html')  
  

@app.route('/voted/<int:id>',methods=['GET','POST'])
def Voted(id):
    if 'user3' in session:
        cur = db.connection.cursor()
        str=session['user3']
        cur.execute('SELECT * FROM voter_registration WHERE (Email=%s AND Status=%s)',(str,'Approved'))
        fetchdata = cur.fetchall()
        count1=cur.rowcount
        cur.execute('SELECT * FROM due_voters WHERE Email=%s',(str,))
        count2=cur.rowcount
        cur.connection.commit()
        if count1==1 and count2==1:

            vote = db.connection.cursor()
            vote.execute('DELETE FROM due_voters WHERE Email=%s',(str,))
            db.connection.commit()
            vote.close()
            vote = db.connection.cursor()
            vote.execute("SELECT VoteCount FROM shortlist_candidate WHERE ID='%d'" % id)
            votes=vote.fetchone()
            print(votes[0])
            vote.execute("""UPDATE shortlist_candidate SET VoteCount=%s WHERE ID=%s""",(votes[0]+1,id)) 
            db.connection.commit()
            flash("Voted")
            return redirect("/")
            
        elif count1==0:
            flash("Error : Can't vote as your application either pending or rejected")
            return redirect('/')    
        else:
            flash("Error : you have already voted")
            return redirect("/")
    else:
        flash("Note : Login in to your voter account")
        return redirect('/vlogin')



@app.route('/status/<string:type>/<string:operation>/<int:id>')
def ChangeStatus(type,operation,id):
    if 'user' in session:
        if type=='voter':
            if operation =='approve':
                obj=db.connection.cursor()
                obj.execute("""UPDATE voter_registration SET Status=%s WHERE ID=%s""",('Approved',id))
                db.connection.commit()
                obj.close()
                return redirect('/Voters')
            else:
                obj=db.connection.cursor()
                obj.execute("""UPDATE voter_registration SET Status=%s WHERE ID=%s""",('Rejected',id))
                db.connection.commit()
                obj.close()
                return redirect('/Voters')
        else:
            if operation =='approve':
                obj=db.connection.cursor()
                obj.execute('SELECT ID FROM candidate_registration WHERE (ID=%s AND Status=%s)',(id,'Pending'))
                count=obj.rowcount
                obj.close()
                if count==1:
                    obj = db.connection.cursor()
                    obj.execute("""UPDATE candidate_registration SET Status=%s WHERE ID=%s""",('Approved',id))
                    obj.close()
                    db.connection.commit()
                return redirect("/Candidates")

            else:
                obj=db.connection.cursor()
                obj.execute('SELECT ID FROM candidate_registration WHERE (ID=%s AND Status=%s)',(id,'Pending'))
                count=obj.rowcount
                obj.close()
                if count==1:
                    obj = db.connection.cursor()
                    obj.execute("""UPDATE candidate_registration SET Status=%s WHERE ID=%s""",('Rejected',id))
                    obj.execute("DELETE FROM shortlist_candidate WHERE ID = '%d'" % (id))
                    obj.close()
                    db.connection.commit()
                return redirect("/Candidates")
    else:
        return ('Requested Url not found')



@app.route('/result')
def Result():
    if 'user' in session:
        curl = db.connection.cursor()
        curl.execute('SELECT Cstart,Cend FROM release_election')
        fetchdata = curl.fetchall()
        curl.close()
        if fetchdata!=():
            rslt1=db.connection.cursor()
            rslt1.execute('SELECT ID,Fname,Lname,Email,VoteCount FROM shortlist_candidate')
            rsltdata1=rslt1.fetchall()
            rslt1.close()
            rslt2=db.connection.cursor()
            rslt2.execute('SELECT Max(VoteCount) FROM shortlist_candidate')
            rsltdata2=rslt2.fetchall()
            count=rslt2.rowcount
            rslt2.close()
            max=rsltdata2[0][0]
            if  max!=None:
                rslt2=db.connection.cursor()
                rslt2.execute("SELECT ID,Fname, Lname, Email,VoteCount FROM shortlist_candidate WHERE VoteCount ='%d'"%(max))
                rsltdata2=rslt2.fetchall()
                rslt2.close()
                return render_template('resultdeclare.html',data=rsltdata1,data1=rsltdata2,data2=fetchdata)
            else:
                return render_template('resultdeclare.html',data2=fetchdata) 
        else:
            return render_template('resultdeclare.html',data2=fetchdata)
    else:
        return("Requested Url not found")

@app.route('/voter_account')
def Accountv():
    if 'user3' in session :
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM voter_registration WHERE Email=%s',(session['user3'],))
        fetchdata = cur.fetchall()
        cur.close()
        return render_template('voter_profile.html',data=fetchdata)
    else:
        flash('Login to your voter account')
        return redirect('/vlogin')

@app.route('/candidate_account')
def Accountc():
    if 'user1' in session :
        cur = db.connection.cursor()
        cur.execute('SELECT * FROM candidate_registration WHERE Email=%s',(session['user1'],))
        fetchdata = cur.fetchall()
        cur.close()
        return render_template('candidate_profile.html',data=fetchdata)
    else:
        flash('Login to your candidate account')
        return redirect('/clogin')

@app.route('/contact')
def Contact():
    obj=db.connection.cursor()
    obj.execute("SELECT * FROM address_new")
    data = obj.fetchone()
    obj.close
    return render_template('contact.html',data=data)


@app.route('/close')
def Close():
    if 'user' in session:
        
        session.pop('user1',None)
        session.pop('user3',None)

        obj1=db.connection.cursor()
        obj1.execute('DELETE FROM voter_registration')
        obj1.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM candidate_registration')
        obj2.close()

        obj3=db.connection.cursor()
        obj3.execute('DELETE FROM shortlist_candidate')
        obj3.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM candidate_registration')
        obj2.close()

        obj2=db.connection.cursor()
        obj2.execute('DELETE FROM due_voters')
        obj2.close()
        
        obj4=db.connection.cursor()
        obj4.execute('DELETE FROM release_election')
        obj4.close()    
        db.connection.commit()

        files = os.listdir("static/images/")

        for i in files:
            os.remove('static/images/'+i)

        flash('Election closed successfully')
        bool=True
        return render_template('add_election.html',bool=bool)
    else:
        return("Requested Url is not found")  

@app.route('/image/<string:token>/<int:id>' , methods=['GET','POST'])
def Image(token,id):
    if token=='voter':
        if 'user3' in session:
            if request.method=='POST':
                pics= db.connection.cursor()
                pics.execute('SELECT Profile_pic FROM voter_registration WHERE ID="%d"'%(id))
                picture=pics.fetchall()
                pics.close()
                img=picture[0][0]
                files = os.listdir("static/images/")

                for i in files:
                    if i==img:
                        os.remove('static/images/'+i)


                image= request.files['imagefile']
                picname=str(uuid.uuid1()) + os.path.splitext(image.filename)[1]

                image.save(os.path.join('static/images',picname))

                pic=db.connection.cursor()

                pic.execute("""UPDATE voter_registration SET Profile_pic=%s WHERE ID=%s""",(picname,id))
                db.connection.commit()
                pic.close()

                return redirect('/voter_account')
            return render_template("image.html",id=id,token=token)
        else:
            return("Requested url is not found")
    elif token=='candidate':
        if 'user1' in session:
            if request.method=='POST':
                pics= db.connection.cursor()
                pics.execute('SELECT Profile_pic FROM candidate_registration WHERE ID="%d"'%(id))
                picture=pics.fetchone()
                pics.close()
        
                files = os.listdir("static/images/")
                img=picture[0]

                for i in files:
                    if i==img:
                        os.remove('static/images/'+i)
            
                pics= db.connection.cursor()
                pics.execute('SELECT Profile_pic FROM shortlist_candidate WHERE ID="%d"'%(id))
                picture=pics.fetchone()
                pics.close()
            
                files = os.listdir("static/images/")
                img='image'
                if picture!=None:
                    img=picture
                files = os.listdir("static/images/")

                for i in files:
                    if i==img:
                        os.remove('static/images/'+i)

                image= request.files['imagefile']
                picname=str(uuid.uuid1())+ os.path.splitext(image.filename)[1]
                image.save(os.path.join('static/images',picname))

                pic=db.connection.cursor()
                pic.execute("UPDATE candidate_registration SET Profile_pic=%s WHERE ID=%s",(picname,id))
                db.connection.commit()
                pic.close

                pic=db.connection.cursor()
                pic.execute("""UPDATE shortlist_candidate SET Profile_pic=%s WHERE ID=%s""",(picname,id))
                db.connection.commit()
                pic.close
        
                return redirect('/candidate_account')
            return render_template("image.html",id=id,token=token)
        else:
            return("Requested Url is not found")


@app.route('/knowMore/<int:id>')
def Vote(id):
    cur=db.connection.cursor()
    cur.execute('SELECT Profile_pic,Fname,Lname,Gender,Dob,Mobile_NO,Introduction FROM candidate_registration WHERE ID="%d"'%(id))
    data = cur.fetchall()
    cur.close()
    return render_template('castvote.html',data=data)

@app.route('/about')
def About():

    obj=db.connection.cursor()
    obj.execute('SELECT ETitle,About FROM release_election')
    data = obj.fetchone()
    count=obj.rowcount
    obj.close()
    print(data)
    return render_template('about.html',data=data)

@app.route('/address' , methods=['GET','POST'])
def Address():
    if 'user' in session:
        add=db.connection.cursor()
        add.execute('SELECT * FROM address_new')
        data=add.fetchone()
        count=add.rowcount
        add.close()
        if count==0:
            if request.method=='POST':    
                plot_no = request.form['plotno']
                strcolony=request.form['strcolony']
                area = request.form['area']
                city= request.form['city']
                state = request.form['state']
                pincode = request.form['pincode']
                email = request.form['email']
                mobile = request.form['mobile']
                link = request.form['maplink']

                add = db.connection.cursor()
                add.execute('INSERT INTO address_new(Plot_No, Colony, Area, City, State ,Pin_Code, Email, Mobile_No,Map_link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)',(plot_no,strcolony,area,city,state,pincode,email,mobile,link))
                db.connection.commit()
                add.close()
                return redirect('/address')
            return render_template('address.html',data=data)
        else:
            return render_template('address.html',data=data)
    else:
        return("Requested url is not found")

@app.route('/addnew')
def Addnew():
    if 'user' in session:
        dlt = db.connection.cursor()
        dlt.execute("DELETE FROM address_new")
        db.connection.commit()
        dlt.close()
        return redirect('/address')
    else:
        return('Requested Url is not found')

@app.route('/edit',methods=['GET','POST'])
def Edit():
    if 'user' in session:
        edit = db.connection.cursor()
        edit.execute('SELECT * FROM release_election')
        data = edit.fetchone()
        edit.close()
    
        if request.method=='POST':
            etitle = request.form['ename']
            rstart = request.form['sdate']
            rend = request.form['edate']
            vstart = request.form['vstart']
            vend = request.form['vend']
            rdeclare = request.form['rdate']
            about = request.form['about']
            cur = db.connection.cursor()
            cur.execute("""UPDATE release_election SET ETitle=%s ,Cstart=%s ,Cend=%s ,Vstart=%s ,Vend=%s ,Rdeclare=%s ,About=%s WHERE EID=%s""",(etitle,rstart,rend,vstart,vend,rdeclare,about,data[0]))
            db.connection.commit()
            flash('Election updated ')
            return redirect('/release')
        return render_template("edit.html",data=data)
    else:
        return('Requested Url is not found')

app.run(debug=False)
