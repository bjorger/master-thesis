from transformers import TFAutoModelForSequenceClassification, AutoTokenizer 
import tensorflow as tf
import numpy as np

tokenizer = AutoTokenizer.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")
model = TFAutoModelForSequenceClassification.from_pretrained("rabindralamsal/finetuned-bertweet-sentiment-analysis")

# INPUT TWEET IS ALREADY NORMALIZED!
example_tweet = ":down_arrow: Top losers of the last hour ( Out of Top 100 ) :chart_decreasing: :red_circle: $ 1.8945 :chart_decreasing: -2.10343533 % :red_circle: $ 0.7081 :chart_decreasing: -1.8364444 % :red_circle: $ 0.2890 :chart_decreasing: -1.8196798 % :red_circle: $ 2.4003 :chart_decreasing: -1.59079707 % :red_circle: $ 0.2607 :chart_decreasing: -1.30812737 % Trade on FTX HTTPURL"

input = tokenizer.encode(example_tweet, return_tensors='tf')
output = model.predict(input)[0]
prediction = tf.nn.softmax(output, axis=1).numpy()
sentiment = np.argmax(prediction)
print(sentiment)
print(prediction)
