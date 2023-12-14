from flask import Flask, flash, jsonify
from flask import render_template
from flask import request, redirect, url_for, session
from mysql import connector
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
from datetime import datetime


app = Flask(__name__)
app.secret_key = 'many random bytes'

#open conection
db = connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = '',
    database = 'profilcc'
)

if db.is_connected():
    print('conection successfull')

@app.route("/")
def home():
    return render_template('index.html')


@app.route('/kegiatan/')
def kegiatan():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM ak")
    result = cursor.fetchall()
    cursor.close()
    return render_template('kegiatan.html', ak=result)

@app.route('/tambah_kegiatan/', methods = ['POST'])
def tambah_kegiatan():
        flash("Data Inserted Successfully")
        nama = request.form['nama']
        hari = request.form['hari']
        tanggal = request.form['tanggal']
        kegiatan = request.form['kegiatan']
        keterangan = request.form['keterangan']
        cur = db.cursor()
        cur.execute ('INSERT INTO ak (nama, hari, tanggal, kegiatan, keterangan) VALUES (%s, %s, %s, %s, %s)', 
        (nama, hari, tanggal, kegiatan, keterangan))
        db.commit()
        return redirect(url_for('kegiatan'))

@app.route('/update_kegiatan/', methods= ['GET','POST'])
def update_kegiatan():
        nama = request.form['nama']
        hari = request.form['hari']
        tanggal = request.form['tanggal']
        kegiatan = request.form['kegiatan']
        keterangan = request.form['keterangan']
        cur = db.cursor()
        sql = '''UPDATE ak
        SET hari=%s, tanggal=%s, kegiatan=%s, keterangan=%s
        where nama=%s '''
        value = (hari, tanggal, kegiatan, keterangan, nama)
        cur.execute(sql,value)
        db.commit()
        flash("Data Updated Successfully")
        return redirect(url_for('kegiatan'))

@app.route('/hapus_kegiatan/<nama>', methods = ['GET'])
def hapus_kegiatan(nama):
    flash("Record Has Been Deleted Successfully")
    cur = db.cursor()
    cur.execute("DELETE FROM ak WHERE nama=%s", (nama,))
    db.commit()
    return redirect(url_for('kegiatan'))

if __name__ == "__main__":
    app.run()