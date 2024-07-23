from flask import Flask, request, jsonify
from dotenv import load_dotenv
from datetime import datetime
from edupage_api import EdupageForSkipSmart
from utils.timetable_utils import get_timetable_for_date_util, get_working_days_util
from utils.group_utils import get_group_by_id
import os

load_dotenv()

app = Flask(__name__)

edupage = EdupageForSkipSmart()
edupage.login(os.environ['EDUPAGE_USERNAME'], os.environ['EDUPAGE_PASSWORD'], os.environ['EDUPAGE_DOMAIN'])

@app.route('/timetable/timetable-for-date')
def get_timetable_for_date():
	data = request.get_json()
	timetable_date = datetime.strptime(data['date'], '%Y-%m-%d').date()
	group = get_group_by_id(edupage, data['group_id'])

	timetable = get_timetable_for_date_util(edupage, group, timetable_date)

	return jsonify(timetable), 200

@app.route('/timetable/working-days')
def get_working_days():
	data = request.get_json()
	start_date = datetime.strptime(data['start_date'], '%Y-%m-%d').date()
	end_date = datetime.strptime(data['end_date'], '%Y-%m-%d').date()
	group = get_group_by_id(edupage, data['group_id'])
	subgroup = data['subgroup']

	working_days = get_working_days_util(edupage, group, subgroup, start_date, end_date)

	return jsonify(working_days), 200