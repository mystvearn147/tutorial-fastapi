from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.oauth2 import get_current_user

router = APIRouter(prefix='/vote', tags=['Vote'])


@router.post('/', status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f'Post {vote.post_id} does not exist')

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == post.id and models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote is not None:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail=f'user {current_user.id} has already voted on post {post.id}')

        new_vote = models.Vote(post_id=post.id, user_id=current_user.id)
        db.add(new_vote)
        db.commit()

        return {'message': 'successfully added vote'}

    else:
        if found_vote is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Vote does not exist')

        vote_query.delete(synchronize_session=False)
        db.commit()

        return {'message': 'successfully deleted vote'}
