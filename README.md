# interfaz-link
Interfaz Link Python app

#DEV

- Python virtualenvironment


    python3 -m venv venv
    source venv/bin/activate
    
- PyQt5, PySerial

    
    pip install PyQt5
    pip install PySerial    

    
- pyinstaller


    pip install pyinstaller    
    pyinstaller interfaz-link.spec
    
    
#DEPLOY WIN64 

    wget https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe  
    wine python-3.8.5-amd64.exe  
    cd ~/.wine/drive_c/Python38/  
    wine python.exe Scripts/pip.exe install pyqt5  
    wine python.exe Scripts/pip.exe install pyserial       
    wine python.exe Scripts/pip.exe install pyinstaller  
    wine ~/.wine/drive_c/Python38/Scripts/pyinstaller.exe interfaz-link.spec     
