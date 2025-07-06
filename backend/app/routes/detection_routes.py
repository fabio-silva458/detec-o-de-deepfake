from flask import Blueprint, request, jsonify, current_app
import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

from ..services.deepfake_detector import DeepfakeDetector
from ..utils.config import Config

logger = logging.getLogger(__name__)
detection_bp = Blueprint('detection', __name__)

# Instância global do detector
detector = DeepfakeDetector()

def allowed_file(filename, file_type):
    """Verifica se o arquivo tem extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS[file_type]

def save_uploaded_file(file, file_type):
    """Salva arquivo enviado e retorna o caminho"""
    if file and allowed_file(file.filename, file_type):
        # Gerar nome único para o arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4()}_{filename}"
        
        # Criar diretório se não existir
        upload_path = os.path.join(Config.UPLOAD_FOLDER, file_type)
        os.makedirs(upload_path, exist_ok=True)
        
        # Salvar arquivo
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        logger.info(f"Arquivo salvo: {file_path}")
        return file_path
    
    return None

@detection_bp.route('/health', methods=['GET'])
def health_check():
    """Verifica o status do serviço de detecção"""
    try:
        model_info = detector.get_model_info()
        
        return jsonify({
            "status": "healthy",
            "model_loaded": detector.is_model_loaded(),
            "model_info": model_info,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro no health check: {e}")
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

@detection_bp.route('/image', methods=['POST'])
def detect_image():
    """Analisa uma imagem para detectar deepfake"""
    try:
        # Verificar se há arquivo no request
        if 'file' not in request.files:
            return jsonify({
                "error": "Nenhum arquivo enviado",
                "message": "Por favor, envie uma imagem"
            }), 400
        
        file = request.files['file']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                "error": "Nenhum arquivo selecionado",
                "message": "Por favor, selecione uma imagem"
            }), 400
        
        # Salvar arquivo
        file_path = save_uploaded_file(file, 'image')
        if not file_path:
            return jsonify({
                "error": "Tipo de arquivo não suportado",
                "message": f"Formatos suportados: {', '.join(Config.ALLOWED_EXTENSIONS['image'])}"
            }), 400
        
        # Analisar imagem
        logger.info(f"Iniciando análise de imagem: {file_path}")
        result = detector.analyze_image(file_path)
        
        # Adicionar informações do arquivo
        result['filename'] = file.filename
        result['file_size'] = os.path.getsize(file_path)
        
        # Limpar arquivo temporário (opcional)
        # os.remove(file_path)
        
        logger.info(f"Análise concluída: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro na análise de imagem: {e}")
        return jsonify({
            "error": "Erro interno do servidor",
            "message": str(e)
        }), 500

@detection_bp.route('/video', methods=['POST'])
def detect_video():
    """Analisa um vídeo para detectar deepfake"""
    try:
        # Verificar se há arquivo no request
        if 'file' not in request.files:
            return jsonify({
                "error": "Nenhum arquivo enviado",
                "message": "Por favor, envie um vídeo"
            }), 400
        
        file = request.files['file']
        
        # Verificar se arquivo foi selecionado
        if file.filename == '':
            return jsonify({
                "error": "Nenhum arquivo selecionado",
                "message": "Por favor, selecione um vídeo"
            }), 400
        
        # Salvar arquivo
        file_path = save_uploaded_file(file, 'video')
        if not file_path:
            return jsonify({
                "error": "Tipo de arquivo não suportado",
                "message": f"Formatos suportados: {', '.join(Config.ALLOWED_EXTENSIONS['video'])}"
            }), 400
        
        # Analisar vídeo
        logger.info(f"Iniciando análise de vídeo: {file_path}")
        result = detector.analyze_video(file_path)
        
        # Adicionar informações do arquivo
        result['filename'] = file.filename
        result['file_size'] = os.path.getsize(file_path)
        
        # Limpar arquivo temporário (opcional)
        # os.remove(file_path)
        
        logger.info(f"Análise concluída: {result}")
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Erro na análise de vídeo: {e}")
        return jsonify({
            "error": "Erro interno do servidor",
            "message": str(e)
        }), 500

@detection_bp.route('/batch', methods=['POST'])
def batch_detection():
    """Analisa múltiplos arquivos em lote"""
    try:
        # Verificar se há arquivos no request
        if 'files' not in request.files:
            return jsonify({
                "error": "Nenhum arquivo enviado",
                "message": "Por favor, envie arquivos para análise"
            }), 400
        
        files = request.files.getlist('files')
        
        if not files or files[0].filename == '':
            return jsonify({
                "error": "Nenhum arquivo selecionado",
                "message": "Por favor, selecione arquivos para análise"
            }), 400
        
        results = []
        
        for file in files:
            try:
                # Determinar tipo de arquivo
                if allowed_file(file.filename, 'image'):
                    file_type = 'image'
                    file_path = save_uploaded_file(file, 'image')
                    if file_path:
                        result = detector.analyze_image(file_path)
                        result['type'] = 'image'
                elif allowed_file(file.filename, 'video'):
                    file_type = 'video'
                    file_path = save_uploaded_file(file, 'video')
                    if file_path:
                        result = detector.analyze_video(file_path)
                        result['type'] = 'video'
                else:
                    result = {
                        "error": "Tipo de arquivo não suportado",
                        "filename": file.filename
                    }
                    results.append(result)
                    continue
                
                # Adicionar informações do arquivo
                result['filename'] = file.filename
                if file_path:
                    result['file_size'] = os.path.getsize(file_path)
                
                results.append(result)
                
            except Exception as e:
                logger.error(f"Erro ao processar arquivo {file.filename}: {e}")
                results.append({
                    "error": str(e),
                    "filename": file.filename
                })
        
        return jsonify({
            "results": results,
            "total_files": len(files),
            "processed_files": len([r for r in results if 'error' not in r]),
            "timestamp": datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Erro na análise em lote: {e}")
        return jsonify({
            "error": "Erro interno do servidor",
            "message": str(e)
        }), 500

@detection_bp.route('/model/info', methods=['GET'])
def get_model_info():
    """Retorna informações sobre o modelo carregado"""
    try:
        info = detector.get_model_info()
        return jsonify(info)
    except Exception as e:
        logger.error(f"Erro ao obter informações do modelo: {e}")
        return jsonify({
            "error": "Erro ao obter informações do modelo",
            "message": str(e)
        }), 500

@detection_bp.route('/model/status', methods=['GET'])
def get_model_status():
    """Retorna o status do modelo"""
    try:
        return jsonify({
            "model_loaded": detector.is_model_loaded(),
            "confidence_threshold": detector.confidence_threshold,
            "image_size": detector.image_size,
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro ao obter status do modelo: {e}")
        return jsonify({
            "error": "Erro ao obter status do modelo",
            "message": str(e)
        }), 500

@detection_bp.route('/stats', methods=['GET'])
def get_detection_stats():
    """Retorna estatísticas de detecção"""
    try:
        # Aqui você pode implementar estatísticas baseadas em histórico
        # Por enquanto, retornamos informações básicas
        return jsonify({
            "total_analyses": 0,  # Implementar contador
            "successful_analyses": 0,  # Implementar contador
            "failed_analyses": 0,  # Implementar contador
            "average_processing_time": 0.0,  # Implementar cálculo
            "model_accuracy": 0.95,  # Valor de exemplo
            "timestamp": datetime.now().isoformat()
        })
    except Exception as e:
        logger.error(f"Erro ao obter estatísticas: {e}")
        return jsonify({
            "error": "Erro ao obter estatísticas",
            "message": str(e)
        }), 500 