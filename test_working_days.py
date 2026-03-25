import os
from datetime import date, timedelta
from dotenv import load_dotenv
from edupage_api import Edupage
from utils.group_utils import get_group_by_id
from utils.timetable_utils import get_working_days_util

load_dotenv()
edupage = Edupage()
edupage.login(os.environ['EDUPAGE_USERNAME'], os.environ['EDUPAGE_PASSWORD'], os.environ['EDUPAGE_DOMAIN'])

group = get_group_by_id(edupage, -157) # Group L2 CE-23 or similar
start = date(2026, 3, 18)
end = start + timedelta(days=14)

wdays = get_working_days_util(
    edupage, group, 
    language_subgroup=1, 
    faculty_subgroup=3, 
    start_date=start, 
    end_date=end, 
    courses="Physics;Mathematics;Computer;French;English"
)

print(f"Working days from {start} to {end}:")
print(wdays)
