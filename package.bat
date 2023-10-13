@echo off
nuitka --mingw64 --standalone --onefile --windows-icon-from-ico=furau.ico --output-filename=DeepOne.exe do_main.py