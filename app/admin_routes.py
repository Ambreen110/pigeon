from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user, UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .forms import LoginForm, AddCupForm, AddCompetitionForm, AddResultsForm, EditParticipantForm
from .models import Cup, Competition, Participant, User
from . import db, login_manager
from werkzeug.utils import secure_filename
import os

# login_manager.init_app(app)
# login_manager.login_view = 'admin.login'

admin_bp = Blueprint('admin', __name__)

UPLOAD_FOLDER = 'app/static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Hard-coded admin credentials
# ADMIN_USERNAME = 'admin'
# ADMIN_PASSWORD_HASH = 'pbkdf2:sha256:600000$D4bDEDofpsQtBc8I$41aafc4c2adcbfcf749e059efc0fe46b5f5c8741ce8782835299a24fae8631f9'  # Hashed password for 'your_secure_password'

# class AdminUser(UserMixin):
#     id = 1
#     username = ADMIN_USERNAME

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate():
        username = form.username.data
        password = form.password.data
        
        # Replace with your actual User model and query
        admin_user = User.query.filter_by(username=username).first()
        
        if admin_user and check_password_hash(admin_user.password_hash, password):
            if login_user(admin_user, remember=True):
                flash('Logged in successfully.', 'success')
                return redirect(url_for('admin.admin_panel'))
            else:
                flash('Could not log in.', 'error')
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('admin/login.html', form=form)

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@admin_bp.route('/')
@login_required
def admin_panel():
    return render_template('admin/panel.html')

@admin_bp.route('/add_cup', methods=['GET', 'POST'])
@login_required
def add_cup():
    form = AddCupForm()
    if request.method == "POST" and form.validate():
        new_cup = Cup(name=form.name.data)
        db.session.add(new_cup)
        db.session.commit()
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin/add_cup.html', form=form)

@admin_bp.route('/add_competition', methods=['GET', 'POST'])
@login_required
def add_competition():
    form = AddCompetitionForm()
    form.cup_id.choices = [(cup.id, cup.name) for cup in Cup.query.all()]
    if request.method == "POST" and form.validate():
        new_competition = Competition(
            name=form.name.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            start_time=form.start_time.data,
            poster=form.poster.data,
            cup_id=form.cup_id.data
        )
        db.session.add(new_competition)
        db.session.commit()
        return redirect(url_for('admin.admin_panel'))
    return render_template('admin/add_competition.html', form=form)

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from werkzeug.utils import secure_filename
import os

@admin_bp.route('/add_results', methods=['GET', 'POST'])
@login_required
def add_results():
    form = AddResultsForm()
    form.competition_id.choices = [(c.id, c.name) for c in Competition.query.order_by('name')]
    competitions = Competition.query.all()
    competitions_data = [
        {
            'id': competition.id,
            'name': competition.name,
            'participants': [
                {
                    'id': participant.id,
                    'name': participant.name,
                    'landing_times1': str(participant.landing_times1),
                    'landing_times2': str(participant.landing_times2),
                    'landing_times3': str(participant.landing_times3),
                    'landing_times3': str(participant.landing_times3),
                    'landing_times4': str(participant.landing_times4),
                    'landing_times5': str(participant.landing_times5),
                    'landing_times6': str(participant.landing_times6),
                    'landing_times7': str(participant.landing_times7),
                    'landing_times8': str(participant.landing_times8),
                    'landing_times9': str(participant.landing_times9),
                    'landing_times10': str(participant.landing_times10),
                    'landing_times11': str(participant.landing_times11),
                    'landing_times12': str(participant.landing_times12),
                    'profile_pic': participant.profile_pic
                }
                for participant in competition.participants
            ]
        }
        for competition in competitions
    ]
    
    if request.method == 'POST' and form.validate():
        competition_id = form.competition_id.data
        competition = Competition.query.get(competition_id)
        
        for participant_form in form.data['participants']:
            print("Part Form: ", participant_form)
            try:
                print(participant_form['profile_pic'].filename)
                if participant_form['profile_pic']:
                    print(participant_form['profile_pic'].filename)
                    profile_pic = participant_form['profile_pic'].filename
            except Exception as e:
                    print(e)
                    profile_pic = None
            participant = Participant(
                name=participant_form['name'],
                competition_id=competition_id,
                profile_pic= profile_pic
            )
            
            # Handle profile picture upload
            if profile_pic:
                profile_pic = participant_form['profile_pic']
                filename = secure_filename(profile_pic.filename)
                profile_pic.save(os.path.join(UPLOAD_FOLDER, filename))
                participant.profile_pic = filename
            
              # Commit to generate the participant id

            # Handle landing times
            
            for i in range(1, 13):
                try:
                    landing_time = participant_form[f'landing_times{i}']
                    setattr(participant, f'landing_times{i}', landing_time)
                except KeyError:
                    setattr(participant, f'landing_times{i}', None)
            
            # Calculate the number of pigeons
            pigeons_count = sum(1 for i in range(1, 13) if participant_form[f'landing_times{i}'])
            print("Pigeon Count: ", pigeons_count)
            # Calculate total time
            participant.calculate_total_time(competition.start_time)
            db.session.add(participant)
            db.session.commit()
        db.session.commit()
        
        flash('Results added successfully!', 'success')
        return redirect(url_for('admin.admin_panel'))
    
    if request.method == "POST":
        print(form.data)
        print(form.errors)
    
    print("Competitions: ", competitions_data)
    return render_template('admin/add_results.html', form=form, competitions=competitions_data)

@admin_bp.route('/update_participant/<int:participant_id>', methods=['GET', 'POST'])
@login_required
def update_participant(participant_id):
    participant = Participant.query.get(participant_id)
    form = EditParticipantForm(obj=participant)

    if request.method == 'POST' and form.validate():
        participant.name = form.name.data

        if form.profile_pic.data:
            image_data = form.profile_pic.name
            open(os.path.join(UPLOAD_FOLDER, form.profile_pic.data), 'w').write(image_data)
            # profile_pic = form.profile_pic
            # filename = secure_filename(profile_pic.filename)
            # profile_pic.save(os.path.join(UPLOAD_FOLDER, filename))
            # participant.profile_pic = filename

        # Update landing times
        for i in range(1, 13):
            landing_time = getattr(form, f'landing_times{i}').data
            if landing_time:
                setattr(participant, f'landing_times{i}', landing_time)

        db.session.commit()

        # Recalculate total time
        competition = Competition.query.get(participant.competition_id)
        participant.calculate_total_time(competition.start_time)

        flash('Participant updated successfully!', 'success')
        return redirect(url_for('admin.add_results'))
    
    if request.method == "POST":
        print(form.errors)
    
    return render_template('admin/edit_participant.html', form=form, participant=participant)

@admin_bp.route('/delete_participant/<int:participant_id>', methods=['POST'])
@login_required
def delete_participant(participant_id):
    participant = Participant.query.get_or_404(participant_id)
    db.session.delete(participant)
    db.session.commit()
    flash('Participant deleted successfully!', 'success')
    return redirect(url_for('admin.add_results'))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)