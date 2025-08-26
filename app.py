from flask import Flask, render_template, g
import auth
from auth import login_required
from contentful import Client
import markdown


app = Flask(__name__)

app.secret_key = 'dev'
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


@app.route('/blog')
def blog():
    entries = client.entries()
    items = []
    for entry in entries:
        id = entry.id
        title = entry.title
        slug = entry.slug
        date = entry.date
        text = entry.content
        excerpt = text.split('\n\n')[0]
        # print(excerpt)
        md = markdown.markdown(excerpt, extensions=['fenced_code', 'codehilite'])
        items.append({ 'id': id, 'title': title,'slug': slug, 'date': date, 'body': md})
        sorted_items = sorted(items, key=lambda x: x['date'], reverse=True)
    return render_template('blog.html', items=sorted_items)


@app.route('/blog/<slug>/<id>')
def blog_post(slug, id):
    entry = client.entry(id)
    title = entry.title
    date = entry.date
    text = entry.content
    md = markdown.markdown(text, extensions=['fenced_code', 'codehilite'])
    item = {'title': title, 'date': date, 'body': md}
    return render_template('blog-post.html', item=item)


@app.route('/about')
def about():
    title = 'About this Website'
    text = 'It does not contain a lot of information.'
    md = markdown.markdown(text, extensions=['fenced_code'])
    return render_template('page.html', title=title, body=md)


if __name__ == '__main__':
    app.run(debug=True)