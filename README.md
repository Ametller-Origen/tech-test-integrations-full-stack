# Prueba Técnica de Integración de Sistemas

## Descripción General

Esta prueba técnica está diseñada para evaluar habilidades de desarrollo full-stack mediante dos fases complementarias:

- **Fase 1 (Backend):** Construir la capa de integración entre dos sistemas con interfaces diferentes
- **Fase 2 (Frontend):** Crear una aplicación web para monitorear y gestionar la sincronización de datos

Ambas fases utilizan los mismos sistemas backend (Sistema A y Sistema B) como base.

## Los Sistemas

### Sistema A - Sistema de Inventario
**Ubicación:** `./system-a/`

Un sistema de gestión de inventario que rastrea los niveles de stock de productos en múltiples ubicaciones (tiendas y almacén central).

**Características:**
- API REST con formato JSON
- Documentación OpenAPI 3.0 disponible en `/openapi.json`
- Base de datos SQLite

**Endpoints principales:**
- Listar todas las ubicaciones
- Consultar niveles de stock en una ubicación específica
- Procesar actualizaciones de inventario (incrementos, decrementos, inventarios completos)

### Sistema B - Sistema de Cumplimiento de Pedidos
**Ubicación:** `./system-b/`

Un sistema de gestión de pedidos que maneja órdenes de clientes y necesita conocer los niveles de stock disponibles.

**Características:**
- API basada en XML (estilo tradicional)
- Documentación en archivo de texto (`API_DOCUMENTATION.txt`)
- Base de datos SQLite

**Endpoints principales:**
- Listar pedidos realizados
- Recibir actualizaciones de niveles de stock

## Despliegue Local

### Requisitos Previos
- Docker Desktop para Windows instalado y en ejecución
- Docker Compose (incluido con Docker Desktop)

### Pasos para Iniciar los Sistemas

1. **Iniciar Sistema A (Inventario)**
   ```bash
   cd system-a
   docker-compose up -d
   ```
   El sistema estará disponible en: `http://localhost:5001`

   Documentación OpenAPI: `http://localhost:5001/openapi.json`

   Interfaz Swagger UI: `http://localhost:5001/docs`

2. **Iniciar Sistema B (Pedidos)**
   ```bash
   cd system-b
   docker-compose up -d
   ```
   El sistema estará disponible en: `http://localhost:5002`

   Documentación: Ver archivo `system-b/API_DOCUMENTATION.txt`

### Reiniciar Datos de Prueba

Cada sistema incluye un script para resetear la base de datos con datos de prueba:

**Sistema A:**
```bash
cd system-a
docker-compose exec app python reset_database.py
```

**Sistema B:**
```bash
cd system-b
docker-compose exec app python reset_database.py
```

### Detener los Sistemas

```bash
# En cada directorio:
docker-compose down
```

## Fase 1: Integración Backend

**Objetivo:** Crear un componente de integración independiente que:

1. **Sincronice el inventario del Sistema A hacia el Sistema B**
   - Lee los niveles de stock desde el Sistema A (JSON/REST)
   - Transforma los datos al formato XML requerido
   - Envía las actualizaciones al Sistema B (XML)

2. **Procese los pedidos del Sistema B**
   - Lee los pedidos desde el Sistema B (XML)
   - Actualiza los niveles de inventario en el Sistema A (JSON/REST)
   - Maneja correctamente los errores (ej: stock insuficiente)

**Documentación detallada:**
- 📖 **[INTEGRATION_GUIDE.md](INTEGRATION_GUIDE.md)** - Especificación completa de la tarea
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Diagramas y arquitectura técnica
- 🚀 **[QUICK_START.md](QUICK_START.md)** - Guía de inicio rápido

**Duración estimada:** 2-4 horas

---

## Fase 2: Frontend Monitor de Sincronización

**Objetivo:** Crear una aplicación web que permita:

1. **Monitorear el estado de sincronización**
   - Visualizar estado actual (sincronizado/desincronizado/error)
   - Mostrar timestamp y estadísticas de última sincronización
   - Alertar cuando los datos están desactualizados

2. **Comparar datos entre sistemas**
   - Tabla comparativa de stock en Sistema A vs Sistema B
   - Resaltar discrepancias visualmente
   - Filtrar y buscar productos

3. **Ejecutar sincronización manual**
   - Botón para sincronizar datos (A → B)
   - Mostrar progreso y resultados
   - Historial de sincronizaciones

**Documentación detallada:**
- 📖 **[FRONTEND_SPEC.md](FRONTEND_SPEC.md)** - Especificación completa de requisitos
- 🎨 **[FRONTEND_MOCKUPS.md](FRONTEND_MOCKUPS.md)** - Wireframes y guías visuales

**Duración estimada:** 3-4 horas

**Stack tecnológico:** Libre elección (React, Vue, Angular, Svelte, etc.)

## Estructura de Directorios

```
.
├── README.md (este archivo)
├── system-a/
│   ├── app.py
│   ├── database.py
│   ├── reset_database.py
│   ├── requirements.txt
│   ├── Dockerfile
│   └── docker-compose.yml
└── system-b/
    ├── app.py
    ├── database.py
    ├── reset_database.py
    ├── requirements.txt
    ├── Dockerfile
    ├── docker-compose.yml
    └── API_DOCUMENTATION.txt
```

## Evaluación

#### Fase 1 - Backend
Se tendrá en cuenta:
- **Funcionalidad** ¿La integración funciona correctamente?
- **Transformación de datos** ¿Se manejan correctamente las diferencias entre JSON y XML?
- **Manejo de errores** ¿Se gestionan apropiadamente los casos de error?
- **Calidad del código** ¿Es el código limpio, legible y mantenible?

#### Fase 2 - Frontend
Se tendrá en cuenta:
- **Funcionalidad** ¿La aplicación cumple todos los requisitos?
- **Calidad del código** ¿Código organizado y mantenible?
- **UI/UX** ¿Diseño profesional y usabilidad intuitiva?
- **Integración con APIs** ¿Manejo correcto de JSON y XML?


## Soporte

Si encuentras problemas con el despliegue de los sistemas A o B, consulta los logs:

```bash
# Ver logs del Sistema A
cd system-a
docker-compose logs -f

# Ver logs del Sistema B
cd system-b
docker-compose logs -f
```

¡Buena suerte!
