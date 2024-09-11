from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from datetime import datetime
from edupage_api import EdupageForSkipSmart
from utils.timetable_utils import get_timetable_for_date_util, get_working_days_util
from utils.group_utils import get_group_by_id
import os

load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": os.environ['ALLOWED_ORIGIN']}})

@app.route('/api/timetable-service/v1/timetable-for-date')
def get_timetable_for_date():
	edupage = EdupageForSkipSmart()
	edupage.login(os.environ['EDUPAGE_USERNAME'], os.environ['EDUPAGE_PASSWORD'], os.environ['EDUPAGE_DOMAIN'])

	key = request.args.get('key')
	if key is None or key != os.environ['PASSWORD_KEY']:
		return jsonify({'message': 'Invalid key'}), 401

	timetable_date = datetime.strptime(request.args.get('date'), '%Y-%m-%d').date()
	group = get_group_by_id(edupage, int(request.args.get('group_id')))

	timetable = get_timetable_for_date_util(edupage, group, timetable_date)

	return jsonify(timetable), 200

@app.route('/api/timetable-service/v1/working-days', methods=['POST'])
def get_working_days():
	edupage = EdupageForSkipSmart()
	edupage.login(os.environ['EDUPAGE_USERNAME'], os.environ['EDUPAGE_PASSWORD'], os.environ['EDUPAGE_DOMAIN'])

	data = request.get_json()

	key = data.get('key')
	if key is None or key != os.environ['PASSWORD_KEY']:
		return jsonify({'message': 'Invalid key'}), 401

	start_date = datetime.strptime(data.get('start_date'), '%Y-%m-%d').date()
	end_date = datetime.strptime(data.get('end_date'), '%Y-%m-%d').date()
	group = get_group_by_id(edupage, int(data.get('group_id')))
	language_subgroup = int(data.get('language_subgroup'))
	faculty_subgroup = int(data.get('faculty_subgroup'))
	courses_param = data.get('courses', '')

	working_days = get_working_days_util(edupage, group, language_subgroup, faculty_subgroup, start_date, end_date, courses_param)

	return jsonify(working_days), 200

if __name__ == '__main__':
	app.run(port=5435)