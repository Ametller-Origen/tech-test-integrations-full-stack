# Guía de Inicio Rápido

## Preparación del Entorno (5 minutos)

### 1. Verificar Docker
```bash
docker --version
docker-compose --version
```

Si no tienes Docker instalado, descárgalo desde: https://www.docker.com/products/docker-desktop

### 2. Iniciar Sistema A (Inventario)
```bash
cd system-a
docker-compose up -d
```

Espera 10-15 segundos para que el sistema inicie completamente.

**Verificar que funciona:**
```bash
curl http://localhost:5001/health
```

Deberías ver: `{"status":"healthy","service":"inventory-system"}`

**Ver documentación:**
Abre en tu navegador: http://localhost:5001/docs

### 3. Iniciar Sistema B (Pedidos)
```bash
cd system-b
docker-compose up -d
```

Espera 10-15 segundos para que el sistema inicie completamente.

**Verificar que funciona:**
```bash
curl http://localhost:5002/health
```

Deberías ver un XML con status "healthy"

## Resetear Bases de Datos

Si necesitas volver al estado inicial:

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

## Ver Logs (Para Debugging)

**Sistema A:**
```bash
cd system-a
docker-compose logs -f
```

**Sistema B:**
```bash
cd system-b
docker-compose logs -f
```

Presiona `Ctrl+C` para salir de los logs.

## Detener los Sistemas

Cuando termines:

```bash
# En cada directorio:
cd system-a
docker-compose down

cd system-b
docker-compose down
```

## Troubleshooting

### Los puertos ya están en uso
Si ves un error como "port is already allocated":
- Verifica que no tengas otros servicios usando los puertos 5001 o 5002
- En Windows: `netstat -ano | findstr :5001`
- Detén el proceso que esté usando el puerto o cambia el puerto en docker-compose.yml

### El contenedor no inicia
```bash
# Ver logs detallados
docker-compose logs

# Reconstruir imagen
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

## Siguiente Paso

Lee `INTEGRATION_GUIDE.md` para entender qué debes construir.

## URLs de Referencia Rápida

- **Sistema A:**
  - Servicio: http://localhost:5001
  - Documentación interactiva: http://localhost:5001/docs
  - OpenAPI spec: http://localhost:5001/openapi.json

- **Sistema B:**
  - Servicio: http://localhost:5002
  - Documentación: Ver archivo `system-b/API_DOCUMENTATION.txt`

¡Todo listo! Ahora puedes comenzar a trabajar en tu integración.
