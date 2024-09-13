
import torch
import numpy as np
from .energy_lstm import LSTMModel

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
