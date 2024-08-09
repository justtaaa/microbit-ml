from microbit import *
import random

# Function to collect data for a specific gesture
def collect_data(label, num_samples=100):
    data = []
    
    # Countdown to give the user time to prepare
    for i in range(3, 0, -1):
        display.scroll(str(i))
        sleep(1000)
    
    display.scroll("Go")
    
    for _ in range(num_samples):
        x = accelerometer.get_x()
        y = accelerometer.get_y()
        z = accelerometer.get_z()
        data.append((x, y, z, label))
        sleep(500)
    
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

# Function to calculate accuracy using a validation set
def calculate_accuracy(validation_data, datasets):
    correct_predictions = 0
    total_predictions = len(validation_data)
    
    for sample in validation_data:
        x, y, z, actual_label = sample
        predicted_label = classify_gesture(x, y, z, datasets)
        if predicted_label == actual_label:
            correct_predictions += 1
    
    accuracy = (correct_predictions / total_predictions) * 100
    return accuracy

# Function to split data into training and validation sets
def split_data(data, validation_ratio=0.2):
    split_index = int(len(data) * (1 - validation_ratio))
    training_data = data[:split_index]
    validation_data = data[split_index:]
    return training_data, validation_data

# Initialize datasets
datasets = []
validation_data = []

# Main loop for data collection and real-time gesture recognition
while True:
    if button_a.is_pressed():
        raw_data = collect_data(0)
        training_data, validation_data_part = split_data(raw_data)
        datasets.append({'label': 0, 'samples': training_data})
        validation_data.extend(validation_data_part)  # Collect data for validation

    if button_b.is_pressed():
        raw_data = collect_data(1)
        training_data, validation_data_part = split_data(raw_data)
        datasets.append({'label': 1, 'samples': training_data})
        validation_data.extend(validation_data_part)  # Collect data for validation

    if pin_logo.is_touched():
        raw_data = collect_data(2)
        training_data, validation_data_part = split_data(raw_data)
        datasets.append({'label': 2, 'samples': training_data})
        validation_data.extend(validation_data_part)  # Collect data for validation

    if pin0.is_touched():
        # Print collected data to serial for inspection
        for dataset in datasets:
            label = dataset['label']
            for sample in dataset['samples']:
                print(','.join(map(str, sample)))

        # Calculate accuracy using the validation data
        accuracy = calculate_accuracy(validation_data, datasets)
        
        # Display accuracy on the screen
        display.scroll("Acc: {:.2f}%".format(accuracy))
        
        # Print accuracy to serial
        print("Accuracy: {:.2f}%".format(accuracy))

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

