from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from flask import flash
from flask_login import login_required
from flask_login import current_user
import requests
import base64
from flask import jsonify


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    is_admin = BooleanField('Register as Admin')
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def landing():
    return render_template('landing.html')


@app.route('/users')
@login_required
def users():
    if current_user.is_admin:
        users = User.query.all()
        return render_template('admin/users.html', users=users)
    else:
        flash("You don't have permission to access this page.", 'error')
        return redirect(url_for('index'))  # Redirect unauthorized users




# Flask Route
@app.route('/user/delete/<int:user_id>', methods=['POST'])
@login_required
def delete_user(user_id):
    if current_user.is_admin:
        user = User.query.get(user_id)
        if user:
            db.session.delete(user)
            db.session.commit()
            flash('User deleted successfully.', 'success')
        else:
            flash('User not found.', 'error')
    else:
        flash("You don't have permission to delete users.", 'error')

    return redirect(url_for('users'))





@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            flash('User already exists. Please use a different email.', 'error')
        else:
            # Proceed with registration
            user = User(email=form.email.data)
            user.set_password(form.password.data)
            user.is_admin = form.is_admin.data
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect(url_for('index'))  # Redirect to index page upon successful login
        else:
            flash('Incorrect email or password. Please try again.', 'error')
    return render_template('login.html', form=form)



@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('landing'))

@app.route('/index')
@login_required
def index():
    return render_template('index.html')

@app.route('/mobilesam')
@login_required
def mobilesam():
    return render_template('mobilesam.html')





# LOGGING FILE
# Function to log messages to a file
def log_to_file(message):
    log_file_path = 'console_log.txt'
    with open(log_file_path, 'a') as log_file:
        log_file.write(message + '\n')

@app.route('/log_message', methods=['POST'])
def log_message():
    data = request.get_json()
    if 'message' in data:
        message = data['message']
        log_to_file(message)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'error': 'Message not provided'}), 400




# Define the route for making predictions
@app.route('/make_prediction', methods=['POST'])
def make_prediction():
    # OpenAI API Key
    api_key = "sk-proj-vYB6U34zh0eHoObVFTJET3BlbkFJpZx0s7KgJrIxFcppyxvi"

    # Function to encode the image
    def encode_image(image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    # Path to your image
    image_path = "assets/masked_image.png"

    # Getting the base64 string
    base64_image = encode_image(image_path)

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }

    payload = {
        "model": "gpt-4-turbo",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Only tell me what is the red masked object and the confidence score like this, there can only be 1 masked object that is this color #ff7f7f, make the first letter of the object capital letter, the masked object will be highlighted {object: confidence%}. 1 object has only 1 red mask."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/png;base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)

    # Extract the content from the response
    content = response.json()['choices'][0]['message']['content']

    # Remove quotes and curly braces
    content = content.replace('"', '').replace('{', '').replace('}', '')

    # Print the content in the Python terminal
    print(content)

    # Return only the content as JSON response
    return jsonify(content)








@app.route('/save_masked_image', methods=['POST'])
def save_masked_image():
    try:
        data = request.json
        masked_image_data_url = data['masked_image_data_url']

        # Extract the base64 data from the data URL
        base64_str = masked_image_data_url.split(',')[1]
        img_data = base64.b64decode(base64_str)

        # Define the path to save the masked image
        save_path = os.path.join(app.root_path, 'assets', 'masked_image.png')

        # Save the masked image
        with open(save_path, 'wb') as f:
            f.write(img_data)

        return jsonify({'message': 'Masked image saved successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


with app.app_context():
    try:
        db.create_all()
        print("Database tables created")
    except Exception as e:
        print("Error creating database tables:", e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8000))
    app.run(host='0.0.0.0', port=port, debug=True)
