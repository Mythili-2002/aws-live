from flask import Flask,render_template,request
from config import *
from pymysql import connections
import boto3

app = Flask(__name__)
bucket = custombucket
region = customregion
database = connections.Connection(host = customhost,
                                  port = 3306,
                                  user = customuser,
                                  password= custompass,
                                  db = customdb)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/update', methods=['POST'])
def update():
    emp_id = request.form['emp_id']
    fname = request.form['fname']
    lname = request.form['lname']
    skill = request.form['skill']
    location = request.form['location']
    picture = request.files['picture']
    emp_full_name = fname + " " + lname
    img_filename = "emp-id" + str(emp_id) + "image_file"

    insert_val = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
    cursor = database.cursor()

    try:
        #Committing the values in database
        cursor.execute(insert_val,(emp_id,fname,lname,skill,location))
        database.commit()

        #Pusing objects into S3
        s3_resource = boto3.resource('s3')
        s3_resource.Bucket(custombucket).put_object(Key=img_filename, Body=picture)
        cursor.close()
        print("all modification done...")
        return render_template('output.html', name=emp_full_name)

    except Exception as e:
            return str(e)


if __name__ == '__main__':
    app.run(debug=True)