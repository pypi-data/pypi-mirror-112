import logging
from typing import List, Optional

from requests import Response

from cognite.well_model.client._api_client import APIClient
from cognite.well_model.client.api.api_base import BaseAPI
from cognite.well_model.client.models.resource_list import TrajectoryDataList, TrajectoryList
from cognite.well_model.client.utils.multi_request import cursor_multi_request
from cognite.well_model.models import (
    TrajectoryDataItems,
    TrajectoryDataRequest,
    TrajectoryDataRequestItems,
    TrajectoryItems,
    WellboresByIds,
)

logger = logging.getLogger("TrajectoryAPI")


class TrajectoriesAPI(BaseAPI):
    def __init__(self, client: APIClient):
        super().__init__(client)

    def _retrieve_multiple_by_wellbores(self, wellbore_external_ids: List[str]) -> TrajectoryList:
        wellbores_by_ids = WellboresByIds(items=wellbore_external_ids)
        path = self._get_path("/trajectories/bywellboreids")
        response: Response = self.client.post(url_path=path, json=wellbores_by_ids.json())
        return TrajectoryList(TrajectoryItems.parse_raw(response.text).items)

    def retrieve_multiple_by_wellbore(self, wellbore_external_id: str) -> TrajectoryList:
        """
        Get trajectories by a wellbore external id

        @param wellbore_external_id: wellbore external id
        @return: list of Trajectory objects
        """
        return self._retrieve_multiple_by_wellbores([wellbore_external_id])

    def retrieve_multiple_by_wellbores(self, wellbore_external_ids: List[str]) -> TrajectoryList:
        """
        Get trajectories by a list of wellbore external ids

        @param wellbore_external_ids: list of wellbore external ids
        @return: list of Trajectory objects
        """
        return self._retrieve_multiple_by_wellbores(wellbore_external_ids)

    def list_data(self, trajectory_data_request_list: List[TrajectoryDataRequest]) -> TrajectoryDataList:
        """
        Get multiple trajectory data by a list of TrajectoryDataRequest

        @param trajectory_data_request_list: list of trajectory data requests
        @return: list of TrajectoryData objects
        """
        trajectory_data_request_items = TrajectoryDataRequestItems(items=trajectory_data_request_list)
        path = self._get_path("/trajectories/data")
        response: Response = self.client.post(url_path=path, json=trajectory_data_request_items.json())
        return TrajectoryDataList(TrajectoryDataItems.parse_raw(response.text).items)
