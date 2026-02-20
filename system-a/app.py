"""
System A - Inventory Management System
REST API with JSON and OpenAPI 3.0 documentation
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import database as db

app = Flask(__name__)
CORS(app)

# Initialize database on startup
db.init_database()


@app.route('/openapi.json', methods=['GET'])
def openapi_spec():
    """OpenAPI 3.0 specification in Spanish"""
    spec = {
        "openapi": "3.0.0",
        "info": {
            "title": "Sistema de Gestión de Inventario - API",
            "description": "API REST para gestionar inventario de productos en múltiples ubicaciones (tiendas y almacenes)",
            "version": "1.0.0"
        },
        "servers": [
            {
                "url": "http://localhost:5001",
                "description": "Servidor de desarrollo local"
            }
        ],
        "paths": {
            "/api/locations": {
                "get": {
                    "summary": "Listar todas las ubicaciones",
                    "description": "Obtiene una lista de todas las ubicaciones (tiendas y almacenes) en el sistema",
                    "responses": {
                        "200": {
                            "description": "Lista de ubicaciones obtenida exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/Location"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/inventory/{location_code}": {
                "get": {
                    "summary": "Obtener inventario de una ubicación",
                    "description": "Obtiene todos los niveles de stock de productos en una ubicación específica",
                    "parameters": [
                        {
                            "name": "location_code",
                            "in": "path",
                            "required": True,
                            "description": "Código único de la ubicación (ej: STORE001, WAREHOUSE)",
                            "schema": {"type": "string"}
                        }
                    ],
                    "responses": {
                        "200": {
                            "description": "Inventario obtenido exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/InventoryItem"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "404": {
                            "description": "Ubicación no encontrada",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            },
            "/api/inventory": {
                "get": {
                    "summary": "Obtener inventario completo",
                    "description": "Obtiene los niveles de stock de todos los productos en todas las ubicaciones",
                    "responses": {
                        "200": {
                            "description": "Inventario completo obtenido exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "type": "array",
                                                "items": {
                                                    "$ref": "#/components/schemas/InventoryItemFull"
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            },
            "/api/inventory/update": {
                "post": {
                    "summary": "Actualizar niveles de inventario",
                    "description": "Procesa una actualización de inventario: puede establecer un valor absoluto, incrementar o decrementar stock",
                    "requestBody": {
                        "required": True,
                        "content": {
                            "application/json": {
                                "schema": {
                                    "$ref": "#/components/schemas/InventoryUpdate"
                                }
                            }
                        }
                    },
                    "responses": {
                        "200": {
                            "description": "Inventario actualizado exitosamente",
                            "content": {
                                "application/json": {
                                    "schema": {
                                        "type": "object",
                                        "properties": {
                                            "success": {"type": "boolean"},
                                            "data": {
                                                "$ref": "#/components/schemas/InventoryUpdateResult"
                                            }
                                        }
                                    }
                                }
                            }
                        },
                        "400": {
                            "description": "Solicitud inválida (datos faltantes o incorrectos)",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        },
                        "404": {
                            "description": "Ubicación o producto no encontrado",
                            "content": {
                                "application/json": {
                                    "schema": {"$ref": "#/components/schemas/Error"}
                                }
                            }
                        }
                    }
                }
            }
        },
        "components": {
            "schemas": {
                "Location": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "description": "ID interno de la ubicación"},
                        "code": {"type": "string", "description": "Código único de la ubicación"},
                        "name": {"type": "string", "description": "Nombre de la ubicación"},
                        "type": {"type": "string", "enum": ["store", "warehouse"], "description": "Tipo de ubicación"}
                    }
                },
                "InventoryItem": {
                    "type": "object",
                    "properties": {
                        "sku": {"type": "string", "description": "Código SKU del producto"},
                        "product_name": {"type": "string", "description": "Nombre del producto"},
                        "description": {"type": "string", "description": "Descripción del producto"},
                        "quantity": {"type": "integer", "description": "Cantidad disponible"},
                        "location_code": {"type": "string", "description": "Código de la ubicación"},
                        "location_name": {"type": "string", "description": "Nombre de la ubicación"}
                    }
                },
                "InventoryItemFull": {
                    "type": "object",
                    "properties": {
                        "location_code": {"type": "string", "description": "Código de la ubicación"},
                        "location_name": {"type": "string", "description": "Nombre de la ubicación"},
                        "location_type": {"type": "string", "enum": ["store", "warehouse"]},
                        "sku": {"type": "string", "description": "Código SKU del producto"},
                        "product_name": {"type": "string", "description": "Nombre del producto"},
                        "quantity": {"type": "integer", "description": "Cantidad disponible"}
                    }
                },
                "InventoryUpdate": {
                    "type": "object",
                    "required": ["location_code", "sku", "quantity"],
                    "properties": {
                        "location_code": {"type": "string", "description": "Código de la ubicación"},
                        "sku": {"type": "string", "description": "Código SKU del producto"},
                        "quantity": {"type": "integer", "description": "Cantidad (significado depende de la operación)"},
                        "operation": {
                            "type": "string",
                            "enum": ["set", "increment", "decrement"],
                            "default": "set",
                            "description": "Tipo de operación: 'set' (valor absoluto), 'increment' (aumentar), 'decrement' (disminuir)"
                        }
                    }
                },
                "InventoryUpdateResult": {
                    "type": "object",
                    "properties": {
                        "location_code": {"type": "string"},
                        "sku": {"type": "string"},
                        "previous_quantity": {"type": "integer", "description": "Cantidad anterior"},
                        "new_quantity": {"type": "integer", "description": "Nueva cantidad"},
                        "operation": {"type": "string", "description": "Operación realizada"}
                    }
                },
                "Error": {
                    "type": "object",
                    "properties": {
                        "success": {"type": "boolean", "example": False},
                        "error": {"type": "string", "description": "Mensaje de error"}
                    }
                }
            }
        }
    }
    return jsonify(spec)


@app.route('/docs', methods=['GET'])
def swagger_ui():
    """Simple Swagger UI redirect"""
    html = """
    <!DOCTYPE html>
    <html lang="es">
    <head>
        <meta charset="UTF-8">
        <title>Sistema de Inventario - Documentación API</title>
        <link rel="stylesheet" type="text/css" href="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui.css">
        <style>
            html { box-sizing: border-box; overflow: -moz-scrollbars-vertical; overflow-y: scroll; }
            *, *:before, *:after { box-sizing: inherit; }
            body { margin:0; padding:0; }
        </style>
    </head>
    <body>
        <div id="swagger-ui"></div>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-bundle.js"></script>
        <script src="https://unpkg.com/swagger-ui-dist@5.9.0/swagger-ui-standalone-preset.js"></script>
        <script>
            window.onload = function() {
                window.ui = SwaggerUIBundle({
                    url: "/openapi.json",
                    dom_id: '#swagger-ui',
                    deepLinking: true,
                    presets: [
                        SwaggerUIBundle.presets.apis,
                        SwaggerUIStandalonePreset
                    ],
                    layout: "StandaloneLayout"
                });
            };
        </script>
    </body>
    </html>
    """
    return html


@app.route('/api/locations', methods=['GET'])
def get_locations():
    """Get all locations"""
    try:
        locations = db.get_all_locations()
        return jsonify({'success': True, 'data': locations})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory/<location_code>', methods=['GET'])
def get_inventory(location_code):
    """Get inventory for a specific location"""
    try:
        # Check if location exists
        location = db.get_location_by_code(location_code)
        if not location:
            return jsonify({'success': False, 'error': f'Location not found: {location_code}'}), 404

        inventory = db.get_inventory_by_location(location_code)
        return jsonify({'success': True, 'data': inventory})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory', methods=['GET'])
def get_all_inventory():
    """Get complete inventory across all locations"""
    try:
        inventory = db.get_all_inventory()
        return jsonify({'success': True, 'data': inventory})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/inventory/update', methods=['POST'])
def update_inventory():
    """Update inventory levels"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data provided'}), 400

        required_fields = ['location_code', 'sku', 'quantity']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'success': False, 'error': f'Missing required fields: {", ".join(missing_fields)}'}), 400

        location_code = data['location_code']
        sku = data['sku']
        quantity = data['quantity']
        operation = data.get('operation', 'set')

        # Validate operation
        if operation not in ['set', 'increment', 'decrement']:
            return jsonify({'success': False, 'error': f'Invalid operation: {operation}. Must be one of: set, increment, decrement'}), 400

        # Validate quantity is integer
        if not isinstance(quantity, int):
            return jsonify({'success': False, 'error': 'Quantity must be an integer'}), 400

        result = db.update_inventory(location_code, sku, quantity, operation)
        return jsonify({'success': True, 'data': result})

    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'inventory-system'})


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    return jsonify({
        'service': 'Sistema de Gestión de Inventario (System A)',
        'version': '1.0.0',
        'documentation': '/docs',
        'openapi_spec': '/openapi.json'
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
