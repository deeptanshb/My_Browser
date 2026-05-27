"""
CORS Proxy for My Browser
==========================
Runs on localhost:8081 and proxies:
  - /api/*          → Ollama at localhost:11434  (AI chat)
  - /search?q=...   → DuckDuckGo instant answers  (chatbot web search)

Why needed:
  The homepage is loaded via setHtml() which gives it a null origin.
  Browsers block cross-origin fetch() from null origins.
  All requests go through this proxy which is same-origin (localhost:8081).
"""

from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import requests as req
import json

app = Flask(__name__)
CORS(app, origins="*")

OLLAMA_BASE = "http://host.docker.internal:11434"


# ── Ollama proxy ──────────────────────────────────────────────────────────────

@app.route('/api/<path:path>', methods=['GET', 'POST', 'OPTIONS'])
def proxy_ollama(path):
    """Forward all /api/* to Ollama"""
    if request.method == 'OPTIONS':
        resp = app.make_default_options_response()
        resp.headers['Access-Control-Allow-Origin'] = '*'
        resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
        return resp

    url = f"{OLLAMA_BASE}/api/{path}"
    try:
        if request.method == 'POST':
            r = req.post(url, json=request.get_json(), timeout=120)
        else:
            r = req.get(url, timeout=10)
        resp = Response(r.content, status=r.status_code,
                        content_type=r.headers.get('Content-Type', 'application/json'))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    except req.exceptions.ConnectionError:
        return jsonify({'error': 'Ollama not running. Start with: ollama serve'}), 503
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# ── Web search endpoint ───────────────────────────────────────────────────────

@app.route('/search', methods=['GET'])
def web_search():
    """
    Search using DuckDuckGo Instant Answer API.
    Returns JSON: { text: str|null, sources: [{title, url}] }

    Called by the chatbot JS as: fetch('http://localhost:8081/search?q=...')
    This works because it's the same origin (localhost:8081) for the chatbot.
    """
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify({'text': None, 'sources': [], 'error': 'No query'}), 400

    try:
        r = req.get(
            'https://api.duckduckgo.com/',
            params={'q': query, 'format': 'json', 'no_html': '1', 'skip_disambig': '1'},
            timeout=8,
            headers={'User-Agent': 'MyBrowser/1.0'}
        )
        data = r.json()

        text    = ''
        sources = []

        if data.get('Abstract'):
            text += 'Summary: ' + data['Abstract'] + '\n'
            if data.get('AbstractURL'):
                sources.append({
                    'title': data.get('AbstractSource', 'Source'),
                    'url':   data['AbstractURL']
                })

        if data.get('Answer'):
            text += 'Direct answer: ' + data['Answer'] + '\n'

        if data.get('RelatedTopics'):
            for i, topic in enumerate(data['RelatedTopics'][:4]):
                if isinstance(topic, dict) and topic.get('Text'):
                    text += f"{i+1}. {topic['Text']}\n"
                    if topic.get('FirstURL'):
                        sources.append({
                            'title': topic['Text'][:60],
                            'url':   topic['FirstURL']
                        })

        return jsonify({
            'text':    text.strip() or None,
            'sources': sources,
            'query':   query
        })

    except req.exceptions.Timeout:
        return jsonify({'text': None, 'sources': [], 'error': 'Search timed out'}), 504
    except Exception as e:
        return jsonify({'text': None, 'sources': [], 'error': str(e)}), 500


# ── Autocomplete endpoint ────────────────────────────────────────────────────

@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    """DuckDuckGo autocomplete suggestions"""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([])
    try:
        r = req.get(
            'https://duckduckgo.com/ac/',
            params={'q': query, 'type': 'list'},
            timeout=3,
            headers={'User-Agent': 'DeepBrowse/1.0'}
        )
        data = r.json()
        suggestions = data[1] if len(data) > 1 else []
        return jsonify(suggestions[:8])
    except Exception as e:
        return jsonify([])


# ── Health check ──────────────────────────────────────────────────────────────

@app.route('/health', methods=['GET'])
def health():
    ollama_ok = False
    try:
        req.get(f'{OLLAMA_BASE}/api/tags', timeout=2)
        ollama_ok = True
    except Exception:
        pass
    return jsonify({'status': 'ok', 'ollama': ollama_ok})


if __name__ == '__main__':
    print("=" * 50)
    print("🔌 CORS Proxy starting on http://localhost:8081")
    print("   /api/*    → Ollama (AI chat)")
    print("   /search   → DuckDuckGo (chatbot web search)")
    print("=" * 50)
    app.run(host='localhost', port=8081, debug=False, threaded=True)