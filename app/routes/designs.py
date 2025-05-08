from bson import ObjectId
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.models.user import User
from app.models.design import Design, DesignCreate, DesignUpdate
from app.utils.auth import get_current_user_from_cookie
from app.database.connection import designs_collection

router = APIRouter(tags=["Designs"])


@router.get("/getAllDesigns", response_model=List[Design])
async def get_all_designs(current_user: User = Depends(get_current_user_from_cookie)):
    """
    Get all designs. Available to all authenticated users.
    """
    designs = list(designs_collection.find())
    return [Design(id=str(design["_id"]), ownerId=design["ownerId"], name=design["name"], data=design["data"])
            for design in designs]


@router.get(
    "/getUserDesigns",
    response_model=List[Design],
    responses={403: {"description": "Only designers can access their designs", "model": str}},
)
async def get_user_designs(current_user: User = Depends(get_current_user_from_cookie)):
    """
    Get designs owned by the current user. Available to designers only.
    """
    if current_user.role != "designer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only designers can access their designs"
        )

    designs = list(designs_collection.find({"ownerId": current_user.id}))
    return [Design(id=str(design["_id"]), ownerId=design["ownerId"], name=design["name"], data=design["data"])
            for design in designs]


@router.post("/createDesign", response_model=Design)
async def create_design(design: DesignCreate, current_user: User = Depends(get_current_user_from_cookie)):
    """
    Create a new design. Available to designers only.
    """
    if current_user.role != "designer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only designers can create designs"
        )

    design_id = ObjectId()
    new_design = {
        "_id": design_id,
        "id": str(design_id),
        "ownerId": current_user.id,
        "name": design.name,
        "data": design.data
    }

    designs_collection.insert_one(new_design)

    return Design(
        id=str(design_id),
        ownerId=current_user.id,
        name=design.name,
        data=design.data
    )


@router.put("/updateDesign/{design_id}", response_model=Design)
async def update_design(
    design_id: str,
    design_update: DesignUpdate,
    current_user: User = Depends(get_current_user_from_cookie)
):
    """
    Update a design. Available to designers who own the design.
    """
    if current_user.role != "designer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only designers can update designs"
        )

    # Check if design exists and belongs to the current user
    existing_design = designs_collection.find_one({"_id": ObjectId(design_id)})
    if not existing_design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )

    if existing_design["ownerId"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only update your own designs"
        )

    # Update design
    update_data = {k: v for k, v in design_update.model_dump(mode="json").items() if v is not None}
    if update_data:
        designs_collection.update_one(
            {"_id": ObjectId(design_id)},
            {"$set": update_data}
        )

    # Get updated design
    updated_design = designs_collection.find_one({"_id": ObjectId(design_id)})

    return Design(
        id=str(updated_design["_id"]),
        ownerId=updated_design["ownerId"],
        name=updated_design["name"],
        data=updated_design["data"]
    )


@router.delete("/deleteDesign/{design_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_design(
    design_id: str,
    current_user: User = Depends(get_current_user_from_cookie)
):
    """
    Delete a design. Available to designers who own the design.
    """
    if current_user.role != "designer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only designers can delete designs"
        )

    # Check if design exists and belongs to the current user
    existing_design = designs_collection.find_one({"_id": ObjectId(design_id)})
    if not existing_design:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Design not found"
        )

    if existing_design["ownerId"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own designs"
        )

    # Delete design
    designs_collection.delete_one({"_id": ObjectId(design_id)})
