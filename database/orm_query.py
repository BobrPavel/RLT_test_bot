import os
import json

# from sqlalchemy import select, update, delete, func, case
from sqlalchemy.ext.asyncio import AsyncSession
# from sqlalchemy.orm import joinedload
from datetime import datetime
from uuid import UUID


from database.models import Videos, Video_snapshots


BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/
JSON_PATH = os.path.join(BASE_DIR, "..", "common", "videos.json")


async def orm_create_db(session: AsyncSession):
    with open(JSON_PATH, encoding="utf-8") as f:
        payload = json.load(f)

    for video_data in payload.get("videos", []):
        video = Videos(
            id=UUID(video_data["id"]),
            video_created_at=datetime.fromisoformat(video_data["video_created_at"]),
            views_count=video_data["views_count"],
            likes_count=video_data["likes_count"],
            reports_count=video_data["reports_count"],
            comments_count=video_data["comments_count"],
            creator_id=UUID(video_data["creator_id"]),
            created_at=datetime.fromisoformat(video_data["created_at"]),
            updated_at=datetime.fromisoformat(video_data["updated_at"]),
        )

        for snap in video_data.get("snapshots", []):
            snapshot = Video_snapshots(
                id=UUID(snap["id"]),
                views_count=snap["views_count"],
                likes_count=snap["likes_count"],
                reports_count=snap["reports_count"],
                comments_count=snap["comments_count"],
                delta_views_count=snap["delta_views_count"],
                delta_likes_count=snap["delta_likes_count"],
                delta_reports_count=snap["delta_reports_count"],
                delta_comments_count=snap["delta_comments_count"],
                created_at=datetime.fromisoformat(snap["created_at"]),
                updated_at=datetime.fromisoformat(snap["updated_at"]),
            )
            video.snapshots.append(snapshot)

        session.add(video)

    await session.commit()
