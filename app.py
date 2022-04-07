from flask import Flask,render_template,url_for,request

import pandas as pd
from string import punctuation

import nltk
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

from flask_mail import Mail, Message


app = Flask(__name__)

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USE_TLS"] = False
app.config["MAIL_USERNAME"] = 'daulat.malut@gmail.com'
app.config["MAIL_PASSWORD"] = 'Malut212'

mail = Mail(app)



df = pd.read_csv('dictionary.csv')
keyword = df['Kata Kunci'].to_list()

tokenizer = nltk.RegexpTokenizer(r"\w+")
factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/prediksi',methods=['POST'])
def prediksi():
	if request.method == 'POST':
		text = [request.form['message']]

		analisis = []
		kata_kunci = []
		text_tok = tokenizer.tokenize(text[0].lower())
		text_clean = stopword.remove(' '.join(text_tok))

		sentence = tokenizer.tokenize(text_clean.lower())
		for word in sentence:
			if word in keyword:
				kata_kunci.append(word)
				analisis.append((df[df['Kata Kunci'] == word]['Analisis']).to_list())
	
	return render_template('result.html', text=text, analisis = analisis, kata_kunci = kata_kunci)

@app.route('/contact', methods=['POST', 'GET'])
def contact():
	if request.method == 'POST':
		name = request.form['name']
		email = request.form['email']
		subject = request.form['subject']
		msg = request.form['message']

		message = Message(subject, sender='daulat.malut@gmail.com', recipients=['daulat.malut@gmail.com'])


		message.body = """ 
		From: %s
		Email: %s
		Pesan: %s """ %(name, email, msg)

		mail.send(message)

		success= 'Pesan Terkirim'


		return render_template('success.html', success=success)


# if __name__ == '__main__':
# 	# app.run(debug=True)
# 	Application().run(app)