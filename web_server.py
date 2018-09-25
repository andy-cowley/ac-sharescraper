from flask import render_template
import connexion

#Create application instance
app = connexion.App(__name__,specification_dir='./')

# Read the swagger.yml file to configure the endpoints
app.add_api('swagger.yml')

#Create URL route for "/"
@app.route('/')
def home():
    """
    This fucntion responds to browser ULR localhost:5000/

    :return:    the rendered template 'home.html'
    """
    return render_template('home.html')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)