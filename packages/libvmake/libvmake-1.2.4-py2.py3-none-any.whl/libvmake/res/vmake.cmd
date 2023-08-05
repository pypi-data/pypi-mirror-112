@echo off

CD %~DP0

SET ROOT=%CD%

SETLOCAL EnableDelayedExpansion

@REM FOR /F "tokens=* USEBACKQ" %%F IN (`command`) DO (
@REM SET var=%%F
@REM )
@REM ECHO %var%

python -c "import sys; sys.exit(0 if sys.version_info.major >= 3 else 1)" 1> NUL 2> NUL
IF !errorlevel! == 0 (
    SET syspython=python
) ELSE (
    python3 -c "import sys; sys.exit(0 if sys.version_info.major >= 3 else 1)" 1> NUL 2> NUL
    IF !errorlevel! == 0 (
        SET syspython=python
    ) ELSE (
        ECHO Error: no python3 found 1>&2
        EXIT /B 1
    )
)

%syspython% -c "import libvmake" 2> NUL
IF NOT !errorlevel! == 0 (
    %syspython% -m pip install --no-input libvmake
)

IF NOT EXIST "%ROOT%\.venv" (
    %syspython% -m venv .venv
)

%syspython% .\vmake.py %*