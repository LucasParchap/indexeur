@echo off
setlocal
cd /d "%~dp0"

echo ================================
echo  Creation de MessageSecret.exe
echo ================================

echo.
python --version >nul 2>&1
if errorlevel 1 (
  echo Python n'est pas installe sur CE PC.
  echo Installe Python depuis python.org puis relance ce fichier.
  pause
  exit /b 1
)

echo Installation / mise a jour de PyInstaller...
python -m pip install --upgrade pyinstaller
if errorlevel 1 goto :error

echo.
echo Creation de l'executable...
python -m PyInstaller --noconfirm --clean --onefile --windowed --name MessageSecret message_secret.py
if errorlevel 1 goto :error

echo.
echo Termine !
echo Ton fichier est ici :
echo %~dp0dist\MessageSecret.exe
explorer "%~dp0dist"
pause
exit /b 0

:error
echo.
echo Une erreur est survenue pendant la creation.
pause
exit /b 1
