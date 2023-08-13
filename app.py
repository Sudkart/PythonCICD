from flask import Flask, render_template, request, jsonify
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


app = Flask(__name__, template_folder="template")

model = tf.keras.models.load_model('dnn_model.h5')
tokenizer = Tokenizer()

@app.route('/')
def index():
    return render_template('index.html')



@app.route('/predict', methods=['POST'])
def predict():
    try:
        input_text = request.form['input_text']
        print("input_text:"+input_text)
        tokenizer.fit_on_texts([input_text])
        sequences = tokenizer.texts_to_sequences([input_text])
        padded_sequences = pad_sequences(sequences,padding='post', maxlen=tokenizer.num_words) 
        # Ensure the padded_sequences shape matches the expected shape
        prediction = model.predict(padded_sequences)

        # Convert ndarray to a serializable list
        prediction_list = prediction.tolist()
        
        return jsonify({'result': prediction_list})
    except Exception as e:
        return jsonify({'error': str(e)})



if __name__=="__main__":
    app.run(debug=True)
