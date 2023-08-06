from django.db import models
from django.contrib.auth.models import AbstractUser, Group
from xlibrary.fields import ForeignKeyOptional
# from accountinginfo.models import Ledger
from invitations.base_invitation import AbstractBaseInvitation
from django.utils.translation import ugettext_lazy as _
from invitations.app_settings import app_settings
from django.utils.crypto import get_random_string
from django.utils import timezone
import datetime
from django.contrib.sites.models import Site
from django.dispatch import receiver
from invitations.signals import invite_accepted
from invitations.adapters import get_invitations_adapter
from invitations import signals
from django.conf import settings
from django.core.exceptions import PermissionDenied
# from invitations.utils import get_invitation_model
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
# Create your models here.


class xManager(models.Manager):
    def __init__(self, key=''):
        super(xManager, self).__init__()
        self.k = key

    def for_user(self, user, methodname=''):
        if methodname == 'GET' and user.has_perm(self.model._meta.app_label + '.view_' + self.model.__name__.lower()) == False:
            # return super(xManager, self).get_queryset().none()
            raise PermissionDenied()
        if user.is_superuser:
            return super(xManager, self).get_queryset()
        elif user.is_staff:
            if user.groups.first().option.privilege == 'GROUP':
                return super(xManager, self).get_queryset().filter(user_created__groups__in=user.groups.all())
            else:
                return super(xManager, self).get_queryset()
        else:
            if self.k != '':
                return super(xManager, self).get_queryset().filter(**{self.k: user})
            else:
                return super(xManager, self).get_queryset().none()

    def all(self):
        return super(xManager, self).get_queryset()


class GroupOptions(models.Model):
    PRIVILEGE_CHOICES = (
        ('ALL', 'Can access all permitted data'),
        ('GROUP', 'Can access permitted data belonging to group only'),
        ('SELF', 'Can access permitted data belonging to the logged in user only'),
    )
    groups = models.OneToOneField(
        Group, on_delete=models.CASCADE, primary_key=True, related_name='FK_%(class)s_option')
    privilege = models.CharField(
        max_length=20, choices=PRIVILEGE_CHOICES, null=False, default='ALL',)

    def delete(self, *args, **kwargs):
        self.groups.delete()
        return super(self.__class__, self).delete(*args, **kwargs)


class User(AbstractUser):
    is_admin=models.BooleanField(default=False, help_text='Designates whether the user is an admin.', verbose_name='admin status')
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


class GuestInvitation(AbstractBaseInvitation):
    email = models.EmailField(unique=True, verbose_name=_('e-mail address'),
                              max_length=app_settings.EMAIL_MAX_LENGTH)
    created = models.DateTimeField(verbose_name=_('created'),
                                   default=timezone.now)
    authorentity = models.IntegerField('author',null=True,blank=True)

    @classmethod
    def create(cls, email, inviter=None, authorentity=None,  **kwargs):
        key = get_random_string(64).lower()
        instance = cls._default_manager.create(
            email=email,
            key=key,
            inviter=inviter,
            authorentity=authorentity,
            **kwargs)
        return instance

    def key_expired(self):
        expiration_date = (
            self.sent + datetime.timedelta(
                days=app_settings.INVITATION_EXPIRY))
        return expiration_date <= timezone.now()

    def send_invitation(self, request, **kwargs):
        current_site = kwargs.pop('site', Site.objects.get_current())
        invite_url = reverse('invitations:accept-invite',
                             args=[self.key])
        invite_url = request.build_absolute_uri(invite_url)
        ctx = kwargs
        ctx.update({
            'invite_url': invite_url,
            'site_name': current_site.name,
            'email': self.email,
            'key': self.key,
            'inviter': self.inviter,
        })
        email_template = 'invitations/email/email_invite'

        get_invitations_adapter().send_mail(
            email_template,
            self.email,
            ctx)
        self.sent = timezone.now()
        self.save()

        signals.invite_url_sent.send(
            sender=self.__class__,
            instance=self,
            invite_url_sent=invite_url,
            inviter=self.inviter)

    class Meta:
        verbose_name = "Guest Invitation"
        verbose_name_plural = "Guest Invitations"


# @receiver(invite_accepted)
# def update_ledger(sender, email, **kwargs):
#     try:
#         # Invitation = get_invitation_model()  # Get the Invitation model
#         # Grab the Invitation instance
#         # invite = Invitation.objects.get(email=email)
#         invite=GuestInvitation.objects.get(email=email)
#         user = User.objects.create(email=email)
#         invite.authorentity.guestlogin = user  # Pass your invitation's patient to the related user
#         invite.authorentity.save()
#     except GuestInvitation.DoesNotExist:
#         print("this was probably not an invited user.")
