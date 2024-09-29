from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

# Load the dataset
data = load_iris()
X = data.data
y = data.target

# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Define hyperparameter grid (depth and criterion)
max_depth_values = [2, 4, 6, 8, 10]
criteria = ['gini', 'entropy']

best_accuracy = 0
best_params = None

# Perform grid search over hyperparameters
for depth in max_depth_values:
    for criterion in criteria:
        clf = DecisionTreeClassifier(max_depth=depth, criterion=criterion)
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        if accuracy > best_accuracy:
            best_accuracy = accuracy
            best_params = {'max_depth': depth, 'criterion': criterion}

# Output the best hyperparameters and accuracy
print(f"\nBest parameters: {best_params}")
print(f"Best accuracy: {best_accuracy}")
