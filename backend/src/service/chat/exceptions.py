class ThreadBaseException(Exception):
    """Base exception for thread base operations"""
    
class ThreadNotFound(ThreadBaseException):
    """Base exceptions when thread is not found"""
class ThreadCreateError(ThreadBaseException):
    """Exceptions when thread creation fails"""
class ThreadRetrievalError(ThreadBaseException):
    """Exception when failure to get thread"""
class ThreadUpdateError(ThreadBaseException):
    """Exception when failure to update thread"""