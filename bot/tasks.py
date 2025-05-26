import logging
import os
import shutil

import docker
from celery import shared_task

from bot.models import Bot
from bot.services import generate_code

logger = logging.getLogger(__name__)


@shared_task
def deploy_bot(bot_id: int) -> dict:
    try:
        bot_instance = Bot.objects.get(id=bot_id)
        code = generate_code(bot_instance)

        dockerfile_dir = f"./factory/{bot_id}"
        os.makedirs(dockerfile_dir, exist_ok=True)
        dockerfile_path = shutil.copyfile(
            "bot/bot_templates/Dockerfile.txt",
            f"{dockerfile_dir}/Dockerfile",
        )
        pythonfile_path = os.path.join(dockerfile_dir, "main.py")

        with open(pythonfile_path, "w") as f:
            f.write(code)

        client = docker.from_env()
        container_name = f"bot-container-{bot_id}"

        # Build the Docker image
        client.images.build(
            path=dockerfile_dir,
            dockerfile="Dockerfile",
            tag=f"bot-{bot_id}",
        )

        # Handle existing container
        try:
            existing_container = client.containers.get(container_name)
            existing_container.stop()
            existing_container.remove()
        except Exception as e:
            logger.error(
                f"Container '{container_name}' does not exist. Proceeding to create a new one. error: {e}",
            )

        # Run new container
        client.containers.run(
            f"bot-{bot_id}",
            detach=True,
            name=container_name,
            privileged=True,
            cpu_count=1,
            cpu_shares=100,
            mem_limit="100m",
        )

        return {
            "status": "success",
            "message": f"Bot {bot_id} has been successfully deployed.",
        }
    except Exception as e:
        logger.error(f"Deployment error for bot {bot_id}: {e}")
        return {"status": "error", "message": str(e)}
