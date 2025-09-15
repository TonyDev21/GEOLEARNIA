# 🔄 Guía para Actualizar el Repositorio Git

## 📋 Comandos Básicos para Subir Cambios

### 1️⃣ Verificar Estado del Repositorio
```bash
git status
```
*Muestra qué archivos han cambiado*

### 2️⃣ Añadir Archivos al Staging
```bash
# Añadir todos los archivos modificados
git add .

# O añadir archivos específicos
git add README.md
git add requirements.txt
git add "Proyecto_SI/templates/pointer.html"
```

### 3️⃣ Hacer Commit con Mensaje Descriptivo
```bash
git commit -m "📝 Actualizar documentación y reorganizar código"

# O con mensaje más detallado
git commit -m "✨ Mejoras principales:
- Actualizar README.md con nueva funcionalidad
- Reorganizar web_pointer.py separando HTML/CSS
- Actualizar requirements.txt con versiones correctas
- Añadir guía de instalación INSTALACION.md"
```

### 4️⃣ Subir Cambios al Repositorio
```bash
git push origin main
```

## 🔄 Flujo Completo de Actualización

```bash
# 1. Verificar cambios
git status

# 2. Añadir archivos
git add .

# 3. Commit con mensaje
git commit -m "🎯 Reorganización completa del proyecto y documentación actualizada"

# 4. Subir al repositorio
git push origin main
```

## 📊 Comandos de Verificación

### Ver Historial de Commits
```bash
git log --oneline
```

### Ver Diferencias
```bash
# Ver qué cambió en un archivo
git diff README.md

# Ver todos los cambios
git diff
```

### Ver Ramas
```bash
git branch -a
```

## 🔧 Comandos Útiles Adicionales

### Deshacer Cambios (Antes de Commit)
```bash
# Deshacer cambios en un archivo específico
git checkout -- README.md

# Deshacer todos los cambios
git checkout -- .
```

### Crear Nueva Rama para Funcionalidad
```bash
# Crear y cambiar a nueva rama
git checkout -b nueva-funcionalidad

# Subir nueva rama
git push origin nueva-funcionalidad
```

### Actualizar desde el Repositorio Remoto
```bash
# Obtener últimos cambios
git pull origin main
```

## 📝 Mensajes de Commit Recomendados

### Tipos de Cambios
- `✨ feat:` Nueva funcionalidad
- `🐛 fix:` Corrección de errores
- `📝 docs:` Actualización de documentación
- `🎨 style:` Cambios de formato/estilo
- `♻️ refactor:` Reorganización de código
- `🚀 perf:` Mejoras de rendimiento
- `✅ test:` Añadir o actualizar tests

### Ejemplos de Buenos Commits
```bash
git commit -m "✨ feat: Añadir sistema de puntero central para detección precisa"
git commit -m "📝 docs: Actualizar README con nuevas instrucciones de instalación"
git commit -m "♻️ refactor: Separar HTML/CSS de web_pointer.py en archivos independientes"
git commit -m "🐛 fix: Corregir error de streaming de video en cámara"
```

## 🎯 Para Este Proyecto Específico

### Subir los Cambios Actuales
```bash
cd "C:\Users\antho\OneDrive\Escritorio\Proyects\GEOLEARNIA"

# Verificar cambios
git status

# Añadir todos los archivos
git add .

# Commit con mensaje descriptivo
git commit -m "🎯 Reorganización completa del proyecto GEOLEARNIA

✨ Nuevas funcionalidades:
- Sistema de puntero central optimizado
- Separación de HTML/CSS en archivos independientes
- Interfaz web mejorada con templates Flask

📝 Documentación actualizada:
- README.md completamente renovado
- Guía de instalación detallada (INSTALACION.md)
- Requirements.txt con versiones actualizadas

♻️ Reorganización de código:
- web_pointer.py limpio sin HTML embebido
- Templates en templates/pointer.html
- Estilos CSS en static/css/styles.css"

# Subir al repositorio
git push origin main
```

## ✅ Verificación Final

Después de hacer push, verifica en GitHub que:
- ✅ Los archivos se subieron correctamente
- ✅ El README.md se ve bien formateado
- ✅ Las carpetas templates/ y static/ están presentes
- ✅ Los commits aparecen en el historial

---
*¡Tu proyecto GEOLEARNIA estará actualizado y bien documentado! 🚀*