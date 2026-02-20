# Mockups y Wireframes - Monitor de Sincronización

Este documento proporciona wireframes y guías visuales para el Monitor de Sincronización de Stock.

> **Nota:** Estos son wireframes de referencia. El candidato tiene libertad creativa en el diseño específico, siempre que cumpla con los requisitos funcionales.

## Vista Principal - Desktop

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Monitor de Sincronización de Stock                      [Auto-refresh]│
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ ESTADO DE SINCRONIZACIÓN                                         │  │
│  │                                                                  │  │
│  │  [🟢 Sincronizado]        Última sincronización: hace 5 minutos  │  │
│  │                                                                  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌──────┐  │  │
│  │  │   Total     │  │ Sincroniza- │  │ Discrepan-  │  │ Solo │  │  │
│  │  │  Productos  │  │    dos      │  │    cias     │  │ en A │  │  │
│  │  │     32      │  │     28      │  │      3      │  │  1   │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └──────┘  │  │
│  │                                                                  │  │
│  │  [Verificar Estado]  [Sincronizar Ahora]                        │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ⚠️ Advertencia: 3 productos tienen discrepancias significativas   [X] │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ COMPARACIÓN DE STOCK                                             │  │
│  │                                                                  │  │
│  │  Filtros:  [Todas las ubicaciones ▼] [Todos los estados ▼]      │  │
│  │           [Buscar por SKU o nombre...]                           │  │
│  │                                                                  │  │
│  │ ┌────────┬──────┬─────────────┬──────┬──────┬─────┬──────────┐ │  │
│  │ │Ubicac. │ SKU  │  Producto   │Sist A│Sist B│Dif. │ Estado   │ │  │
│  │ ├────────┼──────┼─────────────┼──────┼──────┼─────┼──────────┤ │  │
│  │ │STORE001│SKU001│Laptop HP    │  5   │  5   │  0  │🟢 Sync   │ │  │
│  │ │STORE001│SKU002│Mouse Logic. │  15  │  15  │  0  │🟢 Sync   │ │  │
│  │ │STORE001│SKU003│Teclado Cors.│  10  │  8   │ +2  │🟡 Dif.   │ │  │
│  │ │STORE001│SKU004│Monitor Dell │  8   │  8   │  0  │🟢 Sync   │ │  │
│  │ │STORE002│SKU001│Laptop HP    │  3   │  2   │ +1  │🟡 Dif.   │ │  │
│  │ │STORE002│SKU002│Mouse Logic. │  18  │  5   │+13  │🔴 Dif.   │ │  │
│  │ │STORE002│SKU005│Webcam Logit.│  10  │  -   │ -   │⚪ Solo A │ │  │
│  │ │...                                                            │ │  │
│  │ └────────┴──────┴─────────────┴──────┴──────┴─────┴──────────┘ │  │
│  │                                                                  │  │
│  │  Mostrando 1-10 de 32        [1] [2] [3] [4] [>]              │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐  │
│  │ HISTORIAL DE SINCRONIZACIÓN                                      │  │
│  │                                                                  │  │
│  │  [14:35:22] ✓ Sincronización exitosa - 32 registros - 1.2s     │  │
│  │  [14:20:15] ✗ Error - Timeout de conexión al Sistema B          │  │
│  │  [14:05:10] ✓ Sincronización exitosa - 32 registros - 0.9s     │  │
│  │  [13:50:05] ✓ Sincronización exitosa - 28 registros - 1.1s     │  │
│  │  [13:35:00] ✓ Sincronización exitosa - 28 registros - 0.8s     │  │
│  │  ...                                                             │  │
│  └──────────────────────────────────────────────────────────────────┘  │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Vista Principal - Mobile

```
┌─────────────────────────────┐
│ ☰  Monitor de Sincronización│
├─────────────────────────────┤
│                              │
│  ┌──────────────────────┐   │
│  │ [🟢 Sincronizado]    │   │
│  │ hace 5 minutos       │   │
│  └──────────────────────┘   │
│                              │
│  ┌──────────┬──────────┐    │
│  │  Total   │ Sincron. │    │
│  │   32     │    28    │    │
│  └──────────┴──────────┘    │
│  ┌──────────┬──────────┐    │
│  │ Discrep. │  Solo A  │    │
│  │    3     │     1    │    │
│  └──────────┴──────────┘    │
│                              │
│  [Verificar Estado]         │
│  [Sincronizar Ahora]        │
│                              │
│  ⚠️ 3 productos con          │
│     discrepancias            │
│                              │
│  ┌──────────────────────┐   │
│  │ COMPARACIÓN          │   │
│  │                      │   │
│  │ [Filtros ▼]          │   │
│  │ [Buscar...]          │   │
│  │                      │   │
│  │ ┌──────────────────┐ │   │
│  │ │ STORE001         │ │   │
│  │ │ SKU001           │ │   │
│  │ │ Laptop HP ProBook│ │   │
│  │ │ A: 5  B: 5  🟢   │ │   │
│  │ └──────────────────┘ │   │
│  │                      │   │
│  │ ┌──────────────────┐ │   │
│  │ │ STORE001         │ │   │
│  │ │ SKU003           │ │   │
│  │ │ Teclado Corsair  │ │   │
│  │ │ A: 10  B: 8  🟡  │ │   │
│  │ │ Diferencia: +2   │ │   │
│  │ └──────────────────┘ │   │
│  │                      │   │
│  │ [Ver más...]         │   │
│  └──────────────────────┘   │
│                              │
│  [Historial ▼]              │
│                              │
└─────────────────────────────┘
```

## Estados de los Componentes

### Panel de Estado - Variaciones

#### Estado: Sincronizado
```
┌──────────────────────────────────────────────┐
│ [🟢 Sincronizado]  Última sincronización:    │
│                    hace 5 minutos            │
│                                              │
│ Todos los registros están sincronizados     │
└──────────────────────────────────────────────┘
```

#### Estado: Desincronizado
```
┌──────────────────────────────────────────────┐
│ [🟡 Desincronizado]  Última sincronización:  │
│                      hace 15 minutos         │
│                                              │
│ 3 productos con discrepancias detectadas    │
└──────────────────────────────────────────────┘
```

#### Estado: Error
```
┌──────────────────────────────────────────────┐
│ [🔴 Error]  Último intento:                  │
│             hace 2 minutos                   │
│                                              │
│ Error: Timeout de conexión al Sistema B     │
└──────────────────────────────────────────────┘
```

#### Estado: Cargando
```
┌──────────────────────────────────────────────┐
│ [⏳ Verificando...]                          │
│                                              │
│ Obteniendo datos de los sistemas...         │
│ [████████░░░░░░░░░░░░] 40%                  │
└──────────────────────────────────────────────┘
```

### Botón de Sincronización - Estados

#### Normal
```
┌─────────────────────┐
│ Sincronizar Ahora   │
└─────────────────────┘
```

#### Sincronizando
```
┌─────────────────────┐
│ ⏳ Sincronizando...  │ (deshabilitado)
└─────────────────────┘
```

#### Éxito (temporal, 3 segundos)
```
┌─────────────────────┐
│ ✓ Sincronizado      │ (verde)
└─────────────────────┘
```

#### Error (temporal, 5 segundos)
```
┌─────────────────────┐
│ ✗ Error al sync.    │ (rojo)
└─────────────────────┘
```

### Filas de Tabla - Variaciones Visuales

#### Producto Sincronizado
```
┌────────┬──────┬─────────────┬──────┬──────┬─────┬──────────┐
│STORE001│SKU001│Laptop HP    │  5   │  5   │  0  │🟢 Sync   │
└────────┴──────┴─────────────┴──────┴──────┴─────┴──────────┘
Fondo: Verde muy claro (#e8f5e9)
```

#### Discrepancia Pequeña
```
┌────────┬──────┬─────────────┬──────┬──────┬─────┬──────────┐
│STORE001│SKU003│Teclado Cors.│  10  │  8   │ +2  │🟡 Dif.   │
└────────┴──────┴─────────────┴──────┴──────┴─────┴──────────┘
Fondo: Amarillo muy claro (#fff9c4)
```

#### Discrepancia Grande
```
┌────────┬──────┬─────────────┬──────┬──────┬─────┬──────────┐
│STORE002│SKU002│Mouse Logic. │  18  │  5   │+13  │🔴 Dif.   │
└────────┴──────┴─────────────┴──────┴──────┴─────┴──────────┘
Fondo: Rojo muy claro (#ffebee)
```

#### Solo en Sistema A
```
┌────────┬──────┬─────────────┬──────┬──────┬─────┬──────────┐
│STORE002│SKU005│Webcam Logit.│  10  │  -   │ -   │⚪ Solo A │
└────────┴──────┴─────────────┴──────┴──────┴─────┴──────────┘
Fondo: Gris muy claro (#f5f5f5)
```

## Notificaciones Toast

### Éxito
```
┌─────────────────────────────────────────┐
│ ✓ Sincronización completada             │
│   32 registros actualizados en 1.2s     │
└─────────────────────────────────────────┘
Posición: Superior derecha
Color: Verde
Duración: 5 segundos
Auto-dismiss: Sí
```

### Error
```
┌─────────────────────────────────────────┐
│ ✗ Error en sincronización               │
│   Timeout de conexión al Sistema B      │
│   [Reintentar]                          │
└─────────────────────────────────────────┘
Posición: Superior derecha
Color: Rojo
Duración: Manual dismiss o 10 segundos
```

### Advertencia
```
┌─────────────────────────────────────────┐
│ ⚠️ Advertencia                           │
│   Los datos tienen más de 1 hora        │
│   [Sincronizar]                         │
└─────────────────────────────────────────┘
Posición: Superior derecha
Color: Naranja
Duración: Manual dismiss
```

## Banner de Alerta (Datos Obsoletos)

```
┌─────────────────────────────────────────────────────────────┐
│ ⚠️ Advertencia: Los datos en Sistema B tienen más de 1 hora │
│    de antigüedad. Considera sincronizar.                    │
│                                [Sincronizar Ahora]  [X]     │
└─────────────────────────────────────────────────────────────┘
Color de fondo: Amarillo claro (#fff3cd)
Borde: Amarillo (#ffc107)
Posición: Debajo del panel de estado
```

## Historial - Formato de Entradas

```
┌──────────────────────────────────────────────────────────┐
│ HISTORIAL DE SINCRONIZACIÓN                             │
├──────────────────────────────────────────────────────────┤
│                                                          │
│  ✓  14:35:22  Sincronización exitosa                    │
│              32 registros actualizados (1.2s)           │
│                                                          │
│  ✗  14:20:15  Error en sincronización                   │
│              Timeout de conexión al Sistema B           │
│                                                          │
│  ✓  14:05:10  Sincronización exitosa                    │
│              32 registros actualizados (0.9s)           │
│                                                          │
│  ✓  13:50:05  Sincronización exitosa                    │
│              28 registros actualizados (1.1s)           │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

## Filtros y Búsqueda

```
┌──────────────────────────────────────────────────────────┐
│  Filtros:                                                │
│                                                          │
│  [Todas las ubicaciones ▼]  [Todos los estados ▼]      │
│                                                          │
│  Estados:                                                │
│    □ Sincronizado                                        │
│    □ Con discrepancia                                    │
│    □ Solo en Sistema A                                   │
│                                                          │
│  Ubicaciones:                                            │
│    □ WAREHOUSE - Almacén Central                         │
│    □ STORE001 - Tienda Centro                            │
│    □ STORE002 - Tienda Norte                             │
│    □ STORE003 - Tienda Sur                               │
│                                                          │
│  [🔍 Buscar por SKU o nombre de producto...]            │
│                                                          │
│  [Limpiar filtros]                                       │
└──────────────────────────────────────────────────────────┘
```

## Indicador de Auto-refresh (Bonus)

```
┌──────────────────────────────────────┐
│  🔄 Auto-refresh: [ON/OFF]           │
│     Próxima actualización: 45s       │
└──────────────────────────────────────┘
```

## Modal de Confirmación (Opcional)

```
┌─────────────────────────────────────────────────────────┐
│  Confirmar Sincronización                               │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  Se sincronizarán 32 registros de inventario desde     │
│  Sistema A hacia Sistema B.                             │
│                                                         │
│  Esto sobrescribirá los datos actuales en Sistema B.   │
│                                                         │
│  ¿Deseas continuar?                                     │
│                                                         │
│                    [Cancelar]  [Sincronizar]           │
└─────────────────────────────────────────────────────────┘
```

## Paleta de Colores Sugerida

### Estados
- **Sincronizado:** `#4caf50` (verde) / fondo `#e8f5e9`
- **Discrepancia pequeña:** `#ffc107` (amarillo) / fondo `#fff9c4`
- **Discrepancia grande:** `#f44336` (rojo) / fondo `#ffebee`
- **Solo en A:** `#9e9e9e` (gris) / fondo `#f5f5f5`
- **Error:** `#d32f2f` (rojo oscuro)
- **Advertencia:** `#ff9800` (naranja)

### UI General
- **Primario:** `#1976d2` (azul)
- **Secundario:** `#424242` (gris oscuro)
- **Fondo:** `#fafafa` (gris muy claro)
- **Texto:** `#212121` (casi negro)
- **Bordes:** `#e0e0e0` (gris claro)

## Tipografía Sugerida

- **Familia:** Sans-serif (Roboto, Inter, System-UI)
- **Títulos:** 20-24px, peso 500-600
- **Subtítulos:** 16-18px, peso 500
- **Texto normal:** 14px, peso 400
- **Texto pequeño:** 12px, peso 400

## Iconografía

### Símbolos recomendados:
- ✓ Éxito / Sincronizado
- ✗ Error
- ⚠️ Advertencia
- 🔍 Búsqueda
- 🔄 Refresh / Sincronizar
- ⏳ Cargando
- 🟢 Estado verde (OK)
- 🟡 Estado amarillo (advertencia)
- 🔴 Estado rojo (error)
- ⚪ Estado gris (neutral)

Alternativamente, usa una librería de iconos como:
- Material Icons
- Font Awesome
- Heroicons
- Feather Icons

## Responsive Breakpoints (Opcional)

```
Mobile:   < 768px   (1 columna, cards apiladas)
Tablet:   768-1024px (2 columnas o tabla scrollable)
Desktop:  > 1024px  (layout completo)
```

## Animaciones Sutiles (Opcional)

- Fade in/out para notificaciones
- Slide in para alertas
- Smooth scroll al hacer clic en "Ver productos"
- Skeleton loading para tablas
- Progress bar durante sincronización
- Pulse en indicador de auto-refresh

## Accesibilidad

- Contraste de color apropiado (WCAG AA mínimo)
- Textos alternativos para iconos
- Labels para inputs
- Focus visible en elementos interactivos
- Navegación por teclado funcional
- Tamaño de botones táctiles > 44px en mobile

---

**Nota Final:** Estos mockups son guías visuales. El candidato tiene libertad creativa siempre que cumpla con los requisitos funcionales especificados en `FRONTEND_SPEC.md`.
