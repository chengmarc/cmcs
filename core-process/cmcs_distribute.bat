pyinstaller ^
	--distpath .\distribution ^
	--workpath .\distribution ^
	--name CMCScan --add-data "cmcs_icon.ico;." --icon=cmcs_icon.ico ^
	--onefile --noconsole cmcs_gui.py
pause