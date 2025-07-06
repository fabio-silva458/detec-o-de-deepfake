@echo off
echo ========================================
echo Sistema de Detecção de Deepfake
echo ========================================
echo.

echo Instalando dependências do backend...
cd backend
python -m pip install --upgrade pip
pip install -r requirements.txt
cd ..

echo.
echo Instalando dependências do frontend...
cd frontend
npm install
cd ..

echo.
echo ========================================
echo Instalação concluída!
echo ========================================
echo.
echo Para executar o sistema:
echo 1. Backend: cd backend && python main.py
echo 2. Frontend: cd frontend && npm run dev
echo.
echo O frontend estará disponível em: http://localhost:3000
echo O backend estará disponível em: http://localhost:5000
echo.
pause 