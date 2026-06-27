from flask import Flask, render_template, g
import auth
from auth import login_required
from contentful import Client
import markdown


app = Flask(__name__)

app.secret_key = 'dev'

import auth
app.register_blueprint(auth.bp)

client = Client(
    'w6sn00a0nw61',
    'sXe4bg57oay8cu-2MFzjoF6o3F-lH4va_r4DaK3hIFw',
    environment='master'  # Optional - it defaults to 'master'.
)

# @app.before_request
# def on_every_request():
#     entries = client.entries()
#     g.entries = [e.id for e in entries]

@app.route('/')
@login_required
def index():
    title = 'Welcome!'
    text = 'This is a basic demo website that shows how to use Flask for a basic website with some pages and a blog.'
    md = markdown.markdown(text, extensions=['fenced_code'])
    return render_template('page.html', title=title, body=md)


@app.route('/blog/<content_type>')
def blog(content_type):
    entries = client.entries({'content_type': content_type})
    items = []
    for entry in entries:

        text = entry.body
        excerpt = text.split('\n\n')[0]
        md = markdown.markdown(excerpt, extensions=['fenced_code', 'codehilite'])
        # print('Posted:', entry.posted, 'Modified:', entry.modified)
        item = {
            'content_type': content_type,
            'id': entry.id,
            'title': entry.title,
            'posted': entry.posted,
            'modified': entry.modified,
            'body': md
        }

        items.append(item)

    sorted_items = sorted(items, key=lambda x: x['posted'], reverse=True) if items else []

    return render_template('blog.html', items=sorted_items)


@app.route('/blog/<content_type>/<id>')
def blog_post(content_type, id):
    entry = client.entry(id)
    posted = entry.posted

    prev_entries = client.entries({
        'content_type': content_type,
        'fields.posted[gt]': posted,
        'order': 'fields.posted',
        'limit': 1
    })

    next_entries = client.entries({
        'content_type': content_type,
        'fields.posted[lt]': posted,
        'order': '-fields.posted',
        'limit': 1
    })
    
    prev_id = prev_entries[0].id if prev_entries else ''
    next_id = next_entries[0].id if next_entries else '' 

    text = entry.body
    md = markdown.markdown(text, extensions=['fenced_code', 'codehilite', 'tables'])

    item = {
            'title': entry.title,
            'content_type': content_type,
            'posted': posted,
            'modified': entry.modified,
            'prev_id': prev_id,
            'next_id': next_id,
            'body': md
        }
    return render_template('blog-post.html', item=item)


@app.route('/about')
def about():
    title = 'About this Website'
    text = 'It does not contain a lot of information.'
    md = markdown.markdown(text, extensions=['fenced_code'])
    return render_template('page.html', title=title, body=md)


if __name__ == '__main__':
    app.run(debug=True)