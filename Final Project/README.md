# Smart Home IoT System

This project implements an end-to-end IoT solution using MQTT protocol for a smart home temperature monitoring system. The system consists of publishers that send temperature data and subscribers that receive and visualize the data (like people in a house that as subscribers want to know the temperature from different locations (publishers)). Therefore, the system includes a broker, publishers, and subscribers. In summary, about the process, the publisher sends data to the broker and the subscriber receives the data from the broker. The subscriber can also visualize the data in a chart. The publisher is a GUI-based publisher that allows the user to manually generate data or automatically generate data. The subscriber is a GUI-based subscriber that allows the user to visualize the data.


## Components

### Broker
- Uses the Eclipse Mosquitto MQTT broker
- Is configured to use the public test server at `test.mosquitto.org`

### Publishers
- `group_4_publisher_gui.py`: GUI-based publisher for manual and automatic data generation for a single sensor
- `group_4_publisher.py`: Multi-publisher implementation that runs multiple data sources for multiple sensors (three publishers with different configurations as defined in its main() function).
- `group_4_lab6_data_generator.py`: Temperature data generator with realistic patterns
- `group_4_thread_manager.py`: Thread management for MQTT publishing with random transmission skipping

### Subscribers
- `group_4_subscriber_gui.py`: GUI-based subscriber with data visualization
- `group_4_multi_subscriber.py`: Manager for running multiple subscriber instances
- Also it has chart that visualizes the temperature data and detects missing/erroneous values

### System Launcher
- `group_4_main_launcher.py`: Central launcher for the entire system

## Features

- GUI interfaces for all components
- Real-time temperature data visualization
- Detection of missing transmissions
- Handling of out-of-range data
- Support for multiple publishers and subscribers
- Random transmission skipping (1 in very 100 transmissions)


## Requirements

- Python 3.6.5 or later
- Required Python packages:
  - paho-mqtt
  - matplotlib
  - tkinter

## To create a virtual environment

```
python -m venv venv
source venv/bin/activate
```

## To install the required packages
```
pip install -r requirements.txt
```

## To install the required packages individually in the virtual environment

1. Install the required packages:
   ```
   pip install paho-mqtt matplotlib
   ```

2. Run the main launcher:
   ```
   python group_4_main_launcher.py
   ```

3. From the launcher GUI:
   - Launch publisher(s) from the "Publishers" tab
   - Launch subscriber(s) from the "Subscribers" tab

## Alternative Launch Methods

You can run the main launcher:
```
python group_4_main_launcher.py
``` 

Alternatively, you can run each component individually:

- Publishers data generation:
  ```
  python group_4_publisher_gui.py (with GUI)
  or
  python group_4_publisher.py (without GUI)
  ```

- Subscribers data visualization:
  ```
  python group_4_subscriber_gui.py (with GUI)
  or
  python group_4_multi_subscriber.py (without GUI)
  ```

## Project Structure

- `group_4_lab6_data_generator.py`: Temperature data generator

- `group_4_publisher.py`: Multi-publisher implementation with data generation
- `group_4_publisher_gui.py`: GUI publisher with data generation

- `group_4_subscriber.py`: Basic subscriber (command-line only)
- `group_4_subscriber_gui.py`: GUI subscriber with visualization
- `group_4_multi_subscriber.py`: Multi-subscriber manager

- `group_4_thread_manager.py`: Thread management for MQTT publishing
- `group_4_main_launcher.py`: Central system launcher and GUI
- `group_4_util.py`: Utility functions for the project

## Design Decisions

1. **Data Generation**: Uses a combination of random generation methods to create realistic temperature patterns.

2. **Publisher Implementation**: Uses a thread-based approach to simulate multiple devices publishing data.

3. **Subscriber Visualization**: Implements both text and chart-based visualization of temperature data.

4. **Error Handling**: Detects and visualizes missing transmissions and out-of-range data.

5. **System Architecture**: Follows a modular design with separate components for different functions. 

6. **GUI**: Uses tkinter for the GUI components.

7. **Broker**: Uses the Eclipse Mosquitto MQTT broker.

8. **System Architecture**: Follows a modular design with separate components for different functions.