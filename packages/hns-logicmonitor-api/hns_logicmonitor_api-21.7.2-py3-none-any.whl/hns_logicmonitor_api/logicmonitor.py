from hns_logicmonitor_api.lm_base import LMBase
from requests import Response
from typing import Optional, List
from more_itertools import grouper, zip_equal
from hns_logicmonitor_api.exceptions import InvalidNumOfItemsError, RequestFailedError, ItemNotFoundError


class LogicMonitor(LMBase):

    def __init__(self, account_name: str, access_id: str, api_key: str, global_timeout: int = 5):
        """
        API to logic monitor
        :param account_name: Logic monitor account name
        :param access_id: Logic monitor API access ID
        :param api_key: API key
        :param global_timeout: Request timeout in seconds for every request within the session
        """
        super().__init__(account_name, access_id, api_key, global_timeout)
        self._gpon_optics_ds_name = 'GPONOpticStats'

    @staticmethod
    def _prepare_ont_sn(ont_sn: str):
        """ On logicmonitor ONT SN shows in pairs of two separated by colons """

        ont_sn = ont_sn.lower()
        ont = grouper(ont_sn, 2)
        result = []
        for _ in ont:
            result.append(''.join(_))
        return ':'.join(result)

    @staticmethod
    def _check_response(resp: Response, error_msg: str) -> dict:
        """ Checks if the response is good and if not raises exceptions else return response data """

        if not resp.ok:
            raise RequestFailedError(
                response_content=resp.content.decode(),
                response_status=resp.status_code,
                msg=error_msg

            )
        res_data = resp.json()
        if res_data['total'] == 0:
            raise ItemNotFoundError(
                response_content=resp.content.decode(),
                response_status=resp.status_code,
                msg=error_msg
            )
        elif res_data['total'] != 1:
            raise InvalidNumOfItemsError(
                response_content=resp.content.decode(),
                response_status=resp.status_code,
                msg=error_msg
            )
        return res_data

    def get_id(self, url: str, resource_type: str, filter: str) -> int:

        url = url + f'?filter={filter}' + '&fields=id'
        resp = self.get(url)
        res_data = self._check_response(resp, f'{resource_type}: filter: {filter}')
        return res_data['items'][0]['id']

    def get_device_id_by_display_name(self, display_name: str) -> int:
        """
        Gets LM device id by for a devices with the given display name
        :param display_name: Device display name
        :return:
        """

        url = self._devices_base_url
        return self.get_id(url, resource_type='device', filter=f'displayName:"{display_name}"')

    def get_device_gpon_optics_datasource_id(self, device_id: int) -> Optional[int]:
        """
        Gets the GPON Optics datasource ID
        :param device_id: Logic monitor device ID
        :return: GPON Optics datasource ID as int or None if no datasource found
        """

        url = f'{self._devices_base_url}/{device_id}/devicedatasources'
        return self.get_id(
            url,
            resource_type='device_datasources',
            filter=f'dataSourceName:"{self._gpon_optics_ds_name}"'
        )

    def get_device_ont_instance_id(self, ont_sn: str, device_id: int, data_source_id: int) -> Optional[int]:
        """
        Gets the instance ID for an ONT on a device
        :param ont_sn: ONT SN
        :param device_id: Device ID - This is the OLT device ID
        :param data_source_id: Data source ID - This is the GPON Optics datasource ID
        :return: Instance ID as int or None if no instance found
        """

        url = f'{self._devices_base_url}/{device_id}/devicedatasources/{data_source_id}/instances'
        return self.get_id(
            url,
            resource_type='datasource_instances',
            filter=f'name:"{self._gpon_optics_ds_name}-{self._prepare_ont_sn(ont_sn)}"'
        )

    def get_instance_most_recent_data(self, device_id: int, data_source_id: int, instance_id: int) -> dict:
        """
        Gets the most recent instance data
        :param device_id: Device ID
        :param data_source_id: Data source ID
        :param instance_id: Instance ID
        :return: dict of {'timestamp': <int>, 'values': dict}, Empty dict if no data
        example
            {'timestamp': 1605720715000,
             'values': {'Estimated_OLT_Rx': -14.619,
                        'LastDownCause': 13.0,
                        'LastDownTime': 'No Data',
                        'LastUpTime': 'No Data',
                        'OLT_Rx': -23.77,
                        'OLT_Rx_Raw': 7623.0,
                        'ONT_Distance': 498.0,
                        'ONT_Optics_Current': 5.0,
                        'ONT_Optics_Temp': 30.0,
                        'ONT_Optics_Voltage': 33.6,
                        'ONT_Optics_Voltage_Raw': 3360.0,
                        'ONT_Rx': -20.91,
                        'ONT_Rx_Power_Raw': -2091.0,
                        'ONT_Tx': 2.23,
                        'ONT_Tx_Power_Raw': 223.0,
                        'Run_Status': 1.0}}
        :raise RequestFailedError - If request to logic monitor failed, i.e. HTTP status code is not ok
        """

        url = f'{self._devices_base_url}/{device_id}/devicedatasources/{data_source_id}/instances/{instance_id}/data'
        res = self.get(url)
        if res.ok:
            res_data = res.json()
            data_points: list = res_data['dataPoints']
            values: List[list] = res_data['values']
            timestamps: list = res_data['time']
            if timestamps and values:
                return {
                    'timestamp': timestamps[0],
                    'values': dict(zip_equal(data_points, values[0]))
                }
        raise RequestFailedError(
            response_content=res.content.decode(),
            response_status=res.status_code,
            msg=f'Failed to get instance data for instance id: {instance_id}, device_id: {device_id}'
        )

    def get_ont_data(self, site_short_name: str, ont_sn: str) -> dict:
        """
        Gets ONT optical and last downcause related data from logicmonitor
        :param site_short_name: Site short name. Used to find which OLT this ONT is connected to
        :param ont_sn: ONT Serial number
        :return: dict of {'timestamp': <int>, 'values': dict}, Empty dict if no data
        example
            {'timestamp': 1605720715000,
             'values': {'Estimated_OLT_Rx': -14.619,
                        'LastDownCause': 13.0,
                        'LastDownTime': 'No Data',
                        'LastUpTime': 'No Data',
                        'OLT_Rx': -23.77,
                        'OLT_Rx_Raw': 7623.0,
                        'ONT_Distance': 498.0,
                        'ONT_Optics_Current': 5.0,
                        'ONT_Optics_Temp': 30.0,
                        'ONT_Optics_Voltage': 33.6,
                        'ONT_Optics_Voltage_Raw': 3360.0,
                        'ONT_Rx': -20.91,
                        'ONT_Rx_Power_Raw': -2091.0,
                        'ONT_Tx': 2.23,
                        'ONT_Tx_Power_Raw': 223.0,
                        'Run_Status': 1.0}}
        :raise RequestFailedError - If request to logic monitor failed, i.e. HTTP status code is not ok
        :raise ItemNotFoundError - If the requested item is not available on logic monitor
        :raise InvalidNumOfItemsError - If the requested number of items returned from logic monitor is wrong
        """

        with self:
            device_id = self.get_device_id_by_display_name(f'acc.olt1.{site_short_name}')
            ds_id = self.get_device_gpon_optics_datasource_id(device_id)
            instance_id = self.get_device_ont_instance_id(f'{ont_sn}', device_id, ds_id)
            data = self.get_instance_most_recent_data(device_id, ds_id, instance_id)
            return data

