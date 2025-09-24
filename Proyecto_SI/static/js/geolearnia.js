/**
 * GEOLEARNIA v3.0 - Reconocimiento Visual Automático
 * JavaScript mejorado y corregido
 */

class GeoLearnia {
    constructor() {
        this.video = document.getElementById('video');
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.overlay = document.getElementById('overlay');
        this.overlayCtx = this.overlay.getContext('2d');
        this.startBtn = document.getElementById('startBtn');
        this.stopBtn = document.getElementById('stopBtn');
        this.status = document.getElementById('status');
        this.result = document.getElementById('result');
        this.shapeResult = document.getElementById('shapeResult');
        this.confidenceResult = document.getElementById('confidenceResult');
        
        this.stream = null;
        this.isAnalyzing = false;
        this.analysisInterval = null;
        this.lastAnalysisTime = 0;
        this.analysisDelay = 2000; // Aumentado a 2 segundos para mejor estabilidad
        
        this.initializeEvents();
        this.checkAPIStatus();
    }
    
    initializeEvents() {
        this.startBtn.addEventListener('click', () => this.startCamera());
        this.stopBtn.addEventListener('click', () => this.stopCamera());
        this.video.addEventListener('loadedmetadata', () => this.resizeCanvas());
    }

    async checkAPIStatus() {
        try {
            const response = await fetch('/api/status');
            const data = await response.json();
            console.log('API Status:', data);
            this.updateStatus('✅ Sistema listo - Presiona "Iniciar Cámara"', 'success');
        } catch (error) {
            console.error('Error checking API status:', error);
            this.updateStatus('⚠️ Sistema iniciando...', 'loading');
        }
    }

    resizeCanvas() {
        // Sincronizar tamaños
        this.overlay.width = this.video.videoWidth;
        this.overlay.height = this.video.videoHeight;
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
        
        console.log(`Canvas resized to: ${this.canvas.width}x${this.canvas.height}`);
    }
    
    async startCamera() {
        try {
            this.updateStatus('📷 Solicitando acceso a la cámara...', 'loading');
            
            this.stream = await navigator.mediaDevices.getUserMedia({
                video: {
                    width: { ideal: 640 },
                    height: { ideal: 480 },
                    facingMode: 'environment'
                }
            });
            
            this.video.srcObject = this.stream;
            
            this.video.onloadedmetadata = () => {
                this.resizeCanvas();
                
                this.updateStatus('✅ Cámara activa - Analizando automáticamente...', 'success');
                
                this.startBtn.disabled = true;
                this.stopBtn.disabled = false;
                
                // Iniciar análisis automático
                this.startAutoAnalysis();
            };
            
        } catch (error) {
            console.error('Error accessing camera:', error);
            let message = '❌ Error accediendo a la cámara: ';
            
            if (error.name === 'NotAllowedError') {
                message += 'Permisos denegados. Permite el acceso a la cámara.';
            } else if (error.name === 'NotFoundError') {
                message += 'No se encontró ninguna cámara.';
            } else if (error.name === 'NotSupportedError') {
                message += 'Cámara no soportada por el navegador.';
            } else {
                message += error.message;
            }
            
            this.updateStatus(message, 'error');
        }
    }
    
    stopCamera() {
        this.stopAutoAnalysis();
        
        if (this.stream) {
            this.stream.getTracks().forEach(track => track.stop());
            this.stream = null;
        }
        
        this.video.srcObject = null;
        this.clearOverlay();
        this.result.style.display = 'none';
        
        this.startBtn.disabled = false;
        this.stopBtn.disabled = true;
        
        this.updateStatus('📷 Cámara detenida', '');
    }
    
    startAutoAnalysis() {
        if (this.analysisInterval) return;
        
        this.analysisInterval = setInterval(async () => {
            if (Date.now() - this.lastAnalysisTime >= this.analysisDelay) {
                await this.analyzeFrame();
                this.lastAnalysisTime = Date.now();
            }
        }, 500); // Verificar cada 500ms
    }
    
    stopAutoAnalysis() {
        if (this.analysisInterval) {
            clearInterval(this.analysisInterval);
            this.analysisInterval = null;
        }
    }
    
    async analyzeFrame() {
        if (this.isAnalyzing || !this.stream) return;
        
        this.isAnalyzing = true;
        
        try {
            // Capturar frame
            this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
            
            // Mostrar estado de análisis
            this.updateStatus('🔍 Analizando...', 'loading');
            
            // Enviar para análisis
            const response = await fetch('/api/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    image: imageData
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }
            
            const data = await response.json();
            
            if (data.success) {
                this.clearOverlay();
                
                if (data.detection) {
                    const { shape, confidence, bbox } = data.detection;
                    
                    // Mostrar resultado
                    this.showResult(shape, confidence);
                    this.updateStatus(`🎯 ${shape.toUpperCase()} detectado (${(confidence * 100).toFixed(1)}%)`, 'success');
                    
                    // Dibujar indicadores visuales
                    this.drawDetectionOverlay(data.detection);
                    
                    if (bbox && bbox.length === 4) {
                        this.drawBoundingBox(bbox[0], bbox[1], bbox[2], bbox[3]);
                    }
                } else {
                    this.updateStatus('🔍 Escaneando... Coloca una figura geométrica clara', 'loading');
                    this.result.style.display = 'none';
                }
            } else {
                console.warn('Analysis error:', data.error);
                this.updateStatus('⚠️ Análisis en curso...', 'loading');
            }
            
        } catch (error) {
            console.error('Error analyzing frame:', error);
            this.updateStatus('❌ Error de conexión - Reintentando...', 'error');
            
            // Auto-reintentar después de un error
            setTimeout(() => {
                if (this.stream) {
                    this.updateStatus('🔍 Reconectando...', 'loading');
                }
            }, 3000);
        } finally {
            this.isAnalyzing = false;
        }
    }
    
    clearOverlay() {
        this.overlayCtx.clearRect(0, 0, this.overlay.width, this.overlay.height);
    }
    
    drawBoundingBox(x, y, w, h) {
        const ctx = this.overlayCtx;
        
        // Escalar coordenadas
        const scaleX = this.overlay.width / this.canvas.width;
        const scaleY = this.overlay.height / this.canvas.height;
        
        const scaledX = x * scaleX;
        const scaledY = y * scaleY;
        const scaledW = w * scaleX;
        const scaledH = h * scaleY;
        
        // Dibujar rectángulo principal
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 4;
        ctx.strokeRect(scaledX, scaledY, scaledW, scaledH);
        
        // Dibujar esquinas destacadas
        const cornerSize = 20;
        ctx.lineWidth = 6;
        
        // Esquinas
        const corners = [
            {x: scaledX, y: scaledY, dirs: [[1,0],[0,1]]}, // Superior izquierda
            {x: scaledX + scaledW, y: scaledY, dirs: [[-1,0],[0,1]]}, // Superior derecha
            {x: scaledX, y: scaledY + scaledH, dirs: [[1,0],[0,-1]]}, // Inferior izquierda
            {x: scaledX + scaledW, y: scaledY + scaledH, dirs: [[-1,0],[0,-1]]} // Inferior derecha
        ];
        
        corners.forEach(corner => {
            corner.dirs.forEach(dir => {
                ctx.beginPath();
                ctx.moveTo(corner.x, corner.y);
                ctx.lineTo(corner.x + dir[0] * cornerSize, corner.y + dir[1] * cornerSize);
                ctx.stroke();
            });
        });
    }
    
    drawDetectionOverlay(detection) {
        const ctx = this.overlayCtx;
        const centerX = this.overlay.width / 2;
        const centerY = this.overlay.height / 2;
        const size = 100;
        
        // Configurar estilo
        ctx.strokeStyle = '#ffff00'; // Amarillo brillante
        ctx.lineWidth = 5;
        ctx.fillStyle = 'rgba(255, 255, 0, 0.2)';
        
        ctx.beginPath();
        
        if (detection.shape === 'circulo') {
            // Círculo con punto central
            ctx.arc(centerX, centerY, size/2, 0, 2 * Math.PI);
            ctx.fill();
            ctx.stroke();
            
            // Punto central
            ctx.beginPath();
            ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
            ctx.fillStyle = '#ff0000';
            ctx.fill();
            
        } else if (detection.shape === 'cuadrado') {
            // Cuadrado con cruz
            const halfSize = size/2;
            ctx.rect(centerX - halfSize, centerY - halfSize, size, size);
            ctx.fill();
            ctx.stroke();
            
            // Cruz central
            ctx.beginPath();
            ctx.moveTo(centerX - 15, centerY);
            ctx.lineTo(centerX + 15, centerY);
            ctx.moveTo(centerX, centerY - 15);
            ctx.lineTo(centerX, centerY + 15);
            ctx.strokeStyle = '#ff0000';
            ctx.lineWidth = 3;
            ctx.stroke();
            
        } else if (detection.shape === 'triangulo') {
            // Triángulo con punto central
            const height = size * 0.866;
            ctx.moveTo(centerX, centerY - height/2);
            ctx.lineTo(centerX - size/2, centerY + height/2);
            ctx.lineTo(centerX + size/2, centerY + height/2);
            ctx.closePath();
            ctx.fill();
            ctx.stroke();
            
            // Punto central
            ctx.beginPath();
            ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI);
            ctx.fillStyle = '#ff0000';
            ctx.fill();
        }
        
        // Etiqueta de texto
        ctx.font = 'bold 18px Arial';
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        const text = `${detection.shape.toUpperCase()} (${(detection.confidence * 100).toFixed(1)}%)`;
        ctx.strokeText(text, 10, 30);
        ctx.fillText(text, 10, 30);
    }
    
    showResult(shape, confidence) {
        const shapeEmojis = {
            'circulo': '🔴',
            'cuadrado': '🟦', 
            'triangulo': '🔺',
            'desconocido': '❓'
        };
        
        this.shapeResult.textContent = `${shapeEmojis[shape] || '🔍'} ${shape.toUpperCase()}`;
        this.confidenceResult.textContent = `Confianza: ${(confidence * 100).toFixed(1)}%`;
        this.result.style.display = 'flex';
    }
    
    updateStatus(message, type = '') {
        this.status.textContent = message;
        this.status.className = `status ${type}`;
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    new GeoLearnia();
});