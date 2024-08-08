from microbit import *
import random

# Function to collect data for a specific gesture
def collect_data(label):
    data = []
    display.scroll("Go")
    for _ in range(50):  # Collect 50 samples
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        data.append((x, y, z, label))
        sleep(100)
    display.scroll("Done")
    return data

# Function to classify gestures based on accelerometer data
def classify_gesture(x, y, z, datasets):
    min_distance = float('inf')
    predicted_label = -1
    
    for data in datasets:
        for sample in data['samples']:
            distance = ((sample[0] - x) ** 2 + (sample[1] - y) ** 2 + (sample[2] - z) ** 2) ** 0.5
            if distance < min_distance:
                min_distance = distance
                predicted_label = data['label']
    
    return predicted_label

# Function to calculate accuracy
def calculate_accuracy(test_data, datasets):
    correct_predictions = 0
    total_predictions = len(test_data)
    
    for sample in test_data:
        x, y, z, actual_label = sample
        predicted_label = classify_gesture(x, y, z, datasets)
        if predicted_label == actual_label:
            correct_predictions += 1
    
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy

# Initialize datasets
datasets = []
test_data = []

# Main loop for data collection and real-time gesture recognition
while True:
    if button_a.is_pressed():
        datasets.append({'label': 0, 'samples': collect_data(0)})  # Collect data for Shake
    if button_b.is_pressed():
        datasets.append({'label': 1, 'samples': collect_data(1)})  # Collect data for Tilt
    if pin_logo.is_touched():
        datasets.append({'label': 2, 'samples': collect_data(2)})  # Collect data for Freefall
    
    if pin0.is_touched():
        # Collect test data (for simplicity, using the same method)
        test_data = collect_data(0) + collect_data(1) + collect_data(2)  # Collect test data for all gestures
        
        # Calculate accuracy
        accuracy = calculate_accuracy(test_data, datasets)
        print("Accuracy: {:.2f}%".format(accuracy))
        
        # Print collected data to serial for inspection
        for dataset in datasets:
            label = dataset['label']
            for sample in dataset['samples']:
                print(','.join(map(str, sample)))
        break

    # Real-time gesture recognition
    x = accelerometer.get_x()
    y = accelerometer.get_y()
    z = accelerometer.get_z()
    
    gesture = classify_gesture(x, y, z, datasets)
    
    if gesture == 0:
        display.show(Image.SQUARE)
        print("Gesture: Shake")
    elif gesture == 1:
        display.show(Image.ARROW_N)
        print("Gesture: Tilt")
    elif gesture == 2:
        display.show(Image.SKULL)
        print("Gesture: Freefall")
    else:
        display.show(Image.CONFUSED)
        print("Gesture: Unknown")
    
    sleep(1000)  # Wait for 1 second
    display.clear()
