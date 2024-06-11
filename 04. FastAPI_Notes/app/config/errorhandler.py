import aioredis
from celery.exceptions import NotRegistered, TimeoutError
from fastapi import HTTPException
from sqlalchemy.exc import DBAPIError, SQLAlchemyError, StatementError


def handle_exception(error: Exception, logger):
    if isinstance(error, SQLAlchemyError):
        logger.error(f"Database error: {error}")
        raise HTTPException(
            status_code=500, detail="Database error. Please try again later."
        )
    elif isinstance(error, FileNotFoundError):
        logger.error(f"File not found: {error}")
        raise HTTPException(
            status_code=404,
            detail="File not found. Please upload the file and try again.",
        )
    elif isinstance(error, NotRegistered):
        logger.error(f"Task not registered: {error}")
        raise HTTPException(
            status_code=404,
            detail="Task not registered. Please check the unique_id and try again.",
        )
    elif isinstance(error, TimeoutError):
        logger.error(f"Operation timed out: {error}")
        raise HTTPException(
            status_code=408, detail="Operation timed out. Please try again later."
        )
    elif isinstance(error, HTTPException):
        logger.error(f"Authentication failed: {error}")
        raise HTTPException(
            status_code=401,
            detail="Authentication failed. Please check your secret key and try again.",
        )
    elif isinstance(error, StatementError):
        logger.error(f"Statement error: {error}")
        raise HTTPException(
            status_code=400,
            detail="Statement error. Please check your SQL statement and try again.",
        )
    elif isinstance(error, DBAPIError):
        logger.error(f"Database connection error: {error}")
        raise HTTPException(
            status_code=500, detail="Database connection error. Please try again later."
        )
    elif isinstance(error, aioredis.RedisError):
        logger.error(f"Redis error: {error}")
        raise HTTPException(
            status_code=500, detail="Redis error. Please try again later."
        )
    else:
        logger.error(f"Unexpected error: {error}")
        raise HTTPException(
            status_code=500, detail="Unexpected error. Please try again later."
        )
