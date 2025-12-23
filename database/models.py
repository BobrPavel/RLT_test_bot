from datetime import datetime, timezone
from sqlalchemy import UUID, DateTime, ForeignKey, Numeric, String, Text, BigInteger, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Videos(Base):
    __tablename__ = 'videos'

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    video_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]
    creator_id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), nullable=False)
    
    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    
    


class Video_snapshots(Base):
    __tablename__ = 'video_snapshots'

    id: Mapped[UUID] = mapped_column(PG_UUID(as_uuid=True), primary_key=True)
    video_id: Mapped[UUID] = mapped_column(ForeignKey('videos.id', ondelete='CASCADE'), nullable=False)

    views_count: Mapped[int]
    likes_count: Mapped[int]
    reports_count: Mapped[int]
    comments_count: Mapped[int]

    delta_views_count: Mapped[int]
    delta_likes_count: Mapped[int]
    delta_reports_count: Mapped[int]
    delta_comments_count: Mapped[int]


    created_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))


    video: Mapped['Videos'] = relationship(backref='snapshots')






    


    