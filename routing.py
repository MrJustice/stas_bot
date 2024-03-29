import dataclasses

from fastapi import APIRouter

from tg.tg_api.routers import tg_api_router


@dataclasses.dataclass
class AppRouter:
    """The main router of the project, which adds a prefix with the version for all defined routers"""

    v1: tuple[APIRouter, ...] = (tg_api_router,)

    @classmethod
    @property
    def routers(cls) -> tuple[tuple[str, tuple[APIRouter, ...]], ...]:
        """Property that returns a tuple with pairs of api prefix and router for that"""
        return tuple(
            [
                (f"/api/{f_name}", f_obj.default)
                for f_name, f_obj in cls.__dataclass_fields__.items()
                if not f_name.startswith("_")
            ]
        )
