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
  { 'group': 1, 'teacher': 'Tarana Kalantarova' },
  { 'group': 2, 'teacher': 'Latchine Bayramova' },
  { 'group': 3, 'teacher': 'Aytan Babaliyeva' },
  { 'group': 4, 'teacher': 'Vafa Guliyeva' },
  { 'group': 5, 'teacher': 'Tarana Kalantarova' },
  { 'group': 6, 'teacher': 'Irada Piriyeva' }
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
    # Extract lesson details safely
    subject = getattr(lesson, 'subject', {})
    course_name = subject.name if hasattr(subject, 'name') else subject.get('name', '') if isinstance(subject, dict) else ''
    
    teacher = ''
    teachers = getattr(lesson, 'teachers', [])
    if teachers:
        teacher_obj = teachers[0]
        teacher = teacher_obj.name if hasattr(teacher_obj, 'name') else teacher_obj.get('name', '') if isinstance(teacher_obj, dict) else ''
    
    language_subgroup = 0
    faculty_subgroup = 0

    groups = getattr(lesson, 'groups', None)

    if 'English' in course_name or 'French' in course_name:
      if groups and len(groups) > 0:
        language_subgroup = int(groups[0].split()[-1])
    else:
      if groups and len(groups) > 0:
        faculty_subgroup = int(groups[0].split()[-1])

    # Get lesson start and end times (API returns string format "HH:MM:SS")
    start_time_str = str(getattr(lesson, 'start_time', '00:00:00'))
    end_time_str = str(getattr(lesson, 'end_time', '00:00:00'))
    start_time_obj = datetime.strptime(start_time_str, "%H:%M:%S").time()
    end_time_obj = datetime.strptime(end_time_str, "%H:%M:%S").time()

    lesson_start = datetime.combine(datetime.today(), start_time_obj)
    lesson_end = datetime.combine(datetime.today(), end_time_obj)
        
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
          'Groups': [c.name for c in lesson.classes],
          'Teacher': teacher
        })

  return result

# Retrieves timetable for a specific date for a group
def get_timetable_for_date_util(edupage_instance, group, date):
  timetable = edupage_instance.get_timetable(group, date)
  timetable_for_date = []

  # 'timetable' object has a 'lessons' property
  lessons = getattr(timetable, 'lessons', [])
  
  # The new API endpoint returns lessons exactly for that date
  for lesson in lessons:
      # No need to filter by weekday if get_timetable only returns for this date
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
  
  total_days = (end_date - start_date).days + 1
  for i in range(total_days):
    current_date = start_date + timedelta(days=i)
    timetable = edupage_instance.get_timetable(group, current_date)
    lessons = getattr(timetable, 'lessons', [])
    
    for lesson in lessons:
      skip_this_lesson = True
      subject = getattr(lesson, 'subject', {})
      course_name = subject.name if hasattr(subject, 'name') else subject.get('name', '') if isinstance(subject, dict) else ''
      temp_lesson_name = course_name[6:].lower()
      
      for course in courses_list:
        if temp_lesson_name.startswith(course.lower()):
          skip_this_lesson = False
          break

      if skip_this_lesson:
        continue
      
      teachers = getattr(lesson, 'teachers', [])
      teacher_name = ''
      if teachers:
          t_obj = teachers[0]
          teacher_name = t_obj.name if hasattr(t_obj, 'name') else t_obj.get('name', '') if isinstance(t_obj, dict) else ''

      groups = getattr(lesson, 'groups', None)

      if course_name == 'UE323 French A1/IC' and l1_lan_group == 1:
        working_days.add(str(current_date))
      elif course_name == 'UE322 French/IC' and l1_lan_group > 1 and l1_lan_group < 7:
        if teacher_name == get_teacher(l1_lan_group):
          working_days.add(str(current_date))
      else:
        if groups is None or len(groups) == 0 or str(faculty_subgroup) in groups[0]:
          working_days.add(str(current_date))
        
  return list(working_days)