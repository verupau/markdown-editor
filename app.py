from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
from werkzeug.utils import secure_filename
import pathlib

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Cesty
BASE_DIR = pathlib.Path(__file__).parent
MARKDOWN_DIR = BASE_DIR / 'markdown-files'
IMAGES_DIR = MARKDOWN_DIR / 'images'

# Ujistíme se, že složky existují
MARKDOWN_DIR.mkdir(exist_ok=True)
IMAGES_DIR.mkdir(exist_ok=True)

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'svg'}


def allowed_image_file(filename):
    """Kontrola, zda má soubor povolený formát obrázku"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS


def get_file_info(filepath):
    """Získá informace o souboru"""
    stat = filepath.stat()
    return {
        'name': filepath.name,
        'size': stat.st_size,
        'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
        'modified_timestamp': stat.st_mtime
    }


@app.route('/')
def dashboard():
    """Dashboard s přehledem souborů"""
    return render_template('dashboard.html')


@app.route('/editor/<filename>')
def editor(filename):
    """Editor pro konkrétní soubor"""
    filepath = MARKDOWN_DIR / filename
    if not filepath.exists() or filepath.suffix != '.md':
        return "Soubor nenalezen", 404
    return render_template('editor.html', filename=filename)


@app.route('/api/files')
def get_files():
    """API: Vrátí seznam všech markdown souborů"""
    try:
        files = []
        for filepath in MARKDOWN_DIR.glob('*.md'):
            files.append(get_file_info(filepath))
        
        # Seřadíme podle data úpravy (nejnovější první)
        files.sort(key=lambda x: x['modified_timestamp'], reverse=True)
        
        return jsonify({'files': files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/file/<filename>')
def get_file(filename):
    """API: Vrátí obsah markdown souboru"""
    try:
        filepath = MARKDOWN_DIR / filename
        if not filepath.exists() or filepath.suffix != '.md':
            return jsonify({'error': 'Soubor nenalezen'}), 404
        
        content = filepath.read_text(encoding='utf-8')
        return jsonify({
            'content': content,
            'info': get_file_info(filepath)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/file/<filename>', methods=['POST'])
def save_file(filename):
    """API: Uloží změny do markdown souboru"""
    try:
        filepath = MARKDOWN_DIR / filename
        if filepath.suffix != '.md':
            return jsonify({'error': 'Neplatný formát souboru'}), 400
        
        data = request.get_json()
        content = data.get('content', '')
        
        filepath.write_text(content, encoding='utf-8')
        
        return jsonify({
            'success': True,
            'message': 'Soubor uložen',
            'info': get_file_info(filepath)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/upload-image', methods=['POST'])
def upload_image():
    """API: Nahraje obrázek a vrátí relativní cestu"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'Nebyl nahrán žádný soubor'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'Nebyl vybrán žádný soubor'}), 400
        
        if file and allowed_image_file(file.filename):
            # Zabezpečení názvu souboru
            filename = secure_filename(file.filename)
            
            # Přidáme timestamp pro unikátnost
            name, ext = os.path.splitext(filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_filename = f"{name}_{timestamp}{ext}"
            
            filepath = IMAGES_DIR / unique_filename
            file.save(str(filepath))
            
            # Vrátíme relativní cestu pro markdown
            relative_path = f"images/{unique_filename}"
            
            return jsonify({
                'success': True,
                'path': relative_path,
                'filename': unique_filename
            })
        else:
            return jsonify({'error': 'Nepovolený formát obrázku'}), 400
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/markdown-files/<path:filename>')
def serve_markdown_file(filename):
    """Slouží obrázky a další soubory z markdown-files složky"""
    return send_from_directory(MARKDOWN_DIR, filename)


if __name__ == '__main__':
    print(f"🚀 Markdown Editor běží na http://localhost:8000")
    print(f"📁 Markdown soubory: {MARKDOWN_DIR}")
    app.run(debug=True, port=8000)

