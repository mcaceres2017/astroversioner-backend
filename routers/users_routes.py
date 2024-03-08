from typing import List
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from schemas.user.confirm import Confirm
from schemas.user.user import User
from models.user import UserModel
from database.db_connector import get_db

# Create an APIRouter instance
users_router = APIRouter()


@users_router.get("/debug/", response_model=List[User])
async def get_users_debug(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of User objects.
    """

    users = db.query(UserModel).all()
    print(users)
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return users


@users_router.get("/", response_model=List[User])
async def get_users(db: Session = Depends(get_db)):
    """
    Get a list of all users.

    Args:
        db (Session): The database session.

    Returns:
        List[User]: A list of User objects.
    """

    users = db.query(UserModel).all()
    for user in users:
        user.password = "--"
    print(users)
    if not users:
        raise HTTPException(status_code=404, detail="No users found.")
    return users


@users_router.get("/{username}", response_model=User)
async def get_user(username: str, db: Session = Depends(get_db)):
    """
    Get a user.

    Args:
        username: username of user-
        db (Session): The database session.

    Returns:
        User: A User object.
    """

    user = db.query(UserModel).filter(UserModel.username == username).first()
    print(user)
    if not user:
        raise HTTPException(status_code=404, detail="No user found.")
    return user


@users_router.post("/", response_model=Confirm)
async def post_user(user: User, db: Session = Depends(get_db)):
    """
    Authenticate a user based on email and password.

    Args:
        user (User): The User object containing email and password.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed login.
    """
    try:
        users = db.query(UserModel).all()

        for u in users:
            if u.mail == user.mail:
                if u.password == user.password:
                    return Confirm(
                        response=True,
                        detail=u.username,
                        user=User(
                            mail=u.mail, username=u.username, password=u.password
                        ),
                    )
                else:
                    return Confirm(
                        response=False,
                        detail="Incorrect password",
                        user=User(mail="", username="", password=""),
                    )

        return Confirm(
            response=False,
            detail="Incorrect credentials",
            user=User(mail="", username="", password=""),
        )

    except Exception as e:
        return Confirm(
            response=False,
            detail=f"Internal server error {e}",
            user=User(mail="", username="", password=""),
        )


@users_router.post("/add/", response_model=Confirm)
async def post_user_add(user: User, db: Session = Depends(get_db)):
    """
    Register a new user.

    Args:
        user (User): The User object to be registered.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating successful or failed registration.
    """

    try:
        db_user = db.query(UserModel).filter(UserModel.mail == user.mail).first()
        if db_user:
            return Confirm(
                response=False,
                detail="The registered mail has another account associated",
                user=User(mail="", username="", password=""),
            )

        db_user = (
            db.query(UserModel).filter(UserModel.username == user.username).first()
        )
        if db_user:
            return Confirm(
                response=False,
                detail="The username is not available",
                user=User(mail="", username="", password=""),
            )

        new_user = UserModel(
            mail=user.mail, username=user.username, password=user.password
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

        return Confirm(
            response=True,
            detail="",
            user=User(mail=user.mail, username=user.username, password=user.password),
        )
    except Exception as e:
        return Confirm(
            response=False,
            detail=f"Internal server error {e}",
            user=User(privilege=False, mail="", username="", password=""),
        )


@users_router.put("/", response_model=Confirm)
async def update_user(user: User, db: Session = Depends(get_db)):
    """
    Update user data by username.

    Args:
        username (str): The username of the user to be updated.
        user (User): The User object with updated data.
        db (Session): The database session.

    Returns:
        Confirm: A Confirm object indicating success or failure of the update.
    """
    try:
        db_user = (
            db.query(UserModel).filter(UserModel.username == user.username).first()
        )
        if not db_user:
            return Confirm(
                response=False,
                detail="The user does not exist",
                user=User(mail="", username="", password=""),
            )

        if user.password != "":
            db_user.password = user.password

        db.commit()
        db.refresh(db_user)

        return Confirm(
            response=True,
            detail="User data updated successfully",
            user=User(mail=user.mail, username=user.username, password=user.password),
        )
    except Exception as e:
        return Confirm(
            response=False,
            detail=f"Internal server error {e}",
            user=User(mail="", username="", password=""),
        )
