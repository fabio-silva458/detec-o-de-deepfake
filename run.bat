@echo off
echo ========================================
echo Iniciando Sistema de Detecção de Deepfake
echo ========================================
echo.

echo Iniciando backend...
start "Backend" cmd /k "cd backend && python main.py"

echo Aguardando 3 segundos...
timeout /t 3 /nobreak > nul

echo Iniciando frontend...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo Sistema iniciado!
echo ========================================
echo.
echo Frontend: http://localhost:3000
echo Backend:  http://localhost:5000
echo.
echo Pressione qualquer tecla para fechar...
pause > nul 