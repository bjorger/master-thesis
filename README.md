chmod 400 MasterthesisKeyPair.pem
ssh -i "MasterthesisKeyPair.pem" ec2-user@ec2-44-211-40-41.compute-1.amazonaws.com
ssh -L 5901:localhost:5901 -i "MasterthesisKeyPair.pem" ec2-user@ec2-44-211-40-41.compute-1.amazonaws.com

https://medium.com/@jkimera5/installing-a-graphical-user-interface-gui-on-aws-ec2-linux-2-instance-and-accessing-it-over-a-1d96a16949dc
https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
H4lL0$153$

# Install tigerVNC

https://www.cyberciti.biz/faq/install-and-configure-tigervnc-server-on-ubuntu-18-04/

# Transfer files using FileZila

https://it.cornell.edu/academic-web-dynamic-academic-web-static-managed-servers/transfer-files-using-filezilla

# Run a python script 24/7

https://victormerino.medium.com/running-a-python-script-24-7-in-cloud-for-free-amazon-web-services-ec2-76af166ae4fb

# install the working version of twint

pip3 install --user --upgrade git+https://github.com/twintproject/twint.git@origin/master#egg=twint

# Binance API

https://binance-docs.github.io/apidocs/spot/en/#market-data-endpoints
https://binance-docs.github.io/apidocs/spot/en/#old-trade-lookup-market_data

# Pytorch LSTM

https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
https://machinelearningmastery.com/time-series-prediction-lstm-recurrent-neural-networks-python-keras/
https://medium.com/the-handbook-of-coding-in-finance/stock-prices-prediction-using-long-short-term-memory-lstm-model-in-python-734dd1ed6827
https://bobrupakroy.medium.com/multi-variate-lstm-time-series-forecasting-1a736009f6d
https://github.com/MohammadFneish7/Keras_LSTM_Diagram

# Pytorch TCN

https://www.kaggle.com/code/ceshine/pytorch-temporal-convolutional-networks/script

# Experiments

LSTM:

-   BTC
-   Stx
-   Lrc
-   BTC + Twitter Sentiment
-   BTC + Reddit Sentiment
-   BTC + Fear and Greed Index
-   BTC + Twitter & Reddit Sentiment
-   BTC + Fear and Greed Index + Twitter
-   BTC + Fear and Greed Index + Reddit
-   BTC + Fear and Greed Index + Reddit + Twitter
-   Stx + Twitter Sentiment
-   Stx + Reddit Sentiment
-   Stx + Fear and Greed Index
-   Stx + Twitter & Reddit Sentiment
-   Stx + Fear and Greed Index + Twitter
-   Stx + Fear and Greed Index + Reddit
-   Stx + Fear and Greed Index + Reddit + Twitter
-   Lrc + Twitter Sentiment
-   Lrc + Reddit Sentiment
-   Lrc + Fear and Greed Index
-   Lrc + Twitter & Reddit Sentiment
-   Lrc + Fear and Greed Index + Twitter
-   Lrc + Fear and Greed Index + Reddit
-   Lrc + Fear and Greed Index + Reddit + Twitter

add tweet volume to variations as well

# LSTM based sentiment

https://www.ncbi.nlm.nih.gov/pmc/articles/PMC7959635/

https://www.kaggle.com/code/kmkarakaya/lstm-output-types-return-sequences-state/notebook
https://bond-kirill-alexandrovich.medium.com/lstm-in-details-is-easy-501630afbcb9
