# File: predict.py
import pickle

def load_model_and_vectorizer():
    with open("incident_severity_model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
    with open("tfidf_vectorizer.pkl", "rb") as vec_file:
        vectorizer = pickle.load(vec_file)
    return model, vectorizer

def predict_severity(description):
    model, vectorizer = load_model_and_vectorizer()
    description_tfidf = vectorizer.transform([description])
    prediction = model.predict(description_tfidf)
    return prediction[0]

if __name__ == "__main__":
    # Example incident description:
    new_description = "A working woman faced molestation near a railway station in Mumbai.."
    predicted_severity = predict_severity(new_description)
    print(f"Predicted Severity for the incident: {predicted_severity}")
