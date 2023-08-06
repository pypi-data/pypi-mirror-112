from myst.endpoints.base import EndpointsBase
from myst.endpoints.time_series import TimeSeries
from myst.endpoints.users import Users


class Endpoints(EndpointsBase):
    """Entrypoint for our API endpoints.

    This class is hand-written but relies on the auto-generated `Endpoints`
    classes for each route prefix.
    """

    @property
    def users(self) -> Users:
        return Users(self.client)

    @property
    def time_series(self) -> TimeSeries:
        return TimeSeries(self.client)
