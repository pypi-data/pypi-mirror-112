import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import NPTList
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import NPT, DoubleRange, Filter, LengthRange, NPTFilter, NPTItems

logger = logging.getLogger("NPTEventsAPI")


class NPTEventsAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

    def list(
        self,
        md: Optional[LengthRange] = None,
        duration: Optional[DoubleRange] = None,
        npt_codes: Optional[List[str]] = None,
        npt_code_details: Optional[List[str]] = None,
        wellbore_external_ids: Optional[List[str]] = None,
        limit: Optional[int] = 100,
    ) -> NPTList:
        """
        Get NPT events that matches the filter

        @param md - range of measured depth in desired NPT events
        @param duration - duration of desired NDS events
        @param npt_codes - npt_codes of desired NDS events
        @param npt_code_details - npt_code_details of desired NDS events
        @param wellbore_external_ids - list of interested wellbore external ids
        @return: NPTList object
        """

        def request(cursor):
            npt_filter = NPTFilter(
                filter=Filter(
                    measured_depth=md,
                    duration=duration,
                    npt_codes=npt_codes,
                    npt_code_details=npt_code_details,
                    wellbore_external_ids=wellbore_external_ids,
                ),
                cursor=cursor,
            )

            path: str = self._get_path("/npt/list")
            response: Response = self.client.post(url_path=path, json=npt_filter.json())
            npt_items: NPTItems = NPTItems.parse_raw(response.text)
            return npt_items

        items = cursor_multi_request(
            get_cursor=self._get_cursor, get_items=self._get_items, limit=limit, request=request
        )
        return NPTList(items)

    @staticmethod
    def _get_items(npt_items: NPTItems) -> List[NPT]:
        items: List[NPT] = npt_items.items  # For mypy
        return items

    @staticmethod
    def _get_cursor(npt_items: NPTItems) -> Optional[str]:
        next_cursor: Optional[str] = npt_items.next_cursor  # For mypy
        return next_cursor
