10/15/24
This is the AbaloneGUI project. An interface with the JLAB BML 2 Clear device. Currently, the GUI can send commands over BLE and translate magnetometer to displacement within a 0.1 meter range. This range will likely improve with calibration and tinkering.

Start the program by running multi_thread.py 

General Requirements:
Windows 10-11 or above
Python 12
MATLAB 2024b
matlab.engine
all installations from requirements.txt


Powershell Notes:
- Activate venv
    - check what venv on:
        echo $env:VIRTUAL_ENV
    - activate powershell venv when in directory
        .\venv\Scripts\Activate.ps1\

- Installing matlab.engine with R2024b and Python 12
    - make sure you start powershell in administrator
    - go to the C:\Program Files\MATALAB\extern\engine\python
    - run the pip installer when you're on the venv you want
        pip install .
    - ensure that the MATLAB directory in this AbaloneGUI folder is added to the MATLAB directory. Otherwise MATLAB will not know where to find the functions.

# testing magnetometer 2d notes
- note that maybe having the magnet near it at the beginning throws off calibration
- apparently the magnetometer only works at certain higher frequencies though not sure why

ESP32 NOTES
Mac Address: 10:52:1c:66:7e:92
