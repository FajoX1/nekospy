from nekospy import dp

from . import start, watcher

dp.include_router(start.router)
dp.include_router(watcher.router)