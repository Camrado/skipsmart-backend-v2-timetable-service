from datetime import datetime, time, timedelta
import math

periods = [
    (time(8, 30), time(10, 0)),    # Period 1
    (time(10, 15), time(11, 45)),  # Period 2
    (time(12, 45), time(14, 15)),  # Period 3
    (time(14, 30), time(16, 0)),   # Period 4
    (time(16, 15), time(17, 45)),  # Period 5
    (time(18, 0), time(19, 30))    # Period 6
]

# Converts the response from edupage api to the desired format
def convert_lessons_to_dict(lessons):
    result = []

    for lesson in lessons:
        # Extract lesson details
        course_name = lesson.subject_name.name
        if lesson.groups and lesson.groups[0]:
            subgroup = int(lesson.groups[0].split()[-1])
        else:
            subgroup = 0
        
        # Get lesson start and end times
        lesson_start = datetime.combine(datetime.today(), lesson.start_time)
        lesson_end = datetime.combine(datetime.today(), lesson.end_time)
        
        for i, (period_start, period_end) in enumerate(periods):
            # Convert period start and end times to datetime
            period_start_time = datetime.combine(datetime.today(), period_start)
            period_end_time = datetime.combine(datetime.today(), period_end)
            
            # Check if lesson overlaps with the period
            if lesson_start < period_end_time and lesson_end > period_start_time:
                result.append({
                    'CourseName': course_name,
                    'Subgroup': subgroup,
                    'Period': i + 1
                })

    return result

# Retrieves timetable for a specific date for a group
def get_timetable_for_date_util(edupage_instance, group, date):
  timetable = edupage_instance.get_foreign_timetable(group, date)
  timetable_for_date = []

  for t in timetable:
    if t.weekday == date.weekday():
      timetable_for_date.append(t)
  
  return convert_lessons_to_dict(timetable_for_date)

# Returns a list of all the dates where there's at least one lesson for the the specified group and subgroup
def get_working_days_util(edupage_instance, group, subgroup, start_date, end_date):
  working_days = set()
  
  for i in range(math.ceil(((end_date - start_date).days + 1) / 7)):
    timetable = edupage_instance.get_foreign_timetable(group, start_date + timedelta(weeks=i))
    
    for lesson in timetable:
      if lesson.date >= start_date and lesson.date <= end_date:
        if lesson.groups is None or str(subgroup) in lesson.groups[0]:
        	working_days.add(str(lesson.date))
        
  return list(working_days)