from sqlalchemy.orm import Session
from app.database import Base, engine, SessionLocal
from datetime import datetime
from models.user_roles_model import User_Role
from models.categories_model import Category
from models.tags_model import Tag
from models.users_model import User
from models.posts_model import Post
from models.comments_model import Comment
from models.post_categories_model import Post_Category
from models.post_tags_model import Post_Tag



def seed_data():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed User Roles
        if db.query(User_Role).count() == 0:
            user_roles = [
                User_Role(
                    name="Admin",
                    description="Full access to all features",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                User_Role(
                    name="User",
                    description="Can edit and publish, create content",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
            ]
            db.add_all(user_roles)
            db.commit()
            print("User roles seeded successfully")

            # Seed Categories
        if db.query(Category).count() == 0:
            categories = [
                Category(
                    name="Technology",
                    description="Articles about latest tech trends",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Category(
                    name="Science",
                    description="Scientific discoveries and research",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Category(
                    name="Health",
                    description="Health and wellness topics",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Category(
                    name="Travel",
                    description="Travel guides and experiences",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Category(
                    name="Food",
                    description="Recipes and culinary adventures",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
            ]
            db.add_all(categories)
            db.commit()
            print("Categories seeded successfully")

        # Seed Tags
        if db.query(Tag).count() == 0:
            tags = [
                Tag(
                    name="AI",
                    description="Artificial Intelligence related",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Tag(
                    name="Machine Learning",
                    description="ML algorithms and applications",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Tag(
                    name="Web Development",
                    description="Web technologies and frameworks",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Tag(
                    name="Data Science",
                    description="Data analysis and visualization",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
                Tag(
                    name="Cybersecurity",
                    description="Information security topics",
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow(),
                ),
            ]
            db.add_all(tags)
            db.commit()
            print("Tags seeded successfully")

        print("Seed data added successfully")
    except Exception as e:
        print(f"An error occurred while seeding data: {e}")
    finally:
        db.close()
