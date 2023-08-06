import daemon
import daemon.pidfile
import inotify.adapters
import logging
import subprocess
import sys


class CsgoHandler():
    def __init__(self, **kwargs):
        self.open_sequence = (
            "IN_OPEN",
            "IN_ACCESS",
            "IN_CLOSE_NOWRITE",
            "IN_OPEN",
        )
        self.events = list()

        normalise_str_to_list = lambda lst: [lst] if isinstance(lst, str) else lst

        self.csgo_path = kwargs.get("Path")
        self.start_script = normalise_str_to_list(kwargs.get("StartScript"))
        self.stop_script = normalise_str_to_list(kwargs.get("StopScript"))

        try:
            assert all([
                isinstance(self.open_sequence, tuple),
                isinstance(self.events, list),
                isinstance(self.csgo_path, str),
                isinstance(self.start_script, list),
                isinstance(self.stop_script, list),
            ])
        except AssertionError as e:
            raise ValueError("Constructor arguments invalid") from e

    # If running as a daemon, this needs to be done after daemonizing
    # Otherwise we will get stale file handles
    def fh_init(self):
        logging.basicConfig(
            stream=sys.stdout,
            level=logging.DEBUG,
        )
        self.logger = logging.getLogger("csgo_handler")

        self.inotify = inotify.adapters.Inotify()
        self.inotify.add_watch(self.csgo_path)

    def determine_opened_event(self):
        return tuple(self.events[-4:]) == self.open_sequence

    def determine_closed_event(self):
        if len(self.events) > 4:
            return all([
                self.events[-2] == "IN_ACCESS",
                self.events[-1] == "IN_CLOSE_NOWRITE",
                self.events[-4:] != self.open_sequence
            ])
        # Default to False
        return False

    def game_opened_handler(self):
        self.logger.debug("CSGO started")

        pipe = subprocess.Popen(self.start_script, start_new_session=True)
        pipe.communicate()

        if pipe.returncode != 0:
            self.logger.warn("CSGO start script failed")

    def game_closed_handler(self):
        self.logger.debug("CSGO stopped")

        pipe = subprocess.Popen(self.stop_script, start_new_session=True)
        pipe.communicate()

        if pipe.returncode != 0:
            self.logger.warn("CSGO stop script failed")

    def eventloop(self):
        self.fh_init()
        for event in self.inotify.event_gen(yield_nones=False):
            event_msg = event[1][0]

            self.logger.debug("Received event {}".format(event_msg))
            self.events.append(event_msg)
            
            if self.determine_opened_event():
                self.game_opened_handler()
                continue

            if self.determine_closed_event():
                self.game_closed_handler()
                continue

    def daemonize(self):
        print("Starting daemon...")
        with daemon.DaemonContext(
            stdout=sys.stdout,
            pidfile=daemon.pidlockfile.PIDLockFile("/tmp/csgo_handler.pid"),
        ):
            self.eventloop()
