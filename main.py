from swimmer import *
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import train_test_split


test_id = [4969159,5060231,4969162,4443119, 4822817, 5060233, 4784046, 4206537, 4566034,4457697,4204197, 4686351, 4700054, 5142548, 4978681
           ,4450863, 4567074,4458018, 4032770, 4276196, 5062003, 4573843]
swimmers = [Swimmer(date(2000, 12, 29), id, 'M', str(id)) for id in test_id]

dfs = [swimmer.get_regression_pb() for swimmer in swimmers]
df = pd.concat(dfs)

def linear_regression(data, target, test_data, test_target):
    lr = LinearRegression()
    lr.fit(data, target)
    
    predictions = lr.predict(test_data)
    
    mse = mean_squared_error(test_target, predictions)
    r2 = r2_score(test_target, predictions)
    
    print("Mean Squared Error:", mse)
    print("R^2 Score:", r2)
    cdf = lr.coef_
    print(cdf)
    
    return lr


df = df[['100m Freestyle 25m', '400m Freestyle 25m',  '200m Freestyle 25m']].dropna()
data = df[['100m Freestyle 25m', '400m Freestyle 25m']]
target = df[['200m Freestyle 25m']]
train_data, test_data, train_target, test_target = train_test_split(data, target, test_size=0.2)

linear_regression(train_data, train_target, test_data, test_target)