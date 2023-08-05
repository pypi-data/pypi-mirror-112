# Generated by Django 2.2.24 on 2021-07-05 10:16

from django.db import migrations, models

import django_better_admin_arrayfield.models.fields

import mozilla_django_oidc_db.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="OpenIDConnectConfig",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "enabled",
                    models.BooleanField(
                        default=False,
                        help_text="Indicates whether OpenID Connect for authentication/authorization is enabled",
                        verbose_name="enable",
                    ),
                ),
                (
                    "oidc_rp_client_id",
                    models.CharField(
                        help_text="OpenID Connect client ID provided by the OIDC Provider",
                        max_length=1000,
                        verbose_name="OpenID Connect client ID",
                    ),
                ),
                (
                    "oidc_rp_client_secret",
                    models.CharField(
                        help_text="OpenID Connect secret provided by the OIDC Provider",
                        max_length=1000,
                        verbose_name="OpenID Connect secret",
                    ),
                ),
                (
                    "oidc_rp_sign_algo",
                    models.CharField(
                        default="HS256",
                        help_text="Algorithm the Identity Provider uses to sign ID tokens",
                        max_length=50,
                        verbose_name="OpenID sign algorithm",
                    ),
                ),
                (
                    "oidc_rp_scopes_list",
                    django_better_admin_arrayfield.models.fields.ArrayField(
                        base_field=models.CharField(
                            max_length=50, verbose_name="OpenID Connect scope"
                        ),
                        blank=True,
                        default=mozilla_django_oidc_db.models.get_default_scopes,
                        help_text="OpenID Connect scopes that are requested during login",
                        size=None,
                        verbose_name="OpenID Connect scopes",
                    ),
                ),
                (
                    "oidc_op_jwks_endpoint",
                    models.URLField(
                        blank=True,
                        help_text="URL of your OpenID Connect provider JSON Web Key Set endpoint. Required if `RS256` is used as signing algorithm",
                        max_length=1000,
                        verbose_name="JSON Web Key Set endpoint",
                    ),
                ),
                (
                    "oidc_op_authorization_endpoint",
                    models.URLField(
                        help_text="URL of your OpenID Connect provider authorization endpoint",
                        max_length=1000,
                        verbose_name="Authorization endpoint",
                    ),
                ),
                (
                    "oidc_op_token_endpoint",
                    models.URLField(
                        help_text="URL of your OpenID Connect provider token endpoint",
                        max_length=1000,
                        verbose_name="Token endpoint",
                    ),
                ),
                (
                    "oidc_op_user_endpoint",
                    models.URLField(
                        help_text="URL of your OpenID Connect provider userinfo endpoint",
                        max_length=1000,
                        verbose_name="User endpoint",
                    ),
                ),
                (
                    "oidc_rp_idp_sign_key",
                    models.CharField(
                        blank=True,
                        help_text="Key the Identity Provider uses to sign ID tokens in the case of an RSA sign algorithm. Should be the signing key in PEM or DER format",
                        max_length=1000,
                        verbose_name="Sign key",
                    ),
                ),
            ],
            options={
                "verbose_name": "OpenID Connect configuration",
            },
        ),
    ]
