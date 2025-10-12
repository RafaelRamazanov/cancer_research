import joblib
import shap

class Classifier:
    def __init__(self):
        self.model = joblib.load('model_cancer_calibrated.pkl')

    def predict(self, data):
        return self.model.predict_proba(data)

    def explain(self, data):
        explainer = shap.TreeExplainer(self.model)
        shap_values = explainer.shap_values(data)
        return shap.plots.force(shap_values[0, ...])



    # Убрать сотые везде кроме опса и объема подозрительных участков
    # сделать галочку у наличия рака простаты,данные при
    # линейка в pi-rads
    # калибровка модели