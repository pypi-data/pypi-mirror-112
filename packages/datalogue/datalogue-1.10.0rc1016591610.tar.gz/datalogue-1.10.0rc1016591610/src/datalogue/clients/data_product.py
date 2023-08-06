from uuid import UUID

from datalogue.dtl_utils import is_valid_uuid
from datalogue.clients.http import _HttpClient, Union, HttpMethod, Optional
from datalogue.errors import DtlError
from datalogue.models.data_product import DataProduct


class _DataProductClient:
    """
    Client to interact with the Data Products
    """

    def __init__(self, http_client: _HttpClient):
        self.http_client = http_client
        self.service_uri = "/scout"

    def create(self, data_product: DataProduct) -> Union[DtlError, DataProduct]:
        """
        Creates a Data Product
        :param data_product: A Data Product object that user wants to create
        :return: Returns created Data Product object if successful, or DtlError if failed
        """
        payload = data_product._as_payload()
        res = self.http_client.make_authed_request(self.service_uri + "/data-products", HttpMethod.POST, payload)

        if isinstance(res, DtlError):
            return res

        return DataProduct._from_payload(res)

    def update(self, id: UUID, name: Optional[str], description: Optional[str]) -> Union[DtlError, DataProduct]:
        """
          Updates a Data Product
          :param id: id of the Data Product to be updated
          :param name: New name to be applied to the data product
          :param description: New description to be applied to the data product
          :return: Returns an updated Data Product object if successful, or DtlError if failed
        """
        payload = {}

        if is_valid_uuid(id) is False:
            return DtlError("id provided is not a valid UUID format.")

        if name is None and description is None:
            return DtlError("Either name or description must be mentioned to update a Data Product")

        if name is not None:
            payload["name"] = name

        if description is not None:
            payload["description"] = description

        res = self.http_client.make_authed_request(
            self.service_uri + f"/data-products/{id}", HttpMethod.PUT, payload
        )

        if isinstance(res, DtlError):
            return res

        return DataProduct._from_payload(res)

    def get(self, id: UUID) -> Union[DtlError, DataProduct]:
        """
            Retrieve a Data Product by its id.
            :param id: id of an existing Data Product to be retrieved
            :return: Data Product object if successful, or DtlError if failed
        """
        if is_valid_uuid(id) is False:
            return DtlError("id provided is not a valid UUID format.")
        res = self.http_client.make_authed_request(self.service_uri + f"/data-products/{id}", HttpMethod.GET)
        if isinstance(res, DtlError):
            return res
        return DataProduct._from_payload(res)
