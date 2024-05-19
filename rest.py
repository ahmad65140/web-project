from flask import jsonify,request
from __main__ import app, db
from fastapi.encoders import jsonable_encoder
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from app import Users

db.init_app(app)

class Projects(db.Model):
    def project_to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "about": self.about,
            "image_url": self.image_url,
            "video_url": self.video_url,
            "goal_amount": str(self.goal_amount),  
            "pledged_amount": str(self.pledged_amount),  
            "backer_count": self.backer_count,
            "category": self.category,
            "date_added": self.date_added.isoformat(),  
            "duration": self.duration,
            "is_valid": self.is_valid,
            "user_id": self.user_id,
        }

""" class Users(db.Model):
    def user_to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "role": self.role,
            "email": self.email 
        } """
    
""" class Comments(db.Model):
    __table__ = db.metadata.tables['comments']
    def comment_to_dict(self):
        return {
            "id": self.id,
            "content": self.content,
            "project_id": self.project_id,
            "user": {
                "id": self.user.id,
                "username": self.user.username,  # Include only public user info
            }
        }
   """


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