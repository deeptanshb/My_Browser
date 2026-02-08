"""
Simple CORS Proxy for Ollama - Robust Version
Handles all CORS requirements properly
"""

from flask import Flask, request, Response, jsonify
import requests
import json

app = Flask(__name__)

OLLAMA_BASE = 'http://localhost:11434'

@app.after_request
def after_request(response):
    """Add CORS headers to every response"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Max-Age'] = '3600'
    return response

@app.route('/api/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy(path):
    """Proxy requests to Ollama"""
    
    # Handle CORS preflight
    if request.method == 'OPTIONS':
        return '', 200
    
    url = f'{OLLAMA_BASE}/api/{path}'
    
    try:
        if request.method == 'POST':
            # Get request data
            try:
                data = request.get_json()
            except:
                data = request.data
            
            print(f"[PROXY] POST {path}")
            print(f"[PROXY] Data: {json.dumps(data) if isinstance(data, dict) else str(data)[:100]}")
            
            # Forward to Ollama
            resp = requests.post(
                url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=300
            )
            
            print(f"[PROXY] Ollama response status: {resp.status_code}")
            
            return Response(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get('Content-Type', 'application/json')
            )
            
        else:  # GET
            print(f"[PROXY] GET {path}")
            resp = requests.get(url, timeout=5)
            
            return Response(
                resp.content,
                status=resp.status_code,
                content_type=resp.headers.get('Content-Type', 'application/json')
            )
            
    except requests.exceptions.Timeout:
        print(f"[PROXY ERROR] Timeout connecting to Ollama")
        return jsonify({'error': 'Ollama timeout'}), 504
        
    except requests.exceptions.ConnectionError:
        print(f"[PROXY ERROR] Cannot connect to Ollama")
        return jsonify({'error': 'Ollama not running'}), 503
        
    except Exception as e:
        print(f"[PROXY ERROR] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    print("=" * 60)
    print("🚀 CORS Proxy for Ollama")
    print("=" * 60)
    print(f"📡 Ollama: {OLLAMA_BASE}")
    print(f"🌐 Proxy:  http://localhost:8081")
    print("=" * 60)
    print()
    
    # Test Ollama connection
    try:
        test = requests.get(f'{OLLAMA_BASE}/api/tags', timeout=2)
        if test.status_code == 200:
            data = test.json()
            models = data.get('models', [])
            print(f"✅ Ollama is running with {len(models)} model(s)")
            for model in models:
                print(f"   • {model.get('name', 'unknown')}")
        else:
            print(f"⚠️  Ollama returned status {test.status_code}")
    except Exception as e:
        print(f"❌ Cannot connect to Ollama: {e}")
        print("   Make sure Ollama is running: ollama serve")
    
    print()
    print("Starting proxy server...")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()
    
    app.run(host='0.0.0.0', port=8081, debug=False)