from sqlalchemy import Column, Table
from sqlalchemy.types import Text, DateTime, Float, Boolean, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from .database import Base


game_categories = Table(
    "game_categories",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)

game_tags = Table(
    "game_tags",
    Base.metadata,
    Column("game_id", ForeignKey("games.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True),
) 

class Tag(Base):  # Keywords

    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    keyword = Column(String, index=True)
    games = relationship("Game", secondary=game_tags, back_populates="tags")


class Category(Base):

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    type = Column(String, nullable=True, index=True) # main or other
    games = relationship("Game", secondary=game_categories, back_populates="categories")
    main_category_games = relationship("Game", back_populates="categories")



class Game(Base):

    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True)
    description = Column(Text, index=True)
    # desc = Column(Text, nullable=True)  # it/fr/en/de/es
    
    category_id = Column(Integer, ForeignKey("categories.id"))  # Main Category
    category = relationship("Category", back_populates="main_category_games")
    
    author = Column(String, nullable=True)
    thumbnailUrl = Column(String, nullable=True)  # image url
    thumbnailUrl100 = Column(String, nullable=True)
    url = Column(String, nullable=True)  # game url
    rkScore = Column(Float, nullable=True)
    height = Column(Integer, nullable=True)  
    width = Column(Integer, nullable=True)
    orientation = Column(String, nullable=True)
    responsive = Column(Boolean, nullable=True)
    touch = Column(Boolean, nullable=True)
    hwcontrols = Column(Boolean, nullable=True)
    featured = Column(Boolean, nullable=True)
    creation = Column(DateTime, nullable=True)
    lastUpdate = Column(DateTime, nullable=True)
    size = Column(Float, nullable=True)  # game size
    min_android_version = Column(String, nullable=True)
    min_ios_version = Column(String, nullable=True)
    min_wp_version = Column(String, nullable=True)

    categories = relationship("Category", secondary=game_categories, back_populates="games")
    tags = relationship("Tag", secondary=game_tags, back_populates="games")
