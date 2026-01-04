# content_reviewer.py
"""
Simple web interface to review and approve generated content
Run: python content_reviewer.py
Then open: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def index():
    """Main review interface"""
    with open('content_queue.json', 'r') as f:
        posts = json.load(f)
    
    return render_template('review.html', posts=posts)

@app.route('/approve', methods=['POST'])
def approve_post():
    """Mark post as approved"""
    data = request.json
    post_index = data['index']
    
    with open('content_queue.json', 'r') as f:
        posts = json.load(f)
    
    posts[post_index]['approved'] = True
    posts[post_index]['approved_at'] = datetime.now().isoformat()
    
    with open('content_queue.json', 'w') as f:
        json.dump(posts, f, indent=2)
    
    return jsonify({'success': True})

@app.route('/edit', methods=['POST'])
def edit_post():
    """Edit post content"""
    data = request.json
    post_index = data['index']
    new_content = data['content']
    
    with open('content_queue.json', 'r') as f:
        posts = json.load(f)
    
    posts[post_index]['content'] = new_content
    posts[post_index]['edited'] = True
    posts[post_index]['edited_at'] = datetime.now().isoformat()
    
    with open('content_queue.json', 'w') as f:
        json.dump(posts, f, indent=2)
    
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, port=5000)