# ![image info](.github/assets/app_logo.png)

## About

This application is developed in cooperation and with the substantive support of the Mechanical Department of Wrocław University of Science and Technology. Its purpose is to assist in the design of the input mechanism for cycloidal drives. It facilitates strength calculations, structural optimization and modeling of the input shaft, and also enables the selection of appropriate bearings mounted on it. Additionally, it helps identify power losses occurring in the designed mechanism.

![Example GIF](.github/assets/app_demo.gif)

## Caveats

- The application focuses solely on providing design support only for the input mechanism. In the process of determining its mathematical model and calculating the power loss, data and insights from the design phases of other mechanisms of the cycloidal gear were used. However, the details regarding how this data was derived are not included in this project.

- The application has been tested and verified to work on Windows 10 and 11. Its compatibility with other Windows versions or operating systems is currently unknown. The software is still in a gamma stage, meaning it is stable but lacks full functionality. It was primarily developed for demonstration purposes, with the main goal of integrating the code into a larger project that is still in its early development stages.

- Currently, the only available language for the app is Polish.

## Setup copy of this repository

Download/Clone this repository and install dependencies from [requirements.txt](requirements.txt) (preferably use a virtual environment). If you use ```pip```, you can use:

```pip
pip install -r requirements.txt
```

## Run the code

To run the code, type in the comand prompt:

```python
python app/main.py
```

## Build the app

From repository root run [build_app.py](build_app.py):

```python
python build_app.py
```

## Copying

[GNU GPL License](COPYING)
