from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from database.base import Base


# =========================================================
# USER
# =========================================================

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    username = Column(
        String,
        nullable=False,
    )

    email = Column(
        String,
        unique=True,
        nullable=False,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    conversations = relationship(
        "Conversation",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    documents = relationship(
        "Document",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    preferences = relationship(
        "Preference",
        back_populates="user",
        cascade="all, delete-orphan",
    )

    # -----------------------------------------
    # Image Memory
    # -----------------------------------------

    image_memories = relationship(
        "ImageMemory",
        back_populates="user",
        cascade="all, delete-orphan",
    )


# =========================================================
# CONVERSATION
# =========================================================

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    title = Column(
        String,
        nullable=False,
    )

    # -------------------------
    # Conversation Summary
    # -------------------------

    summary = Column(
        Text,
        nullable=True,
    )

    summary_updated = Column(
        DateTime,
        nullable=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # -------- Adaptive Memory Metadata --------

    last_accessed = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    access_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    importance = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="conversations",
    )

    messages = relationship(
        "Message",
        back_populates="conversation",
        cascade="all, delete-orphan",
    )

    # -----------------------------------------
    # Image Memory
    # -----------------------------------------

    image_memories = relationship(
        "ImageMemory",
        back_populates="conversation",
    )


# =========================================================
# MESSAGE
# =========================================================

class Message(Base):
    __tablename__ = "messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
    )

    role = Column(
        String,
        nullable=False,
    )

    content = Column(
        Text,
        nullable=False,
    )

    timestamp = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # -------- Adaptive Memory Metadata --------

    last_accessed = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    access_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    importance = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    conversation = relationship(
        "Conversation",
        back_populates="messages",
    )


# =========================================================
# DOCUMENT
# =========================================================

class Document(Base):
    __tablename__ = "documents"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    filename = Column(
        String,
        nullable=False,
    )

    filepath = Column(
        String,
        nullable=False,
    )

    uploaded_at = Column(
        DateTime,
        default=datetime.utcnow,
    )

    # -------- Adaptive Memory Metadata --------

    last_accessed = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    access_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    importance = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="documents",
    )


# =========================================================
# PREFERENCE
# =========================================================

class Preference(Base):
    __tablename__ = "preferences"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    key = Column(
        String,
        nullable=False,
    )

    value = Column(
        String,
        nullable=False,
    )

    # -------- Adaptive Memory Metadata --------

    last_accessed = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    access_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    importance = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    user = relationship(
        "User",
        back_populates="preferences",
    )


# =========================================================
# IMAGE MEMORY
# =========================================================

class ImageMemory(Base):
    """
    Stores persistent memory about uploaded and edited images.

    Each edited version is stored as a separate ImageMemory
    record so the original image and complete edit history
    remain available.
    """

    __tablename__ = "image_memories"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    conversation_id = Column(
        Integer,
        ForeignKey("conversations.id"),
        nullable=True,
    )

    # -----------------------------------------
    # Image Information
    # -----------------------------------------

    filename = Column(
        String,
        nullable=False,
    )

    filepath = Column(
        String,
        nullable=False,
    )

    description = Column(
        Text,
        nullable=True,
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    # -----------------------------------------
    # Image Edit History
    # -----------------------------------------

    parent_image_id = Column(
        Integer,
        ForeignKey("image_memories.id"),
        nullable=True,
    )

    edit_instruction = Column(
        Text,
        nullable=True,
    )

    edit_version = Column(
        Integer,
        default=1,
        nullable=False,
    )

    # -----------------------------------------
    # Adaptive Memory Metadata
    # -----------------------------------------

    last_accessed = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False,
    )

    access_count = Column(
        Integer,
        default=0,
        nullable=False,
    )

    importance = Column(
        Float,
        default=1.0,
        nullable=False,
    )

    # -----------------------------------------
    # Relationships
    # -----------------------------------------

    user = relationship(
        "User",
        back_populates="image_memories",
    )

    conversation = relationship(
        "Conversation",
        back_populates="image_memories",
    )

    parent_image = relationship(
        "ImageMemory",
        remote_side="ImageMemory.id",
        back_populates="edited_versions",
    )

    edited_versions = relationship(
        "ImageMemory",
        back_populates="parent_image",
    )