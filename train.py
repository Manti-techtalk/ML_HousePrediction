import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error,r2_score
from joblib import dump


#load the dataset
data = pd.read_csv('/Users/mantimokone/Downloads/housing.csv')
 
print("____Infor___")
print(data.info())
print("____Describe___")
print(data.describe())

#clean the data for missing and duplicates values
data.dropna(inplace=True)
data.drop_duplicates(inplace=True)

#select features and target variable
x = data[['latitude','longitude','total_rooms','population','households','median_income',]]

y = data[['median_house_value']]


# split the dataset
x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.2,random_state=42)

#tain the model witht the train portion of the data
model = LinearRegression()
fitted = model.fit(x_train,y_train) # supervised learning bcz the modek has both the input and the output label
predicted_y = model.predict(x_test)

#evaluating the model using the test and predicted y features
mse = mean_squared_error(y_test,predicted_y)
mae = mean_absolute_error(y_test,predicted_y)
r_score = r2_score(y_test,predicted_y)

print('Mean Square Error', mse)
print('Mean Absolute Error',mae)
print('R Score',r_score)

#save the model using hoblb
dump(model,'HousePrediction.joblib')