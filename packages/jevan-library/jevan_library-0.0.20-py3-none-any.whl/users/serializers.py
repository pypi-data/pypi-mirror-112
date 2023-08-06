from .models import GuestInvitation as InvitationModel, GroupOptions, User
# from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from invitations.adapters import get_invitations_adapter
from invitations.exceptions import (AlreadyAccepted, AlreadyInvited,
                                    UserRegisteredEmail)
from rest_framework import serializers
from xtrm_drest.serializers import (
    DynamicModelSerializer,
    DynamicRelationField
)
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from .utils import get_author_model
errors = {
    "already_invited": _("This e-mail address has already been"
                         " invited."),
    "already_accepted": _("This e-mail address has already"
                          " accepted an invite."),
    "email_in_use": _("An active user is using this e-mail address"),
}

AuthorModel = get_author_model()


class EmailListField(serializers.ListField):
    child = serializers.EmailField()


class InvitationWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationModel
        fields = ('email', 'authorentity',)

    def _validate_invitation(self, email):
        if InvitationModel.objects.all_valid().filter(
                email__iexact=email, accepted=False):
            raise AlreadyInvited
        elif InvitationModel.objects.filter(
                email__iexact=email, accepted=True):
            raise AlreadyAccepted
        elif User.objects.filter(email__iexact=email):
            raise UserRegisteredEmail
        else:
            return True

    def validate_authorentity(self, authorentity):
        if isinstance(authorentity, AuthorModel):
            author = authorentity
        else:
            try:
                author = AuthorModel.objects.get(pk=authorentity)
            except AuthorModel.DoesNotExist:
                author = None
        if author is None:
            raise serializers.ValidationError(
                ['Please specify a valid ' + AuthorModel._meta.verbose_name])
        elif not author.guestlogin is None:
            raise serializers.ValidationError(
                [AuthorModel._meta.verbose_name + ' has already been assigned a Guest Account'])

    def validate_email(self, email):
        email = get_invitations_adapter().clean_email(email)

        try:
            self._validate_invitation(email)
        except(AlreadyInvited):
            raise serializers.ValidationError(errors["already_invited"])
        except(AlreadyAccepted):
            raise serializers.ValidationError(errors["already_accepted"])
        except(UserRegisteredEmail):
            raise serializers.ValidationError(errors["email_in_use"])
        return email

    def create(self, validate_data):
        return InvitationModel.create(**validate_data)


class InvitationReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvitationModel
        fields = '__all__'


class InvitationBulkWriteSerializer(InvitationWriteSerializer):

    email = EmailListField()

    class Meta(InvitationWriteSerializer.Meta):
        model = InvitationModel
        fields = InvitationWriteSerializer.Meta.fields

    def validate_email(self, email_list):
        if len(email_list) == 0:
            raise serializers.ValidationError(
                _('You must add one or more email addresses')
            )
        for email in email_list:
            email = get_invitations_adapter().clean_email(email)
            try:
                self._validate_invitation(email)
            except(AlreadyInvited):
                raise serializers.ValidationError(errors["already_invited"])
            except(AlreadyAccepted):
                raise serializers.ValidationError(errors["already_accepted"])
            except(UserRegisteredEmail):
                raise serializers.ValidationError(errors["email_in_use"])
            return email_list


class ContenttypeSerializer(DynamicModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class GroupSerializer(DynamicModelSerializer):
    permissions = DynamicRelationField("PermissionSerializer", many=True)

    class Meta:
        model = Group
        fields = '__all__'


class UserSerializer(DynamicModelSerializer):
    groups = DynamicRelationField(GroupSerializer, many=True)
    class Meta:

        model = User
        exclude = ('user_permissions', 'password',)


class PermissionSerializer(DynamicModelSerializer):
    content_type = DynamicRelationField("ContenttypeSerializer")

    class Meta:
        model = Permission
        fields = '__all__'


class GroupOptionsSerializer(DynamicModelSerializer):
    groups = DynamicRelationField(GroupSerializer, writable=True)

    class Meta:
        model = GroupOptions
        fields = '__all__'
        read_only_fields = ('is_admin',)


class CUserSerializer(serializers.ModelSerializer):
    group_id = serializers.CharField(write_only=True)
    # author = serializers.IntegerField(write_only=True,required=False)

    class Meta:
        exclude = ('user_permissions',)
        read_only_fields = ('last_login', 'is_superuser',
                            'is_staff', 'date_joined', 'groups')
        model = User
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        if self.instance and self.instance.is_staff == False:
            raise serializers.ValidationError(
                {'username': ['You can not modify Guests']})
        if 'group_id' in data and data['group_id'] == "2":
            raise serializers.ValidationError(
                {'username': ['You can not create a Guest User, You need to invite him/her']})
        return data

    def create(self, validated_data):
        group_id = validated_data.pop('group_id', None)
        # author_id = validated_data.pop('author', None)
        if group_id == "-1":
            group_id = "2"
        user = User.objects.create(**validated_data)
        user.is_active = True
        user.is_superuser = False
        if group_id == "2":
            user.is_staff = False
        else:
            user.is_staff = True
        if group_id == "1":
            user.is_admin = True
        else:
            user.is_admin = False
        user.set_password(validated_data['password'])
        user.groups.add(group_id)
        user.save()
        # if author_id:
        #     authorObj=AuthorModel.objects.get(pk=author_id)
        #     if authorObj:
        #         authorObj.guestlogin=user
        #         authorObj.save()
        return user

    def update(self, instance, validated_data):
        group_id = validated_data.pop('group_id', None)
        user = super(CUserSerializer, self).update(instance, validated_data)
        user.is_superuser = False
        if group_id == 2:
            user.is_staff = False
        else:
            user.is_staff = True
        user.groups.clear()
        user.groups.add(group_id)
        user.save()
        return user


class CGroupSerializer(serializers.ModelSerializer):
    privilege = serializers.CharField(
        source='groups.privilege', read_only=True)
    option = serializers.CharField(write_only=True)

    def associate_permission(self, permission, group):
        ct_obj = set(p.content_type.model_class() for p in permission if hasattr(p.content_type.model_class(
        ), "xtrmMeta") and hasattr(p.content_type.model_class().xtrmMeta, "associate_model"))
        if ct_obj:
            asList = []
            for mclass in ct_obj:
                pList = tuple(
                    p.codename for p in permission if p.content_type.model_class() == mclass)
                for p in pList:
                    x = p.split('_')
                    for m in mclass.xtrmMeta.associate_model:
                        asList.append(x[0] + '_' + m.lower())
            if asList and len(asList) > 0:
                permission.extend(list(Permission.objects.filter(
                    codename__in=asList).values_list('id', flat=True)))
        group.permissions.set(permission)

    def create(self, validated_data):
        opts = validated_data.get('option')
        if opts:
            opts = validated_data.pop('option')
        perms = validated_data.get('permissions')
        if perms:
            perms = validated_data.pop('permissions')
        gp = Group.objects.create(**validated_data)
        if perms:
            self.associate_permission(perms, gp)
        if opts:
            GroupOptions.objects.create(groups=gp, privilege=opts)
        return gp

    def update(self, instance, validated_data):
        opts = validated_data.get('option')
        if opts:
            opts = validated_data.pop('option')
        perms = validated_data.get('permissions')
        if perms:
            perms = validated_data.pop('permissions')
        oinstance = super(CGroupSerializer, self).update(
            instance, validated_data)
        oinstance.permissions.clear()
        if perms:
            self.associate_permission(perms, oinstance)
        groupOption = GroupOptions.objects.get(groups=oinstance)
        if groupOption and opts:
            groupOption.privilege = opts
            groupOption.save()
        return oinstance

    class Meta:
        model = Group
        name = 'group'
        fields = '__all__'


# class CGroupOptionsSerializer(serializers.ModelSerializer):
#     groups = GroupSerializer(required=False, read_only=False)

#     class Meta:
#         model = GroupOptions
#         fields = '__all__'
