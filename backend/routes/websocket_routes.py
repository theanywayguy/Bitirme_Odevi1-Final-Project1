from fastapi import APIRouter, WebSocket
from backend.core.progress import get_progress, delete_progress
import asyncio

router = APIRouter()

@router.websocket("/ws/progress/{task_id}")
async def websocket_progress(ws: WebSocket, task_id: str):
    await ws.accept()
    try:
        while True:
            update = get_progress(task_id)
            if update:
                await ws.send_json(update)
                if update.get("progress") == 100:
                    break
            await asyncio.sleep(0.5)
    finally:
        await ws.close()
        delete_progress(task_id)
