from flask import Flask, render_template, request
import config
import webapp.aicontent
import hashlib 
from werkzeug.security import generate_password_hash
from webapp.oauth import oauth
import webapp.auth
from webapp.sqla import sqla
from webapp.login import login_manager
from  flask_login import login_required
from flask import session

def page_not_found(e):
  return render_template('404.html'), 404


app = Flask(__name__)
app.config.from_object(config.config['development'])
app.register_error_handler(404, page_not_found)
oauth.init_app(app)
sqla.init_app(app)
login_manager.init_app(app)


@app.route('/', methods=["GET", "POST"])
@login_required
def index():
    messages = []    
    with open("querylog.txt", 'r', encoding="utf-8") as file:

        for line in file:
            messages.append(line.strip())
    messages = messages[::-1]
    messages = messages[0:4]



    return render_template('index.html',  **locals())



@app.route('/content', methods=["GET", "POST"])
@login_required
def coldEmails():
    if request.method == 'POST':
        submission = request.form['cadena']
        temp = request.form["temp"]
        chars = request.form["chars"]
        ia = request.form["IA"]
        query = format(submission)

        email = session["Username"]
        openAIAnswerUnformatted = webapp.aicontent.openAIQuery(query,temp,chars,ia)
        openAIAnswer = openAIAnswerUnformatted.replace('\n', '<br>')
        prompt = 'La AI sugiere {} :'.format(submission)
        with open("querylog.txt", 'a+', encoding="utf-8") as log:
            log.write( "<hr>" + email + " Consulta: " + query +  openAIAnswer + "\n" )

    return render_template('content.html', **locals())

@app.route('/historial', methods=["GET", "POST"])
@login_required
def historial():
    messages = []
    with open("querylog.txt", 'r', encoding="utf-8") as file:
        for line in file:
            messages.append(line.strip())
    messages = messages[::-1]
    return render_template('historial.html',  **locals())

app.register_blueprint(webapp.auth.bp)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug = True)