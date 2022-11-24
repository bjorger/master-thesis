from transformers import TFAutoModelForSequenceClassification, AutoTokenizer 
import tensorflow as tf
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
model = TFAutoModelForSequenceClassification.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")

# INPUT TWEET IS ALREADY NORMALIZED!
example_tweet = "The NEET exams show our Govt in a poor light: unresponsiveness to genuine concerns; admit cards not delivered to aspirants in time; failure to provide centres in towns they reside, thus requiring unnecessary & risky travels. What a disgrace to treat our #Covid warriors like this!"

input = tokenizer.encode(example_tweet, return_tensors='tf')
output = model.predict(input)[0]
prediction = tf.nn.softmax(output, axis=1).numpy()
sentiment = np.argmax(prediction)
print(sentiment)
print(prediction)
