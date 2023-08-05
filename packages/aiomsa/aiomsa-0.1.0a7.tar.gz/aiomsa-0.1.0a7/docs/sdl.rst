.. _aiomsa-sdl:

===
SDL
===

.. currentmodule:: aiomsa.abc

The *Shared Data Layer* is for storing information about the topology of the network.
RIC platform developers are expected to implement the asynchronous, abstract methods
defined in the :class:`~.SDLClient`.

.. autoclass:: SDLClient
   :members:
   :special-members: __aenter__, __aexit__
