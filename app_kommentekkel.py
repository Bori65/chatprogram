from datetime import datetime 
from flask import render_template, Flask, escape, request, session, redirect, url_for
from flask_bootstrap import Bootstrap
import hashlib
import configparser
#importáljuk a könyvtárkat illetve a könyvtárkból a classokat

app = Flask(__name__) 
Bootstrap(app)
app.secret_key=b'd#\t.gbn24#@-54_#\n/\\' #egy byte string

page_chat='chat.html'
page_login='login.html'
page_register='register.html'
#valtozokba menti a html oldalakat

messagesSoFar = [] #tömb, ahova az üzenetek lesznek mentve
limit=100	#ez határozza meg az üzenetek számát
mesLengthLimit=200	#ez határozza meg az üzenetek hosszát


configfile='users.properties' # elmenti a konfiguracios file nevet
userdata=configparser.RawConfigParser() #elemti a parser osztalyt

userdata.read(configfile) #beolvassa a konfiguracios filet aminek a nevet elraktuk az elobb letrehozott parserral

@app.route('/') #megadjuk az URL-t
@app.route('/index') #megadjuk az URL-t
def index(): #funkciot hozunk letre
    if 'username' in session:
        return redirect(url_for('message'))
    return render_template(page_login)		
	#ha felhasznalonev benne van sessionben, akkor letrehoz egy oldalat, ha nem, akkor a loginbe kuld
	
@app.route('/login', methods=['GET','POST'])#megadjuk az URL-t, get,post metodust hasznaljuk
def login(): #funkciot hoz letre
    message=None #uzenetek eltuntetese
    if 'username' in session:
        return sendChatPage()
	#ha felhasznalonev benne van sessionben, akkor atiranyit a chatbe
    if request.method == 'POST': 	#ha a metodus post akkor elmenti ezekbe a valtozokba a felhasznalonevet es a jelszot
        acquiredUname=request.form['usr']
        acquiredPsswd=request.form['pwd']
        if isUserValid(acquiredUname, acquiredPsswd):
		#leellenorzi a nevet es a jelszot, ha jo akkor atiranyit az uzenetekhez, ha rossz akkor kiirja, hogy sikertelen a bejelentkezes
            session['username']=acquiredUname
            return redirect(url_for('message'))
        message='Login unsuccessful. Please try again.'
    return render_template(page_login, mes=message)

@app.route('/register', methods=['GET', 'POST'])#megadjuk az URL-t, get,post metodust hasznaljuk
def register(): #funkciot hoz letre
    if request.method=='POST':	#ha a metodus post akkor elmenti ezekbe a valtozokba a felhasznalonevet es a jelszotkat
        usr=request.form['usr']
        pwd1=request.form['pwd1']
        pwd2=request.form['pwd2']
        if not pwd1 == pwd2:
		
            render_template(page_register,mes="Password doesn't match.")
        addUser(usr,pwd1)
        return redirect(url_for('login'))
    return render_template(page_register)
#a jelszavakat osszehasonlitja, ha nem egyeznek meg akkor uzenetet ir ki, ha megegyeznek akkor uj felhasznalot add hozza es a login oldalra megy at
	
@app.route('/logout')	#megadjuk az URL-t
def logout():
    if 'username' in session:
        session.pop('username', None) #kijelentkezeskor a sessionbol eltavolitja a felhasznalot
    return redirect(url_for('index')) #atiranyit a bejelentkezo oldalra

@app.route('/message', methods=['GET','POST']) #megadjuk az URL-t, get,post metodust hasznaljuk
def message():	
    if not 'username' in session:
        return render_template(page_login) #ha nincs a felhasznalonev a sessionben, akkor visszakapjuk a login oldalt

    user=session['username']

    if request.method ==  'POST':	#ha a metodus post akkor elmenti a valtozoba az uzenetet
        recmes=request.form['mes']
        if len(recmes) > mesLengthLimit: #ha az uzenet hosszabb mint a limit akkor az elejerol levag
            recmes = recmes[:mesLengthLimit]
        messagesSoFar.append('[' + getCurrentDatetime() + '] ['  + user + ']: ' + recmes)

    return sendChatPage()

def concatMessages(): #lancba szedi az uzeneteket
    ret=""		#üres változó
    for i in messagesSoFar:
        ret = ret + "<br/>" + i
    return ret

def getCurrentDatetime():	#kiirja, mikor lett elkuldve az uzenet
    dateNow=datetime.now()
    return dateNow.strftime("%Y.%m.%d %H:%M:%S")

def addUser(uname, psswd): #hozzaadja a felhasznalo nevet es a jelszavanak a hash-et a tobbi koze
    hashedPassword=hashlib.sha256(psswd.encode('utf-8')).hexdigest()#hashedPassword valtozoba menti el a funkcioba leadott jelszo hash-et
    userdata.set('users',uname,hashedPassword) #a parser API-enek a set metodusaval letrehozzuk a felhasznalonev es a hozzatartozo hash parosat
    with open(configfile,'w') as cfgfile: #megnyitjuk a configuracios filet iro modban
        userdata.write(cfgfile)	#beirja a fileba a userdatat
    userdata.read(configfile)	#configuracios fileba beolvassa a userdatat

def isUserValid(uname, psswd):
    if userdata.has_option('users',uname):
        storedPassword=userdata.get('users',uname)#valtozoba menti a raktarozott hash-t
        hashedPassword=hashlib.sha256(psswd.encode('utf-8')).hexdigest()#valtozoba menti a raktarozott hash-t
        if hashedPassword == storedPassword: #osszehasonlitja a beirt jelszo hash-et es az elmentett jelszoet,majd civisszaadja a funkcio hogy true vagy false
            return True
    return False

def sendChatPage(): #letrehozza a chat feluletet
    return render_template(page_chat, message=concatMessages(), usr=session['username'])

