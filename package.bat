@echo off
nuitka --mingw64 --standalone --onefile --include-data-file=libmpg123-0.dll=libmpg123-0.dll --windows-icon-from-ico=furau.ico --output-filename=DeepOne.exe do_main.py