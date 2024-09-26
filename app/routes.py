from flask import Blueprint, render_template
from .models import Cup, Competition, Participant
from datetime import timedelta
main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    most_recent_competition = Competition.query.order_by(Competition.end_date.desc()).first()
    if most_recent_competition:
        participants = Participant.query.filter_by(competition_id=most_recent_competition.id).all()
    else:
        participants = []
    cups = Cup.query.all()
    max_pigeons = 0
    total_times = {}
    timings = {}
    pigeon_counts = {}
    for participant in participants:
        times_count = [
                participant.landing_times1,
                participant.landing_times2,
                participant.landing_times3,
                participant.landing_times4,
                participant.landing_times5,
                participant.landing_times6,
                participant.landing_times7,
                participant.landing_times8,
                participant.landing_times9,
                participant.landing_times10,
                participant.landing_times11,
                participant.landing_times12
            ]
        count = 0
        timings[participant.id] = times_count
        for i in times_count:
            if i:
                count += 1
        pigeon_counts[participant.id] = count
        if max_pigeons < count:
            max_pigeons = count
        
        total_times[participant.id] = participant.calculate_total_time(most_recent_competition.start_time)
        
    return render_template('home.html', most_recent_competition=most_recent_competition, cups=cups, participants=participants, max_pigeons=max_pigeons, total_times=total_times, timings=timings, pigeon_counts=pigeon_counts)

@main_bp.route('/championship/<int:cup_id>')
def championship_list(cup_id):
    cup = Cup.query.get_or_404(cup_id)
    cups = Cup.query.all()
    
    for competition in cup.competitions:
        for participant in competition.participants:
            print("PART: ", participant, type(participant))
            participant.total_time = str(timedelta(seconds=sum([landing_time.hour * 3600 + landing_time.minute * 60 + landing_time.second for landing_time in participant.times if landing_time])))
    
    return render_template('championship_list.html', cup=cup, cups=cups)


@main_bp.route('/competition/<int:competition_id>', methods=['GET'])
def competition_detail(competition_id):
    competition = Competition.query.get_or_404(competition_id)
    participants = Participant.query.filter_by(competition_id=competition.id).all()

    # Calculate total time for each participant and store it
    for participant in participants:
        participant.calculate_total_time(competition.start_time)  # Pass the start time

    # Sort participants by total time after calculating it
    participants.sort(key=lambda p: p.total_time)  # Sort by the total_time attribute

    cups = Cup.query.all()
    return render_template('competition_detail.html', cups=cups, competition=competition, participants=participants)

