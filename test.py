from datetime import datetime
import json
import os

from edupage_api import Edupage
from dotenv import load_dotenv
from utils.group_utils import get_group_by_id
from utils.timetable_utils import get_timetable_for_date_util

load_dotenv()


edupage = Edupage()

edupage.login(os.environ['EDUPAGE_USERNAME'], os.environ['EDUPAGE_PASSWORD'], os.environ['EDUPAGE_DOMAIN'])
    
timetable_date = datetime.strptime("2026-04-01", '%Y-%m-%d').date()
group = get_group_by_id(edupage, int(-157))

timetable = get_timetable_for_date_util(edupage, group, timetable_date)

import json
print(json.dumps(timetable, default=str, indent=4))

# print(edupage.get_classes())