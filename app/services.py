from typing import Optional, Tuple
from bson import ObjectId
from fastapi import HTTPException, status

from .database import orgs_collection, admins_collection, master_db, org_collection_name
from .auth import hash_password, verify_password

class OrgService:
    @staticmethod
    async def create_org(organization_name: str, email: str, password: str) -> dict:
        existing = await orgs_collection.find_one({"organization_name": organization_name})
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Organization already exists")

        coll_name = org_collection_name(organization_name)
        org_coll = master_db[coll_name]

        # ensure collection exists by inserting and removing a seed doc
        await org_coll.insert_one({"_seed": True})
        await org_coll.delete_one({"_seed": True})

        hashed_pw = hash_password(password)
        admin_doc = {"email": email, "password": hashed_pw, "role": "admin"}
        admin_res = await admins_collection.insert_one(admin_doc)

        org_doc = {
            "organization_name": organization_name,
            "collection_name": coll_name,
            "admin_id": admin_res.inserted_id
        }
        org_res = await orgs_collection.insert_one(org_doc)

        return {
            "id": str(org_res.inserted_id),
            "organization_name": organization_name,
            "collection_name": coll_name,
            "admin_email": email
        }

    @staticmethod
    async def get_org_by_name(organization_name: str) -> dict:
        org = await orgs_collection.find_one({"organization_name": organization_name})
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")
        admin = await admins_collection.find_one({"_id": org["admin_id"]})
        return {
            "id": str(org["_id"]),
            "organization_name": org["organization_name"],
            "collection_name": org["collection_name"],
            "admin_email": admin["email"] if admin else None
        }

    @staticmethod
    async def update_org(current_name: str,
                         new_name: Optional[str],
                         email: Optional[str],
                         password: Optional[str],
                         requesting_org_id: str) -> dict:
        org = await orgs_collection.find_one({"organization_name": current_name})
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        if str(org["_id"]) != requesting_org_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this org")

        update_fields = {}

        # rename org => migrate collection
        if new_name and new_name != current_name:
            if await orgs_collection.find_one({"organization_name": new_name}):
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="New organization name already exists")

            old_coll = master_db[org["collection_name"]]
            new_coll_name = org_collection_name(new_name)
            new_coll = master_db[new_coll_name]

            cursor = old_coll.find({})
            async for doc in cursor:
                doc.pop("_id", None)
                if doc.get("_seed"):
                    continue
                await new_coll.insert_one(doc)

            await old_coll.drop()

            update_fields["organization_name"] = new_name
            update_fields["collection_name"] = new_coll_name

        # update admin creds
        admin = await admins_collection.find_one({"_id": org["admin_id"]})
        if not admin:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Admin record missing")

        admin_update = {}
        if email:
            admin_update["email"] = email
        if password:
            admin_update["password"] = hash_password(password)
        if admin_update:
            await admins_collection.update_one({"_id": admin["_id"]}, {"$set": admin_update})

        if update_fields:
            await orgs_collection.update_one({"_id": org["_id"]}, {"$set": update_fields})

        return {"message": "Organization updated successfully"}

    @staticmethod
    async def delete_org(organization_name: str, requesting_org_id: str) -> dict:
        org = await orgs_collection.find_one({"organization_name": organization_name})
        if not org:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

        if str(org["_id"]) != requesting_org_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this org")

        coll = master_db[org["collection_name"]]
        await coll.drop()

        await admins_collection.delete_one({"_id": org["admin_id"]})
        await orgs_collection.delete_one({"_id": org["_id"]})

        return {"message": "Organization deleted successfully"}


class AdminService:
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[Tuple[dict, dict]]:
        admin = await admins_collection.find_one({"email": email})
        if not admin:
            return None
        if not verify_password(password, admin["password"]):
            return None
        org = await orgs_collection.find_one({"admin_id": admin["_id"]})
        return admin, org
