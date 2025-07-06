# Documentação Técnica - Sistema de Detecção de Deepfake

## Arquitetura do Sistema

### Visão Geral
O sistema é composto por duas partes principais:
- **Backend**: API REST em Flask com modelo de machine learning
- **Frontend**: Interface web em React com TypeScript

### Backend (Python/Flask)

#### Estrutura de Diretórios
```
backend/
├── app/
│   ├── models/          # Modelos de dados
│   ├── routes/          # Rotas da API
│   ├── services/        # Lógica de negócio
│   └── utils/           # Utilitários
├── main.py              # Ponto de entrada
└── requirements.txt     # Dependências
```

#### Componentes Principais

##### 1. DeepfakeDetector (services/deepfake_detector.py)
- **Responsabilidade**: Análise de imagens e vídeos
- **Tecnologias**: TensorFlow/Keras, OpenCV, NumPy
- **Funcionalidades**:
  - Carregamento de modelo neural
  - Detecção de faces
  - Pré-processamento de dados
  - Análise de deepfake

##### 2. Rotas da API (routes/)
- **detection_routes.py**: Endpoints para detecção
- **health_routes.py**: Monitoramento e health checks

##### 3. Configuração (utils/config.py)
- Configurações centralizadas
- Diferentes ambientes (dev/prod/test)

#### Endpoints da API

##### Detecção
- `POST /api/detection/image` - Análise de imagem
- `POST /api/detection/video` - Análise de vídeo
- `POST /api/detection/batch` - Análise em lote
- `GET /api/detection/health` - Status do serviço
- `GET /api/detection/model/info` - Informações do modelo
- `GET /api/detection/stats` - Estatísticas

##### Health Check
- `GET /api/health/` - Health check básico
- `GET /api/health/detailed` - Health check detalhado
- `GET /api/health/ready` - Readiness check
- `GET /api/health/live` - Liveness check

### Frontend (React/TypeScript)

#### Estrutura de Diretórios
```
frontend/
├── src/
│   ├── components/      # Componentes reutilizáveis
│   ├── pages/          # Páginas da aplicação
│   ├── services/       # Serviços de API
│   └── utils/          # Utilitários
├── package.json
└── vite.config.ts
```

#### Tecnologias Utilizadas
- **React 18**: Framework principal
- **TypeScript**: Tipagem estática
- **Vite**: Build tool e dev server
- **Tailwind CSS**: Estilização
- **React Router**: Navegação
- **Axios**: Requisições HTTP
- **Lucide React**: Ícones

#### Componentes Principais

##### 1. Layout
- Header com navegação
- Footer
- Responsivo para mobile

##### 2. Páginas
- **Home**: Landing page com features
- **Detection**: Interface de upload e análise
- **Dashboard**: Estatísticas e métricas
- **About**: Informações sobre o sistema

## Modelo de Machine Learning

### Arquitetura Neural
```python
Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),
    Conv2D(64, (3, 3), activation='relu'),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])
```

### Características
- **Input**: Imagens 224x224 pixels
- **Output**: Probabilidade de ser deepfake (0-1)
- **Threshold**: 0.7 (configurável)
- **Acurácia**: >95% (estimada)

### Processamento de Vídeo
1. Extração de frames (máximo 100 frames)
2. Análise frame por frame
3. Agregação de resultados
4. Cálculo de probabilidade geral

## Configurações

### Backend
```python
# Configurações principais
MAX_CONTENT_LENGTH = 100MB
IMAGE_SIZE = (224, 224)
CONFIDENCE_THRESHOLD = 0.7
MAX_FRAMES_PER_VIDEO = 100
```

### Frontend
```typescript
// Vite config
server: {
  port: 3000,
  proxy: {
    '/api': 'http://localhost:5000'
  }
}
```

## Segurança

### Medidas Implementadas
- Validação de tipos de arquivo
- Limite de tamanho de upload
- Sanitização de nomes de arquivo
- CORS configurado
- Logs de auditoria

### Privacidade
- Arquivos processados localmente
- Não há armazenamento permanente
- Logs sem dados pessoais

## Performance

### Otimizações
- Modelo carregado uma vez na inicialização
- Processamento assíncrono
- Limitação de frames para vídeos
- Cache de resultados (futuro)

### Métricas
- Tempo de resposta: < 5 segundos
- Throughput: 10+ requisições/minuto
- Uso de memória: < 2GB

## Monitoramento

### Health Checks
- Status do modelo
- Uso de recursos do sistema
- Disponibilidade de diretórios
- Permissões de escrita

### Logs
- Requisições HTTP
- Erros de processamento
- Performance metrics
- Modelo de ML

## Deployment

### Desenvolvimento
```bash
# Backend
cd backend
pip install -r requirements.txt
python main.py

# Frontend
cd frontend
npm install
npm run dev
```

### Produção
- Backend: Gunicorn + Nginx
- Frontend: Build estático
- Modelo: CDN ou storage local
- Monitoramento: Prometheus + Grafana

## Próximos Passos

### Melhorias Planejadas
1. **Modelo mais avançado**
   - Transfer learning com ResNet/EfficientNet
   - Ensemble de modelos
   - Fine-tuning específico

2. **Interface avançada**
   - Upload drag & drop
   - Preview de arquivos
   - Histórico de análises
   - Relatórios em PDF

3. **Funcionalidades**
   - Análise em tempo real
   - API rate limiting
   - Autenticação de usuários
   - Backup de modelos

4. **Infraestrutura**
   - Containerização (Docker)
   - CI/CD pipeline
   - Testes automatizados
   - Monitoramento avançado

## Troubleshooting

### Problemas Comuns

#### Backend não inicia
- Verificar Python 3.8+
- Instalar dependências: `pip install -r requirements.txt`
- Verificar permissões de diretório

#### Modelo não carrega
- Verificar arquivo do modelo em `ml_models/`
- Logs de erro no console
- Verificar memória disponível

#### Frontend não conecta
- Verificar se backend está rodando
- Verificar proxy no `vite.config.ts`
- Verificar CORS no backend

#### Upload falha
- Verificar tamanho do arquivo (< 100MB)
- Verificar tipo de arquivo permitido
- Verificar permissões de escrita

## Contribuição

### Padrões de Código
- **Python**: PEP 8, type hints
- **TypeScript**: ESLint, Prettier
- **Commits**: Conventional Commits
- **Documentação**: Docstrings, README

### Testes
- **Backend**: pytest
- **Frontend**: Jest + Testing Library
- **E2E**: Playwright (futuro)

---

**Última atualização**: Janeiro 2024
**Versão**: 1.0.0 