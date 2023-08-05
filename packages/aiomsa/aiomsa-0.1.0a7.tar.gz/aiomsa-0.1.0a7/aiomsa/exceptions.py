#!/usr/bin/env python3
# Copyright 2004-present Facebook. All Rights Reserved.

from typing import Optional


class AioMsaError(Exception):
    """Base class for all *aiomsa* errors."""

    pass


class DuplicateRouteError(AioMsaError):
    """Raised if more than one route has the same method and path."""

    pass


class ClientError(AioMsaError):
    """Base class for all client errors."""

    pass


class ClientStoppedError(ClientError):  # pragma: no cover
    """Raised if a client is used before it's started.

    Args:
        msg: The exception message.
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is None:
            msg = "The client cannot be used before it's started"
        super().__init__(msg)


class ClientRuntimeError(ClientError):  # pragma: no cover
    """Raised if a client operation fails.

    Args:
        msg: The exception message.
    """

    def __init__(self, msg: Optional[str] = None) -> None:
        if msg is None:
            msg = "An issue with the client occurred at runtime"
        super().__init__(msg)
