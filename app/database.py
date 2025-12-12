from motor.motor_asyncio import AsyncIOMotorClient
from .config import settings

client = AsyncIOMotorClient(settings.MONGO_URI)
master_db = client[settings.MASTER_DB_NAME]

# Master collections
orgs_collection = master_db["organizations"]
admins_collection = master_db["admins"]

def safe_slug(s: str) -> str:
    s = s.strip().lower()
    s = s.replace(" ", "_")
    s = "".join(ch for ch in s if ch.isalnum() or ch == "_")
    return s or "org"

def org_collection_name(org_name: str) -> str:
    slug = safe_slug(org_name)
    return f"org_{slug}"
