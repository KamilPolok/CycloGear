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
## CREATE EXECUTABLE
- Run from repository base directory:

    ```shell
        mkdir -p appexe && cd appexe && flet pack ../app/main.py --name dbsample --add-data "../app/lozyska_kulkowe.csv;." && cd ..
    ```
  The path to executable will be: ```appexe/dist/dbsample.exe```

## EXECUTABLE
Executable can be also found in compressed form: ```dbsample.zip```. Just unzip it and find ```dbsample.exe```