# -*- coding: utf-8 -*-

from sqlalchemy import ForeignKey, Column
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relation, backref
from sqlalchemy.types import String, Integer, DateTime, Interval
from sqlalchemy.schema import Index
from geoalchemy import WKTSpatialElement
from geoalchemy.geometry import GeometryColumn, LineString, GeometryDDL
from geoalchemy.postgis import PGComparator

from skylines.model.base import DeclarativeBase
from skylines.model.session import DBSession
from skylines.model.flight import Flight
from skylines.model.geo import Location


class Trace(DeclarativeBase):
    """
    This table saves the locations and visiting times of the turnpoints
    of an optimized Flight.
    """

    __tablename__ = 'traces'

    id = Column(Integer, autoincrement=True, primary_key=True)

    flight_id = Column(Integer, ForeignKey('flights.id', ondelete='CASCADE'),
                       nullable=False)
    flight = relation('Flight', primaryjoin=(flight_id == Flight.id),
                      backref=backref('traces', cascade="all"))

    contest_type = Column(String, nullable=False)
    trace_type = Column(String, nullable=False)

    distance = Column(Integer)
    duration = Column(Interval)

    times = Column(postgresql.ARRAY(DateTime), nullable=False)
    _locations = GeometryColumn('locations', LineString(2, wkt_internal=True),
                                nullable=False, comparator=PGComparator)

    @property
    def speed(self):
        if self.distance is None or self.duration is None:
            return None

        return float(self.distance) / self.duration.total_seconds()

    @property
    def locations(self):
        return [Location(longitude=location[0], latitude=location[1])
                for location in self._locations.coords(DBSession)]

    @locations.setter
    def locations(self, locations):
        points = ['{} {}'.format(location.longitude, location.latitude)
                  for location in locations]
        wkt = "LINESTRING({})".format(','.join(points))
        self._locations = WKTSpatialElement(wkt)

GeometryDDL(Trace.__table__)

Index('traces_contest_idx',
      Trace.flight_id, Trace.contest_type, Trace.trace_type,
      unique=True)
