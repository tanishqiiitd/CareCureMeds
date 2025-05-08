# 💊 CareCureMeds
  
CareCureMeds is a smart hospital recommendation web app that guides you to the best medical facility based on your **symptoms**, **location**, and **urgency level**.

---

## 🩺 About the Project

**CareCureMeds** bridges the gap between your health symptoms and the most appropriate hospital using:

- ✅ **ML-powered disease prediction** (Random Forest Classifier with over 90% accuracy)
- 📍 A **customized shortest path algorithm** that factors in:
  - Distance from your location
  - ⭐ Hospital ratings
  - 🚨 Emergency readiness

Currently, the platform supports hospital data across the **United States**, sourced from **Kaggle** and official **government datasets**.

---

## 🔍 Key Features

- **🧠 Symptom-Based Diagnosis**  
  Enter your symptoms — our trained ML model predicts the most probable disease.

- **📍 Smart Hospital Recommendation**  
  Get nearby hospital options based on a hybrid scoring system:
  - Distance
  - Quality Rating
  - Emergency Availability

- **🌐 Real-Time Location Input**  
  Search results are tailored to your address using geolocation.

- **🖥️ User-Friendly Interface**  
  A simple, clean interface designed for accessibility and quick results.

---

## 🧠 Tech Stack

- **Frontend:** HTML, CSS, JavaScript  
- **Backend:** Python (Flask or Django)  
- **ML Model:** Scikit-learn Random Forest Classifier  
- **Mapping:** Geopy, Google Maps API  
- **Pathfinding:** Modified Weighted Shortest Path Algorithm  
- **Dataset:** U.S. hospital and healthcare data from Kaggle + Government APIs

---


