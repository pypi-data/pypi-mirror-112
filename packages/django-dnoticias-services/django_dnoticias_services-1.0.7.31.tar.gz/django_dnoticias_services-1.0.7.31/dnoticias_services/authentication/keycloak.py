import json
import base64
from distutils.util import strtobool
from uuid import uuid4

from django.conf import settings
from django.contrib.auth import get_backends, get_user_model
from django.core.files.storage import get_storage_class
from django.core.exceptions import SuspiciousOperation
from dnoticias_services.mail import mail
from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from keycloak import KeycloakAdmin, KeycloakOpenID

User = get_user_model()


class BaseKeyCloak(object):
    def __init__(self):
        self.server_url = getattr(settings, "KEYCLOAK_SERVER_URL", "")
        self.admin_realm_name = getattr(settings, "KEYCLOAK_ADMIN_REALM_NAME", "")
        self.user_realm_name = getattr(settings, "KEYCLOAK_USER_REALM_NAME", "") or self.admin_realm_name
        self.username = getattr(settings, "KEYCLOAK_ADMIN_USERNAME", "")
        self.password = getattr(settings, "KEYCLOAK_ADMIN_PASSWORD", "")
        self.client_id = getattr(settings, "KEYCLOAK_CLIENT_ID", "")
        self.client_secret_key = getattr(settings, "KEYCLOAK_CLIENT_SECRET_KEY", "")

        self.keycloak_admin = KeycloakAdmin(
                                server_url=self.server_url,
                                username=self.username,
                                password=self.password,
                                realm_name=self.admin_realm_name,
                                user_realm_name=self.user_realm_name,
                                verify=True
                            )

        self.keycloak_openid = KeycloakOpenID(
                                server_url=self.server_url,
                                client_id=self.client_id,
                                realm_name=self.user_realm_name,
                                client_secret_key=self.client_secret_key,
                                verify=True
                            )

    def get_backend(self):
        backends = get_backends()

        for backend in backends:
            if issubclass(backend.__class__, OIDCAuthenticationBackend):
                return backend

        raise ValueError("No backend that is subclass of OIDCAuthenticationBackend")


class UpdateUser(BaseKeyCloak):
    """
    Updates an user in both sides (Keycloak and backends).
    """
    def __call__(self, email, first_name='', last_name='', enabled=True, is_staff=False, is_superuser=False):
        self.keycloak_admin.refresh_token()
        user_id_keycloack = self.keycloak_admin.get_user_id(email)

        if user_id_keycloack is None:
            message = "That user doesn't exists in keycloak"
            raise SuspiciousOperation(message)

        payload = {
            'firstName': first_name,
            'lastName': last_name,
            'enabled': enabled,
            'attributes': {
                'is_staff': is_staff,
                'is_superuser': is_superuser,
            }
        }

        self.keycloak_admin.update_user(
            user_id=user_id_keycloack,
            payload=payload,
        )

        user_info = self.keycloak_admin.get_user(user_id_keycloack)

        backend = self.get_backend()
        claims_verified = backend.verify_claims(user_info)

        if not claims_verified:
            message = 'Claims verification failed'
            raise SuspiciousOperation(message)

        users = backend.filter_users_by_claims(user_info)

        user_info['given_name'] = first_name
        user_info['family_name'] = last_name
        user_info['is_active'] = enabled

        if len(users) == 1:
            return backend.update_user(users[0], user_info)
        else:
            message = 'Cannot update the user. Users returned zero or more than one entry.'
            raise SuspiciousOperation(message)

        return None


class CreateUser(BaseKeyCloak):
    def __call__(self, email, first_name='', last_name='', enabled=True, email_verified=False, password=None, temporary_password=True, is_staff=False, is_superuser=False, send_email_to_user=False, **kwargs):
        self.keycloak_admin.refresh_token()

        user_id_keycloack = self.keycloak_admin.get_user_id(email)

        if user_id_keycloack is None:
            if temporary_password:
                password = uuid4()

            credentials = {
                "type": "password",
            }

            if kwargs.get('credential_data') and kwargs.get('secret_data'):
                salt = kwargs['secret_data'].get('salt', '')
                salt = salt.encode()
                kwargs['secret_data']['salt'] = base64.b64encode(salt).decode()
                credentials['credentialData'] = json.dumps(kwargs.get('credential_data'))
                credentials['secretData'] = json.dumps(kwargs.get('secret_data'))
            else:
                credentials['value'] = str(password)
            
            credentials["temporary"] = temporary_password

            user_id_keycloack = self.keycloak_admin.create_user(
                {
                    "email": email,
                    "username": email,
                    "firstName": first_name,
                    "lastName": last_name,
                    "enabled": enabled,
                    "emailVerified" : email_verified,
                    "credentials": [credentials],
                    "realmRoles": ["user_default",],
                    "attributes": {
                        "is_staff": is_staff,
                        "is_superuser": is_superuser,
                    }
                }
            )

        user_info = self.keycloak_admin.get_user(user_id_keycloack)
        self.normalize_user_info(user_info)

        email = user_info.get('email')

        backend = self.get_backend()
        claims_verified = backend.verify_claims(user_info)
        if not claims_verified:
            msg = 'Claims verification failed'
            raise SuspiciousOperation(msg)

        # email based filtering
        users = backend.filter_users_by_claims(user_info)

        user_info['given_name'] = first_name
        user_info['family_name'] = last_name
        user_info['is_active'] = enabled

        if len(users) == 1:
            return backend.update_user(users[0], user_info)
        elif len(users) > 1:
            # In the rare case that two user accounts have the same email address,
            # bail. Randomly selecting one seems really wrong.
            msg = 'Multiple users returned'
            raise SuspiciousOperation(msg)
        elif backend.get_settings('OIDC_CREATE_USER', True):
            if send_email_to_user:
                mail.send_email(
                    email=email,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    template_uuid=settings.EMAIL_TEMPLATE_LOGIN_INFO_UUID,
                    brand_group_uuid=settings.EMAIL_BRAND_GROUP_UUID,
                    subject=settings.EMAIL_USER_CREATION_SUBJECT,
                    context={
                        'first_name': first_name,
                        'last_name': last_name,
                        'email': email,
                        'new_password': str(password),
                    }
                )

            return backend.create_user(user_info)
        
        return None

    def normalize_user_info(self, user_info):
        attributes = user_info.get("attributes", {})

        for key in attributes:
            if isinstance(attributes[key], list):
                value = attributes[key][0] if len(attributes[key]) == 1 else attributes[key] 
                try:
                    attributes[key] = bool(strtobool(value))
                except ValueError as e:
                    attributes[key] = value
        
        user_info.update(attributes)


class UpdatePassword(BaseKeyCloak):
    def __call__(self, email, password, temporary=False, send_email_to_user=False, **kwargs):
        self.keycloak_admin.refresh_token()
        user_id_keycloack = self.keycloak_admin.get_user_id(email)
        self.keycloak_admin.set_user_password(user_id=user_id_keycloack, password=password, temporary=temporary)

        if send_email_to_user:
            mail.send_email(
                email=email,
                from_email=settings.DEFAULT_FROM_EMAIL,
                template_uuid=settings.EMAIL_TEMPLATE_RESET_LOGIN_INFO_UUID,
                brand_group_uuid=settings.EMAIL_BRAND_GROUP_UUID,
                subject=settings.EMAIL_USER_PASSWORD_NOTIFICATION_SUBJECT,
                context={
                    'name': kwargs.get('name', ''),
                    'email': email,
                    'plain_password': password,
                }
            )


class GetToken(BaseKeyCloak):
    def __call__(self, email, password):
        return self.keycloak_openid.token(email, password)

update_user = UpdateUser()
create_user = CreateUser()
update_password = UpdatePassword()
get_token = GetToken()
