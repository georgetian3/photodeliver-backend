from uuid import UUID

from fastapi import APIRouter

section_router = APIRouter()


@section_router.get("/sections")
async def get_sections(album_id: UUID): ...


@section_router.put("/sections")
async def create_section(album_id: UUID) -> None: ...


@section_router.post("/sections/{section_id}")
async def update_section(section_id: UUID): ...


@section_router.delete("/sections/{section_id}")
async def delete_section(): ...
