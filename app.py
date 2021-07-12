from typing import Text
from flask import Flask,render_template, request,send_file
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)

ENV ='dev'

if ENV == 'dev':
    app.debug = True
    app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:hp@localhost/postgres'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI']=''
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
class Invoice(db.Model):
    __tablename__='invoice'
    id = db.Column(db.Integer, primary_key= True)
    invoice_no = db.Column(db.String, unique=True)
    from_business = db.Column(db.String)
    client = db.Column(db.String)
    invoice_date = db.Column(db.Date)
    quantity = db.Column(db.Integer)
    rate = db.Column(db.Numeric)
    amount = db.Column(db.Numeric)

    def __init__(self,invoice_no,from_business,client,invoice_date,quantity,rate,amount):
        self.invoice_no = invoice_no
        self.from_business = from_business
        self.client = client
        self.invoice_date = invoice_date
        self.quantity = quantity
        self.rate = rate
        self.amount = amount
    

@app.route('/')
def index():
    return render_template('index.html')



#@app.route('/submit',methods=['POST'])
@app.route('/newinvoice', methods =["GET", "POST"])
def submit():
    if request.method == 'POST':
        print(request.form.get("download"))
        invoice_no=request.form['invoice_no']
        from_business=request.form['from_business']
        client=request.form['client']
        invoice_date=request.form['invoice_date']
        quantity=request.form['quantity']
        rate=request.form['rate']
        amount=request.form['amount']
        result=request.form
        if invoice_no=='' or from_business=='':
            return render_template('index.html', message='Please enter required fields')
       
        if db.session.query(Invoice).filter(Invoice.invoice_no==invoice_no).count()==0:
            data = Invoice(invoice_no,from_business,client,invoice_date,quantity,rate,amount)
            db.session.add(data)
            db.session.commit()
            #invoice = Invoice.query.all()
            # 2021-07-08 to display whatever was entered in the form
        elif db.session.query(Invoice).filter(Invoice.invoice_no==invoice_no).count()>0:
            return render_template('index.html', message='You have already submitted this invoice')
    if request.form.get("download"):        #print(invoice_no,from_business, client, invoice_date)
        return send_file('test.pdf', as_attachment=True)
    return render_template('newinvoice.html',invoice_no=invoice_no,from_business=from_business,
            client=client,invoice_date=invoice_date,quantity=quantity, rate=rate,amount=amount)    
                        # do something
    
                # do something else
        #elif request.method == "GET":
                # do something
        #result = request.form
     
            #return render_template('success.html')
    
# @app.route("/downloadfile/<filename>", methods = ['GET'])
# def download_file():
#     return render_template('download.html',invoice_no=invoice_no,from_business=from_business,
#             client=client,invoice_date=invoice_date,quantity=quantity, rate=rate,amount=amount)
#         # if request.method=="GET":
        #     #tl contains a list of topic list
        #     result = request.form
        #     return render_template('index.html',result=result)

        

if __name__ == '__main__':
    app.run()
