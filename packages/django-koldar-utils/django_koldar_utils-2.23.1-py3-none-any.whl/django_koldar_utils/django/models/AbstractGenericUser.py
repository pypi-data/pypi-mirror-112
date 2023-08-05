import abc
from typing import Optional

from arrow import Arrow
from django.contrib.auth.base_user import AbstractBaseUser
from django.core.mail import send_mail

from django.db import models
from django_koldar_utils.django.Orm import Orm
from django_koldar_utils.django.managers import ExtendedUserManager
from django_koldar_utils.django.models.mixins.ArrowAuditMixin import ArrowAuditMixIn


class AbstractGenericUser(AbstractBaseUser, ArrowAuditMixIn):
    """
    A class that substitute the standard User in django framework. Used to explicitly differentiate with the base user
    class that we are going to use in this django project to store each user additional properties.

    Any derived class of this user needs to specify the permission mixin it wants to use.
    There are 2 available:

    - django django.contrib.auth.models.PermissionsMixin which assume 2 relationshi groups and permissions
    - DatabaselessPermissionsMixin django_koldar_utils.django.models.DatabaselessPermissionsMixin which does not

    To chose, implement the class as follows:

    .. code-block :: python

        class MyUser(AbstractGenericUser, DatabaselessPermissionsMixin):
            # implementation

    If this user does not hav the capability you need, you can agument it using mixins
    """
    class Meta:
        db_table = Orm.create_table_name("User")
        default_permissions = ()
        abstract = True
    objects = ExtendedUserManager()

    username = Orm.required_unique_string(
        description="Username of the user. Used in the authentication method. Must be unique,")
    email = Orm.required_email(
        description="email address used for resetting the password"
    )

    active = Orm.required_boolean(
        default_value=True,
        description="If true, the user can log and work withint the system. False otherwise.",
    )
    is_superuser = Orm.required_boolean(
        default_value=False,
        description = "True if this user is an admin, False otherwise",
    )
    is_staff = Orm.required_boolean(
        default_value=False,
        description="Designates whether the user can log into this admin site."
    )

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to this user.

        :param subject: suvject of the email
        :param message. body of the message to send
        :param from_email: the entity that sends this email
        :param kwargs: arguments to pass to the mail server
        """
        send_mail(subject, message, from_email, [getattr(self, self.EMAIL_FIELD)], **kwargs)