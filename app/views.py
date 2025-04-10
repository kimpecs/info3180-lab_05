from flask import Blueprint, jsonify, render_template, request, send_file, send_from_directory, current_app
from app import db
from app.models import Movie
from app.forms import MovieForm
import os
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

@bp.route('/api/v1/movies', methods=['POST'])
def add_movie():
    form = MovieForm()
    
    # Debug print to see what data is being received
    print("Form data received:", request.form)
    print("Files received:", request.files)
    
    # Handle both form data and file upload
    if form.validate_on_submit():
        try:
            poster = form.poster.data
            if not poster:
                return jsonify({"errors": ["No poster file provided"]}), 400
                
            filename = secure_filename(poster.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            
            # Create upload folder if it doesn't exist
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save file
            filepath = os.path.join(upload_folder, filename)
            poster.save(filepath)
            
            # Create and save movie record
            movie = Movie(
                title=form.title.data,
                description=form.description.data,
                poster=filename
            )
            db.session.add(movie)
            db.session.commit()
            
            return jsonify({
                "message": "Movie successfully added",
                "title": movie.title,
                "poster": filename,
                "description": movie.description
            }), 201
            
        except Exception as e:
            db.session.rollback()
            print("Error saving movie:", str(e))
            return jsonify({"errors": [f"Server error: {str(e)}"]}), 500
    
    # Return validation errors
    return jsonify({"errors": form_errors(form)}), 400

@bp.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf_token():
    return jsonify({'csrf_token': generate_csrf()})

@bp.route('/api/v1/movies', methods=['GET'])
def get_movies():
    movies = Movie.query.all()
    return jsonify({
        "movies": [
            {
                "id": movie.id,
                "title": movie.title,
                "description": movie.description,
                "poster": f"/api/v1/posters/{movie.poster}"
            } for movie in movies
        ]
    })

@bp.route('/api/v1/posters/<filename>')
def get_poster(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

# ----------- Utility Functions -----------
def form_errors(form):
    error_messages = []
    for field, errors in form.errors.items():
        for error in errors:
            message = f"Error in the {getattr(form, field).label.text} field - {error}"
            error_messages.append(message)
    return error_messages

@bp.route('/<file_name>.txt')
def send_text_file(file_name):
    return send_file(f'static/{file_name}.txt')

@bp.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404