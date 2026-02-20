"""
System B - Order Fulfillment System
XML-based API (legacy style)
"""
from flask import Flask, request, Response
from flask_cors import CORS
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom
import database as db

app = Flask(__name__)
CORS(app)

# Initialize database on startup
db.init_database()


def dict_to_xml(tag, data):
    """Convert dictionary to XML element"""
    elem = ET.Element(tag)
    if isinstance(data, dict):
        for key, val in data.items():
            child = dict_to_xml(key, val)
            elem.append(child)
    elif isinstance(data, list):
        for item in data:
            child = dict_to_xml('item', item)
            elem.append(child)
    else:
        elem.text = str(data)
    return elem


def prettify_xml(elem):
    """Return a pretty-printed XML string"""
    rough_string = ET.tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")


def xml_response(root_tag, data, status=200):
    """Create XML response"""
    root = dict_to_xml(root_tag, data)
    xml_str = prettify_xml(root)
    return Response(xml_str, status=status, mimetype='application/xml')


def parse_stock_update_xml(xml_data):
    """Parse stock update XML request"""
    try:
        root = ET.fromstring(xml_data)

        # Expecting format:
        # <stock_update>
        #   <location>
        #     <location_code>...</location_code>
        #     <products>
        #       <product>
        #         <sku>...</sku>
        #         <product_name>...</product_name>
        #         <quantity>...</quantity>
        #       </product>
        #     </products>
        #   </location>
        # </stock_update>

        stock_items = []

        for location_elem in root.findall('location'):
            location_code = location_elem.find('location_code').text if location_elem.find('location_code') is not None else None

            if not location_code:
                continue

            products_elem = location_elem.find('products')
            if products_elem is not None:
                for product_elem in products_elem.findall('product'):
                    sku = product_elem.find('sku').text if product_elem.find('sku') is not None else None
                    product_name = product_elem.find('product_name').text if product_elem.find('product_name') is not None else None
                    quantity_text = product_elem.find('quantity').text if product_elem.find('quantity') is not None else '0'

                    if sku and product_name:
                        stock_items.append({
                            'location_code': location_code,
                            'sku': sku,
                            'product_name': product_name,
                            'quantity': int(quantity_text)
                        })

        return stock_items
    except Exception as e:
        raise ValueError(f"Invalid XML format: {str(e)}")


@app.route('/', methods=['GET'])
def index():
    """Root endpoint"""
    info = {
        'service': 'Sistema de Cumplimiento de Pedidos (System B)',
        'version': '1.0.0',
        'documentation': 'Ver archivo API_DOCUMENTATION.txt',
        'api_type': 'XML-based'
    }
    return xml_response('service_info', info)


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return xml_response('health', {'status': 'healthy', 'service': 'order-fulfillment-system'})


@app.route('/api/orders', methods=['GET'])
def list_orders():
    """List all orders"""
    try:
        # Check for status filter
        status_filter = request.args.get('status', None)

        if status_filter == 'pending':
            orders = db.get_pending_orders()
        else:
            orders = db.get_all_orders()

        response_data = {
            'status': 'success',
            'count': len(orders),
            'orders': orders
        }

        return xml_response('orders_response', response_data)

    except Exception as e:
        error_data = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=500)


@app.route('/api/orders/<order_number>', methods=['GET'])
def get_order(order_number):
    """Get specific order by number"""
    try:
        order = db.get_order_by_number(order_number)

        if not order:
            error_data = {
                'status': 'error',
                'error_code': 'ORDER_NOT_FOUND',
                'message': f'Order not found: {order_number}'
            }
            return xml_response('error_response', error_data, status=404)

        response_data = {
            'status': 'success',
            'order': order
        }

        return xml_response('order_response', response_data)

    except Exception as e:
        error_data = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=500)


@app.route('/api/stock/update', methods=['POST'])
def update_stock():
    """Receive stock level updates from external system (System A)"""
    try:
        # Get XML data from request
        xml_data = request.data.decode('utf-8')

        if not xml_data:
            error_data = {
                'status': 'error',
                'error_code': 'MISSING_DATA',
                'message': 'No XML data provided'
            }
            return xml_response('error_response', error_data, status=400)

        # Parse XML
        stock_items = parse_stock_update_xml(xml_data)

        if not stock_items:
            error_data = {
                'status': 'error',
                'error_code': 'INVALID_DATA',
                'message': 'No valid stock items found in XML'
            }
            return xml_response('error_response', error_data, status=400)

        # Update database
        count = db.update_stock_levels(stock_items)

        response_data = {
            'status': 'success',
            'message': 'Stock levels updated successfully',
            'records_updated': count
        }

        return xml_response('stock_update_response', response_data)

    except ValueError as e:
        error_data = {
            'status': 'error',
            'error_code': 'INVALID_XML',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=400)
    except Exception as e:
        error_data = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=500)


@app.route('/api/stock', methods=['GET'])
def get_stock():
    """Get current stock levels"""
    try:
        stock_levels = db.get_stock_levels()

        response_data = {
            'status': 'success',
            'count': len(stock_levels),
            'stock_levels': stock_levels
        }

        return xml_response('stock_response', response_data)

    except Exception as e:
        error_data = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=500)


@app.route('/api/orders/<order_number>/check_availability', methods=['GET'])
def check_availability(order_number):
    """Check if order can be fulfilled based on current stock"""
    try:
        availability = db.check_order_availability(order_number)

        response_data = {
            'status': 'success',
            'availability': availability
        }

        return xml_response('availability_response', response_data)

    except Exception as e:
        error_data = {
            'status': 'error',
            'error_code': 'INTERNAL_ERROR',
            'message': str(e)
        }
        return xml_response('error_response', error_data, status=500)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)
