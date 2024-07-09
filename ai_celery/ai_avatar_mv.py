import json
import logging
import os.path
import shutil
from datetime import datetime

from celery import Task
from ai_celery.celery_app import app
from configs.env import settings
from ai_celery.common import Celery_RedisClient, CommonCeleryService

import torch
from interface import avatar_mv


class AiAvatarMVTask(Task):
    """
    Abstraction of Celery's Task class to support AI Avatar MV
    """
    abstract = True

    def __init__(self):
        super().__init__()

    def __call__(self, *args, **kwargs):
        return self.run(*args, **kwargs)


@app.task(
    bind=True,
    base=AiAvatarMVTask,
    name="{query}.{task_name}".format(
        query=settings.AI_QUERY_NAME,
        task_name=settings.AI_AVATAR_MV
    ),
    queue=settings.AI_AVATAR_MV
)
def ai_avatar_mv_task(self, task_id: str, data: bytes, task_request: bytes, file: bytes):
    """
    Service Ai Avatar MV tasks

    task_request example:
        file: {'image_file': 'static/public/ai_cover_gen/a.png', 'audio_file': 'static/public/ai_cover_gen/a.mp3'}
    """
    print(f"============= Ai Avatar MV task {task_id}: Started ===================")
    try:
        # Load data
        data = json.loads(data)
        request = json.loads(task_request)
        file = json.loads(file)
        Celery_RedisClient.started(task_id, data)

        # Check task removed
        Celery_RedisClient.check_task_removed(task_id)

        # Predict
        image_file = file.get('image_file').split("/")[-1]
        image_file = "/app/static/public/ai_cover_gen/" + image_file
        audio_file = file.get('audio_file').split("/")[-1]
        audio_file = "/app/static/public/ai_cover_gen/" + audio_file
        output_dir, output, time_execute = avatar_mv(image_file, audio_file)

        # Save s3
        urls = {
            "avatar_mv": CommonCeleryService.fast_upload_s3_files([output], settings.AI_AVATAR_MV),
        }

        # Successful
        metadata = {
            "task": settings.AI_AVATAR_MV,
            "tool": "local",
            "model": "hallo",
            "usage": None,
            "time_execute": time_execute,
        }
        response = {"urls": urls, "metadata": metadata}
        Celery_RedisClient.success(task_id, data, response)

        try:
            shutil.rmtree(output_dir)
        except:
            pass

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return

    except ValueError as e:
        logging.getLogger().error(str(e), exc_info=True)
        err = {'code': "400", 'message': str(e).split('!')[0].strip()}
        Celery_RedisClient.failed(task_id, data, err)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return

    except Exception as e:
        logging.getLogger().error(str(e), exc_info=True)
        err = {'code': "500", 'message': "Internal Server Error"}
        Celery_RedisClient.failed(task_id, data, err)

        if torch.cuda.is_available():
            torch.cuda.empty_cache()
            torch.cuda.synchronize()

        import gc;
        gc.collect()

        return
