docker run -v "$(pwd):/src/" --entrypoint /bin/sh cdrx/pyinstaller-windows:python3-32bit -c "pip install flask flask-socketio pyqt5 pyfirmata pyinterfaz && /entrypoint.sh"
