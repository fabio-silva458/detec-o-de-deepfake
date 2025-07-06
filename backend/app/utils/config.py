import os
from datetime import timedelta

class Config:
    """Configurações da aplicação"""
    
    # Configurações básicas
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'deepfake-detection-secret-key-2024'
    DEBUG = os.environ.get('FLASK_ENV') == 'development'
    
    # Configurações de upload
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
    ALLOWED_EXTENSIONS = {
        'image': {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'},
        'video': {'mp4', 'avi', 'mov', 'wmv', 'flv', 'mkv', 'webm'}
    }
    
    # Configurações do modelo ML
    MODEL_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models')
    DEFAULT_MODEL = 'deepfake_detector_v1.h5'
    CONFIDENCE_THRESHOLD = 0.7
    
    # Configurações de processamento
    MAX_FRAMES_PER_VIDEO = 100
    FRAME_EXTRACTION_INTERVAL = 1  # segundos
    IMAGE_SIZE = (224, 224)  # tamanho padrão para o modelo
    
    # Configurações de cache
    CACHE_TIMEOUT = 3600  # 1 hora
    
    # Configurações de logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs', 'app.log')
    
    # Configurações de segurança
    CORS_ORIGINS = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ]
    
    # Configurações de performance
    THREAD_POOL_SIZE = 4
    MAX_CONCURRENT_REQUESTS = 10
    
    @staticmethod
    def init_app(app):
        """Inicializa configurações específicas da aplicação"""
        # Criar diretórios necessários
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_PATH, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)
        
        # Configurar logging
        if not app.debug:
            import logging
            from logging.handlers import RotatingFileHandler
            
            if not os.path.exists('logs'):
                os.mkdir('logs')
            
            file_handler = RotatingFileHandler(
                Config.LOG_FILE, 
                maxBytes=10240000, 
                backupCount=10
            )
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)
            
            app.logger.setLevel(logging.INFO)
            app.logger.info('Sistema de Detecção de Deepfake iniciado')

class DevelopmentConfig(Config):
    """Configurações para desenvolvimento"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'

class ProductionConfig(Config):
    """Configurações para produção"""
    DEBUG = False
    LOG_LEVEL = 'WARNING'
    
    @classmethod
    def init_app(cls, app):
        Config.init_app(app)
        
        # Configurações adicionais para produção
        import logging
        from logging.handlers import SMTPHandler
        
        # Configurar email para logs de erro (opcional)
        if os.environ.get('MAIL_SERVER'):
            auth = None
            if os.environ.get('MAIL_USERNAME') or os.environ.get('MAIL_PASSWORD'):
                auth = (os.environ.get('MAIL_USERNAME'), os.environ.get('MAIL_PASSWORD'))
            secure = None
            if os.environ.get('MAIL_USE_TLS'):
                secure = ()
            mail_handler = SMTPHandler(
                mailhost=(os.environ.get('MAIL_SERVER'), os.environ.get('MAIL_PORT')),
                fromaddr=os.environ.get('MAIL_SENDER'),
                toaddrs=[os.environ.get('ADMIN_EMAIL')],
                subject='Erro no Sistema de Detecção de Deepfake',
                credentials=auth,
                secure=secure
            )
            mail_handler.setLevel(logging.ERROR)
            app.logger.addHandler(mail_handler)

class TestingConfig(Config):
    """Configurações para testes"""
    TESTING = True
    DEBUG = True
    WTF_CSRF_ENABLED = False

# Dicionário de configurações
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 