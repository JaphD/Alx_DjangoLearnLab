README: Permissions & Groups Setup
This document summarizes how role-based access is configured in the LibraryProject using Django’s permissions and groups.

1. Custom Permissions
Add to relationship_app/models.py:

class Book(models.Model):
    # … fields …

    class Meta:
        permissions = [
            ("can_view",   "Can v

Run migrations:
python manage.py makemigrations
python manage.py migrate

2. Groups & Permissions
Create 0002_create_groups.py migration:

def create_groups(apps, schema_editor):
    Group      = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')

    group_perms = {
        "Viewers": ["can_view"],
        "Editors": ["can_view", "can_create", "can_edit"],
        "Admins":  ["can_view", "can_create", "can_edit", "can_delete"],
    }

    for name, codenames in group_perms.items():
        group, _ = Group.objects.get_or_create(name=name)
        for codename in codenames:
            perm = Permission.objects.get(
                codename=codename,
                content_type__app_label='relationship_app'
            )
            group.permissions.add(perm)

Apply:
python manage.py migrate

3. Protecting Views
Use @permission_required:

@permission_required('relationship_app.can_create', raise_exception=True)
def create_book(request): …
Unauthorized access returns HTTP 403.

4. Template Checks
Show links only when allowed:

{% if perms.relationship_app.can_edit %}
  <a href="{% url 'relationship_app:book-edit' book.pk %}">Edit</a>
{% endif %}

5. Verification
- Assign users to Viewers/Editors/Admins.
- Confirm UI buttons and direct URLs respect permissions.
- Test each role for correct list/create/edit/delete access.






