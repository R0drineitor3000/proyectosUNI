@echo off
chcp 65001 >nul
SETLOCAL ENABLEDELAYEDEXPANSION

REM Verifica que pip esté disponible
pip --version >nul 2>&1
IF ERRORLEVEL 1 (
    ECHO Pip no está disponible. Asegúrate de tener Python correctamente instalado.
    PAUSE
    EXIT /B
)

REM Iterar sobre cada línea en el archivo de requerimientos
FOR /F "usebackq tokens=*" %%L IN ("utils\libreries.required") DO (
    ECHO Verificando si %%L está instalado...
    pip show %%L >nul 2>&1
    IF !ERRORLEVEL! EQU 0 (
        ECHO %%L ya está instalado.
    ) ELSE (
        ECHO %%L no está instalado. Instalando...
        pip install %%L
    )
    ECHO -----------------------------
)

REM Ejecutar la aplicación
ECHO Encendiendo servidor...
timeout /t 5 /nobreak >nul
ECHO Ejecutando aplicación...
python app.py

PAUSE
