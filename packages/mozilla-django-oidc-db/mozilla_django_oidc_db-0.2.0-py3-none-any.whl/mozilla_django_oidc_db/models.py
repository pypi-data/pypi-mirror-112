from django.conf import settings
from django.db import models
from django.utils.encoding import force_text
from django.utils.translation import gettext_lazy as _

from django_better_admin_arrayfield.models.fields import ArrayField
from solo.models import SingletonModel, get_cache

import mozilla_django_oidc_db.settings as oidc_settings


def get_default_scopes():
    """
    Returns the default scopes to request for OpenID Connect logins
    """
    return ["openid", "email", "profile"]


class OpenIDConnectConfig(SingletonModel):
    """
    Configuration for authentication/authorization via OpenID connect
    """

    enabled = models.BooleanField(
        _("enable"),
        default=False,
        help_text=_(
            "Indicates whether OpenID Connect for authentication/authorization is enabled"
        ),
    )

    oidc_rp_client_id = models.CharField(
        _("OpenID Connect client ID"),
        max_length=1000,
        help_text=_("OpenID Connect client ID provided by the OIDC Provider"),
    )
    oidc_rp_client_secret = models.CharField(
        _("OpenID Connect secret"),
        max_length=1000,
        help_text=_("OpenID Connect secret provided by the OIDC Provider"),
    )
    oidc_rp_sign_algo = models.CharField(
        _("OpenID sign algorithm"),
        max_length=50,
        help_text=_("Algorithm the Identity Provider uses to sign ID tokens"),
        default="HS256",
    )
    oidc_rp_scopes_list = ArrayField(
        verbose_name=_("OpenID Connect scopes"),
        base_field=models.CharField(_("OpenID Connect scope"), max_length=50),
        default=get_default_scopes,
        blank=True,
        help_text=_("OpenID Connect scopes that are requested during login"),
    )

    oidc_op_jwks_endpoint = models.URLField(
        _("JSON Web Key Set endpoint"),
        max_length=1000,
        help_text=_(
            "URL of your OpenID Connect provider JSON Web Key Set endpoint. Required if `RS256` is used as signing algorithm"
        ),
        blank=True,
    )

    oidc_op_authorization_endpoint = models.URLField(
        _("Authorization endpoint"),
        max_length=1000,
        help_text=_("URL of your OpenID Connect provider authorization endpoint"),
    )
    oidc_op_token_endpoint = models.URLField(
        _("Token endpoint"),
        max_length=1000,
        help_text=_("URL of your OpenID Connect provider token endpoint"),
    )
    oidc_op_user_endpoint = models.URLField(
        _("User endpoint"),
        max_length=1000,
        help_text=_("URL of your OpenID Connect provider userinfo endpoint"),
    )
    oidc_rp_idp_sign_key = models.CharField(
        _("Sign key"),
        max_length=1000,
        help_text=_(
            "Key the Identity Provider uses to sign ID tokens in the case of an RSA sign algorithm. Should be the signing key in PEM or DER format"
        ),
        blank=True,
    )

    class Meta:
        verbose_name = _("OpenID Connect configuration")

    def __str__(self):
        return force_text(self._meta.verbose_name)

    @property
    def oidc_rp_scopes(self):
        """
        Scopes should be formatted as a string with spaces
        """
        return " ".join(self.oidc_rp_scopes_list)

    @classmethod
    def clear_cache(cls):
        cache_name = getattr(
            settings, "OIDC_CACHE", oidc_settings.MOZILLA_DJANGO_OIDC_DB_CACHE
        )
        if cache_name:
            cache = get_cache(cache_name)
            cache_key = cls.get_cache_key()
            cache.delete(cache_key)

    def set_to_cache(self):
        cache_name = getattr(
            settings,
            "MOZILLA_DJANGO_OIDC_DB_CACHE",
            oidc_settings.MOZILLA_DJANGO_OIDC_DB_CACHE,
        )
        if not cache_name:
            return None
        cache = get_cache(cache_name)
        cache_key = self.get_cache_key()
        timeout = getattr(
            settings,
            "MOZILLA_DJANGO_OIDC_DB_TIMEOUT",
            oidc_settings.MOZILLA_DJANGO_OIDC_DB_TIMEOUT,
        )
        cache.set(cache_key, self, timeout)

    @classmethod
    def get_cache_key(cls):
        prefix = getattr(
            settings,
            "MOZILLA_DJANGO_OIDC_DB_PREFIX",
            oidc_settings.MOZILLA_DJANGO_OIDC_DB_PREFIX,
        )
        return "%s:%s" % (prefix, cls.__name__.lower())

    @classmethod
    def get_solo(cls):
        cache_name = getattr(
            settings,
            "MOZILLA_DJANGO_OIDC_DB_CACHE",
            oidc_settings.MOZILLA_DJANGO_OIDC_DB_CACHE,
        )
        if not cache_name:
            obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
            return obj
        cache = get_cache(cache_name)
        cache_key = cls.get_cache_key()
        obj = cache.get(cache_key)
        if not obj:
            obj, created = cls.objects.get_or_create(pk=cls.singleton_instance_id)
            obj.set_to_cache()
        return obj
