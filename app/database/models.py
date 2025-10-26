from database import Base, DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List

class Organization(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'))

    phones: Mapped[List['Phone']] = relationship('Phone',back_populates='organization')
    building: Mapped['Building'] = relationship('Building',back_populates='organizations')
    activities: Mapped[List['Activity']] = relationship('Activity',secondary='organization_activity_rels',back_populates='organizations')

class Phone(Base):
    number: Mapped[str] = mapped_column(nullable=False, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    
    organization: Mapped[Organization] = relationship('organization', back_populates='phones')

class Building(Base):
    address: Mapped[str] = mapped_column(nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations: Mapped[List[Organization]] = relationship('organization',back_populates='building')

class Activity(Base):
    name: Mapped[str] = mapped_column(nullable=False,index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('activitys.id'))

    parent: Mapped['Activity'] = relationship('Activity',remote_side=['id'],back_populates='childrens')
    childrens: Mapped[List['Activity']] = relationship('Activity',back_populates='parent')
    organizations: Mapped[List[Organization]] = relationship('Organization',secondary='organization_activity_rels',back_populates='activities')

class Organization_Activity_Rel(DeclarativeBase):
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'),primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activity.id'),primary_key=True)