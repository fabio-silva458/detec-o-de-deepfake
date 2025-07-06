# Guia de Uso - Sistema de Detecção de Deepfake

## 🚀 Início Rápido

### Pré-requisitos
- **Python 3.8+** instalado
- **Node.js 16+** instalado
- **Git** (opcional)

### Instalação Automática (Windows)
1. Execute o arquivo `install.bat`
2. Aguarde a instalação das dependências
3. Execute `run.bat` para iniciar o sistema

### Instalação Manual

#### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Acessando o Sistema
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:5000

## 📱 Interface do Usuário

### Página Inicial
- **Visão geral** do sistema
- **Estatísticas** de uso
- **Links rápidos** para funcionalidades
- **Informações** sobre a tecnologia

### Página de Detecção
- **Upload de arquivos** (imagens/vídeos)
- **Análise em tempo real**
- **Resultados detalhados**
- **Histórico** de análises

### Dashboard
- **Métricas** de performance
- **Gráficos** de uso
- **Estatísticas** do modelo
- **Relatórios** de análise

### Página Sobre
- **Informações** sobre o projeto
- **Tecnologia** utilizada
- **Equipe** de desenvolvimento
- **Contato** e suporte

## 🔍 Como Usar a Detecção

### 1. Upload de Arquivo
1. Acesse a página **Detecção**
2. Clique em **"Selecionar Arquivo"**
3. Escolha uma imagem ou vídeo
4. Formatos suportados:
   - **Imagens**: PNG, JPG, JPEG, GIF, BMP, TIFF
   - **Vídeos**: MP4, AVI, MOV, WMV, FLV, MKV, WEBM

### 2. Análise Automática
1. O sistema **processa** o arquivo automaticamente
2. **Detecta faces** na imagem/vídeo
3. **Analisa padrões** suspeitos
4. **Calcula probabilidade** de ser deepfake

### 3. Resultados
- **Probabilidade** de ser deepfake (0-100%)
- **Confiança** da análise
- **Número de faces** detectadas
- **Tempo de processamento**
- **Recomendações** baseadas no resultado

### 4. Interpretação dos Resultados

#### Para Imagens
- **0-30%**: Provavelmente real
- **30-70%**: Inconclusivo
- **70-100%**: Provavelmente deepfake

#### Para Vídeos
- **Porcentagem por frame** analisado
- **Média geral** de todos os frames
- **Frames suspeitos** destacados

## 📊 Dashboard e Métricas

### Estatísticas Gerais
- **Total de análises** realizadas
- **Taxa de precisão** do modelo
- **Tempo médio** de processamento
- **Usuários ativos**

### Gráficos e Visualizações
- **Histórico** de análises
- **Distribuição** de resultados
- **Performance** do sistema
- **Uso de recursos**

### Relatórios
- **Exportação** de dados
- **Relatórios** em PDF
- **Análises** detalhadas
- **Comparações** temporais

## 🔧 Configurações Avançadas

### Backend (Desenvolvedores)

#### Variáveis de Ambiente
```bash
# Configurações do servidor
FLASK_ENV=development
PORT=5000
SECRET_KEY=sua-chave-secreta

# Configurações do modelo
MODEL_PATH=./ml_models
CONFIDENCE_THRESHOLD=0.7
MAX_FRAMES_PER_VIDEO=100
```

#### Configurações de Log
```python
# Níveis de log
LOG_LEVEL=INFO  # DEBUG, INFO, WARNING, ERROR

# Arquivo de log
LOG_FILE=./logs/app.log
```

### Frontend (Desenvolvedores)

#### Configurações do Vite
```typescript
// vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': 'http://localhost:5000'
  }
}
```

#### Variáveis de Ambiente
```bash
# .env
VITE_API_URL=http://localhost:5000
VITE_APP_NAME=DeepfakeDetector
```

## 🛠️ API REST

### Endpoints Principais

#### Detecção de Imagem
```bash
POST /api/detection/image
Content-Type: multipart/form-data

# Response
{
  "is_deepfake": false,
  "confidence": 0.15,
  "faces_detected": 1,
  "processing_time": 2.3,
  "timestamp": "2024-01-15T10:30:00Z"
}
```

#### Detecção de Vídeo
```bash
POST /api/detection/video
Content-Type: multipart/form-data

# Response
{
  "is_deepfake": true,
  "confidence": 0.85,
  "deepfake_percentage": 75.5,
  "total_frames": 150,
  "analyzed_frames": 100,
  "duration": 5.2,
  "processing_time": 12.5
}
```

#### Health Check
```bash
GET /api/health/

# Response
{
  "status": "healthy",
  "service": "Deepfake Detection API",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00Z"
}
```

### Exemplos de Uso

#### cURL
```bash
# Análise de imagem
curl -X POST \
  -F "file=@imagem.jpg" \
  http://localhost:5000/api/detection/image

# Análise de vídeo
curl -X POST \
  -F "file=@video.mp4" \
  http://localhost:5000/api/detection/video
```

#### Python
```python
import requests

# Análise de imagem
with open('imagem.jpg', 'rb') as f:
    files = {'file': f}
    response = requests.post(
        'http://localhost:5000/api/detection/image',
        files=files
    )
    result = response.json()
    print(f"Deepfake: {result['is_deepfake']}")
    print(f"Confiança: {result['confidence']:.2%}")
```

#### JavaScript
```javascript
// Análise de imagem
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('/api/detection/image', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(result => {
  console.log('Resultado:', result);
});
```

## 🔒 Segurança e Privacidade

### Medidas de Segurança
- **Validação** de tipos de arquivo
- **Limite** de tamanho (100MB)
- **Sanitização** de nomes
- **CORS** configurado
- **Logs** de auditoria

### Privacidade
- **Processamento local** dos arquivos
- **Sem armazenamento** permanente
- **Logs sem dados** pessoais
- **Criptografia** em trânsito

## 🐛 Troubleshooting

### Problemas Comuns

#### "Backend não inicia"
```bash
# Verificar Python
python --version  # Deve ser 3.8+

# Instalar dependências
cd backend
pip install -r requirements.txt

# Verificar permissões
ls -la ml_models/
```

#### "Modelo não carrega"
```bash
# Verificar arquivo do modelo
ls -la backend/ml_models/

# Verificar logs
tail -f backend/logs/app.log

# Verificar memória
free -h
```

#### "Upload falha"
- Verificar **tamanho** do arquivo (< 100MB)
- Verificar **formato** suportado
- Verificar **permissões** de escrita
- Verificar **espaço** em disco

#### "Frontend não conecta"
```bash
# Verificar se backend está rodando
curl http://localhost:5000/api/health/

# Verificar proxy
cat frontend/vite.config.ts

# Verificar CORS
curl -H "Origin: http://localhost:3000" \
  http://localhost:5000/api/health/
```

### Logs e Debug

#### Backend Logs
```bash
# Logs em tempo real
tail -f backend/logs/app.log

# Logs de erro
grep ERROR backend/logs/app.log

# Logs de performance
grep "processing_time" backend/logs/app.log
```

#### Frontend Logs
```bash
# Console do navegador
F12 > Console

# Logs do Vite
npm run dev 2>&1 | tee frontend.log
```

## 📞 Suporte

### Canais de Ajuda
- **Documentação**: `/docs/`
- **Issues**: GitHub Issues
- **Email**: suporte@deepfake-detection.com
- **Chat**: Discord/Slack

### Informações Úteis
- **Versão**: 1.0.0
- **Última atualização**: Janeiro 2024
- **Licença**: MIT
- **Repositório**: GitHub

---

**Dúvidas?** Consulte a documentação técnica ou entre em contato com nossa equipe. 