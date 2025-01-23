import os
import sqlite3
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import mean_squared_error, r2_score
from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)
app.secret_key = '@aB12345'  # Set a secret key for session management

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to initialize the database
init_db()

# Load and preprocess the data
data = pd.read_csv("C:/Users/91982/Documents/Cognifyz Technologies/Task 1/Dataset.csv")

# Handle missing values
data.dropna(inplace=True)

# Remove duplicate rows
data.drop_duplicates(inplace=True)

# Encode categorical variables
label_encoders = {}
for column in ['City', 'Has Table booking', 'Has Online delivery', 'Is delivering now', 'Price range']:
    le = LabelEncoder()
    data[column] = le.fit_transform(data[column])
    label_encoders[column] = le

# Feature selection
features = ['Country Code', 'City', 'Average Cost for two', 'Has Table booking', 
            'Has Online delivery', 'Is delivering now', 'Price range', 'Votes']
target = 'Aggregate rating'
X = data[features]
y = data[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train a Random Forest Regressor model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Save the model and label encoders
pickle.dump(model, open('random_forest_model.pkl', 'wb'))  # Ensure no space before .pkl
pickle.dump(label_encoders, open('label_encoders.pkl', 'wb'))  # Ensure no space before .pkl

# Create a folder for visualizations
visualization_folder = 'static/images/visualizations'
os.makedirs(visualization_folder, exist_ok=True)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session['user'] = email
            return redirect(url_for('home'))  # Redirect to the home page
        else:
            return render_template('login.html', error="Invalid email or password.")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        conn = sqlite3.connect('users.db')
        cursor = conn.cursor()
        try:
            cursor.execute('INSERT INTO users (email, password) VALUES (?, ?)', (email, password))
            conn.commit()
            return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            return render_template('register.html', error="Email already exists.")
        finally:
            conn.close()
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    if 'user' in session:
        return render_template('index.html', mse=mse, r2=r2)
    return redirect(url_for('login'))

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Load the model and label encoders
        model = pickle.load(open('random_forest_model.pkl', 'rb'))
        label_encoders = pickle.load(open('label_encoders.pkl', 'rb'))

        # Extract features from form input
        country_code = int(request.form['country_code'])
        city = label_encoders['City'].transform([request.form['city']])[0]
        average_cost = float(request.form['average_cost'])
        has_table_booking = label_encoders['Has Table booking'].transform([request.form['has_table_booking']])[0]
        has_online_delivery = label_encoders['Has Online delivery'].transform([request.form['has_online_delivery']])[0]
        is_delivering_now = label_encoders['Is delivering now'].transform([request.form['is_delivering_now']])[0]
        price_range = label_encoders['Price range'].transform([request.form['price_range']])[0]
        votes = int(request.form['votes'])

        # Create input dataframe
        new_data = pd.DataFrame({
            'Country Code': [country_code],
            'City': [city],
            'Average Cost for two': [average_cost],
            'Has Table booking': [has_table_booking],
            'Has Online delivery': [has_online_delivery],
            'Is delivering now': [is_delivering_now],
            'Price range': [price_range],
            'Votes': [votes]
        })

        # Predict Aggregate Rating
        prediction = model.predict(new_data)[0]
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {e}", mse=mse, r2=r2)

    return render_template('index.html', prediction_text=f"Predicted Aggregate Rating: {prediction:.2f}", mse=mse, r2=r2)

@app.route('/visualizations')
def visualizations():
    # Generate visualizations
    create_visualizations()
    
    # List of visualization filenames
    visualizations = [
        'average_cost_vs_rating_colored.png',
        'votes_vs_rating.png',
        'distribution_of_aggregate_ratings.png',
        'aggregate_rating_by_city.png',
        'top_10_cities.png',
        'correlation_matrix.png'
    ]

    # Dynamically serve visualization images
    return render_template('visualization.html', visualizations=visualizations)

def create_visualizations():
    # 1. Scatter Plot: Average Cost vs. Aggregate Rating (Colored by Price Range)
    plt.figure(figsize=(8, 6))
    price_ranges = {
        1: 'green',
        2: 'orange',
        3: 'blue',
        4: 'red'
    }
    for price_range, color in price_ranges.items():
        subset = data[data['Price range'] == price_range]
        sns.scatterplot(x='Average Cost for two', y='Aggregate rating', data=subset, color=color, label=f'Price Range: {price_range}')
    plt.title('Average Cost vs. Aggregate Rating (Colored by Price Range)')
    plt.xlabel('Average Cost for two')
    plt.ylabel('Aggregate Rating')
    plt.legend()
    plt.savefig(os.path.join(visualization_folder, 'average_cost_vs_rating_colored.png'))
    plt.close()

    # 2. Scatter Plot: Votes vs. Aggregate Rating
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x='Votes', y='Aggregate rating', data=data, hue='Price range', palette='viridis', s=100)
    plt.title('Votes vs. Aggregate Rating (Colored by Price Range)')
    plt.xlabel('Votes')
    plt.ylabel('Aggregate Rating')
    plt.savefig(os.path.join(visualization_folder, 'votes_vs_rating.png'))
    plt.close()

    # 3. Distribution of Aggregate Ratings
    plt.figure(figsize=(10, 6))
    sns.histplot(data['Aggregate rating'], kde=True, color='skyblue', bins=20)
    plt.title('Distribution of Aggregate Ratings', fontsize=16, fontweight='bold', color='#333333')
    plt.xlabel('Aggregate Rating', fontsize=12, color='#555555')
    plt.ylabel('Frequency', fontsize=12, color='#555555')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    sns.despine()
    plt.savefig(os.path.join(visualization_folder, 'distribution_of_aggregate_ratings.png'))
    plt.close()

    # 4. Boxplot of Aggregate Rating by City (Top 10 Cities)
    top_10_cities = data['City'].value_counts().nlargest(10).index
    plt.figure(figsize=(12, 6))
    sns.boxplot(x='City', y='Aggregate rating', data=data[data['City'].isin(top_10_cities)], palette='Set3')
    plt.xticks(rotation=45, ha='right')
    plt.title('Aggregate Rating Distribution by City (Top 10)', fontsize=16, fontweight='bold')
    plt.xlabel('City', fontsize=12)
    plt.ylabel('Aggregate Rating', fontsize=12)
    plt.tight_layout()
    plt.savefig(os.path.join(visualization_folder, 'aggregate_rating_by_city.png'))
    plt.close()

    # 5. Bar Plot: Top 10 Cities by Restaurant Count
    city_counts = data['City'].value_counts().head(10)
    plt.figure(figsize=(10, 6))
    sns.barplot(x=city_counts.index, y=city_counts.values)
    plt.title('Top 10 Cities by Restaurant Count')
    plt.xlabel('City')
    plt.ylabel('Number of Restaurants')
    plt.xticks(rotation=45, ha='right')
    plt.savefig(os.path.join(visualization_folder, 'top_10_cities.png'))
    plt.close()

    # 6. Correlation Matrix Heatmap
    numerical_features = data.select_dtypes(include=['number'])
    correlation_matrix = numerical_features.corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(correlation_matrix, annot=True , cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Matrix of Numerical Features')
    plt.savefig(os.path.join(visualization_folder, 'correlation_matrix.png'))
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
