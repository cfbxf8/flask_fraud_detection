# flask_fraud_detection
Fraud Detection Flask App

Simulates live "users" hitting the site and attempting to create items they will be trying to sell ('/score' endpoint)
Real-time deployment of a Gradient Boosting Classifier on the new user 
  - Training data used was actual data from an E-Commerce company
Then, using the predicted probability of fraud from the model determines "High", "Medium", "Low", or "Unlikely"
  - Fraud was quite costly to the company so the probability breaks were influenced by this (higher type I error)
All of the user data is immediately stored in a MongoDB table and all of the prediction data is stored in a seperate MongoDB table (to maintain data integrity in the case of a flawed model output), but a shared key is created across both tables.
This MongoDB is then queried when the '/dashboard' endpoint is visited.
This simple dashboard (image below) could then be used by a Customer Service team to respond via email or phone and with the relevant information including reasons for the fraud flag.

![alt tag](https://github.com/cfbxf8/flask_fraud_detection/blob/master/imgs/Screen%20Shot%202017-01-17%20at%2010.53.18%20PM.png)

![alt tag](https://github.com/cfbxf8/flask_fraud_detection/blob/master/imgs/Screen%20Shot%202017-01-17%20at%2011.03.38%20PM.png)
