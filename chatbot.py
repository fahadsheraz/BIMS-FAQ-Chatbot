from flask import Flask, request, jsonify, send_file
from chatbot_service import BIMSChatbotService
import os

app = Flask(__name__, static_folder='static')
service = BIMSChatbotService()

# ===== STATIC ROUTES =====
@app.route('/')
def index():
    return send_file('static/index.html')

# ===== API ENDPOINTS =====

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint."""
    return jsonify({
        "status": "ok",
        "service": "BIMS FAQ Chatbot API",
        "version": "1.0"
    }), 200

@app.route('/api/info', methods=['GET'])
def api_info():
    """Get service information."""
    return jsonify(service.get_service_info()), 200

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """Main chat endpoint - returns answer with confidence."""
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({
                "error": "Missing 'query' field in request",
                "success": False
            }), 400
        
        query = data['query']
        result = service.get_answer(query)
        return jsonify(result), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "success": False
        }), 500

@app.route('/api/faq', methods=['GET'])
def get_all_faq():
    """Get all FAQ pairs."""
    return jsonify({
        "faq": service.get_all_faq(),
        "count": service.get_faq_count()
    }), 200

@app.route('/api/faq/search', methods=['POST'])
def search_faq():
    """Search FAQ by keyword."""
    try:
        data = request.get_json()
        if not data or 'keyword' not in data:
            return jsonify({
                "error": "Missing 'keyword' field in request",
                "results": []
            }), 400
        
        keyword = data['keyword']
        results = service.search_faq(keyword)
        return jsonify({
            "keyword": keyword,
            "results": results,
            "count": len(results)
        }), 200
    
    except Exception as e:
        return jsonify({
            "error": str(e),
            "results": []
        }), 500

@app.route('/api/faq/count', methods=['GET'])
def faq_count():
    """Get total FAQ count."""
    return jsonify({
        "total_faq": service.get_faq_count()
    }), 200

# ===== LEGACY ENDPOINT (for backward compatibility) =====
@app.route('/chat', methods=['POST'])
def chat():
    """Legacy endpoint - maintains backward compatibility."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        result = service.get_answer(query)
        return jsonify({'answer': result['answer']}), 200
    except Exception as e:
        return jsonify({'answer': f'Error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)