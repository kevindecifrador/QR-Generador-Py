# QRStudio - Generador Profesional de Códigos QR Personalizados 🚀🎨

Aplicación de escritorio con interfaz gráfica (GUI) moderna desarrollada a la medida para el **Departamento de Comunicación y Difusión del Instituto Tecnológico de Chilpancingo (TecNM)**, utilizada activamente para la automatización y branding de activos digitales institucionales.

## 📌 El Problema
El personal administrativo y de diseño institucional requería generar códigos QR de forma masiva para los flyers, anuncios y posts de la página oficial. Las herramientas web gratuitas convencionales limitan la personalización visual, imponen publicidad, caducan, no permiten la inserción segura de logotipos corporativos y presentan riesgos de privacidad al procesar enlaces institucionales en servidores externos.

## 💡 La Solución
**QRStudio** es una herramienta de escritorio ligera y autónoma que permite al departamento diseñar códigos QR con calidad de imprenta en segundos. La aplicación procesa toda la lógica localmente y ofrece características avanzadas de diseño como renderizado de módulos redondeados, inyección proporcional de logotipos con capas de aislamiento y enmascaramiento por canal alfa, exportando archivos PNG de alta fidelidad con transparencia nativa.

---

## 🛠️ Stack Tecnológico

* **Lenguaje de Programación:** Python 3.
* **Interfaz Gráfica de Usuario (GUI):** `tkinter` potenciado con **`ttkbootstrap`** (Aplicando el esquema de diseño moderno e institucional *Superhero*).
* **Motor de Generación QR:** `qrcode` con soporte de renderizado estilizado (`StyledPilImage`, `RoundedModuleDrawer`).
* **Procesamiento de Imágenes (Graphics Engine):** **Pillow (PIL)** encargado de la manipulación binaria de mapas de bits, máscaras de opacidad y remuestreo de vectores lógicos (`LANCZOS`).

---

## 🌟 Características Avanzadas e Ingeniería de Código

El software destaca por implementar soluciones eficientes a nivel de código para garantizar la legibilidad del código QR sin sacrificar el diseño estético:

* **Estructura Reactiva (Real-Time Preview):** Mediante el mapeo de eventos del sistema operativo (`<KeyRelease>`), la aplicación recalcula y re-renderiza la matriz del QR en tiempo real conforme el usuario escribe, ajustando dinámicamente las dimensiones a la ventana.
* **Aislamiento de Logotipos Corporativos:** Para evitar que los módulos binarios del QR se mezclen con el logo (lo que rompería la legibilidad), el script calcula el centro geométrico exacto de la matriz, superpone un cuadro de protección del color del fondo y estampa el isotipo de forma proporcional.
* **Enmascaramiento Alfa Real (Anti-Clipping Mask):** El redondeo exterior del código QR no utiliza parches de color; genera dinámicamente un canal de transparencia real (`RGBA`) aplicando una máscara con niveles de gris (`L`), garantizando que el QR pueda usarse sobre cualquier fondo o diseño publicitario.

---

## 🏗️ Flujo Lógico de la Aplicación
    [ Entrada de Enlace/Texto ] ✏️ (Actualización dinámica al teclear)
    │
    ▼
    ┌────────────────────────────────────────────────────────┐
    │   PROCESAMIENTO GRÁFICO LOCAL (Pillow Engine)          │
    ├────────────────────────────────────────────────────────┤
    │  1. Generación de Matriz Base (qrcode Core)            │
    │  2. Renderizado de Módulos (Square/Rounded Drawer)     │
    │  3. Aplicación de Máscara de Color (RGB Mask)          │
    │  4. Estampado de Logotipo + Capa de Protección        │
    │  5. Recorte de Esquinas por Canal Alfa (Opacity Mask)   │
    └──────────────────────────┬─────────────────────────────┘
    │
    ▼
    [ Exportación a PNG Nativo ] 💾


## ⚙️ Estructura del Proyecto

Al ser una herramienta utilitaria compacta, el código fuente está centralizado bajo una arquitectura orientada a objetos para facilitar su mantenimiento:

    QR-Generator-TecNM/
    ├── qr_studio.py        # Código fuente principal, inicialización de GUI y lógica Pillow
    ├── requirements.txt    # Dependencias del entorno (qrcode, pillow, ttkbootstrap)
    └── README.md           # Documentación técnica del proyecto

## 📦 Distribución y Despliegue (Standalone Execution)
Para garantizar una experiencia de usuario óptima y mitigar la fricción de instalación en equipos administrativos sin conocimientos técnicos, el software fue empaquetado y compilado de forma nativa. Se distribuye dentro de un archivo comprimido que contiene el ejecutable binario independiente, permitiendo su ejecución inmediata (*portable*) en los entornos de trabajo del departamento sin requerir la instalación previa de Python o dependencias de consola.

---

## 🛡️ Licencia y Créditos
Desarrollado de forma integral por **Kevin Sánchez** (2026) para el Tecnológico Nacional de México Campus Chilpancingo.
