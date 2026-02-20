# Guía de Integración - Para el Candidato

## Objetivo de la Prueba

Tu tarea es crear un componente de integración que conecte los dos sistemas proporcionados:
- **Sistema A** (Inventario) - API REST con JSON
- **Sistema B** (Pedidos) - API XML (legacy)

## Lo Que Debes Construir

Crea un servicio/script de integración independiente que:

### 1. Sincronización de Inventario (Sistema A → Sistema B)

Implementa una funcionalidad que:
- Lee los niveles de stock completos desde Sistema A usando su API REST
- Transforma los datos de JSON a XML
- Envía los niveles de stock al Sistema B usando su endpoint XML

**Puntos clave:**
- El Sistema A expone `/api/inventory` que devuelve JSON con todos los niveles de stock
- El Sistema B espera recibir XML en `/api/stock/update`
- Debes mapear correctamente los campos entre ambos formatos
- Considera manejar errores de red y validación

### 2. Procesamiento de Pedidos (Sistema B → Sistema A)

Implementa una funcionalidad que:
- Lee los pedidos pendientes desde Sistema B
- Para cada pedido, actualiza el inventario en Sistema A (decrementando stock)
- Maneja casos de error (stock insuficiente, productos no encontrados)

**Puntos clave:**
- El Sistema B expone `/api/orders?status=pending` que devuelve XML
- El Sistema A tiene `/api/inventory/update` para actualizar stock (acepta JSON)
- Debes transformar de XML a JSON
- Los pedidos tienen múltiples items que deben procesarse
- Maneja transacciones: si un item falla, ¿qué hacer con el resto?

## Formato de Datos

### Sistema A - Inventario Completo (JSON)
```json
{
  "success": true,
  "data": [
    {
      "location_code": "STORE001",
      "location_name": "Tienda Centro",
      "location_type": "store",
      "sku": "SKU001",
      "product_name": "Laptop HP ProBook 450",
      "quantity": 5
    }
  ]
}
```

### Sistema B - Actualización de Stock (XML)
```xml
<stock_update>
  <location>
    <location_code>STORE001</location_code>
    <products>
      <product>
        <sku>SKU001</sku>
        <product_name>Laptop HP ProBook 450</product_name>
        <quantity>5</quantity>
      </product>
    </products>
  </location>
</stock_update>
```

### Sistema B - Pedidos (XML)
```xml
<orders_response>
  <status>success</status>
  <orders>
    <item>
      <order_number>ORD-2024-001</order_number>
      <location_code>STORE001</location_code>
      <items>
        <item>
          <sku>SKU001</sku>
          <quantity>2</quantity>
        </item>
      </items>
    </item>
  </orders>
</orders_response>
```

### Sistema A - Actualización de Inventario (JSON)
```json
{
  "location_code": "STORE001",
  "sku": "SKU001",
  "quantity": 2,
  "operation": "decrement"
}
```

## Consideraciones de Implementación

### Lenguaje y Framework
Puedes usar cualquier lenguaje o framework que prefieras:
- Python (requests, xml.etree, Flask/FastAPI)
- Node.js (axios, xml2js, Express)
- Java (Spring Boot, HttpClient, JAXB)
- C# (.NET, HttpClient, XmlSerializer)
- Otro de tu elección

### Estructura Sugerida
```
integration/
├── README.md           # Instrucciones de uso
├── requirements.txt    # Dependencias (Python)
├── package.json        # Dependencias (Node.js)
├── sync_inventory.py   # Script de sincronización de inventario
├── process_orders.py   # Script de procesamiento de pedidos
└── tests/             # Tests unitarios (opcional pero valorado)
```

### Aspectos a Considerar

1. **Transformación de Datos**
   - Mapeo correcto entre JSON y XML
   - Agrupación de datos por ubicación (para el XML de stock)
   - Extracción correcta de datos anidados

2. **Manejo de Errores**
   - Validar respuestas de las APIs
   - Manejar timeouts de red
   - Loggear errores apropiadamente
   - Stock insuficiente en pedidos

3. **Calidad del Código**
   - Código limpio y legible
   - Funciones con responsabilidades claras
   - Constantes para URLs y configuración
   - Comentarios donde sea necesario

4. **Documentación**
   - README claro con instrucciones de instalación
   - Ejemplos de uso
   - Descripción de decisiones de diseño

## Ejemplos de Uso Esperado

Tu integración debería poder ejecutarse así:

```bash
# Sincronizar inventario de A a B
python sync_inventory.py

# Procesar pedidos pendientes
python process_orders.py

# O un script único
python integration.py --sync-inventory
python integration.py --process-orders
```

## Criterios de Evaluación

1. **Funcionalidad**
   - ¿La integración funciona correctamente?
   - ¿Se sincronizan los datos apropiadamente?

2. **Transformación de Datos**
   - ¿Se manejan correctamente JSON y XML?
   - ¿Los datos se mapean correctamente?

3. **Manejo de Errores**
   - ¿Se gestionan apropiadamente los errores?
   - ¿Hay logging útil?

4. **Calidad del Código**
   - ¿Es el código limpio y mantenible?
   - ¿Está bien documentado?

## Entrega

Crea un directorio `integration/` con:
- Código fuente
- README.md con instrucciones
- Archivo de dependencias
- Cualquier otro archivo necesario

Tu código deberá subirse en una rama independiente del repositorio.

## Recursos

- Sistema A: http://localhost:5001
  - Documentación: http://localhost:5001/docs
  - OpenAPI: http://localhost:5001/openapi.json

- Sistema B: http://localhost:5002
  - Documentación: Ver `system-b/API_DOCUMENTATION.txt`

## Preguntas Frecuentes

**P: ¿Debo crear una interfaz de usuario?**
R: No, un script de línea de comandos es suficiente.

**P: ¿Debo hacer que se ejecute automáticamente (como un servicio)?**
R: No es necesario, pero si implementas un scheduler/cron está bien (no es requerido).

**P: ¿Puedo usar librerías externas?**
R: Sí, puedes usar cualquier librería que te ayude.

**P: ¿Debo escribir tests?**
R: No es obligatorio, pero es valorado positivamente.

**P: ¿Cuánto tiempo debería tomar?**
R: La prueba está diseñada para completarse en 2-4 horas.

**P: Los sistemas no responden, ¿qué hago?**
R: Verifica que Docker esté en ejecución y que hayas ejecutado `docker-compose up -d` en cada directorio de sistema. Revisa los logs con `docker-compose logs -f`.

¡Buena suerte!
