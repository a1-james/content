from google.cloud import secretmanager
import json5
from Tests.scripts.utils import logging_wrapper as logging

SPECIAL_CHARS = [' ', '(', '(', ')', '.', '']


class GoogleSecreteManagerModule:
    def __init__(self, service_account_file: str):
        self.client = self.init_secret_manager_client(service_account_file)

    @staticmethod
    def convert_to_gsm_format(name: str) -> str:
        """
        param name: the name to transform
        return: the name after it's been transformed to a GSM supported format
        """

        for char in SPECIAL_CHARS:
            name = name.replace(char, '')
        return name

    def get_secret(self, project_id: str, secret_id: str, version_id: str = 'latest') -> dict:
        name = f"projects/{project_id}/secrets/{secret_id}/versions/{version_id}"
        response = self.client.access_secret_version(request={"name": name})
        try:
            return json5.loads(response.payload.data.decode("UTF-8"))
        except Exception as e:
            logging.error(
                f'Secret json is malformed for: {secret_id} version: {response.name.split("/")[-1]}, got error: {e}')

    def list_secrets(self, project_id: str, name_filter: list = [], with_secret=False, attr_validation=tuple()) -> list:
        secrets = []
        parent = f"projects/{project_id}"
        for secret in self.client.list_secrets(request={"parent": parent}):
            secret.name = str(secret.name).split('/')[-1]
            try:
                labels = dict(secret.labels)
            except Exception as e:
                labels = {}
                logging.error(f'Error the secret: {secret.name} has no labels, got the error: {e}')
            secret_pack_id = labels.get('pack_id')
            logging.debug(f'Getting the secret: {secret.name}')
            formatted_integration_search_ids = [GoogleSecreteManagerModule.convert_to_gsm_format(s.lower()) for s in
                                                name_filter]
            if name_filter and not secret_pack_id and secret_pack_id not in formatted_integration_search_ids:
                continue
            if with_secret:
                try:
                    secret_value = self.get_secret(project_id, secret.name)
                    # We make sure that the keys we want in the dict are present
                    missing_attrs = [attr for attr in attr_validation if attr not in secret_value]
                    if missing_attrs:
                        missing_attrs_str = ','.join(missing_attrs)
                        logging.error(
                            f'Error getting the secret: {secret.name}, it\'s missing the following required attributes: {missing_attrs_str}')  # noqa: E501
                        continue
                    secrets.append(secret_value)
                except Exception as e:
                    logging.error(f'Error getting the secret: {secret.name}, got the error: {e}')
            else:
                secrets.append(secret)

        return secrets

    @staticmethod
    def init_secret_manager_client(service_account: str) -> secretmanager.SecretManagerServiceClient:
        try:
            client = secretmanager.SecretManagerServiceClient.from_service_account_json(
                service_account)  # type: ignore # noqa
            return client
        except Exception as e:
            logging.error(f'Could not create GSM client, error: {e}')
