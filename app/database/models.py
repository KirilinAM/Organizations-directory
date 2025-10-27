from app.database.database import Base, BaseWithId
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from typing import List, Optional

class Organization(BaseWithId):
    name: Mapped[str] = mapped_column(nullable=False)
    building_id: Mapped[int] = mapped_column(ForeignKey('buildings.id'))

    phones: Mapped[List['Phone']] = relationship('Phone',back_populates='organization')
    building: Mapped['Building'] = relationship('Building',back_populates='organizations')
    activities: Mapped[List['Activity']] = relationship('Activity',secondary='organization_activity_rels',back_populates='organizations')

class Phone(BaseWithId):
    number: Mapped[str] = mapped_column(nullable=False, index=True)
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id'))
    
    organization: Mapped['Organization'] = relationship('Organization', back_populates='phones')

class Building(BaseWithId):
    address: Mapped[str] = mapped_column(nullable=False, index=True)
    latitude: Mapped[float] = mapped_column(nullable=False)
    longitude: Mapped[float] = mapped_column(nullable=False)

    organizations: Mapped[List[Organization]] = relationship('Organization',back_populates='building')

class Activity(BaseWithId):
    name: Mapped[str] = mapped_column(nullable=False,index=True)
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey('activitys.id'),nullable=True)

    parent: Mapped['Activity'] = relationship('Activity',remote_side='Activity.id',back_populates='childrens')
    childrens: Mapped[List['Activity']] = relationship('Activity',back_populates='parent')
    organizations: Mapped[List[Organization]] = relationship('Organization',secondary='organization_activity_rels',back_populates='activities')

class Organization_Activity_Rel(Base):
    organization_id: Mapped[int] = mapped_column(ForeignKey('organizations.id',ondelete='CASCADE'),primary_key=True)
    activity_id: Mapped[int] = mapped_column(ForeignKey('activitys.id',ondelete='CASCADE'),primary_key=True)