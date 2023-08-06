import logging
from uvicorn.subprocess import get_subprocess
from uvicorn.supervisors.statreload import StatReload

import requests

logger = logging.getLogger("uvicorn.error")


class ChangeReloader(StatReload):
    def should_restart(self) -> bool:
        flag = super().should_restart()
        if flag:
            logger.warning("pre-reloading! sending shutdown request...")
            requests.get(f"http://localhost:{self.config.port}/api/shutdown", timeout=1)
        return flag
