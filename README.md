# 🍽️🔍 Machine Learning Restaurant Task - End-to-End ML Application

This project implements an **end-to-end machine learning system** for **restaurant analytics and prediction** using Python and Scikit-Learn. It provides insights into restaurant ratings based on various features like location, reviews, and pricing.

---

## ✅ Features

- **Data Preprocessing**: Handles missing values, feature selection, and scaling.
- **Machine Learning Models**: Implements **Linear Regression, Decision Tree, and Random Forest**.
- **Performance Evaluation**: Uses **Mean Absolute Error (MAE)** and **R² Score**.
- **Data Visualization**: Includes heatmaps, correlation matrices, and scatter plots.
- **User Interaction**: Allows users to input restaurant details and get predictions.

---

## 📜 Prerequisites

Ensure the following are installed:

1. **Python 3.9 or above**  
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
2. **Required Libraries** (Install from `requirements.txt`):
   ```sh
   pip install -r requirements.txt
   ```
3. **Dataset**: Ensure `Dataset.csv` is in the project directory.

---

## 🛠 Setup Instructions

### 1️⃣ Clone the Repository

```sh
git clone https://github.com/Ronak1231/Machine_Learning_Restaurant_Task-1.git
cd Machine_Learning_Restaurant_Task-1
```

### 2️⃣ Install Dependencies

```sh
pip install -r requirements.txt
```

### 3️⃣ Run the Jupyter Notebook

```sh
jupyter notebook
```

---

## 🗃️ File Structure

```
Machine_Learning_Restaurant_Task-1/
│
├── Dataset.csv                     # Dataset file
├── Static
│   ├── Images
|        ├── Visualization
│   ├── css
|        ├── style.css
│   ├── js
|        ├── script.js
|
├── Trail
│   ├── Restaurant_Task-1_
|
├── templates
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── visualization.html
├── app.py
├── requirements.txt
├── LICENSE
├── README.md                                 # Project documentation
```

---

## 🤷 How It Works

### Backend Flow

1. **Data Loading**: Reads and processes the dataset.
2. **Feature Engineering**: Selects key features affecting restaurant ratings.
3. **Model Training**: Trains **Linear Regression, Decision Tree, and Random Forest** models.
4. **Model Evaluation**: Compares performance using MAE and R² score.
5. **Prediction**: Provides estimated ratings for new restaurants based on user input.

### Frontend Flow

- Users interact with the **Jupyter Notebook UI** to process data.
- Visualizations help in **understanding trends and patterns**.
- Users can enter restaurant details and receive **real-time predictions**.

---

## 🤖 Technologies Used

- **Python**: Programming language for data processing and ML.
- **Pandas & NumPy**: Data preprocessing and manipulation.
- **Scikit-Learn**: ML models for predictions.
- **Matplotlib & Seaborn**: Data visualization tools.
- **Jupyter Notebook**: Interactive development environment.

---

## 🚚 Deployment

This project can be deployed using **Flask API, FastAPI, or Streamlit** for a web-based UI.

---

## 🔜 Future Improvements

1. Add a **real-time API** for online predictions.
2. Integrate a **restaurant recommendation system**.
3. Implement **deep learning models** for improved accuracy.

---

## ✍️ Author  
[Ronak Bansal](https://github.com/Ronak1231)

---

## 🙌 Contributing  
1. **Fork** the repository  
2. **Create a new branch** (`git checkout -b feature-branch`)  
3. **Commit your changes** (`git commit -m "Added new feature"`)  
4. **Push to the branch** (`git push origin feature-branch`)  
5. **Create a Pull Request**  

---

## 📜 License

This project is licensed under the **MIT License** - see the `LICENSE` file for details.

---

## 🐛 Troubleshooting  
If you encounter issues, create an issue in this repository.

---

## 📧 Contact  
For inquiries or support, contact **ronakbansal12345@gmail.com**.

---

🚀 **Feel free to ⭐ this repository if you find it useful!**  
