from typing import Any, Dict

from dagster import Field, IntSource, Noneable, Permissive, StringSource, check
from gql import Client, gql
from gql.transport.requests import RequestsHTTPTransport
from requests.auth import HTTPBasicAuth

from ..auth import API_TOKEN_HEADER
from .errors import GraphQLStorageError


class GqlShimClient:
    """Adapter between the gql.Client and graphene.test.Client interfaces.

    Provides a uniform signature for execute(), uniform nesting of the return value, and a
    common error class."""

    def __init__(self, client: Client):
        self._client = check.inst_param(client, "client", Client)

    def execute(self, query: str, variable_values: Dict[str, Any] = None):
        try:
            return {"data": self._client.execute(gql(query), variable_values=variable_values)}
        except Exception as exc:  # pylint: disable=broad-except
            raise GraphQLStorageError(exc.__str__()) from exc


def create_proxy_client(url: str, config_value: Dict[str, Any], fetch_schema_from_transport=True):
    auth = HTTPBasicAuth("", "")
    transport = RequestsHTTPTransport(
        url=url,
        use_json=True,
        headers={
            "Content-type": "application/json",
            API_TOKEN_HEADER: config_value["agent_token"],
            **config_value.get("headers", {}),
        },
        verify=config_value.get("verify", True),
        retries=config_value.get("retries", 8),
        method=config_value.get("method", "POST"),
        timeout=config_value.get("timeout", None),
        cookies=config_value.get("cookies", {}),
        auth=auth,
    )
    return GqlShimClient(
        client=Client(transport=transport, fetch_schema_from_transport=fetch_schema_from_transport)
    )


def dagster_cloud_api_config():
    return {
        "url": Field(StringSource, default_value="http://localhost:2873"),
        "agent_token": Field(StringSource, is_required=True),
        "headers": Field(Permissive(), default_value={}),
        "cookies": Field(Permissive(), default_value={}),
        "timeout": Field(Noneable(IntSource), default_value=None),
        "verify": Field(bool, default_value=True),
        # This may be how we want to implement our retry policy, but it may be too restrictive:
        # we may want to put this logic into the storage itself so that we can do some kind of
        # logging
        "retries": Field(IntSource, default_value=8),
        "method": Field(StringSource, default_value="POST"),
    }
