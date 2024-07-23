# Returns a group object by its id
def get_group_by_id(edupage_instance, group_id):
  groups = edupage_instance.get_classes()
  for g in groups:
    if g.class_id == group_id:
      return g
  return None