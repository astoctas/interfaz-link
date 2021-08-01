sh update-pyInterfaz.sh
pip freeze --exclude pyInterfaz > requirements.txt
docker run -v "$(pwd):/src/" cdrx/pyinstaller-linux:python3
