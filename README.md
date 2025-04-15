# Multi-Modal Emergency Response & Incident Analysis Systems
# Women & Child Safety - Tensor Titans

# Demo ->>>  https://www.youtube.com/watch?v=mpyxZMKK5W4

A comprehensive project suite that leverages computer vision and machine learning to enhance emergency response and incident management. This repository integrates diverse systems—from gesture-based alerts and facial recognition for missing persons to violence detection and incident severity prediction—enabling rapid decision-making in high-pressure situations.

---

## Table of Contents

- [Overview](#overview)
- [Project Descriptions](#project-descriptions)
  - [1. Hand Gesture Recognition Emergency Alert System](#1-hand-gesture-recognition-emergency-alert-system)
  - [2. Facial Recognition for Missing Person Identification](#2-facial-recognition-for-missing-person-identification)
  - [3. Violence Detection System Using YOLO11s-Pose and XGBoost](#3-violence-detection-system-using-yolo11s-pose-and-xgboost)
  - [4. Incident Severity Prediction Model](#4-incident-severity-prediction-model)
- [Research & Motivation](#research--motivation)
- [Datasets & Metrics](#datasets--metrics)
- [Results & Visualizations](#results--visualizations)
- [Future Work](#future-work)
- [Conclusion](#conclusion)
- [Contact](#contact)

---

## Overview

This repository encompasses several cutting-edge projects designed to improve emergency management by automating the detection and analysis of critical events. By combining state-of-the-art computer vision techniques, natural language processing, and machine learning, these projects provide robust, real-time systems for enhancing public safety and streamlining emergency response strategies.

---

## Project Descriptions

### 1. Hand Gesture Recognition Emergency Alert System

- **Objective:**  
  Enable users to trigger emergency alerts through intuitive hand gestures, significantly aiding individuals with mobility challenges.

- **Methodology:**  
  Utilizes a deep learning model that classifies hand gestures into five categories. The system processes video frames in real time using OpenCV, generating a confusion matrix and classification report.  
  **Key Performance Metrics:**  
  - **Accuracy:** 93%
  - **Precision:** 83% to 100%
  - **Recall:** 86% to 98%
  - **Dataset:** 1440 sample images

- **Impact:**  
  Provides an accessible emergency alert mechanism, reducing reliance on traditional input devices and enabling rapid alerts during emergencies.

---

### 2. Facial Recognition for Missing Person Identification

- **Objective:**  
  Implement a facial recognition system for real-time identification of missing persons, which supports prompt intervention by authorities.

- **Methodology:**  
  Employs OpenCV and face recognition libraries to detect and encode facial features. The system compares captured encodings with a stored target using a 0.6 similarity threshold, processing every alternate frame to balance efficiency with detection accuracy.  
  **Key Features:**  
  - **Real-Time Processing**
  - **Multi-threaded Email Alerts** upon positive detection

- **Impact:**  
  Enhances search operations and supports law enforcement by providing quick and reliable missing person identification.

---

### 3. Violence Detection System Using YOLO11s-Pose and XGBoost

- **Objective:**  
  Detect violent incidents and suspicious activities on roads to facilitate timely emergency responses.

- **Methodology:**  
  Leverages the YOLO11s-pose model for pose estimation to capture human posture data, coupled with an XGBoost classifier to evaluate the likelihood of violence. The system analyzes every 3rd frame for efficiency and considers predictions with a confidence score above 0.55.  
  **Key Features:**  
  - **Pose Estimation:** Extracts keypoints and bounding boxes for individuals.
  - **Automated Alerts:** Initiates real-time alerts and visual annotations on video frames.
  - **Scalable Detection:** Supports continuous video monitoring with minimal computational overhead.

- **Impact:**  
  Improves public safety by automating the identification of violent incidents and facilitating quick emergency responses.

---

### 4. Incident Severity Prediction Model

- **Objective:**  
  Predict the severity of incidents based on descriptive text, thereby aiding authorities in prioritizing responses effectively.

- **Methodology:**  
  Implements TF-IDF for feature extraction from incident descriptions, followed by a machine learning classifier trained on a self-made dataset of over 10,000 records derived from Indian crime history.  
  **Key Features:**  
  - **Advanced NLP Techniques:** TF-IDF and ML algorithms to evaluate textual data.
  - **Comprehensive Dataset:** Over 10,000 incident records for robust model training.
  - **Actionable Insights:** Offers severity scores to prioritize emergency responses.

- **Impact:**  
  Assists in resource allocation and emergency planning by providing a reliable, data-driven assessment of incident criticality.

---

## Research & Motivation

The motivation behind these projects stems from the urgent need for innovative solutions in emergency management. By harnessing artificial intelligence, the projects aim to:

- **Reduce Response Times:** Automate critical processes to shorten the gap between incident detection and emergency intervention.
- **Enhance Accessibility:** Provide alternative interaction methods for users with physical constraints through gesture and face recognition technologies.
- **Improve Public Safety:** Utilize real-time video analytics and natural language processing to monitor, assess, and respond to high-risk incidents efficiently.
- **Data-Driven Decision Making:** Leverage self-curated datasets and rigorous performance metrics to train models that provide accurate and actionable insights.

---

## Datasets & Metrics

| Project                                            | Sample Size    | Accuracy/Threshold             | Key Metrics                           |
| -------------------------------------------------- | -------------- | ------------------------------ | ------------------------------------- |
| Hand Gesture Recognition                           | 1440 samples   | Accuracy: 93%                  | Precision: 83–100%, Recall: 86–98%      |
| Facial Recognition for Missing Person Identification | N/A          | Face match threshold: 0.6      | Real-time processing; alternate frames|
| Violence Detection                                 | N/A            | Confidence threshold: >0.55    | YOLO11s-pose keypoints; frame-skipping  |
| Incident Severity Prediction                       | 10,000+ records| Data-driven model              | TF-IDF based feature extraction       |

---

## Results & Visualizations

- **Performance Graphs:**  
  Detailed graphs displaying confusion matrices, ROC curves, and precision-recall plots are provided in the repository's `visuals/` directory.

- **Data Tables:**  
  Tabulated results summarizing accuracy, precision, recall, and support for various classes give insight into model performance.

- **Real-Time Demonstrations:**  
  Video demonstrations of the emergency systems in action illustrate the effectiveness of the real-time detection and alert mechanisms.

---

## Future Work

- **Model Integration:**  
  Explore the unification of all modules into a centralized dashboard to provide a comprehensive view of emergency situations.

- **Enhanced Optimization:**  
  Further optimize real-time processing through algorithmic improvements and hardware acceleration.

- **Data Expansion:**  
  Augment the incident severity dataset with more diverse and up-to-date records, enhancing model robustness.

- **User Experience:**  
  Develop an intuitive, user-friendly interface for first responders and emergency personnel.

---

## Conclusion

This repository demonstrates the practical application of advanced AI techniques in addressing real-world challenges related to emergency and incident management. By combining computer vision, machine learning, and natural language processing, the projects offer scalable, efficient, and highly accurate systems that can significantly enhance public safety and streamline emergency response efforts.

---

## Contact

For more information or to contribute to this project, please contact:

- **Name:** [Your Name]
- **Email:** [Your Email Address]
- **LinkedIn:** [Your LinkedIn Profile URL]

Contributions, feedback, and suggestions are highly appreciated as we continue to refine and expand these systems for improved public safety.

---

*This work is part of ongoing research and innovation in emergency management technologies. All models and datasets are custom-developed with a focus on applicability, accuracy, and real-time performance.*
