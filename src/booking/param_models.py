from pydantic import Field

from basis.param_models import BasisModel

from .constants.bookings import Station


class BookingRequestParam(BasisModel):
    depart_station: int = Field(ge=Station.Nangang, le=Station.Zuouing)
    dest_station: int = Field(ge=Station.Nangang, le=Station.Zuouing)
    # type_of_trip: int
    # booking_method: int
    # seat_prefer: int
    adult_num: int
    child_num: int
    disabled_num: int
    elder_num: int
    college_num: int
    depart_date: str = Field(pattern=r'^((19|20)?[0-9]{2}[- /.](0?[1-9]|1[012])[- /.](0?[1-9]|[12][0-9]|3[01]))$')
    earliest_depart_time: str = Field(pattern=r'^\d{3,4}[AP]$')
    latest_arrival_time: str = Field(pattern=r'^\d{3,4}[AP]$')

    @property
    def total_num(self):
        return self.adult_num + self.child_num + self.disabled_num + self.elder_num + self.college_num
