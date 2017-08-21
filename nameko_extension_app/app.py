import os
import flask
import flask_nameko


template_dir = os.path.abspath('./nameko_extension_app/templates')
app = flask.Flask(__name__, template_folder=template_dir)

# TODO: get this config from config file
# create a class with it and put all configs in there.
app.config['NAMEKO_AMQP_URI'] = 'amqp://localhost'

rpc = flask_nameko.FlaskPooledClusterRpcProxy()
rpc.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():

    if flask.request.method == 'GET':

        people = rpc.people.get_people()

        if people is None:
            return flask.abort(500)

        return flask.render_template('index.html', people=people)

    elif flask.request.method == 'POST':
        name = flask.request.form['name'] 
        age = flask.request.form['age']
        
        result = rpc.people.add_person(name, age)
            
        if result:
            return flask.redirect(flask.url_for('index'))

        return flask.abort(500)


if __name__ == '__main__':
    app.run(debug=True)
