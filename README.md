# DATABASE SAMPLE

## SETUP
- Download this repository
- Create your own virtual environment (use venv that is already included with Python 3.3):
    - Go to repository base directory and run:

        ```shell
        python -m venv <your_virtual_environment_name>
        ```
    - Activate your virtul environment:
        - using bash:

            ```shell
            source my_venv/Scripts/activate
            ```
        - using PowerShell:
            ```shell
            my_venv\Scripts\activate
            ```
- Install required tools:

    ```shell
    pip install -r requirements.txt
    ```
## RUN
- You can run the sample with python:

    ```shell
    python app/main.py
    ```
  or using flet - that enables also Hot Reload

    ```shell
    flet app/main.py
    ```
## BUILD EXECUTABLE

### FOR WINDOWS
- From repository root run:

   ```shell
    pyinstaller --name 'CycloGear2024' --noconsole --distpath .\build\dist --specpath .\build\spec .\app\main.py ; Copy-Item -Path ".\data" -Destination ".\build\dist\CycloGear2024\data" -Recurse
   ```
- Copy 'data' folder to build 

## EXECUTABLE
Executable can be also found in compressed form: ```dbsample.zip```. Just unzip it and find ```dbsample.exe```