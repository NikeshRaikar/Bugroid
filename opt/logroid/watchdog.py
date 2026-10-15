import time

from opt.logroid.shutdown import shutdown_event


def watchdog(threads, logger):
    while not shutdown_event.is_set():

        for thread in threads:

            if not thread.is_alive():
                logger.error(
                    "Thread died: %s",
                    thread.name,
                )

        time.sleep(30)