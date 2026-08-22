"""DSH Chat backend: manage the local DeepSeek Harness web server."""

import asyncio
import os
import socket

import decky_plugin  # type: ignore

PORT = 3080
URL = f"http://127.0.0.1:{PORT}"
DSH_BIN = "dsh"
LOG_NAME = "dsh-web.log"


def _port_open(port: int) -> bool:
    try:
        with socket.create_connection(("127.0.0.1", port), timeout=1.0):
            return True
    except OSError:
        return False


class Plugin:
    server_proc: asyncio.subprocess.Process | None = None
    log_file = None

    async def _main(self):
        # Auto-start the chat server when the plugin loads, unless
        # something is already serving the port.
        decky_plugin.logger.info("DSH Chat loaded; checking server state")
        if not _port_open(PORT):
            res = await self.start_server()
            decky_plugin.logger.info(f"auto-start: {res}")
        else:
            decky_plugin.logger.info("port %d already serving", PORT)

    async def get_status(self) -> dict:
        managed = self.server_proc is not None and self.server_proc.returncode is None
        return {
            "running": managed or _port_open(PORT),
            "managed": managed,
            "port": PORT,
            "url": URL,
        }

    async def start_server(self) -> dict:
        if self.server_proc is not None and self.server_proc.returncode is None:
            return {"ok": True, "message": "already running"}
        if _port_open(PORT):
            return {"ok": True, "message": "port already serving"}

        user_home = decky_plugin.DECKY_USER_HOME
        env = dict(os.environ)
        env.update(
            {
                "HOME": user_home,
                "USER": decky_plugin.DECKY_USER,
                "DSH_HOME": os.path.join(user_home, ".dsh"),
                "PATH": os.path.join(user_home, ".local/bin")
                + ":/usr/local/bin:/usr/bin:/bin",
            }
        )

        log_path = os.path.join(decky_plugin.DECKY_PLUGIN_LOG_DIR, LOG_NAME)
        try:
            self.log_file = open(log_path, "a")
        except OSError as e:
            decky_plugin.logger.error(f"cannot open log {log_path}: {e}")
            self.log_file = None

        try:
            self.server_proc = await asyncio.create_subprocess_exec(
                DSH_BIN,
                "web",
                "--no-open",
                "--port",
                str(PORT),
                stdout=self.log_file,
                stderr=self.log_file,
                env=env,
                cwd=user_home,
                start_new_session=True,
            )
        except Exception as e:  # noqa: BLE001
            decky_plugin.logger.error(f"failed to spawn dsh web: {e}")
            return {"ok": False, "message": str(e)}

        for _ in range(20):
            if self.server_proc.returncode is not None:
                return {
                    "ok": False,
                    "message": f"dsh web exited with code {self.server_proc.returncode}",
                }
            if _port_open(PORT):
                return {"ok": True, "message": "started"}
            await asyncio.sleep(0.5)
        return {"ok": True, "message": "started (port not yet open)"}

    async def stop_server(self) -> dict:
        if self.server_proc is None or self.server_proc.returncode is not None:
            return {"ok": True, "message": "not running"}
        try:
            os.killpg(os.getpgid(self.server_proc.pid), 15)  # SIGTERM
        except (ProcessLookupError, PermissionError):
            pass
        try:
            await asyncio.wait_for(self.server_proc.wait(), timeout=5)
        except asyncio.TimeoutError:
            try:
                os.killpg(os.getpgid(self.server_proc.pid), 9)
            except (ProcessLookupError, PermissionError):
                pass
        self.server_proc = None
        return {"ok": True, "message": "stopped"}

    async def _unload(self):
        if self.server_proc is not None and self.server_proc.returncode is None:
            decky_plugin.logger.info("stopping dsh web on plugin unload")
            await self.stop_server()
        if self.log_file is not None:
            try:
                self.log_file.close()
            except OSError:
                pass
