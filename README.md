# CycloGear

This application is intended to support the design of the input mechanism for cycloidal drive. It helps with strength calculations, structural optimization and modeling of the input shaft and also enables the selection of appropriate bearings mounted on it. Furthermore, it helps identify power loss occurring in the designed mechanism.

## Caveats

- The application focuses solely on providing design support only for the input mechanism. In the process of determining its mathematical model and calculating the power loss, data and insights from the design phases of other mechanisms of the cycloidal gear were used. However, the details regarding how this data was derived are not included in this project.

- The application has been tested and verified to work on Windows 10 and 11. Its compatibility with other Windows versions or operating systems is currently unknown. The software is still in a gamma stage, meaning it is stable but lacks full functionality. It was primarily developed for demonstration purposes, with the main goal of integrating the code into a larger project that is still in its early development stages.

- Currently, the only available language for the app is Polish.

## Setup copy of this repository 
Download/Clone this repository and install dependencies from [requirements.txt](requirements.txt) (preferably use a virtual environment). If you use ```pip```, you can use:

```ps1
pip install -r requirements.txt
```
## Run the code
To run the code, type in the comand prompt:

```ps1
python app/main.py
```

## Build the app
From repository root run:

```ps1
pyinstaller --name 'CycloGear2024' --icon ..\..\data\icons\app_icon.ico --noconsole --distpath .\build\dist --specpath .\build\spec .\app\main.py ; Copy-Item -Path ".\data" -Destination ".\build\dist\CycloGear2024\data" -Recurse
```

## COPYING
[GNU GPL License](COPYING)
