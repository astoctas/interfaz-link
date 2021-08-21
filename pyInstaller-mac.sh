# en M1 correr en Rosetta
sh update-pyInterfaz.sh
pip freeze --exclude pyInterfaz > requirements.txt
/usr/bin/arch -x86_64 pyinstaller interfaz-link.spec