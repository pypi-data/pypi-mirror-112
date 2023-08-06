from django.apps import apps as django_apps
from django.core.exceptions import ImproperlyConfigured

from django.conf import settings


def get_author_model():
    """
    Returns the Invitation model that is active in this project.
    """
    path = getattr(settings, 'INVITATIONS_AUTHOR_MODEL')
    try:
        return django_apps.get_model(path)
        print(django_apps.get_model(path).Meta.verbose_name)
    except ValueError:
        raise ImproperlyConfigured(
            "path must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            "path refers to model that\
             has not been installed"
        )
