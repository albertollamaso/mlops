import pickle
import nltk
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.data import load
from nltk.stem import PorterStemmer
from flask import Flask, request,render_template


nltk.download('punkt')

app = Flask(__name__)
app.config['DEBUG'] = True

def custom_tokenizer_with_English_stemmer(text):
    # my text was unicode so I had to use the unicode-specific translate function. If your documents are strings, you will need to use a different `translate` function here. `Translated` here just does search-replace. See the trans_table: any matching character in the set is replaced with `None`
    tokens = [word for word in nltk.word_tokenize(text)]
    stems = [stemmerEN.stem(item.lower()) for item in tokens]
    return stems

def predictSMSdata(test_text):
    categories = ["legitimate", "spam"]
    categories.sort()

    # load model
    filename1 = "LinearSVC_SMS_spam_EN.pickle"
    file_handle1 = open(filename1, "rb")
    classifier = pickle.load(file_handle1)
    file_handle1.close()

    # load tfidf_vectorizer for transforming test text data
    filename2 = "tfidf_vectorizer_EN.pickle"
    file_handle2 = open(filename2, "rb")
    tfidf_vectorizer = pickle.load(file_handle2)
    file_handle2.close()

    test_list=[test_text]
    tfidf_vectorizer_vectors_test = tfidf_vectorizer.transform(test_list)
    predicted = classifier.predict(tfidf_vectorizer_vectors_test)
    print(categories[predicted[0]])
    return categories[predicted[0]]

# Porter Stemmer for English
stemmerEN = PorterStemmer()

@app.route('/', methods = ["GET","POST"])
def index():
	if(request.method == "POST"):
		text_msg = request.form['sms']
		prediction = predictSMSdata(text_msg)
		print("out: {}".format(prediction))
		x = ""
		if(prediction == "legitimate"):
			x = "Not a spam, it's legitimate"
		else:
			x = "it's a spam" 
		return render_template('mainpage.html',prediction = x)
	else:
		return render_template('mainpage.html')	

if __name__ == "__main__":
	app.run(debug = True, port=5000, host='0.0.0.0')
