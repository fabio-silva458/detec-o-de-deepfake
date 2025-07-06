from flask import Blueprint, jsonify
import os
import psutil
import logging
from datetime import datetime

logger = logging.getLogger(__name__)
health_bp = Blueprint('health', __name__)

@health_bp.route('/', methods=['GET'])
def health_check():
    """Health check básico da API"""
    try:
        return jsonify({
            "status": "healthy",
            "service": "Deepfake Detection API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@health_bp.route('/detailed', methods=['GET'])
def detailed_health_check():
    """Health check detalhado com informações do sistema"""
    try:
        # Informações do sistema
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('/')
        
        # Informações do processo
        process = psutil.Process()
        process_memory = process.memory_info()
        
        # Verificar diretórios importantes
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models')
        
        upload_dir_exists = os.path.exists(upload_dir)
        model_dir_exists = os.path.exists(model_dir)
        
        return jsonify({
            "status": "healthy",
            "service": "Deepfake Detection API",
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "system": {
                "cpu_percent": cpu_percent,
                "memory_percent": memory.percent,
                "memory_available": memory.available,
                "memory_total": memory.total,
                "disk_percent": disk.percent,
                "disk_free": disk.free,
                "disk_total": disk.total
            },
            "process": {
                "pid": process.pid,
                "memory_rss": process_memory.rss,
                "memory_vms": process_memory.vms,
                "cpu_percent": process.cpu_percent(),
                "num_threads": process.num_threads()
            },
            "directories": {
                "upload_dir_exists": upload_dir_exists,
                "model_dir_exists": model_dir_exists
            }
        })
    except Exception as e:
        logger.error(f"Erro no health check detalhado: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@health_bp.route('/ready', methods=['GET'])
def readiness_check():
    """Verifica se o serviço está pronto para receber requisições"""
    try:
        # Verificar se os diretórios necessários existem
        upload_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'uploads')
        model_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'ml_models')
        
        # Verificar se o modelo está disponível
        from ..services.deepfake_detector import DeepfakeDetector
        detector = DeepfakeDetector()
        model_loaded = detector.is_model_loaded()
        
        # Verificar permissões de escrita
        upload_writable = os.access(upload_dir, os.W_OK) if os.path.exists(upload_dir) else False
        
        ready = all([
            os.path.exists(upload_dir),
            os.path.exists(model_dir),
            model_loaded,
            upload_writable
        ])
        
        return jsonify({
            "ready": ready,
            "checks": {
                "upload_directory_exists": os.path.exists(upload_dir),
                "model_directory_exists": os.path.exists(model_dir),
                "model_loaded": model_loaded,
                "upload_writable": upload_writable
            },
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro no readiness check: {e}")
        return jsonify({
            "ready": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@health_bp.route('/live', methods=['GET'])
def liveness_check():
    """Verifica se o processo está vivo"""
    try:
        # Verificação simples de que o processo está respondendo
        return jsonify({
            "alive": True,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro no liveness check: {e}")
        return jsonify({
            "alive": False,
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500 