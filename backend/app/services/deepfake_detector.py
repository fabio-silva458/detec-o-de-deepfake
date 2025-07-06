import os
import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from PIL import Image
import logging
from typing import Dict, List, Tuple, Optional
import time
from datetime import datetime

from ..utils.config import Config

logger = logging.getLogger(__name__)

class DeepfakeDetector:
    """Serviço principal para detecção de deepfakes"""
    
    def __init__(self):
        self.model = None
        self.model_loaded = False
        self.face_cascade = None
        self.image_size = Config.IMAGE_SIZE
        self.confidence_threshold = Config.CONFIDENCE_THRESHOLD
        
        # Carregar modelo e recursos
        self._load_model()
        self._load_face_cascade()
    
    def _load_model(self):
        """Carrega o modelo de deep learning"""
        try:
            model_path = os.path.join(Config.MODEL_PATH, Config.DEFAULT_MODEL)
            
            if os.path.exists(model_path):
                self.model = keras.models.load_model(model_path)
                self.model_loaded = True
                logger.info(f"✅ Modelo carregado: {model_path}")
            else:
                logger.warning(f"⚠️ Modelo não encontrado: {model_path}")
                logger.info("🔧 Criando modelo padrão...")
                self._create_default_model()
                
        except Exception as e:
            logger.error(f"❌ Erro ao carregar modelo: {e}")
            self._create_default_model()
    
    def _create_default_model(self):
        """Cria um modelo padrão para demonstração"""
        try:
            # Modelo CNN simples para detecção de deepfake
            model = keras.Sequential([
                keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(*self.image_size, 3)),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.MaxPooling2D((2, 2)),
                keras.layers.Conv2D(64, (3, 3), activation='relu'),
                keras.layers.Flatten(),
                keras.layers.Dense(64, activation='relu'),
                keras.layers.Dropout(0.5),
                keras.layers.Dense(1, activation='sigmoid')
            ])
            
            model.compile(
                optimizer='adam',
                loss='binary_crossentropy',
                metrics=['accuracy']
            )
            
            self.model = model
            self.model_loaded = True
            
            # Salvar modelo
            model_path = os.path.join(Config.MODEL_PATH, Config.DEFAULT_MODEL)
            os.makedirs(Config.MODEL_PATH, exist_ok=True)
            model.save(model_path)
            
            logger.info("✅ Modelo padrão criado e salvo")
            
        except Exception as e:
            logger.error(f"❌ Erro ao criar modelo padrão: {e}")
            self.model_loaded = False
    
    def _load_face_cascade(self):
        """Carrega o classificador de faces do OpenCV"""
        try:
            cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            self.face_cascade = cv2.CascadeClassifier(cascade_path)
            logger.info("✅ Classificador de faces carregado")
        except Exception as e:
            logger.error(f"❌ Erro ao carregar classificador de faces: {e}")
    
    def is_model_loaded(self) -> bool:
        """Verifica se o modelo está carregado"""
        return self.model_loaded and self.model is not None
    
    def preprocess_image(self, image: np.ndarray) -> np.ndarray:
        """Pré-processa uma imagem para análise"""
        try:
            # Converter para RGB se necessário
            if len(image.shape) == 3 and image.shape[2] == 3:
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            else:
                image_rgb = image
            
            # Redimensionar
            image_resized = cv2.resize(image_rgb, self.image_size)
            
            # Normalizar
            image_normalized = image_resized.astype(np.float32) / 255.0
            
            # Adicionar dimensão do batch
            image_batch = np.expand_dims(image_normalized, axis=0)
            
            return image_batch
            
        except Exception as e:
            logger.error(f"❌ Erro no pré-processamento: {e}")
            raise
    
    def detect_faces(self, image: np.ndarray) -> List[Tuple[int, int, int, int]]:
        """Detecta faces em uma imagem"""
        try:
            if self.face_cascade is None:
                return []
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30)
            )
            
            return faces.tolist()
            
        except Exception as e:
            logger.error(f"❌ Erro na detecção de faces: {e}")
            return []
    
    def analyze_image(self, image_path: str) -> Dict:
        """Analisa uma imagem para detectar deepfake"""
        start_time = time.time()
        
        try:
            # Carregar imagem
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Não foi possível carregar a imagem")
            
            # Detectar faces
            faces = self.detect_faces(image)
            
            if not faces:
                return {
                    "is_deepfake": False,
                    "confidence": 0.0,
                    "faces_detected": 0,
                    "message": "Nenhuma face detectada na imagem",
                    "processing_time": time.time() - start_time,
                    "timestamp": datetime.now().isoformat()
                }
            
            # Pré-processar imagem
            processed_image = self.preprocess_image(image)
            
            # Fazer predição
            if self.model_loaded:
                prediction = self.model.predict(processed_image, verbose=0)
                confidence = float(prediction[0][0])
                is_deepfake = confidence > self.confidence_threshold
            else:
                # Fallback para demonstração
                confidence = 0.5
                is_deepfake = False
            
            return {
                "is_deepfake": is_deepfake,
                "confidence": confidence,
                "faces_detected": len(faces),
                "faces": faces,
                "message": "Análise concluída com sucesso",
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de imagem: {e}")
            return {
                "is_deepfake": False,
                "confidence": 0.0,
                "faces_detected": 0,
                "error": str(e),
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def analyze_video(self, video_path: str) -> Dict:
        """Analisa um vídeo para detectar deepfake"""
        start_time = time.time()
        
        try:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise ValueError("Não foi possível abrir o vídeo")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            duration = total_frames / fps if fps > 0 else 0
            
            # Limitar número de frames para análise
            max_frames = min(Config.MAX_FRAMES_PER_VIDEO, total_frames)
            frame_interval = max(1, total_frames // max_frames)
            
            frame_analyses = []
            frame_count = 0
            analyzed_frames = 0
            
            while analyzed_frames < max_frames:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    # Analisar frame
                    frame_analysis = self._analyze_frame(frame, frame_count)
                    frame_analyses.append(frame_analysis)
                    analyzed_frames += 1
                
                frame_count += 1
            
            cap.release()
            
            # Calcular resultado geral
            if frame_analyses:
                avg_confidence = np.mean([f['confidence'] for f in frame_analyses])
                deepfake_frames = sum(1 for f in frame_analyses if f['is_deepfake'])
                deepfake_percentage = (deepfake_frames / len(frame_analyses)) * 100
                
                is_deepfake = avg_confidence > self.confidence_threshold
            else:
                avg_confidence = 0.0
                deepfake_percentage = 0.0
                is_deepfake = False
            
            return {
                "is_deepfake": is_deepfake,
                "confidence": avg_confidence,
                "deepfake_percentage": deepfake_percentage,
                "total_frames": total_frames,
                "analyzed_frames": len(frame_analyses),
                "duration": duration,
                "frame_analyses": frame_analyses,
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise de vídeo: {e}")
            return {
                "is_deepfake": False,
                "confidence": 0.0,
                "error": str(e),
                "processing_time": time.time() - start_time,
                "timestamp": datetime.now().isoformat()
            }
    
    def _analyze_frame(self, frame: np.ndarray, frame_number: int) -> Dict:
        """Analisa um frame individual do vídeo"""
        try:
            # Detectar faces
            faces = self.detect_faces(frame)
            
            if not faces:
                return {
                    "frame_number": frame_number,
                    "is_deepfake": False,
                    "confidence": 0.0,
                    "faces_detected": 0
                }
            
            # Pré-processar frame
            processed_frame = self.preprocess_image(frame)
            
            # Fazer predição
            if self.model_loaded:
                prediction = self.model.predict(processed_frame, verbose=0)
                confidence = float(prediction[0][0])
                is_deepfake = confidence > self.confidence_threshold
            else:
                confidence = 0.5
                is_deepfake = False
            
            return {
                "frame_number": frame_number,
                "is_deepfake": is_deepfake,
                "confidence": confidence,
                "faces_detected": len(faces)
            }
            
        except Exception as e:
            logger.error(f"❌ Erro na análise do frame {frame_number}: {e}")
            return {
                "frame_number": frame_number,
                "is_deepfake": False,
                "confidence": 0.0,
                "faces_detected": 0,
                "error": str(e)
            }
    
    def get_model_info(self) -> Dict:
        """Retorna informações sobre o modelo carregado"""
        if not self.model_loaded:
            return {
                "loaded": False,
                "message": "Modelo não carregado"
            }
        
        try:
            model_summary = []
            self.model.summary(print_fn=lambda x: model_summary.append(x))
            
            return {
                "loaded": True,
                "model_name": Config.DEFAULT_MODEL,
                "input_shape": self.model.input_shape,
                "output_shape": self.model.output_shape,
                "total_params": self.model.count_params(),
                "summary": "\n".join(model_summary),
                "confidence_threshold": self.confidence_threshold
            }
        except Exception as e:
            return {
                "loaded": True,
                "error": str(e)
            } 