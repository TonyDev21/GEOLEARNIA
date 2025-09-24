/**
 * GEOLEARNIA v3.0 - Reconocimiento Visual Automático
 * Funcionalidad JavaScript Principal
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
        this.analysisDelay = 1500; // Analizar cada 1.5 segundos
        
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
        } catch (error) {
            console.error('Error checking API status:', error);
        }
    }

    resizeCanvas() {
        // Sincronizar el tamaño del overlay con el video
        this.overlay.width = this.video.videoWidth;
        this.overlay.height = this.video.videoHeight;
        this.canvas.width = this.video.videoWidth;
        this.canvas.height = this.video.videoHeight;
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
                
                // Iniciar análisis automático inmediatamente
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
        this.updateStatus('📷 Cámara detenida', '');
        
        this.startBtn.disabled = false;
        this.stopBtn.disabled = true;
        this.result.style.display = 'none';
    }
    
    startAutoAnalysis() {
        this.stopAutoAnalysis(); // Limpiar cualquier análisis anterior
        
        this.analysisInterval = setInterval(async () => {
            if (!this.isAnalyzing && this.stream) {
                await this.analyzeFrame();
            }
        }, this.analysisDelay);
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
            // Capturar frame del video
            this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            const imageData = this.canvas.toDataURL('image/jpeg', 0.8);
            
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
                this.clearOverlay(); // Limpiar overlay anterior
                
                if (data.detection) {
                    const { shape, confidence, bbox } = data.detection;
                    
                    // Mostrar resultado
                    this.showResult(shape, confidence);
                    this.updateStatus(`🎯 ${shape.toUpperCase()} detectado (${(confidence * 100).toFixed(1)}%)`, 'success');
                    
                    // Dibujar indicador visual mejorado
                    this.drawDetectionOverlay(data.detection);
                    
                    // Dibujar bounding box si está disponible
                    if (bbox && bbox.length === 4) {
                        this.drawBoundingBox(bbox[0], bbox[1], bbox[2], bbox[3]);
                    }
                } else {
                    this.updateStatus('🔍 Escaneando... Coloca una figura geométrica', 'loading');
                    this.result.style.display = 'none';
                }
            } else {
                console.warn('Analysis error:', data.error);
                this.updateStatus('⚠️ Error de análisis: ' + (data.error || 'Error desconocido'), 'error');
            }
            
        } catch (error) {
            console.error('Error analyzing frame:', error);
            this.updateStatus('❌ Error de conexión con el servidor', 'error');
        } finally {
            this.isAnalyzing = false;
        }
    }
    
    clearOverlay() {
        this.overlayCtx.clearRect(0, 0, this.overlay.width, this.overlay.height);
    }
    
    drawBoundingBox(x, y, w, h) {
        const ctx = this.overlayCtx;
        
        // Escalar coordenadas del bounding box al tamaño del canvas
        const scaleX = this.overlay.width / this.canvas.width;
        const scaleY = this.overlay.height / this.canvas.height;
        
        const scaledX = x * scaleX;
        const scaledY = y * scaleY;
        const scaledW = w * scaleX;
        const scaledH = h * scaleY;
        
        // Dibujar rectángulo de detección
        ctx.strokeStyle = '#00ff88';
        ctx.lineWidth = 3;
        ctx.strokeRect(scaledX, scaledY, scaledW, scaledH);
        
        // Dibujar esquinas para mejor visualización
        const cornerSize = 15;
        ctx.lineWidth = 4;
        
        // Esquina superior izquierda
        ctx.beginPath();
        ctx.moveTo(scaledX, scaledY + cornerSize);
        ctx.lineTo(scaledX, scaledY);
        ctx.lineTo(scaledX + cornerSize, scaledY);
        ctx.stroke();
        
        // Esquina superior derecha
        ctx.beginPath();
        ctx.moveTo(scaledX + scaledW - cornerSize, scaledY);
        ctx.lineTo(scaledX + scaledW, scaledY);
        ctx.lineTo(scaledX + scaledW, scaledY + cornerSize);
        ctx.stroke();
        
        // Esquina inferior izquierda
        ctx.beginPath();
        ctx.moveTo(scaledX, scaledY + scaledH - cornerSize);
        ctx.lineTo(scaledX, scaledY + scaledH);
        ctx.lineTo(scaledX + cornerSize, scaledY + scaledH);
        ctx.stroke();
        
        // Esquina inferior derecha
        ctx.beginPath();
        ctx.moveTo(scaledX + scaledW - cornerSize, scaledY + scaledH);
        ctx.lineTo(scaledX + scaledW, scaledY + scaledH);
        ctx.lineTo(scaledX + scaledW, scaledY + scaledH - cornerSize);
        ctx.stroke();
    }
    
    drawDetectionOverlay(detection) {
        const ctx = this.overlayCtx;
        const centerX = this.overlay.width / 2;
        const centerY = this.overlay.height / 2;
        const size = 100; // Tamaño del indicador
        
        // Configurar estilo del dibujo
        ctx.strokeStyle = '#00ff88';
        ctx.lineWidth = 4;
        ctx.fillStyle = 'rgba(0, 255, 136, 0.2)';
        
        // Dibujar según la forma detectada
        ctx.beginPath();
        
        if (detection.shape === 'circulo') {
            ctx.arc(centerX, centerY, size/2, 0, 2 * Math.PI);
            ctx.stroke();
            ctx.fill();
            
            // Texto indicador
            this.drawShapeLabel(centerX, centerY - size/2 - 30, '🔴 CÍRCULO', detection.confidence);
            
        } else if (detection.shape === 'cuadrado') {
            ctx.rect(centerX - size/2, centerY - size/2, size, size);
            ctx.stroke();
            ctx.fill();
            
            this.drawShapeLabel(centerX, centerY - size/2 - 30, '🟦 CUADRADO', detection.confidence);
            
        } else if (detection.shape === 'triangulo') {
            ctx.moveTo(centerX, centerY - size/2);
            ctx.lineTo(centerX - size/2, centerY + size/2);
            ctx.lineTo(centerX + size/2, centerY + size/2);
            ctx.closePath();
            ctx.stroke();
            ctx.fill();
            
            this.drawShapeLabel(centerX, centerY - size/2 - 30, '🔺 TRIÁNGULO', detection.confidence);
        }
        
        // Crosshair en el centro
        this.drawCrosshair(centerX, centerY);
    }
    
    drawShapeLabel(x, y, text, confidence) {
        const ctx = this.overlayCtx;
        
        ctx.font = 'bold 18px Arial';
        ctx.fillStyle = '#00ff88';
        ctx.textAlign = 'center';
        ctx.shadowColor = 'rgba(0, 0, 0, 0.8)';
        ctx.shadowBlur = 4;
        
        ctx.fillText(text, x, y);
        ctx.fillText(`${(confidence * 100).toFixed(1)}%`, x, y + 25);
        
        ctx.shadowBlur = 0; // Reset shadow
    }
    
    drawCrosshair(x, y) {
        const ctx = this.overlayCtx;
        const size = 20;
        
        ctx.strokeStyle = '#ff4444';
        ctx.lineWidth = 2;
        
        // Cruz horizontal y vertical
        ctx.beginPath();
        ctx.moveTo(x - size, y);
        ctx.lineTo(x + size, y);
        ctx.moveTo(x, y - size);
        ctx.lineTo(x, y + size);
        ctx.stroke();
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

// Inicializar la aplicación cuando se cargue la página
document.addEventListener('DOMContentLoaded', () => {
    new GeoLearnia();
});