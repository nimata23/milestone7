from time import timezone
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from os.path import dirname
import pandas as pd
from datetime import datetime



class Hawkins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date(), default=func.now())
    # time = db.Column(db.Time())
    # name = db.Column(db.String(100))
    # segment = db.Column(db.String(10))
    # position = db.Column(db.String(10))
    # type = db.Column(db.String(30))
    # excluded = db.Column(db.String(30))
    # tags = db.Column(db.String(50))
    # these below can be string "N/A"
    # sys_weight = db.Column(db.Integer)
    # init_threshold = db.Column(db.Integer)
    peak_force = db.Column(db.Integer)
    # net_peak_force = db.Column(db.Integer)
    # relative_peak_force = db.Column(db.Integer)
    # relative_peak_force_BW = db.Column(db.Integer)
    # LR_peak_force = db.Column(db.Integer)
    # lef_peak_force = db.Column(db.Integer)
    # right_peak_force = db.Column(db.Integer)


# Commented because we don't know what data is important to actually view.
# Ask Naser and peak team about the graphs that they show
    # 0
    # force_at_0_ms = db.Column(db.Integer)
    # net_force_at_0_ms = db.Column(db.Integer)
    # relative_force_at_0_ms= db.Column(db.Integer)
    # relative_force_at_0_ms_BW = db.Column(db.Integer)
    # left_force_at_0_ms = db.Column(db.Integer)
    # right_force_at_0_ms = db.Column(db.Integer)
    # # 50
    # force_at_50_ms = db.Column(db.Integer)
    # net_force_at_50_ms = db.Column(db.Integer)
    # relative_force_at_50_ms= db.Column(db.Integer)
    # relative_force_at_50_ms_BW = db.Column(db.Integer)
    # left_force_at_50_ms = db.Column(db.Integer)
    # right_force_at_50_ms = db.Column(db.Integer)
    # rfd_0to50_ms = db.Column(db.Integer)
    # impulse_0to50_ms = db.Column(db.Integer)
    # net_impulse_0to50_ms = db.Column(db.Integer)
    # # 100
    # force_at_100_ms = db.Column(db.Integer)
    # net_force_at_100_ms = db.Column(db.Integer)
    # relative_force_at_100_ms= db.Column(db.Integer)
    # relative_force_at_100_ms_BW = db.Column(db.Integer)
    # left_force_at_100_ms = db.Column(db.Integer)
    # right_force_at_100_ms = db.Column(db.Integer)
    # rfd_0to100_ms = db.Column(db.Integer)
    # impulse_0to100_ms = db.Column(db.Integer)
    # net_impulse_0to100_ms = db.Column(db.Integer)
    # # 150
    # force_at_150_ms = db.Column(db.Integer)
    # net_force_at_150_ms = db.Column(db.Integer)
    # relative_force_at_150_ms= db.Column(db.Integer)
    # relative_force_at_150_ms_BW = db.Column(db.Integer)
    # left_force_at_150_ms = db.Column(db.Integer)
    # right_force_at_150_ms = db.Column(db.Integer)
    # rfd_0to150_ms = db.Column(db.Integer)
    # impulse_0to150_ms = db.Column(db.Integer)
    # net_impulse_0to150_ms = db.Column(db.Integer)
    # # 200
    # force_at_200_ms = db.Column(db.Integer)
    # net_force_at_200_ms = db.Column(db.Integer)
    # relative_force_at_200_ms= db.Column(db.Integer)
    # relative_force_at_200_ms_BW = db.Column(db.Integer)
    # rfd_0to200_ms = db.Column(db.Integer)#based on data headers this is here, not below rightforce
    # left_force_at_200_ms = db.Column(db.Integer)
    # right_force_at_200_ms = db.Column(db.Integer)
    # impulse_0to200_ms = db.Column(db.Integer)
    # net_impulse_0to200_ms = db.Column(db.Integer)
    # # 250
    # force_at_250_ms = db.Column(db.Integer)
    # net_force_at_250_ms = db.Column(db.Integer)
    # relative_force_at_250_ms= db.Column(db.Integer)
    # relative_force_at_250_ms_BW = db.Column(db.Integer)
    # rfd_0to250_ms = db.Column(db.Integer)#based on data headers this is here, not below rightforce
    # left_force_at_250_ms = db.Column(db.Integer)
    # right_force_at_250_ms = db.Column(db.Integer)
    # impulse_0to250_ms = db.Column(db.Integer)
    # net_impulse_0to250_ms = db.Column(db.Integer)
    # pull_length = db.Column(db.Integer)
    # time_to_peak_force = db.Column(db.Integer)


    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))




class User(db.Model, UserMixin): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    password = db.Column(db.String(150))
    role = db.Column(db.String(150))
    # teams = db.Column(MutableList.as_mutable(PickleType),default=[])
    # append to teams with teams = teams + [any_data_type]
    # relationships down here
    notes = db.relationship('Note')
    hawkins = db.relationship('Hawkins')
    nutrition = db.relationship('Nutrition')
    sleep = db.relationship('Sleep')
    readiness = db.relationship('Readiness')
    # teams = db.relationship('Team')
    
    

users_table = db.Table('users',
                        db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
                        db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True)
                        )


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    users = db.relationship('User', secondary=users_table, lazy='subquery',
        backref=db.backref('teams', lazy=True))


# Sports medicine notes
class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(400))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Nutrition(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    calories = db.Column(db.Integer)
    # protein = db.Column(db.Integer)
    # carbohydrates = db.Column(db.Integer)
    # fats = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Sleep(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    # SleepScore = db.Column(db.Integer)
    TotalSleepScore = db.Column(db.Integer)
    # REMSleepScore = db.Column(db.Integer)
    # DeepSleepScore = db.Column(db.Integer)
    # SleepEfficiencyScore = db.Column(db.Integer)
    # RestfulnessScore = db.Column(db.Integer)
    # SleepLatencyScore = db.Column(db.Integer)
    # SleepTimingScore = db.Column(db.Integer)
    TotalSleepDuration = db.Column(db.Integer)
    # TotalBedtime = db.Column(db.Integer)	
    # AwakeTime = db.Column(db.Integer)
    # REMSleepDuration = db.Column(db.Integer)
    # LightSleepDuration = db.Column(db.Integer)
    # DeepSleepDuration = db.Column(db.Integer)
    # RestlessSleep = db.Column(db.Integer)
    # SleepEfficiency = db.Column(db.Integer)
    # SleepLatency = db.Column(db.Integer)
    # SleepTiming = db.Column(db.Integer)
    # BedtimeStart = db.Column(db.DateTime(timezone=True), default=func.now())
    # BedtimeEnd = db.Column(db.DateTime(timezone=True), default=func.now())
    # AverageRestingHeartRate = db.Column(db.Float)
    # LowestRestingHeartRate = db.Column(db.Integer)
    # AverageHRV = db.Column(db.Integer)
    # TemperatureDeviationC = db.Column(db.Float)
    # TemperatureTrendDeviation = db.Column(db.Float)
    # RespiratoryRate = db.Column(db.Float)
    # ActivityScore = db.Column(db.Integer)
    # StayActiveScore = db.Column(db.Integer)
    # MoveEveryHourScore = db.Column(db.Integer)
    # MeetDailyTargetsScore = db.Column(db.Integer)	
    # TrainingFrequencyScore = db.Column(db.Integer)
    # TrainingVolumeScore = db.Column(db.Integer)
    # ActivityBurn = db.Column(db.Integer)
    # TotalBurn = db.Column(db.Integer)
    # Steps = db.Column(db.Integer)
    # EquivalentWalkingDistance = db.Column(db.Integer)
    # InactiveTime = db.Column(db.Integer)
    # RestTime = db.Column(db.Integer)
    # LowActivityTime = db.Column(db.Integer)
    # MediumActivityTime = db.Column(db.Integer)
    # HighActivityTime = db.Column(db.Integer)
    # NonwearTime = db.Column(db.Integer)
    # AverageMET = db.Column(db.Float)
    # LongPeriodsofInactivity = db.Column(db.Integer)
    
    # PreviousNightScore = db.Column(db.Integer)
    # SleepBalanceScore = db.Column(db.Integer)
    # PreviousDayActivityScore = db.Column(db.Integer)
    # ActivityBalanceScore = db.Column(db.Integer)
    # TemperatureScore = db.Column(db.Integer)
    # RestingHeartRateScore = db.Column(db.Integer)
    # HRVBalanceScore = db.Column(db.Integer)
   
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class Readiness(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    RecoveryIndexScore = db.Column(db.Integer)  # From Jonna's csv files
    ReadinessScore = db.Column(db.Integer)  # From Jonna's csv files



def parse_csv(data_type: str, filename: str) -> None:
    """Parse a csv file."""
    # get the csv directory and merge it with filename
    csv_directory = f"{dirname(dirname(__file__))}/csvs"
    filepath = f"{csv_directory}/{filename}"
    # read the data from the csv
    csv_data = pd.read_csv(filepath_or_buffer=filepath, header=0)

    # conditional data ingestion
    if data_type == "user":
        data = []
        for row in csv_data.itertuples():
            # create a new User object
            user = User(
                email = row.email,
                first_name = row.first_name,
                last_name = row.last_name,
                password = row.password,
                role = row.role
            )
            # add the user to the database
            db.session.add(user)
            db.session.commit()

    elif data_type == "nutrition":
        data = []
        for row in csv_data.itertuples():
            # create a new Nutrition object
            nutrition = Nutrition(
                date = datetime.strptime(row.date, '%m/%d/%y'),
                calories = row.calories,
                protein = row.protein,
                carbohydrates = row.carbohydrates,
                fats = row.fats
            )
            # add the nutrition object to the database
            db.session.add(nutrition)
            db.session.commit()

    elif data_type == "readiness":
        data = []
        for row in csv_data.itertuples():
            # create a new Readiness object
            readiness = Readiness(
                date = datetime.strptime(row.date, '%m/%d/%y'),
                force = row.force
            )
            # add the readiness object to the database
            db.session.add(readiness)
            db.session.commit()

    # else, sleep data
    else:
        data = []
        for row in csv_data.itertuples():
            # create a new Sleep object
            sleep = Sleep(
                date = datetime.strptime(row.date, '%m/%d/%y'),
                total_duration = row.total_duration,
                REM = row.REM,
                deep_sleep = row.deep_sleep,
                light_sleep = row.light_sleep
            )
            # add the Sleep object to the database
            db.session.add(sleep)
            db.session.commit()
