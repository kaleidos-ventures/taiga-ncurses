from gmncurses.ui import views, signals


def login_view(username, password):
    login_view = views.LoginView("username", "password")
    login_view._username_editor.set_edit_text(username)
    login_view._password_editor.set_edit_text(password)
    return login_view

def api_successful_login_response(username):
    return {
        'auth_token': 'eyJ1c2VyX2lkIjoxfQ:1Vmjdp:ILIJVRazEdK_pObFedQc2aZNWd0',
        'color': '',
        'default_language': '',
        'default_timezone': '',
        'description': '',
        'email': 'niwi@niwi.be',
        'first_name': '',
        'full_name': 'admin',
        'id': 1,
        'is_active': True,
        'last_name': '',
        'notify_changes_by_me': False,
        'notify_level': 'all_owned_projects',
        'photo': '',
        'projects': [],
        'username': username,
    }
