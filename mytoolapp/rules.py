import rules
import guardian


@rules.predicate
def is_project_owner(user, project):
    return project.author == user


@rules.predicate
def has_model_level_permission(user):
    return user.has_perm('mytoolapp.delete_project')


@rules.predicate
def has_object_level_permission(user, project):
    return user.has_perm('mytoolapp.delete_project', project)


rules.add_perm('mytoolapp.can_delete_project',
               is_project_owner)  # mytoolapp要る？
#rules.add_rule('can_delete_project', is_project_owner)

"""
rules.add_perm('mytoolapp.rules_delete_project', is_project_owner |
               has_model_level_permission |
               has_object_level_permission)
"""
