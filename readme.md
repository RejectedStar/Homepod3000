# DIY Alexa with ESP32 and Wit.ai

Welcome to the DIY Alexa project! This guide will walk you through the process of building your own Alexa-like voice assistant using the ESP32 microcontroller and Wit.ai for speech recognition. By the end of this project, you will have a fully functional voice assistant capable of recognizing voice commands and executing tasks.

## Table of Contents

1. [Introduction](#introduction)
2. [Prerequisites](#prerequisites)
3. [Hardware Requirements](#hardware-requirements)
4. [Software Requirements](#software-requirements)
5. [Getting Started](#getting-started)
6. [Project Structure](#project-structure)
7. [Wake Word Detection](#wake-word-detection)
   - [Training the Model](#training-the-model)
   - [Converting the Model to TensorFlow Lite](#converting-the-model-to-tensorflow-lite)
8. [Audio Capture and Processing](#audio-capture-and-processing)
   - [Microphone Setup](#microphone-setup)
   - [Audio Processing](#audio-processing)
9. [Speech Recognition with Wit.ai](#speech-recognition-with-witai)
   - [Setting Up Wit.ai](#setting-up-witai)
   - [Integrating with ESP32](#integrating-with-esp32)
10. [Intent Recognition](#intent-recognition)
   - [Understanding Intents and Entities](#understanding-intents-and-entities)
   - [Handling Commands](#handling-commands)
11. [Building and Flashing the Firmware](#building-and-flashing-the-firmware)
   - [Compiling the Code](#compiling-the-code)
   - [Uploading to ESP32](#uploading-to-esp32)
12. [Testing and Debugging](#testing-and-debugging)
   - [Common Issues](#common-issues)
   - [Troubleshooting](#troubleshooting)
13. [Extending the Project](#extending-the-project)
   - [Adding New Commands](#adding-new-commands)
   - [Integrating with IoT Devices](#integrating-with-iot-devices)
14. [Contributing](#contributing)
15. [License](#license)
16. [Support](#support)
17. [Acknowledgments](#acknowledgments)

---

## Introduction

This project aims to create a DIY Alexa using the ESP32 microcontroller and Wit.ai for natural language processing. The assistant will detect a wake word, process spoken commands, and execute the corresponding actions. The project is modular, making it easy to extend and integrate with other systems.

---

## Prerequisites

Before starting, ensure you have the following:

- Basic knowledge of electronics and microcontrollers
- Familiarity with Python and C++ programming
- Installed software: [Visual Studio Code](https://code.visualstudio.com/), [PlatformIO](https://platformio.org/), [Python 3+](https://www.python.org/downloads/)

---

## Hardware Requirements

To build this project, you will need the following hardware components:

1. **ESP32 Dev Kit**: A powerful microcontroller with built-in Wi-Fi and Bluetooth.
2. **I2S MEMS Microphone**: Preferably the INMP441 or ICS-43434 for capturing audio.
3. **Speaker and Amplifier**: For audio output, use a 4Ω or 8Ω speaker with an I2S amplifier.
4. **Breadboard and Jumper Wires**: For prototyping and connecting components.
5. **Power Supply**: 5V USB power supply or equivalent.

### Optional Components

- **LEDs and Resistors**: For visual feedback.
- **Buttons**: For manual interaction.
- **Enclosure**: To house your project.

---

## Software Requirements

You will need the following software tools:

1. **PlatformIO**: An IDE extension for Visual Studio Code, tailored for embedded systems.
2. **TensorFlow**: For machine learning and wake word detection.
3. **Wit.ai Account**: To set up and manage speech recognition.
4. **ESP-IDF**: The official development framework for ESP32.

### Libraries

Ensure the following libraries are installed in your PlatformIO environment:

- `ArduinoJson`
- `ESPAsyncWebServer`
- `AsyncTCP`
- `TensorFlowLite`

---

## Getting Started

### Cloning the Repository

Start by cloning the project repository:

```bash
git clone https://github.com/yourusername/diy-alexa.git
cd diy-alexa
```

### Setting Up the Environment

Open the project in Visual Studio Code:

```bash
code .
```

Install the necessary PlatformIO extensions and libraries:

```bash
pio init --board esp32dev
pio lib install
```

---

## Project Structure

The project is organized into the following directories:

```plaintext
diy-alexa/
│
├── firmware/               # ESP32 firmware source code
│   ├── src/
│   ├── include/
│   ├── lib/
│   ├── platformio.ini      # PlatformIO configuration file
│
├── model/                  # Machine learning models and scripts
│   ├── data/
│   ├── notebooks/
│   ├── trained_model.tflite
│
├── hardware/               # Schematics and hardware setup guides
│
├── README.md               # Project documentation
└── LICENSE                 # License information
```

---

## Wake Word Detection

### Training the Model

The wake word detection model listens for a specific keyword (e.g., "Marvin"). We use TensorFlow to train this model.

#### Data Preparation

Use the [Speech Commands Dataset](https://www.tensorflow.org/datasets/catalog/speech_commands) for training:

1. Download the dataset and place it in the `model/data/` directory.
2. Use the provided Jupyter notebooks in the `model/notebooks/` directory to preprocess the data and generate spectrograms.

#### Model Training

Train the model using the `Train Model.ipynb` notebook:

```python
# Load and preprocess data
# Define and compile the model
# Train and evaluate the model
```

### Converting the Model to TensorFlow Lite

After training, convert the model to TensorFlow Lite format for use on the ESP32:

```python
import tensorflow as tf

converter = tf.lite.TFLiteConverter.from_saved_model('saved_model')
tflite_model = converter.convert()

with open('model/trained_model.tflite', 'wb') as f:
    f.write(tflite_model)
```

---

## Audio Capture and Processing

### Microphone Setup

Connect the I2S MEMS microphone to the ESP32:

```plaintext
ESP32 Pin   |   Microphone Pin
-------------------------------
3.3V        |   VCC
GND         |   GND
DOUT        |   DIN
BCK         |   BCLK
LRC         |   LRCL
```

### Audio Processing

The audio processing pipeline includes:

1. **Capture**: Using the I2S interface to capture raw audio data.
2. **Preprocessing**: Convert the audio data into spectrograms.
3. **Inference**: Feed the spectrograms into the TensorFlow Lite model to detect the wake word.

---

## Speech Recognition with Wit.ai

### Setting Up Wit.ai

1. **Create a Wit.ai Account**: Sign up at [Wit.ai](https://wit.ai/).
2. **Create a New App**: Name your application and configure the languages.
3. **Training**: Provide example phrases and train the app to recognize intents and entities.

### Integrating with ESP32

Use the `WiFiClientSecure` library to send audio data from the ESP32 to Wit.ai:

```cpp
WiFiClientSecure client;
client.connect("api.wit.ai", 443);
client.print("POST /speech HTTP/1.1\r\n");
client.print("Authorization: Bearer YOUR_WITAI_ACCESS_TOKEN\r\n");
client.print("Content-Type: audio/wav\r\n");
client.print("Content-Length: " + String(audioSize) + "\r\n");
client.print("\r\n");
client.write(audioData, audioSize);
```

---

## Intent Recognition

### Understanding Intents and Entities

Intents represent the user's intention (e.g., "Turn on the lights"), while entities are the specific objects being referenced (e.g., "lights").

### Handling Commands

Based on the recognized intent and entities, the ESP32 will execute corresponding actions. For example, turning on a light, controlling a fan, etc.

---

## Building and Flashing the Firmware

### Compiling the Code

To compile the firmware, use PlatformIO:

```bash
pio run
```

### Uploading to ESP32

Flash the firmware to the ESP32:

```bash
pio run --target upload
```

---

## Testing and Debugging

### Common Issues

- **Wake Word Detection Failure**: Check microphone connections and ensure the TensorFlow model is correctly loaded.
- **Wit.ai Integration Issues**: Ensure the correct access token is used and that the device is connected to Wi-Fi.

### Troubleshooting

- **No Audio Output**: Verify speaker connections and amplifier functionality.
- **ESP32 Crashes**: Check power supply stability and ESP32 flash settings.

---

## Extending the Project

### Adding New Commands

To add new voice commands, train the Wit.ai model with additional phrases and update the ESP32 code to handle new intents.

### Integrating with IoT Devices

Expand the

 project by integrating with IoT platforms like MQTT or Home Assistant. This allows for controlling smart home devices directly with your voice assistant.

---

## Contributing

We welcome contributions to this project! If you'd like to contribute, please fork the repository and submit a pull request. Ensure your code follows our coding standards and is well-documented.

### Contribution Guidelines

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Write clear, concise commit messages.
4. Submit a pull request, explaining your changes.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more information.

---

## Support

If you encounter any issues or have questions, please open an issue on GitHub or contact the project maintainers.

---

## Acknowledgments

We'd like to thank the following resources and contributors:

- [TensorFlow](https://www.tensorflow.org/) for their machine learning libraries.
- [Wit.ai](https://wit.ai/) for providing the speech recognition API.
- The open-source community for their contributions and support.

---
