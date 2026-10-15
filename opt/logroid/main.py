import signal
from threading import Thread

from bugreport import bugreport_loop
from logcat import logcat_loop
from logger_config import get_logger
from shutdown import shutdown_event
from storage import (
    cleanup_storage,
    initialize_storage,
)
from sync import sync_loop

logger = get_logger()


def signal_handler(signum, frame):
    logger.info(
        "Shutdown signal %s",
        signum,
    )

    shutdown_event.set()


def main():
    initialize_storage()

    signal.signal(
        signal.SIGINT,
        signal_handler,
    )

    signal.signal(
        signal.SIGTERM,
        signal_handler,
    )

    threads = [
        Thread(
            target=bugreport_loop,
            args=(logger,),
            daemon=True,
            name="BUGREPORT",
        ),
        Thread(
            target=logcat_loop,
            args=(logger,),
            daemon=True,
            name="LOGCAT",
        )
        # Thread(
        #     target=sync_loop,
        #     args=(logger,),
        #     daemon=True,
        #     name="SYNC",
        # ),
    ]

    for thread in threads:
        thread.start()

    while not shutdown_event.wait(60):
        cleanup_storage(logger)

    logger.info("Service stopped")


if __name__ == "__main__":
    main()