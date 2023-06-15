import demistomock as demisto
from CommonServerPython import *  # noqa # pylint: disable=unused-wildcard-import
from CommonServerUserPython import *  # noqa
import smc
from smc import session
from smc.elements.network import IPList, DomainName
from smc.policy.layer3 import FirewallTemplatePolicy, FirewallPolicy
from smc.policy.rule import Rule
from smc.api.exceptions import ElementNotFound
import urllib3
from typing import Dict, Any

# Disable insecure warnings
urllib3.disable_warnings()


''' CONSTANTS '''

DATE_FORMAT = '%Y-%m-%dT%H:%M:%SZ'  # ISO8601 format with UTC, default in XSOAR
DEFAULT_LIMIT = 50
''' CLIENT CLASS '''


class Client(BaseClient):
    """Client class to interact with the service API

    This Client implements API calls, and does not contain any XSOAR logic.
    Should only do requests and return data.
    It inherits from BaseClient defined in CommonServer Python.
    Most calls use _http_request() that handles proxy, SSL verification, etc.
    For this  implementation, no special attributes defined
    """
    def __init__(self, url: str, api_key: str, insecure: bool, proxy: bool, port: str):
        self.url = url + ':' + port
        self.api_key = api_key
        self.insecure = insecure  # How to use ssl?
        self.proxy = proxy

    def login(self):
        """Logs into a session of smc
        """
        session.login(url=self.url, api_key=self.api_key, verify=self.insecure)

    def logout(self):
        """logs out of a session in smc
        """
        session.logout()


''' COMMAND FUNCTIONS '''


def test_module(client: Client) -> str:
    """Tests API connectivity and authentication'

    Returning 'ok' indicates that the integration works like it is supposed to.
    Connection to the service is successful.
    Raises exceptions if something goes wrong.

    :type client: ``Client``
    :param Client: client to use

    :return: 'ok' if test passed, anything else will fail the test.
    :rtype: ``str``
    """

    client.login()
    return 'ok'


def create_address_command(args: Dict[str, Any]) -> CommandResults:
    """Creating IP List with a list of addresses.

    Args:
        args (Dict[str, Any]): The command args.

    Returns:
        CommandResults
    """
    name = args.get('name')
    addresses = argToList(args.get('addresses', []))
    comment = args.get('comment', '')

    ip_list = IPList.create(name=name, iplist=addresses, comment=comment)

    outputs = {'Name': ip_list.name,
               'Addresses': ip_list.iplist,
               'Comment': ip_list.comment,
               'Deleted': False}
    return CommandResults(
        outputs_prefix='ForcepointSMC.Address',
        outputs=outputs,
        raw_response=outputs,
        readable_output=f'IP List {name} was created successfully.'
    )


def update_address_command(args: Dict[str, Any]) -> CommandResults:
    """Updating an IP List.

    Args:
        args (Dict[str, Any]): The command args.

    Returns:
        CommandResults
    """
    name = args.get('name')
    addresses = argToList(args.get('addresses', []))
    comment = args.get('comment', '')
    is_overwrite = args.get('is_overwrite', False)

    ip_list = IPList.update_or_create(name=name, append_lists=not is_overwrite, iplist=addresses, comment=comment)

    outputs = {'Name': ip_list.name,
               'Addresses': ip_list.iplist,
               'Comment': ip_list.comment}

    return CommandResults(
        outputs_prefix='ForcepointSMC.Address',
        outputs=outputs,
        raw_response=outputs,
        outputs_key_field='Name',
        readable_output=f'IP List {name} was updated successfully.'
    )


def list_address_command(args: Dict[str, Any]) -> CommandResults:
    """Lists the IP Lists in the system.

    Args:
        args (Dict[str, Any]): The command args.

    Returns:
        CommandResults
    """
    name = args.get('name', '')
    limit = arg_to_number(args.get('limit', DEFAULT_LIMIT))
    all_results = argToBoolean(args.get('all_results', False))

    ip_lists = []
    if name:
        ip_lists = list(IPList.objects.filter(name))
    elif all_results:
        ip_lists = list(IPList.objects.all())
    else:
        ip_lists = list(IPList.objects.limit(limit))

    outputs = []
    for ip_list in ip_lists:
        outputs.append({'Name': ip_list.name,
                        'Addresses': ip_list.iplist,
                        'Comment': ip_list.comment})

    return CommandResults(
        outputs_prefix='ForcepointSMC.Address',
        outputs=outputs,
        raw_response=outputs,
        outputs_key_field='Name',
        readable_output=tableToMarkdown(name='IP Lists:', t=outputs, removeNull=True),
    )


def delete_address_command(args: Dict[str, Any]) -> CommandResults:
    """Deleting IP List with a list of addresses.

    Args:
        args (Dict[str, Any]): The command args.

    Returns:
        CommandResults
    """
    name = args.get('name')

    try:
        ip_list = IPList(name).delete()

    except ElementNotFound:
        return CommandResults(readable_output=f'IP List {name} was not found.')

    outputs = {'Name': ip_list.name,
               'Deleted': True}

    return CommandResults(
        outputs_prefix='ForcepointSMC.Address',
        outputs_key_field='Name',
        outputs=outputs,
        readable_output=f'IP List {name} was deleted successfully.'
    )


''' MAIN FUNCTION '''


def main() -> None:
    """main function, parses params and runs command functions
    """
    params = demisto.params()
    url = params.get('url')
    api_key = params.get('credentials', {}).get('password')
    port = params.get('port')
    insecure = params.get('insecure', False)
    proxy = params.get('proxy', False)
    command = demisto.command()

    demisto.debug(f'Command being called is {command}')
    try:

        client = Client(
            url=url,
            api_key=api_key,
            insecure=insecure,
            proxy=proxy,
            port=port)

        if demisto.command() == 'test-module':
            result = test_module(client)
            return_results(result)

        client.login()

        if command == 'forcepoint-smc-address-create':
            return_results(create_address_command(demisto.args()))
        elif command == 'forcepoint-smc-address-update':
            return_results(update_address_command(demisto.args()))
        elif command == 'forcepoint-smc-address-list':
            return_results(list_address_command(demisto.args()))
        elif command == 'forcepoint-smc-address-delete':
            return_results(delete_address_command(demisto.args()))
    # Log exceptions and return errors
    except Exception as e:
        return_error(f'Failed to execute {command} command.\nError:\n{str(e)}')
    finally:
        client.logout()


''' ENTRY POINT '''


if __name__ in ('__main__', '__builtin__', 'builtins'):
    main()
