from django.shortcuts import render
from .energy_lstm import LSTMModel
import torch
from .models import PowerUsageData, PredictionResult
import numpy as np



class TimeSequenceModel:
    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    def load_model(self, model_path):
        model = LSTMModel(LSTMModel.input_size, LSTMModel.hidden_size, LSTMModel.num_layers) 
        model.load_state_dict(torch.load(model_path))
        model.eval()
        return model

    def predict(self, num_steps, past_data):
        self.model.eval()
        predictions = []
        # Prepare the input data
        input_data = torch.tensor(past_data.reshape(1, -1, 1), dtype=torch.float32)
        
        with torch.no_grad():
            for _ in range(num_steps):
                # Predict the next value
                next_value = self.model(input_data)
                
                # Collect the predicted value
                predictions.append(next_value.squeeze().item())
                
                # Update input_data to include the new prediction
                next_value = next_value.unsqueeze(0)  # Add batch dimension
                next_value = next_value[:, -1:, :]    # Keep the last prediction
                
                # Update input_data by shifting and appending the new prediction
                input_data = torch.cat([input_data[:, 1:, :], next_value], dim=1)

        return predictions
    
def predict_power_usage(request):
    # Load the model
    model = TimeSequenceModel(r'/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth')

    # Get the latest power usage data
    recent_data = PowerUsageData.objects.order_by('-timestamp')[:10]
    input_sequence = [data.power_usage for data in recent_data][::-1]

    # Make a prediction
    predicted_usage = model.predict(3, (np.array([8.36, 6.56, 4.19, 3.98, 7.97, 8.21, 8.49, 8.51, 8.50, 8.77, 8.81, 8.67, 8.86, 8.90, 8.91], dtype=np.float32)))

    # Save the prediction to the database
    prediction = PredictionResult(predicted_usage=str(predicted_usage))
    prediction.save()

    context = {
        'recent_data': recent_data,
        'predicted_usage': predicted_usage,
    }
    return render(request, 'predictions/predict.html', context)


