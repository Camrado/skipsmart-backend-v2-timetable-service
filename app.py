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

@app.route('/api/timetable-service/v1/timetable-for-date')
def get_timetable_for_date():
	key = request.args.get('key')
	if key is None or key != os.environ['PASSWORD_KEY']:
		return jsonify({'message': 'Invalid key'}), 401

	timetable_date = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
	group = get_group_by_id(edupage, int(request.args.get('group_id')))

	timetable = get_timetable_for_date_util(edupage, group, timetable_date)

	return jsonify(timetable), 200

@app.route('/api/timetable-service/v1/working-days')
def get_working_days():
	key = request.args.get('key')
	if key is None or key != os.environ['PASSWORD_KEY']:
		return jsonify({'message': 'Invalid key'}), 401

	start_date = datetime.strptime(request.args.get('start_date'), '%Y-%m-%d').date()
	end_date = datetime.strptime(request.args.get('end_date'), '%Y-%m-%d').date()
	group = get_group_by_id(edupage, int(request.args.get('group_id')))
	language_subgroup = int(request.args.get('language_subgroup'))
	faculty_subgroup = int(request.args.get('faculty_subgroup'))

	working_days = get_working_days_util(edupage, group, language_subgroup, faculty_subgroup, start_date, end_date)

	return jsonify(working_days), 200