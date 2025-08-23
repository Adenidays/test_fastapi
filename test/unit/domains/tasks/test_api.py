import pytest
from uuid import uuid4
from httpx import AsyncClient
from fastapi import status
from fastapi import status as http_status

pytestmark = pytest.mark.asyncio


async def _api_create_task(
    client, title="Title", description="Desc", status_val="created"
):
    payload = {"title": title, "description": description, "status": status_val}
    resp = await client.post("/task/", json=payload)
    if resp.status_code != http_status.HTTP_201_CREATED:
        print("REQUEST PAYLOAD:", payload)
        print("RESPONSE BODY:", await resp.aread())
    assert resp.status_code == http_status.HTTP_201_CREATED
    return resp.json()


async def test_create_task_201(client: AsyncClient):
    data = await _api_create_task(client, "My", "Do", "created")
    assert "id" in data and "created_at" in data
    assert data["title"] == "My"
    assert data["description"] == "Do"
    assert data["status"] == "created"


async def test_list_tasks(client: AsyncClient):
    await _api_create_task(client, "A", "a", "created")
    await _api_create_task(client, "B", "b", "in_progress")
    resp = await client.get("/task/")
    assert resp.status_code == status.HTTP_200_OK
    items = resp.json()
    titles = {i["title"] for i in items}
    assert {"A", "B"}.issubset(titles)


async def test_get_task_ok_and_404(client: AsyncClient):
    created = await _api_create_task(client, "Read me", "desc", "created")
    tid = created["id"]

    ok = await client.get(f"/task/{tid}")
    assert ok.status_code == status.HTTP_200_OK
    assert ok.json()["id"] == tid

    missing = await client.get(f"/task/{uuid4()}")
    assert missing.status_code == status.HTTP_404_NOT_FOUND


async def test_patch_task_partial(client: AsyncClient):
    created = await _api_create_task(client, "T1", "D1", "created")
    tid = created["id"]

    patch = {"title": "T1-new"}
    resp = await client.patch(f"/task/{tid}", json=patch)
    assert resp.status_code == status.HTTP_200_OK
    updated = resp.json()
    assert updated["id"] == tid
    assert updated["title"] == "T1-new"
    assert updated["description"] == "D1"
    assert updated["status"] == "created"


async def test_patch_task_404(client: AsyncClient):
    resp = await client.patch(f"/task/{uuid4()}", json={"title": "X"})
    assert resp.status_code == status.HTTP_404_NOT_FOUND


async def test_delete_task_then_404(client: AsyncClient):
    created = await _api_create_task(client, "ToDel", "D", "created")
    tid = created["id"]

    del_resp = await client.delete(f"/task/{tid}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    get_resp = await client.get(f"/task/{tid}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND
