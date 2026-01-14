import os
import subprocess
import platform

SYSTEM = platform.system()

def open_app(app_name: str) -> str:
    app_name = app_name.lower()

    if SYSTEM == "Windows":
        apps = {
            "chrome": "start chrome",
            "notepad": "notepad",
            "calculator": "calc",
            "vs code": "code"
        }

        if app_name in apps:
            os.system(apps[app_name])
            return f"Opening {app_name}"

    return "I cannot open that application."

def shutdown(confirm: bool) -> str:
    if not confirm:
        return "Shutdown cancelled."

    if SYSTEM == "Windows":
        os.system("shutdown /s /t 5")
        return "Shutting down the system."

    return "Shutdown not supported."

def restart(confirm: bool) -> str:
    if not confirm:
        return "Restart cancelled."

    if SYSTEM == "Windows":
        os.system("shutdown /r /t 5")
        return "Restarting the system."

    return "Restart not supported."
