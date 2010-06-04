from plone.app.users.browser.register import RegistrationForm
from plone.app.users.browser.register import AddUserForm

class CaptchaRegistrationForm(RegistrationForm):
    """Registration form with captacha."""

class CaptchaAddUserForm(RegistrationForm):
    """Add user form with captacha."""
