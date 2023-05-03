import logging
from sqlalchemy import (
    Table, Column, Integer, String, Text, Date,
    ForeignKey
)
from sqlalchemy.orm import registry, relationship
from Domain.model import Bookmark, Tag

logger = logging.getLogger(__name__)

mapper_registry = registry()
Base = mapper_registry.generate_base()
metadata = mapper_registry.metadata

# Define the bookmarks table
bookmarks = Table(
    "bookmarks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("title", String(255), nullable=False),
    Column("url", String(255), nullable=False),
    Column("notes", Text),
    Column("date_added", Date, nullable=False),
    Column("date_edited", Date, nullable=False),
)

# Define the tags table
tags = Table(
    "tags",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(50), nullable=False),
    Column("bookmark_id", Integer, ForeignKey("bookmarks.id")),
)

# Define the many-to-many relationship between bookmarks and tags
bookmark_tags = Table(
    "bookmark_tags",
    metadata,
    Column("bookmark_id", Integer, ForeignKey("bookmarks.id")),
    Column("tag_id", Integer, ForeignKey("tags.id")),
)

def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(Bookmark, bookmarks)
    mapper_registry.map_imperatively(Tag, tags)

    # Define the many-to-many relationship between bookmarks and tags
    mapper_registry.map_imperatively(
        Bookmark,
        relationship(
            Tag,
            secondary=bookmark_tags,
            backref="bookmarks",
        ),
    )
