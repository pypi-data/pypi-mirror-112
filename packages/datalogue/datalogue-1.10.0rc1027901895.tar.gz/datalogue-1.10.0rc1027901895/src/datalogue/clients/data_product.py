from uuid import UUID
from typing import List

from datalogue.dtl_utils import is_valid_uuid
from datalogue.clients.http import _HttpClient, Union, HttpMethod, Optional
from datalogue.dtl_utils import _parse_list
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

    def add_pipelines(self, data_product_id: UUID, pipeline_ids: List[UUID]) -> Union[DtlError, DataProduct]:
        """
        Add Pipelines to a Data Product.
        :param data_product_id: id of the Data Product
        :param pipeline_ids: ids of the pipelines that need to be added to a Data Product
        :return: updated Data Product object if successful, or DtlError if failed
        """
        if is_valid_uuid(data_product_id) is False:
            return DtlError("data_product_id provided is not a valid UUID format.")
        if len(pipeline_ids) == 0:
            return DtlError("Please specify at least 1 pipeline id under pipeline_ids")
        else:
            payload = {
                "streamIds": pipeline_ids,
                "streamAction": "add"
            }

        res = self.http_client.make_authed_request(
            self.service_uri + f"/data-products/{data_product_id}/streams", HttpMethod.POST, payload
        )
        if isinstance(res, DtlError):
            return res
        return DataProduct._from_payload(res)

    def remove_pipelines(self, data_product_id: UUID, pipeline_ids: List[UUID]) -> Union[DtlError, DataProduct]:
        """
        Remove Pipelines from a Data Product.
        :param data_product_id: id of the Data Product
        :param pipeline_ids: ids of the pipelines to be removed from a Data Product
        :return: updated Data Product object if successful, or DtlError if failed
        """
        if is_valid_uuid(data_product_id) is False:
            return DtlError("data_product_id provided is not a valid UUID format.")
        if len(pipeline_ids) == 0:
            return DtlError("Please specify at least 1 pipeline id under pipeline_ids")
        else:
            payload = {
                "streamIds": pipeline_ids,
                "streamAction": "remove"
            }

        res = self.http_client.make_authed_request(
            self.service_uri + f"/data-products/{data_product_id}/streams", HttpMethod.POST, payload
        )
        if isinstance(res, DtlError):
            return res
        return DataProduct._from_payload(res)

    def delete(self, id: UUID, delete_pipelines: bool = True) -> Union[DtlError, bool]:
        """
        Deletes the given Data Product

        :param id: id of the data product to be deleted
        :param delete_pipelines: cascade delete all pipelines with permissions of this Data Product, default True
        :return: true if successful, DtlError otherwise
        """
        if is_valid_uuid(id) is False:
            return DtlError("id provided is not a valid UUID format.")
        res = self.http_client.make_authed_request(self.service_uri + f"/data-products/{id}?delete-streams={delete_pipelines}", HttpMethod.DELETE)
        if isinstance(res, DtlError):
            return res
        else:
            return True

    def list(self, by_name: str = '', page: int = 1, size: int = 25)\
            -> Union[DtlError, List[DataProduct]]:
        """
        List all the data products that are saved

        :param by_name: optionally filter your list by data product names, containing the supplied keyword, default ''
        :param page: page to be retrieved, default 1
        :param size: number of items to be put in a page, default 25
        :return: Returns a List of all the available data products or DtlError
        """
        params = {"page": page, "size": size, "search-in-name": by_name}
        res = self.http_client.make_authed_request(
            path=self.service_uri + f"/data-products",
            method=HttpMethod.GET,
            params=params
        )
        if isinstance(res, DtlError):
            return res
        return _parse_list(DataProduct._from_payload)(res)
