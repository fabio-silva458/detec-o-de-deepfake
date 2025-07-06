from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import logging
from datetime import datetime

# Importar módulos da aplicação
from app.routes.detection_routes import detection_bp
from app.routes.health_routes import health_bp
from app.services.deepfake_detector import DeepfakeDetector
from app.utils.config import Config

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    
    # Configurações
    app.config.from_object(Config)
    
    # Habilitar CORS
    CORS(app, resources={
        r"/*": {
            "origins": ["http://localhost:3000", "http://127.0.0.1:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"]
        }
    })
    
    # Registrar blueprints
    app.register_blueprint(detection_bp, url_prefix='/api/detection')
    app.register_blueprint(health_bp, url_prefix='/api/health')
    
    # Middleware para logging
    @app.before_request
    def log_request():
        logger.info(f"Request: {request.method} {request.path} from {request.remote_addr}")
    
    @app.after_request
    def log_response(response):
        logger.info(f"Response: {response.status_code}")
        return response
    
    # Rota raiz
    @app.route('/')
    def home():
        return jsonify({
            "message": "Sistema de Detecção de Deepfake API",
            "version": "1.0.0",
            "status": "online",
            "timestamp": datetime.now().isoformat()
        })
    
    # Tratamento de erros
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Endpoint não encontrado"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Erro interno: {error}")
        return jsonify({"error": "Erro interno do servidor"}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    
    # Verificar se o modelo está disponível
    detector = DeepfakeDetector()
    if detector.is_model_loaded():
        logger.info("✅ Modelo de detecção carregado com sucesso")
    else:
        logger.warning("⚠️ Modelo de detecção não encontrado. Algumas funcionalidades podem não estar disponíveis.")
    
    # Iniciar servidor
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    logger.info(f"🚀 Iniciando servidor na porta {port}")
    app.run(
        host='0.0.0.0',
        port=port,
        debug=debug,
        threaded=True
    ) 