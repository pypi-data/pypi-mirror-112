import aurorax
import datetime
from typing import Dict, List
import pprint
from pydantic import BaseModel


class AvailabilityResult(BaseModel):
    """
    Availability result data type

    :param data_source: data source that the ephemeris record is associated with
    :type data_source: aurorax.sources.DataSource
    :param available_data_products: data product availability dictionary of date keys "YYYY-MM-DD"
    :param available_data_products: Dict
    :type available_ephemeris: ephemeris availability dictionary of date keys "YYYY-MM-DD"
    :param available_ephemeris: Dict
    """
    data_source: aurorax.sources.DataSource
    available_data_products: Dict = None
    available_ephemeris: Dict = None

    def __str__(self) -> str:
        """
        String method

        :return: string format
        :rtype: str
        """
        return self.__repr__()

    def __repr__(self) -> str:
        """
        Object representation

        :return: object representation
        :rtype: str
        """
        return pprint.pformat(self.__dict__)

def ephemeris(start: datetime.date,
              end: datetime.date,
              program: str = None,
              platform: str = None,
              instrument_type: str = None,
              source_type: str = None,
              owner: str = None,
              format: str = "basic_info") -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing ephemeris records

    :param start: start date
    :type start: datetime
    :param end: end date
    :type end: datetime
    :param program: program name to filter sources by, defaults to None
    :type program: str, optional
    :param platform: platform name to filter sources by, defaults to None
    :type platform: str, optional
    :param instrument_type: instrument type to filter sources by, defaults to None
    :type instrument_type: str, optional
    :param source_type: source type to filter sources by (heo, leo, lunar, or ground), defaults to None
    :type source_type: str, optional
    :param owner: owner ID to filter sources by, defaults to None
    :type owner: str, optional
    :param format: the format of the ephemeris source returned (identifier_only, basic_info,
                   full_record), defaults to "basic_info"
    :type format: str, optional

    :return: list of ephemeris availability results
    :rtype: List[aurorax.availability.AvailabilityResult]
    """
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }

    # do request
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.ephemeris_availability_url, params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]

def data_products(start: datetime,
                  end: datetime,
                  program: str = None,
                  platform: str = None,
                  instrument_type: str = None,
                  source_type: str = None,
                  owner: str = None,
                  format: str = "basic_info") -> List[AvailabilityResult]:
    """
    Retrieve information about the number of existing data product records

    :param start: start date
    :type start: datetime
    :param end: end date
    :type end: datetime
    :param program: program name to filter sources by, defaults to None
    :type program: str, optional
    :param platform: platform name to filter sources by, defaults to None
    :type platform: str, optional
    :param instrument_type: instrument type to filter sources by, defaults to None
    :type instrument_type: str, optional
    :param source_type: source type to filter sources by (heo, leo, lunar, or ground), defaults to None
    :type source_type: str, optional
    :param owner: owner ID to filter sources by, defaults to None
    :type owner: str, optional
    :param format: the format of the ephemeris source returned (identifier_only, basic_info,
                   full_record), defaults to "basic_info"
    :type format: str, optional

    :return: list of data product availability results
    :rtype: List[aurorax.availability.AvailabilityResult]
    """
    # set parameters
    params = {
        "start": start.strftime("%Y-%m-%d"),
        "end": end.strftime("%Y-%m-%d"),
        "program": program,
        "platform": platform,
        "instrument_type": instrument_type,
        "source_type": source_type,
        "owner": owner,
        "format": format,
    }

    # do request
    req = aurorax.AuroraXRequest(method="get", url=aurorax.api.urls.data_products_availability_url, params=params)
    res = req.execute()

    # return
    return [AvailabilityResult(**av) for av in res.data]
