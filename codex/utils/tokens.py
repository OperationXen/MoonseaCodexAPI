from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return six.text_type(user.pk) + six.text_type(timestamp) + six.text_type(user.email_verified)

account_activation_token = AccountActivationTokenGenerator()


class PasswordResetToken(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        """ Include current hash and login time - if password changed or you log in, this token is invalidated """
        login_timestamp = '' if user.last_login is None else user.last_login.replace(microsecond=0, tzinfo=None)
        return (six.text_type(user.pk) + user.password + six.text_type(login_timestamp) + six.text_type(timestamp))

password_reset_token = PasswordResetToken()
