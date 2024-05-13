from flask import Flask,render_template,redirect,request,url_for,flash,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from datetime import datetime,timezone
from werkzeug.utils import secure_filename
import uuid as uuid


from fastapi.encoders import jsonable_encoder


import os

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1982Aa2003@localhost/crowdfunding_db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Recommended for performance
app.config['UPLOAD_FOLDER'] = 'static/img'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'mov'}
app.config['SECRET_KEY'] = "secret-secret-key"
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

db = SQLAlchemy(app)
login_manager = LoginManager(app)

def create_database(app):
    with app.app_context():
        db.create_all()


class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False) 
    comments = db.relationship('Comments', backref='auhtor') 
    def user_to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "email": self.email 
        }


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.Text)
    about = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    video_url = db.Column(db.String(255))
    goal_amount = db.Column(db.DECIMAL(10, 2))
    pledged_amount = db.Column(db.DECIMAL(10, 2),default=0)
    backer_count = db.Column(db.Integer,default=0)
    category = db.Column(db.Text)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    duration = db.Column(db.Integer)
    is_valid = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('Users', backref='projects')
    comments = db.relationship('Comments', backref='project', cascade='all, delete-orphan')
    
    def project_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "about": self.about,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "goal_amount": str(self.goal_amount),  # Convert decimal to string
            "pledged_amount": str(self.pledged_amount),  # Convert decimal to string
            "backer_count": self.backer_count,
            "category": self.category,
            "date_added": self.date_added.isoformat(),  # Convert datetime to ISO format
            "duration": self.duration,
            "is_valid": self.is_valid,
            "user_id": self.user_id,
        }

class Comments(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('Users', backref='author') 
    def comment_to_dict(self):
        project = Projects.query.get(self.project_id)  # Fetch the project object
        return {
            "id": self.id,
            "content": self.content,
            "project_id": self.project_id,
            "username": self.user.username,
            "project_title": project.title
        }






@app.route("/")
def index():
    if current_user.is_authenticated and current_user.role=='admin':
        show_admin_button = True
    else:
        show_admin_button = False

    if current_user.is_authenticated:
        logging_btns = True
    else:
        logging_btns = False

    projects = Projects.query.order_by(desc(Projects.pledged_amount/Projects.goal_amount)).limit(4).all()
    return render_template('index.html',projects=projects,show_admin_button=show_admin_button,logging_btns=logging_btns)


@app.route("/explore")
def explore():
    projects = Projects.query.all()
    return render_template('explore.html', projects=projects)


@app.route("/contact",methods=['POST'])
@login_required
def contact():
    if request.method=='POST' :
        project_name = request.form.get('project-name', '')
        category = request.form.get('project-category', '')
        description = request.form.get('project-description', '')
        goal_amount = request.form.get('project-goal', '')
        duration = request.form.get('project-duration', '')
        image_file = request.files.get('project-image')
        video_file = request.files.get('project-video')

        if request.files['project-image']:
            image_file = request.files['project-image']
            pic_filename = secure_filename(image_file.filename)
            pic_name = str(uuid.uuid1())+"-"+pic_filename
            saver = request.files['project-image']
            image_file = pic_name

            new_project = Projects(title=project_name, category=category, description=description, goal_amount=goal_amount, duration=duration,image_url=image_file,user_id=current_user.id)
            db.session.add(new_project)
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER'], pic_name))

            flash('Project added successfully', 'success')
            return redirect(url_for('explore'))
        
        
    return render_template('contact.html')

@app.route("/contact",methods=['GET'])
def getcontact():        
    return render_template('contact.html')

@app.route("/about/<int:id>")
def about(id):
    project =  Projects.query.get_or_404(id)
    comments = Comments.query.filter_by(project_id=id).all()
    return render_template('about.html',project=project,comments=comments)

@login_manager.user_loader
def load_user(id):
    return Users.query.get(int(id))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        # if user and user.password == password:
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/manage')
@login_required
def manage():
    if current_user.role == 'admin':
        return render_template('manage.html',manager = current_user.username)
    else:
        return 'Access Denied'


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        user_name = request.form['username']
        email = request.form['email']
        password = request.form['password']
        new_user = Users(username = user_name,email = email ,password_hash = generate_password_hash(password), role="user")
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
        
    return render_template('signup.html')



@app.route('/fund/<int:id>', methods=['GET','POST'])
@login_required
def fund(id):
    number = float(number.strip())  # Convert number part to float, removing whitespace
    comment = comment.strip()
    new_comment = Comments(content=comment,project_id=id,user_id=current_user.id)
    db.session.add(new_comment)
    db.session.commit()
    return redirect(url_for('about', id=id))

























#REST

@app.route('/api/users', methods=['GET'])
def getuser():
    users = Users.query.all()
    return (jsonable_encoder(users))

@app.route('/api/users/<int:id>', methods=['GET'])
def getuser_id(id):
    user =  Users.query.get_or_404(id)
    return (jsonable_encoder(user))

@app.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Users.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message' : 'delete success'}), 200

@app.route('/update/user/<int:id>', methods=['GET', 'POST'])
def update_user(id):
     return render_template('edit_user.html', userid=id)




@app.route('/api/projects', methods=['GET'])
def getprojects():
    projects = Projects.query.all()
    return (jsonable_encoder(projects))

@app.route('/api/projects/<int:id>', methods=['GET'])
def getproject_id(id):
    project =  Projects.query.get_or_404(id)
    return (jsonable_encoder(project))

@app.route('/api/projects/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Projects.query.get_or_404(id)
    db.session.delete(project)
    db.session.commit()
    return jsonify({'message' : 'delete success'}), 200

@app.route('/update/project/<int:id>', methods=['GET', 'POST'])
def update_project(id):
     return render_template('edit_project.html', projectid=id)




@app.route('/api/comments', methods=['GET'])
def getcomments():
    comments = Comments.query.all()  # Fetch all comments
    comment_dicts = [comment.comment_to_dict() for comment in comments]
    return jsonify(comment_dicts)

@app.route('/api/comments/<int:id>', methods=['GET'])
def getcomment_id(id):
    comment =  Comments.query.get_or_404(id)
    return (jsonable_encoder(comment))

@app.route('/api/comments/<int:id>', methods=['DELETE'])
def delete_comment(id):
    comment = Comments.query.get_or_404(id)
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message' : 'delete success'}), 200


if __name__=='__main__':
    app.run(debug=True)

