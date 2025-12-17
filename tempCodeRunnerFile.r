import numpy as np

# Generate some random data
X = np.random.rand(100, 10)
y = np.random.rand(100)

# Fit the model
model = LinearRegression()
model.fit(X, y)

# Calculate the bias
bias = np.mean(y - model.predict(X))
print("Bias:", bias)

# Calculate the variance
predictions = model.predict(X)
variance = np.mean((predictions - y) ** 2)
print("Variance:", variance)
from sklearn.linear_model import LinearRegression

# Create an instance of the LinearRegression class
regressor = LinearRegression()

# Fit the model to the dataset
regressor.fit(X_train, y_train)

# Generate predictions on new data
y_pred = regressor.predict(X_test)