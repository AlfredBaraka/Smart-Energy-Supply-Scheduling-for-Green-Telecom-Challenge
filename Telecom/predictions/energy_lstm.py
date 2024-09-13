import torch.nn as nn
import torch



class LSTMModel(nn.Module):
    # Parameters
    input_size = 1  # Number of features
    hidden_size = 50
    num_layers = 2


    def __init__(self, input_size, hidden_size, num_layers):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, num_layers, batch_first=True)
        self.fc = nn.Linear(hidden_size, 1)
        self.hidden_size = hidden_size

    def forward(self, x):
        # Initialize hidden states with correct batch size
        h0 = torch.zeros(self.lstm.num_layers, x.size(0), self.hidden_size)
        c0 = torch.zeros(self.lstm.num_layers, x.size(0), self.hidden_size)
        
        # Forward pass
        out, _ = self.lstm(x, (h0, c0))
        out = self.fc(out[:, -1, :])
        return out


