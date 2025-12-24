# --------------------------------------------------------------------------------
# Все ORM запросы проекта
# --------------------------------------------------------------------------------
# Импорты
# --------------------------------------------------------------------------------

import os
import json

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from uuid import UUID

from database.models import Videos, Video_snapshots

# --------------------------------------------------------------------------------
# Настройки и константы
# --------------------------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # app/
JSON_PATH = os.path.join(BASE_DIR, "..", "common", "videos.json")

# --------------------------------------------------------------------------------
# ORM запросы
# --------------------------------------------------------------------------------


async def orm_create_db(session: AsyncSession): # ORM запрос на создание базы данных

    for model in (Videos, Video_snapshots):
        query = select(model).limit(1)  # проверка есть ли уже записи
        result = await session.execute(query)
        if result.first():  # если хотя бы одна запись есть, то прекращаем выполнение
            return


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



async def execute_query(plan: dict, session: AsyncSession): # Получапет QueryPlan, преобразует его в ORM запрос и исполняет

    # Метрики. По ним преобразуется QueryPlan в запрос
    MODEL_MAP = {
        "videos": Videos,
        "video_snapshots": Video_snapshots,
    }

    METRIC_MAP = {
        "videos": {
            "videos": "id",
            "video_snapshots": "video_id",
            "delta": "video_id",
        },
        "views": {
            "videos": "views_count",
            "video_snapshots": "views_count",
            "delta": "delta_views_count",
        },
        "likes": {
            "videos": "likes_count",
            "video_snapshots": "likes_count",
            "delta": "delta_likes_count",
        },
    }

    OPERATION_MAP = {
        "count": func.count,
        "sum": func.sum,
        "delta": func.sum,
    }

    model = MODEL_MAP[plan["source"]]
    metric_type = "delta" if plan["operation"] == "delta" else plan["source"]

    column_name = METRIC_MAP[plan["metric"]][metric_type]
    column = getattr(model, column_name)
    agg_column = OPERATION_MAP[plan["operation"]](column)

    # ❗ ВАЖНО: select, а не session.query
    stmt = select(agg_column)

    # Filters (=)
    for field, value in plan.get("filters", {}).items():
        if value is not None:
            stmt = stmt.where(getattr(model, field) == value)

    # Conditions
    for cond in plan.get("conditions", []):
        col = getattr(model, cond["field"])
        op = cond["operator"]
        val = cond["value"]

        if op == ">":
            stmt = stmt.where(col > val)
        elif op == ">=":
            stmt = stmt.where(col >= val)
        elif op == "<":
            stmt = stmt.where(col < val)
        elif op == "<=":
            stmt = stmt.where(col <= val)
        elif op == "=":
            stmt = stmt.where(col == val)

    # Time range

    time_range = plan.get("time_range")

    if time_range:
        if time_range["type"] == "last_n_days":
            stmt = stmt.where(
                model.created_at >= datetime.now(tz=timezone.utc)
                - timedelta(days=time_range["value"])
            )

        elif time_range["type"] == "between":
            date_column = (
                model.video_created_at
                if plan["source"] == "videos"
                else model.created_at
            )

            start_date = datetime.fromisoformat(time_range["from"]).replace(
                tzinfo=timezone.utc
            )
            end_date = (
                datetime.fromisoformat(time_range["to"])
                .replace(tzinfo=timezone.utc)
                + timedelta(days=1)
            )

            stmt = stmt.where(
                date_column >= start_date,
                date_column < end_date,
            )


    # Execute
    result = await session.execute(stmt)
    value = result.scalar()

    return int(value or 0)
