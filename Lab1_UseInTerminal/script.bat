ECHO OFF

IF "%1"=="" GOTO USAGE

"C:/Program Files/Blender Foundation/Blender 3.2/blender.exe" -b -P %1
GOTO END

:USAGE
ECHO script.bat [SCRIPT.py]

:END
