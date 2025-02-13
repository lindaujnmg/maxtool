# MaxTool

MaxTool is a Python program that allows for dynamic control of audio volumes across various applications on Windows. 

## Features

- Adjust the audio volume for the default audio playback device.
- Increase or decrease the volume in customizable increments.

## Prerequisites

- Windows operating system.
- Python 3.x installed on your system.

## Installation

1. Clone the repository or download the `max_tool.py` file.
2. Ensure that Python is installed on your system and available in your PATH.

## Usage

Open a terminal or command prompt and navigate to the directory containing `max_tool.py`. Use the following command:

```bash
python max_tool.py [up|down]
```

- `up`: Increase the volume by the predefined increment (default is 5%).
- `down`: Decrease the volume by the predefined increment (default is 5%).

Example:

```bash
python max_tool.py up
```

## License

This project is licensed under the MIT License.
```

Note: The above code attempts to use the Windows API to interact with audio devices, which is a complex task that typically requires more robust error handling and setup than provided here. The code is illustrative and may not work out-of-the-box without additional configuration and debugging on a Windows system.