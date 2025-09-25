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
        
        // ANÁLISIS INMEDIATO EN TIEMPO REAL
        this.analysisInterval = setInterval(async () => {
            await this.analyzeFrame();
        }, 100); // Cada 100ms para detección instantánea
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
            // Capturar frame INMEDIATAMENTE
            this.ctx.drawImage(this.video, 0, 0, this.canvas.width, this.canvas.height);
            
            // ANÁLISIS DIRECTO DE IMAGEN - Sin servidor
            const detection = this.detectShapeDirectly();
            
            // Debug - ver qué está devolviendo la detección
            if (detection && detection.found) {
                console.log('✅ Detección encontrada:', detection.shape, detection.confidence);
            } else {
                console.log('❌ No se detectó nada');
            }
            
            this.clearOverlay();
            
            if (detection && detection.found) {
                const { shape, confidence } = detection;
                
                // PUNTERO FIJO EN EL CENTRO SIEMPRE
                const screenCenterX = this.overlay.width / 2;
                const screenCenterY = this.overlay.height / 2;
                
                // MARCO SIMPLE en el centro
                this.drawSimpleFrame(shape, confidence, screenCenterX, screenCenterY);
                this.updateStatus(`🎯 ${shape.toUpperCase()} ${Math.round(confidence * 100)}%`, 'success');
                
            } else {
                // Punto de escaneo
                this.drawScanningPoint();
                this.updateStatus('🔍 Escaneando formas...', 'loading');
                this.result.style.display = 'none';
            }
            
        } catch (error) {
            this.drawScanningPoint();
        } finally {
            this.isAnalyzing = false;
        }
    }
    
    // DETECCIÓN DIRECTA DE FORMAS - Filtrada para objetos reales
    detectShapeDirectly() {
        const imageData = this.ctx.getImageData(0, 0, this.canvas.width, this.canvas.height);
        const data = imageData.data;
        const width = imageData.width;
        const height = imageData.height;
        
        // Convertir a escala de grises y detectar bordes
        const edges = this.detectEdges(data, width, height);
        
        // DETECCIÓN SIMPLE - SIN COMPLICACIONES
        const centerX = width / 2;
        const centerY = height / 2;
        const searchRadius = Math.min(width, height) / 3; // Área más grande para detectar mejor
        
        const contours = this.findContoursInArea(edges, width, height, centerX, centerY, searchRadius);
        
        console.log(`🔍 Contornos encontrados: ${contours.length}`);
        
        if (contours.length > 0) {
            // FILTROS SIMPLES - que funcionen
            const validContours = contours.filter(contour => {
                const area = this.calculateArea(contour.points);
                return area > 200 && area < 20000; // Más permisivo
            });
            
            console.log(`✅ Contornos válidos: ${validContours.length}`);
            
            if (validContours.length > 0) {
                const largest = validContours.reduce((max, contour) => 
                    this.calculateArea(contour.points) > this.calculateArea(max.points) ? contour : max
                );
                
                const shape = this.classifyShape(largest.points);
                console.log(`🔍 Clasificación: ${shape.name}, confianza: ${shape.confidence.toFixed(2)}`);
                
                // UMBRAL MÁS BAJO para que detecte más fácil
                if (shape.confidence > 0.4) { // Muy bajo para que funcione
                    // Centro simple que funciona bien
                    const centerX = largest.points.reduce((sum, p) => sum + p.x, 0) / largest.points.length;
                    const centerY = largest.points.reduce((sum, p) => sum + p.y, 0) / largest.points.length;
                    
                    return {
                        found: true,
                        shape: shape.name,
                        confidence: shape.confidence,
                        centerX: centerX,
                        centerY: centerY,
                        points: largest.points,
                        contour: largest.points
                    };
                }
            }
        }
        
        return { found: false };
    }
    
    // Buscar contornos solo en área específica
    findContoursInArea(edges, width, height, centerX, centerY, radius) {
        const visited = new Uint8Array(width * height);
        const contours = [];
        
        const minX = Math.max(0, Math.floor(centerX - radius));
        const maxX = Math.min(width, Math.floor(centerX + radius));
        const minY = Math.max(0, Math.floor(centerY - radius));
        const maxY = Math.min(height, Math.floor(centerY + radius));
        
        for (let y = minY; y < maxY; y++) {
            for (let x = minX; x < maxX; x++) {
                // Solo buscar cerca del centro
                const dist = Math.sqrt((x - centerX) * (x - centerX) + (y - centerY) * (y - centerY));
                if (dist > radius) continue;
                
                if (edges[y * width + x] === 255 && !visited[y * width + x]) {
                    const contour = this.traceContour(edges, visited, x, y, width, height);
                    if (contour.length > 20) { // Más puntos requeridos
                        contours.push({ points: contour });
                    }
                }
            }
        }
        
        return contours;
    }
    
    // Detección de bordes simple
    detectEdges(data, width, height) {
        const edges = new Uint8Array(width * height);
        const threshold = 50;
        
        for (let y = 1; y < height - 1; y++) {
            for (let x = 1; x < width - 1; x++) {
                const idx = (y * width + x) * 4;
                
                // Convertir a escala de grises
                const gray = (data[idx] + data[idx + 1] + data[idx + 2]) / 3;
                
                // Gradiente simple
                const gx = data[((y * width) + x + 1) * 4] - data[((y * width) + x - 1) * 4];
                const gy = data[((y + 1) * width + x) * 4] - data[((y - 1) * width + x) * 4];
                const gradient = Math.sqrt(gx * gx + gy * gy);
                
                edges[y * width + x] = gradient > threshold ? 255 : 0;
            }
        }
        
        return edges;
    }
    
    // Encontrar contornos básicos
    findContours(edges, width, height) {
        const visited = new Uint8Array(width * height);
        const contours = [];
        
        for (let y = 0; y < height; y++) {
            for (let x = 0; x < width; x++) {
                if (edges[y * width + x] === 255 && !visited[y * width + x]) {
                    const contour = this.traceContour(edges, visited, x, y, width, height);
                    if (contour.length > 10) {
                        contours.push({ points: contour });
                    }
                }
            }
        }
        
        return contours;
    }
    
    // Trazar contorno
    traceContour(edges, visited, startX, startY, width, height) {
        const points = [];
        const stack = [{ x: startX, y: startY }];
        
        while (stack.length > 0 && points.length < 1000) {
            const { x, y } = stack.pop();
            
            if (x < 0 || x >= width || y < 0 || y >= height) continue;
            if (visited[y * width + x] || edges[y * width + x] !== 255) continue;
            
            visited[y * width + x] = 1;
            points.push({ x, y });
            
            // Vecinos 8-conectados
            for (let dy = -1; dy <= 1; dy++) {
                for (let dx = -1; dx <= 1; dx++) {
                    if (dx === 0 && dy === 0) continue;
                    stack.push({ x: x + dx, y: y + dy });
                }
            }
        }
        
        return points;
    }
    
    // Clasificar forma basada en puntos del contorno - MEJORADO
    classifyShape(points) {
        if (points.length < 20) return { name: 'desconocido', confidence: 0.1 };
        
        // Calcular propiedades geométricas
        const hull = this.convexHull(points);
        if (hull.length < 3) return { name: 'desconocido', confidence: 0.1 };
        
        const area = this.calculateArea(hull);
        const perimeter = this.calculatePerimeter(hull);
        
        if (area < 100) return { name: 'desconocido', confidence: 0.1 };
        
        const circularity = (4 * Math.PI * area) / (perimeter * perimeter);
        const corners = this.detectCorners(hull);
        const aspectRatio = this.calculateAspectRatio(hull);
        
        // Clasificación mejorada
        if (circularity > 0.75) {
            // Muy circular
            return { name: 'circulo', confidence: Math.min(0.9, circularity + 0.1) };
        } else if (corners === 4 && aspectRatio > 0.7 && aspectRatio < 1.3) {
            // 4 esquinas y proporción cuadrada
            return { name: 'cuadrado', confidence: 0.85 };
        } else if (corners === 3) {
            // 3 esquinas claras
            return { name: 'triangulo', confidence: 0.8 };
        } else if (corners === 4) {
            // 4 esquinas pero no cuadrado perfecto - podría ser rectángulo/cuadrado
            return { name: 'cuadrado', confidence: 0.7 };
        } else if (circularity > 0.5 && corners <= 6) {
            // Forma redondeada
            return { name: 'circulo', confidence: 0.6 };
        }
        
        return { name: 'desconocido', confidence: 0.2 };
    }
    
    // Calcular relación de aspecto
    calculateAspectRatio(points) {
        let minX = Infinity, maxX = -Infinity;
        let minY = Infinity, maxY = -Infinity;
        
        points.forEach(p => {
            minX = Math.min(minX, p.x);
            maxX = Math.max(maxX, p.x);
            minY = Math.min(minY, p.y);
            maxY = Math.max(maxY, p.y);
        });
        
        const width = maxX - minX;
        const height = maxY - minY;
        
        return Math.min(width, height) / Math.max(width, height);
    }
    
    // Envolvente convexa simple
    convexHull(points) {
        if (points.length < 3) return points;
        
        points.sort((a, b) => a.x - b.x || a.y - b.y);
        
        const lower = [];
        for (let i = 0; i < points.length; i++) {
            while (lower.length >= 2 && this.cross(lower[lower.length-2], lower[lower.length-1], points[i]) <= 0) {
                lower.pop();
            }
            lower.push(points[i]);
        }
        
        const upper = [];
        for (let i = points.length - 1; i >= 0; i--) {
            while (upper.length >= 2 && this.cross(upper[upper.length-2], upper[upper.length-1], points[i]) <= 0) {
                upper.pop();
            }
            upper.push(points[i]);
        }
        
        upper.pop();
        lower.pop();
        return lower.concat(upper);
    }
    
    cross(O, A, B) {
        return (A.x - O.x) * (B.y - O.y) - (A.y - O.y) * (B.x - O.x);
    }
    
    calculateArea(points) {
        let area = 0;
        for (let i = 0; i < points.length; i++) {
            const j = (i + 1) % points.length;
            area += points[i].x * points[j].y;
            area -= points[j].x * points[i].y;
        }
        return Math.abs(area) / 2;
    }
    
    calculatePerimeter(points) {
        let perimeter = 0;
        for (let i = 0; i < points.length; i++) {
            const j = (i + 1) % points.length;
            const dx = points[j].x - points[i].x;
            const dy = points[j].y - points[i].y;
            perimeter += Math.sqrt(dx * dx + dy * dy);
        }
        return perimeter;
    }
    
    detectCorners(points) {
        if (points.length < 6) return 0;
        
        const corners = [];
        const minAngle = Math.PI * 0.4; // ~72 grados mínimo para considerar esquina
        const windowSize = Math.max(3, Math.floor(points.length * 0.05)); // Ventana adaptativa
        
        for (let i = 0; i < points.length; i++) {
            const prev = points[(i - windowSize + points.length) % points.length];
            const curr = points[i];
            const next = points[(i + windowSize) % points.length];
            
            // Vectores
            const v1 = {
                x: curr.x - prev.x,
                y: curr.y - prev.y
            };
            const v2 = {
                x: next.x - curr.x,
                y: next.y - curr.y
            };
            
            // Normalizar vectores
            const len1 = Math.sqrt(v1.x * v1.x + v1.y * v1.y);
            const len2 = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
            
            if (len1 > 5 && len2 > 5) { // Evitar vectores muy pequeños
                v1.x /= len1;
                v1.y /= len1;
                v2.x /= len2;
                v2.y /= len2;
                
                // Producto punto para ángulo
                const dotProduct = v1.x * v2.x + v1.y * v2.y;
                const angle = Math.abs(Math.acos(Math.max(-1, Math.min(1, dotProduct))));
                
                // Si el ángulo es significativo, es una esquina
                if (angle > minAngle) {
                    corners.push({ point: curr, angle: angle, index: i });
                }
            }
        }
        
        // Filtrar esquinas muy cercanas entre sí
        const filteredCorners = [];
        const minDistance = Math.sqrt(points.length) * 2; // Distancia mínima entre esquinas
        
        corners.sort((a, b) => b.angle - a.angle); // Ordenar por ángulo descendente
        
        for (const corner of corners) {
            let tooClose = false;
            for (const existing of filteredCorners) {
                const dist = Math.sqrt(
                    Math.pow(corner.point.x - existing.point.x, 2) +
                    Math.pow(corner.point.y - existing.point.y, 2)
                );
                if (dist < minDistance) {
                    tooClose = true;
                    break;
                }
            }
            
            if (!tooClose) {
                filteredCorners.push(corner);
            }
        }
        
        return filteredCorners.length;
    }
    
    calculateAngle(p1, p2, p3) {
        const v1 = { x: p1.x - p2.x, y: p1.y - p2.y };
        const v2 = { x: p3.x - p2.x, y: p3.y - p2.y };
        const dot = v1.x * v2.x + v1.y * v2.y;
        const mag1 = Math.sqrt(v1.x * v1.x + v1.y * v1.y);
        const mag2 = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
        return Math.acos(dot / (mag1 * mag2));
    }
    
    // Calcular límites reales del objeto detectado - SIMPLE Y FUNCIONAL
    calculateObjectBounds(contourPoints) {
        let minX = Infinity, maxX = -Infinity;
        let minY = Infinity, maxY = -Infinity;
        
        contourPoints.forEach(point => {
            minX = Math.min(minX, point.x);
            maxX = Math.max(maxX, point.x);
            minY = Math.min(minY, point.y);
            maxY = Math.max(maxY, point.y);
        });
        
        return {
            minX, maxX, minY, maxY,
            centerX: (minX + maxX) / 2,  // Centro simple que funciona
            centerY: (minY + maxY) / 2,  // Centro simple que funciona
            width: maxX - minX,
            height: maxY - minY
        };
    }
    
    // Marco CUADRADO FIJO en el centro - TRIPLICADO DE TAMAÑO
    drawSimpleFrame(shape, confidence, centerX, centerY) {
        const ctx = this.overlayCtx;
        
        // CUADRADO FIJO MÁS GRANDE - sin importar la forma
        const size = 450; // Triplicado de 150 a 450
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 4; // Línea más gruesa para el tamaño
        ctx.strokeRect(centerX - size/2, centerY - size/2, size, size);
        
        // Marco interior más pequeño
        ctx.strokeStyle = '#00ff00';
        ctx.lineWidth = 3;
        const innerSize = 360; // Triplicado de 120 a 360
        ctx.strokeRect(centerX - innerSize/2, centerY - innerSize/2, innerSize, innerSize);
        
        // PUNTERO FIJO en el centro (más grande también)
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(centerX, centerY, 10, 0, 2 * Math.PI); // Aumentado de 6 a 10
        ctx.fill();
        ctx.stroke();
        
        // Punto verde en el centro (más grande)
        ctx.fillStyle = '#00ff00';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 5, 0, 2 * Math.PI); // Aumentado de 3 a 5
        ctx.fill();
        
        // Texto arriba del cuadro (más grande)
        ctx.font = 'bold 20px Arial'; // Aumentado de 16px a 20px
        ctx.fillStyle = '#00ff00';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 3;
        ctx.textAlign = 'center';
        
        const text = `${shape.toUpperCase()} ${Math.round(confidence * 100)}%`;
        ctx.strokeText(text, centerX, centerY - 245); // Ajustado para el nuevo tamaño
        ctx.fillText(text, centerX, centerY - 245);
        ctx.textAlign = 'left';
    }
    
    // Dibujar marco según la forma detectada - PUNTERO FIJO EN EL CENTRO
    drawShapeFrame(shape, confidence, fixedCenterX, fixedCenterY, bounds) {
        const ctx = this.overlayCtx;
        
        // Color según confianza
        const color = confidence > 0.8 ? '#00ff00' : confidence > 0.6 ? '#ffff00' : '#ff8800';
        ctx.strokeStyle = color;
        ctx.lineWidth = 3;
        
        // Tamaño del marco basado en el objeto detectado pero centrado en la pantalla
        const frameSize = Math.max(bounds.width, bounds.height) + 30; // Tamaño base + padding
        const minSize = 80; // Tamaño mínimo
        const maxSize = 200; // Tamaño máximo
        const finalSize = Math.max(minSize, Math.min(maxSize, frameSize));
        
        if (shape === 'circulo') {
            // Para círculos: marco circular FIJO EN EL CENTRO
            const radius = finalSize / 2;
            ctx.beginPath();
            ctx.arc(fixedCenterX, fixedCenterY, radius, 0, 2 * Math.PI);
            ctx.stroke();
            
            // Círculo interior
            ctx.lineWidth = 2;
            ctx.beginPath();
            ctx.arc(fixedCenterX, fixedCenterY, radius * 0.6, 0, 2 * Math.PI);
            ctx.stroke();
            
        } else {
            // Para cuadrados y triángulos: marco rectangular FIJO EN EL CENTRO
            const halfSize = finalSize / 2;
            const frameX = fixedCenterX - halfSize;
            const frameY = fixedCenterY - halfSize;
            
            ctx.strokeRect(frameX, frameY, finalSize, finalSize);
            
            // Marco interior
            ctx.lineWidth = 2;
            const innerSize = finalSize * 0.7;
            const innerHalf = innerSize / 2;
            ctx.strokeRect(
                fixedCenterX - innerHalf, 
                fixedCenterY - innerHalf,
                innerSize,
                innerSize
            );
        }
        
        // PUNTERO FIJO EN EL CENTRO SIEMPRE
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        
        // Círculo blanco con borde negro
        ctx.beginPath();
        ctx.arc(fixedCenterX, fixedCenterY, 5, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
        
        // Punto interno del color del marco
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(fixedCenterX, fixedCenterY, 2, 0, 2 * Math.PI);
        ctx.fill();
        
        // Texto arriba del marco
        ctx.font = 'bold 14px Arial';
        ctx.fillStyle = color;
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 2;
        ctx.textAlign = 'center';
        
        const text = `${shape.toUpperCase()} ${Math.round(confidence * 100)}%`;
        ctx.strokeText(text, fixedCenterX, fixedCenterY - finalSize/2 - 15);
        ctx.fillText(text, fixedCenterX, fixedCenterY - finalSize/2 - 15);
        ctx.textAlign = 'left';
    }
    
    // CUADRADO DE ESCANEO FIJO en el centro - TRIPLICADO
    drawScanningPoint() {
        const ctx = this.overlayCtx;
        const centerX = this.overlay.width / 2;
        const centerY = this.overlay.height / 2;
        
        // CUADRADO FIJO de detección MÁS GRANDE
        const size = 450; // Triplicado de 150 a 450
        ctx.strokeStyle = 'rgba(255,255,255,0.6)';
        ctx.lineWidth = 3; // Línea más gruesa
        ctx.strokeRect(centerX - size/2, centerY - size/2, size, size);
        
        // Cuadrado interior pulsante MÁS GRANDE
        const pulseSize = 360 + Math.sin(Date.now() / 400) * 20; // Triplicado y más pulso
        ctx.strokeStyle = 'rgba(255,255,255,0.4)';
        ctx.lineWidth = 2;
        ctx.strokeRect(centerX - pulseSize/2, centerY - pulseSize/2, pulseSize, pulseSize);
        
        // Punto central MÁS GRANDE
        ctx.fillStyle = '#ffffff';
        ctx.beginPath();
        ctx.arc(centerX, centerY, 8, 0, 2 * Math.PI); // Aumentado de 4 a 8
        ctx.fill();
        
        // Esquinas del cuadrado para mejor visibilidad - MÁS GRANDES
        const cornerLength = 60; // Triplicado de 20 a 60
        ctx.strokeStyle = 'rgba(255,255,255,0.8)';
        ctx.lineWidth = 4; // Línea más gruesa
        
        const halfSize = size / 2;
        
        // Esquina superior izquierda
        ctx.beginPath();
        ctx.moveTo(centerX - halfSize, centerY - halfSize + cornerLength);
        ctx.lineTo(centerX - halfSize, centerY - halfSize);
        ctx.lineTo(centerX - halfSize + cornerLength, centerY - halfSize);
        ctx.stroke();
        
        // Esquina superior derecha
        ctx.beginPath();
        ctx.moveTo(centerX + halfSize - cornerLength, centerY - halfSize);
        ctx.lineTo(centerX + halfSize, centerY - halfSize);
        ctx.lineTo(centerX + halfSize, centerY - halfSize + cornerLength);
        ctx.stroke();
        
        // Esquina inferior izquierda
        ctx.beginPath();
        ctx.moveTo(centerX - halfSize, centerY + halfSize - cornerLength);
        ctx.lineTo(centerX - halfSize, centerY + halfSize);
        ctx.lineTo(centerX - halfSize + cornerLength, centerY + halfSize);
        ctx.stroke();
        
        // Esquina inferior derecha
        ctx.beginPath();
        ctx.moveTo(centerX + halfSize - cornerLength, centerY + halfSize);
        ctx.lineTo(centerX + halfSize, centerY + halfSize);
        ctx.lineTo(centerX + halfSize, centerY + halfSize - cornerLength);
        ctx.stroke();
        
        // Texto instructivo MÁS GRANDE
        ctx.font = 'bold 16px Arial'; // Aumentado de 12px a 16px
        ctx.fillStyle = 'rgba(255,255,255,0.8)';
        ctx.textAlign = 'center';
        ctx.fillText('Coloca objeto dentro del cuadro', centerX, centerY + 280); // Ajustado para el nuevo tamaño
        ctx.textAlign = 'left';
    }
    
    // ESTILO DE RECONOCIMIENTO FACIAL - Marco con esquinas y etiqueta
    drawFaceDetectionStyle(shape, confidence) {
        const ctx = this.overlayCtx;
        const centerX = this.overlay.width / 2;
        const centerY = this.overlay.height / 2;
        const boxSize = 180;
        
        // Determinar color según confianza
        let frameColor = '#00ff00'; // Verde alta confianza
        if (confidence < 0.7) frameColor = '#ffff00'; // Amarillo media
        if (confidence < 0.5) frameColor = '#ff8800'; // Naranja baja
        
        // Coordenadas del marco
        const x = centerX - boxSize / 2;
        const y = centerY - boxSize / 2;
        
        // Marco principal
        ctx.strokeStyle = frameColor;
        ctx.lineWidth = 3;
        ctx.strokeRect(x, y, boxSize, boxSize);
        
        // Esquinas reforzadas (efecto reconocimiento facial)
        ctx.lineWidth = 5;
        const cornerLength = 25;
        
        // Esquina superior izquierda
        ctx.beginPath();
        ctx.moveTo(x, y + cornerLength);
        ctx.lineTo(x, y);
        ctx.lineTo(x + cornerLength, y);
        ctx.stroke();
        
        // Esquina superior derecha
        ctx.beginPath();
        ctx.moveTo(x + boxSize - cornerLength, y);
        ctx.lineTo(x + boxSize, y);
        ctx.lineTo(x + boxSize, y + cornerLength);
        ctx.stroke();
        
        // Esquina inferior izquierda
        ctx.beginPath();
        ctx.moveTo(x, y + boxSize - cornerLength);
        ctx.lineTo(x, y + boxSize);
        ctx.lineTo(x + cornerLength, y + boxSize);
        ctx.stroke();
        
        // Esquina inferior derecha
        ctx.beginPath();
        ctx.moveTo(x + boxSize - cornerLength, y + boxSize);
        ctx.lineTo(x + boxSize, y + boxSize);
        ctx.lineTo(x + boxSize, y + boxSize - cornerLength);
        ctx.stroke();
        
        // Etiqueta con nombre de la figura
        this.drawShapeLabel(shape, confidence, x, y - 15);
    }
    
    // Etiqueta con el nombre de la figura detectada
    drawShapeLabel(shape, confidence, x, y) {
        const ctx = this.overlayCtx;
        const text = `${shape.toUpperCase()} ${Math.round(confidence * 100)}%`;
        
        // Configurar fuente
        ctx.font = 'bold 16px Arial';
        const textMetrics = ctx.measureText(text);
        const textWidth = textMetrics.width;
        const padding = 8;
        
        // Fondo de la etiqueta
        ctx.fillStyle = 'rgba(0, 0, 0, 0.8)';
        ctx.fillRect(x - padding, y - 22, textWidth + padding * 2, 22);
        
        // Texto blanco
        ctx.fillStyle = '#ffffff';
        ctx.fillText(text, x, y - 6);
    }
    
    // Marco de búsqueda cuando no hay detección
    drawSearchFrame() {
        const ctx = this.overlayCtx;
        const centerX = this.overlay.width / 2;
        const centerY = this.overlay.height / 2;
        const frameSize = 200;
        
        // Marco punteado
        ctx.strokeStyle = 'rgba(255, 255, 255, 0.6)';
        ctx.lineWidth = 2;
        ctx.setLineDash([10, 5]);
        
        const x = centerX - frameSize / 2;
        const y = centerY - frameSize / 2;
        
        ctx.strokeRect(x, y, frameSize, frameSize);
        
        // Instrucciones
        ctx.setLineDash([]);
        ctx.font = 'bold 14px Arial';
        ctx.fillStyle = 'rgba(255, 255, 255, 0.8)';
        ctx.textAlign = 'center';
        ctx.fillText('Coloca una figura aquí', centerX, y - 10);
        ctx.fillText('○  □  △', centerX, y + frameSize + 20);
        
        // Restaurar alineación
        ctx.textAlign = 'left';
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
        // DESHABILITADO - El usuario no quiere el cuadro grande de resultados
        // Solo usar el texto pequeño en el marco de detección
        /*
        const shapeEmojis = {
            'circulo': '🔴',
            'cuadrado': '🟦', 
            'triangulo': '🔺',
            'desconocido': '❓'
        };
        
        this.shapeResult.textContent = `${shapeEmojis[shape] || '🔍'} ${shape.toUpperCase()}`;
        this.confidenceResult.textContent = `Confianza: ${(confidence * 100).toFixed(1)}%`;
        this.result.style.display = 'flex';
        */
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