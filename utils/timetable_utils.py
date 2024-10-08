from datetime import datetime, time, timedelta
import math
import re

periods = [
  (time(8, 30), time(10, 0)),    # Period 1
  (time(10, 15), time(11, 45)),  # Period 2
  (time(12, 45), time(14, 15)),  # Period 3
  (time(14, 30), time(16, 0)),   # Period 4
  (time(16, 15), time(17, 45)),  # Period 5
  (time(18, 0), time(19, 30))    # Period 6
]

L1_LANGUAGE_GROUPS = [
  { 'group': 1, 'teacher': 'A1 Khalid Aslanov', 'language': 'French' },
  { 'group': 2, 'teacher': 'Tarana Kalantarova', 'language': 'French' },
  { 'group': 3, 'teacher': 'Khalid Aslanov', 'language': 'French' },
  { 'group': 4, 'teacher': 'Vafa Guliyeva', 'language': 'French' },
  { 'group': 5, 'teacher': 'Aytan Babaliyeva', 'language': 'French' },
  { 'group': 6, 'teacher': 'Latchine Bayramova', 'language': 'French' },
  { 'group': 7, 'teacher': 'Sveta Gadimova ', 'language': 'English' },
  { 'group': 8, 'teacher': 'Shabnam Aliyeva', 'language': 'English' }
]

def get_teacher(l1_lan_group):
  for group_info in L1_LANGUAGE_GROUPS:
    if group_info['group'] == l1_lan_group:
      return group_info['teacher']
  return None  # If the group is not found


# Converts the response from edupage api to the desired format
def convert_lessons_to_dict(lessons):
  result = []

  for lesson in lessons:
    # Extract lesson details
    course_name = lesson.subject_name.name
    teacher = ''
    language_subgroup = 0
    faculty_subgroup = 0

    if 'English' in course_name or 'French' in course_name:
      if course_name == 'UE221 French A1/IC':
        teacher = 'A1 ' + lesson.teachers[0].name
      else:
        teacher = lesson.teachers[0].name
      if lesson.groups and lesson.groups[0]:
        language_subgroup = int(lesson.groups[0].split()[-1])
    else:
      if lesson.groups and lesson.groups[0]:
        faculty_subgroup = int(lesson.groups[0].split()[-1])
        
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
          'LanguageSubgroup': language_subgroup,
          'FacultySubgroup': faculty_subgroup,
          'Period': i + 1,
          'Teacher': teacher
        })

  return result

# Retrieves timetable for a specific date for a group
def get_timetable_for_date_util(edupage_instance, group, date):
  timetable = edupage_instance.get_foreign_timetable(group, date)
  timetable_for_date = []

  for lesson in timetable:
    if lesson.weekday == date.weekday():
      timetable_for_date.append(lesson)
  
  return convert_lessons_to_dict(timetable_for_date)

# Returns a list of all the dates where there's at least one lesson for the the specified group and subgroup
def get_working_days_util(edupage_instance, group, language_subgroup, faculty_subgroup, start_date, end_date, courses):
  working_days = set()
  courses_list = courses.split(';')
  l1_lan_group = -1

  for course in courses_list:
    if course.startswith('English') or course.startswith('French'):
      match = re.search(r'(\d+)$', course.strip())
      if match:
        l1_lan_group = int(match.group(1))
  
  for i in range(math.ceil(((end_date - start_date).days + 1) / 7)):
    timetable = edupage_instance.get_foreign_timetable(group, start_date + timedelta(weeks=i))
    
    for lesson in timetable:
      skip_this_lesson = True
      temp_lesson_name = lesson.subject_name.name[6:].lower()
      for course in courses_list:
        if temp_lesson_name.startswith(course.lower()):
          skip_this_lesson = False
          break

      if skip_this_lesson:
        continue

      if lesson.date >= start_date and lesson.date <= end_date:
        if lesson.subject_name.name == 'UE221 French A1/IC' and l1_lan_group == 1:
          working_days.add(str(lesson.date))
        elif lesson.subject_name.name == 'UE219 French/IC' and l1_lan_group > 1 and l1_lan_group < 7:
          if lesson.teachers[0].name == get_teacher(l1_lan_group):
            working_days.add(str(lesson.date))
        elif lesson.subject_name.name == 'UE218 English/IC' and l1_lan_group > 6 and l1_lan_group < 9:
          if lesson.teachers[0].name == get_teacher(l1_lan_group):
            working_days.add(str(lesson.date))
        else:
          if lesson.groups is None or str(faculty_subgroup) in lesson.groups[0]:
            working_days.add(str(lesson.date))
        
  return list(working_days)