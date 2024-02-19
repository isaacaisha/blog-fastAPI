from fastapi import FastAPI, Body, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from sqlalchemy import func

from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/greetings")
async def get_home():
    return {"message": "Welcome to my api 🔥👌🏿😇💪🏿🔥 ¡!¡"}


@router.get("/all", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
              limit: int = 11, skip: int = 0, search: Optional[str] = ""):
              
    posts = db.query(models.Post) \
        .filter(models.Post.title.contains(search)) \
        .options(joinedload(models.Post.owner, innerjoin=True)) \
        .options(joinedload(models.Post.votes)) \
        .limit(limit) \
        .offset(skip) \
        .all()

    post_out_list = []
    for post in posts:
        # Count the votes for the current post
        votes_count = len(post.votes)

        # Create a UserOut object for the owner
        owner_out = schemas.UserOut(
            id=post.owner.id,
            email=post.owner.email,
            created_at=post.owner.created_at
        )

        # Create a PostOut instance for the current post
        post_out = schemas.PostOut(
                conversation_id=post.id,
                title=post.title,
                content=post.content,
                created_at=post.created_at,
                owner_id=post.owner.id,  # owner_id is a foreign key in Post model
                owner=owner_out,
            votes=votes_count
        )

        # Append the PostOut instance to the list
        post_out_list.append(post_out)

    return post_out_list


@router.get("/individual", response_model=List[schemas.PostResponse])
def get_individual_post(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
                          limit: int = 3, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()(db: Session = Depends(get_db)):
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).filter(models.Post.owner_id == current_user.id).all()
    print(f'current_user.id:\n{current_user.id} 👌🏿\n')
    print(f'posts:\n{posts} 👌🏿\n')
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)):
    #print(f'Title: {post.title}\nContent: {post.content}\n'
    #      f'Published: {post.published}\nRating: {post.rating}\n')
    #print(f'new_post.model_dump(): {post.model_dump()}\n')
#
    #post_dict = post.model_dump()
    #post_dict['id'] = randrange(0, 1000000)
    #print(f'post_dict["id"]: {post_dict["id"]}\n')
    #my_posts.append(post_dict)
    #return {"data": post_dict}

    #ursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, 
    #              (post.title, post.content, post.published))
    #ew_post = cursor.fetchone()
    #onn.commit()
    new_post = models.Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    print(f'current_user:{current_user.email}\n')

    return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # Fetch the post from the database
    post = db.query(models.Post).filter(models.Post.id == id).first()

    # Check if the post exists
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} not found")

    # Fetch the vote count for the post
    votes_count = db.query(func.count(models.Vote.post_id)).filter(models.Vote.post_id == post.id).scalar()

    # Create a UserOut object for the owner
    owner_out = schemas.UserOut(
        id=post.owner.id,
        email=post.owner.email,
        created_at=post.owner.created_at
    )

    # Create a PostOut instance for the current post
    post_out = schemas.PostOut(
        conversation_id=post.id,  # post.id is the conversation_id
        title=post.title,
        content=post.content,
        created_at=post.created_at,
        owner=owner_out,
        votes=votes_count
    )

    return post_out


@router.put("/{id}", response_model=schemas.PostOut)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'posts with id: {id} does no exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action 😝 ¡!¡')

    
    post_query.update(updated_post.model_dump(), synchronize_session=False)
    db.commit()

    # Use Pydantic's model.dict() to convert the SQLAlchemy model to a dictionary
    post_dict = schemas.PostCreate(**updated_post.__dict__).model_dump()
    print(f'\npost:\n{post_dict}\n')

    return post_query.first()


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_guery = db.query(models.Post).filter(models.Post.id == id)

    post = post_guery.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'posts with id: {id} does no exist')
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Not authorized to perform requested action 😝 ¡!¡')

    post.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
