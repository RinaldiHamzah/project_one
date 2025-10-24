import joblib
from sklearn.feature_extraction.text import TfidfVectorizer


class ModelPredict:
    def __init__(self):
        self.__naive_bayes_loaded = joblib.load('model_ml/naive_bayes_model.pkl')
        self.__svm_loaded = joblib.load('model_ml/SVM_model.pkl')
        self.__vectorizer = joblib.load('model_ml/vectorizer.pkl')

    def __vectorizer_text(self, text):
        return self.__vectorizer.transform([text])
    
    def __sentiments_text(self, predicted_val):
        if predicted_val[0] == 1:
            return "POSITIF"
        else:
            return "NEGATIF"

    def model_predict_nvm(self, text):
        temp_vec = self.__vectorizer_text(text)
        return self.__sentiments_text(self.__naive_bayes_loaded.predict(temp_vec))
    
    def model_predict_svm(self, text):
        temp_vec = self.__vectorizer_text(text)
        return self.__sentiments_text(self.__svm_loaded.predict(temp_vec))
    




    
