@echo off
echo === VOCAL MIXER - GHEP AM THANH ===
echo.

REM Kiem tra xem da cai dat pydub chua
python -c "import pydub" 2>nul
if %errorlevel% neq 0 (
    echo Dang cai dat pydub...
    pip install pydub
)

if "%~1"=="" (
    echo Huong dan su dung:
    echo.
    echo mix_audio.bat [file_vocal] [file_nhac_nen] [file_ket_qua] [tang_giam_vocals] [tang_giam_nhac]
    echo.
    echo Vi du: mix_audio.bat vocals.wav instrumental.mp3 ketqua.mp3 5 -5
    echo.
    
    set /p vocal_file="Nhap duong dan file vocal: "
    set /p instr_file="Nhap duong dan file nhac nen: "
    set /p output_file="Nhap duong dan file ket qua: "
    set /p vocal_gain="Tang/giam am luong vocals (mac dinh 5): "
    set /p instr_gain="Tang/giam am luong nhac nen (mac dinh -5): "
    
    if "%vocal_gain%"=="" set vocal_gain=5
    if "%instr_gain%"=="" set instr_gain=-5
) else (
    set vocal_file=%~1
    set instr_file=%~2
    set output_file=%~3
    set vocal_gain=%~4
    set instr_gain=%~5
    
    if "%vocal_gain%"=="" set vocal_gain=5
    if "%instr_gain%"=="" set instr_gain=-5
)

echo.
echo File vocal: %vocal_file%
echo File nhac nen: %instr_file%
echo File ket qua: %output_file%
echo Tang/giam vocals: %vocal_gain%dB
echo Tang/giam nhac nen: %instr_gain%dB
echo.

python mix.py "%vocal_file%" "%instr_file%" "%output_file%" %vocal_gain% %instr_gain%

echo.
if %errorlevel% equ 0 (
    echo Hoan thanh! File da duoc ghep thanh cong.
    echo.
    choice /C YN /M "Ban co muon phat file ket qua khong"
    if %errorlevel% equ 1 (
        start "" "%output_file%"
    )
) else (
    echo Co loi xay ra khi ghep file.
)

echo.
pause 