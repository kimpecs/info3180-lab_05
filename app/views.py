from flask import Blueprint, jsonify, render_template, request, send_file
from app import db
from app.models import Movie
from app.forms import MovieForm
import os

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify(message="This is the beginning of our API")

# Form error utility (keep this)
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

@app.route('/api/v1/movies', methods=['POST'])
def movies():
    form = MovieForm()
    if form.validate_on_submit():
        # Save poster to uploads folder
        poster = form.poster.data
        filename = secure_filename(poster.filename)
        poster.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        # Save to database
        movie = Movie(
            title=form.title.data,
            description=form.description.data,
            poster=filename
        )
        db.session.add(movie)
        db.session.commit()

        return jsonify({
            "message": "Movie Successfully added",
            "title": form.title.data,
            "poster": filename,
            "description": form.description.data
        })
    return jsonify({"errors": form_errors(form)}), 400