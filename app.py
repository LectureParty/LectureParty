from flask import *
app = Flask(__name__, static_url_path='/static', template_folder='templates')
@app.route('/')
def index():
    return render_template('base.html')
@app.route('/test/<path:path>')
def test(path):
    return render_template(path)
if __name__ == '__main__':
    app.run()
