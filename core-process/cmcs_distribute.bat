pyinstaller ^
	--distpath .\distribution ^
	--workpath .\distribution ^
	--exclude-module jupyterlab ^
	--exclude-module matplotlib ^
    --exclude-module scipy ^
    --exclude-module PIL ^
    --exclude-module PyQt4 ^
    --exclude-module PyQt5 ^
    --exclude-module sqlite3 ^
    --exclude-module beautifulsoup4 ^
	--name CMCScan --add-data "cmcs_icon.ico;." --icon=cmcs_icon.ico ^
	--onefile cmcs_gui.py
pause