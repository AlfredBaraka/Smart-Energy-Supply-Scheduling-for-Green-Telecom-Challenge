from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from predictions.views import TimeSequenceModel
from datetime import datetime
from datetime import timedelta
import numpy as np
from predictions.models import PowerUsageData, PredictionResult
from datetime import timedelta
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def intro(request):
    return render(request, 'intro.html')

@login_required


def index(request):
    # Load the model
    model = TimeSequenceModel(r'/home/egovridc/Desktop/Smart-Energy-Supply-Scheduling-for-Green-Telecom-Challenge/data/energy_lstm_model_better2.pth')

    # Get the latest power usage data
    recent_data = PowerUsageData.objects.order_by('-timestamp')[:10]

    # Extract the power usage values and convert them to floats, handling any possible None values
    input_sequence = [float(data.power_usage) if data.power_usage is not None else 0.0 for data in recent_data][::-1]

    # Convert the input sequence to a NumPy array and reshape it
    input_sequence = np.array(input_sequence, dtype=np.float32).reshape(1, -1, 1)

    # Make a prediction for the next 3 time steps
    predicted_usage = model.predict(5, input_sequence)

    # Generate future timestamps for the predictions
    last_timestamp = recent_data[0].timestamp if recent_data else timezone.now()
    future_timestamps = [last_timestamp + timedelta(hours=i) for i in range(1, 4)]

    # Save each prediction with its corresponding timestamp to the database
    for timestamp, usage in zip(future_timestamps, predicted_usage):
        prediction = PredictionResult(timestamp=timestamp, predicted_usage=usage)
        prediction.save()

    # Generate labels (timestamps) for the graph including dates
    labels = [data.timestamp.strftime('%Y-%m-%d %H:%M') for data in recent_data][::-1]

    context = {
        'recent_data': recent_data,
        'labels': labels + [ts.strftime('%Y-%m-%d %H:%M') for ts in future_timestamps],  # Combine past and future labels
        'data': input_sequence.flatten().tolist() + predicted_usage,  # Combine past data and predictions
    }
    return render(request, 'index.html', context)


@csrf_exempt
def submit_readings(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for entry in data:
                timestamp = entry.get('timestamp')
                power_usage = entry.get('powerUsage')
                if timestamp and power_usage is not None:
                    PowerUsageData.objects.create(
                        timestamp=timestamp,
                        power_usage=power_usage
                    )
            return JsonResponse({'status': 'success'}, status=200)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid method'}, status=405)