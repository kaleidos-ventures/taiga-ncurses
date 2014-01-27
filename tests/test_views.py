from taiga_ncurses.ui import views


def test_login_views_username_property_is_the_typed_username():
    lv = views.auth.LoginView("username", "password")
    username = "Hulk Hogan"
    lv._username_editor.set_edit_text(username)
    assert lv.username == username

def test_login_views_password_property_is_the_typed_password():
    lv = views.auth.LoginView("username", "password")
    password = "1234567890"
    lv._password_editor.set_edit_text(password)
    assert lv.password == password
