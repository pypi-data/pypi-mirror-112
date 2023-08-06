import os
import atexit
import signal
import logging
import threading
import subprocess


from pathlib import Path

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class Player(object):
    
    def __init__(self, source,
                 args=None):
        logger.debug('Instantiating OMXPlayer')

        if args is None:
            self.args = []
        elif isinstance(args, str):
            import shlex
            self.args = shlex.split(args)
        else:
            self.args = list(map(str, args))
        self._source = Path(source)

        self._process = None
        self._force_kill()
        self.load(source)
        
    def _force_kill(self):
        try:
            subprocess.call(["killall", "omxplayer.bin"])
        finally:
            pass 

    def load(self, source):
        self._source = source
        self._process = self._setup_omxplayer_process(source)

    def _run_omxplayer(self, source, devnull):
        def on_exit(self, exit_status):
            logger.info("OMXPlayer process is dead, all DBus calls from here "
                        "will fail")
            self.exitEvent(self, exit_status)

        def monitor(self, process, on_exit):
            process.wait()
            on_exit(self, process.returncode)

        try:
            source = str(source.resolve())
        except AttributeError:
            pass
        command = ['omxplayer'] + self.args + [source]
        logger.debug("Opening omxplayer with the command: %s" % command)
        
        try:
            process = subprocess.Popen(command,
                                    stdin=devnull,
                                    stdout=devnull,
                                    preexec_fn=os.setsid)
        except:
            if os.getenv("DEBUG"):
                logger.debug("Process omxplayer faliture")
                return None
            else:
                raise
        try:
            self._process_monitor = threading.Thread(target=monitor,
                                                     args=(self, process, on_exit))
            self._process_monitor.start()
            return process
        except:
            # Make sure to not leave any dangling process on failure
            self._terminate_process(process)
            raise

    def _setup_omxplayer_process(self, source):
        logger.debug('Setting up OMXPlayer process')

        with open(os.devnull, 'w') as devnull:
            process = self._run_omxplayer(source, devnull)
        logger.debug('Process opened with PID %s' % process)

        return process

    def _terminate_process(self, process):
        try:
            process_group_id = os.getpgid(process.pid)
            os.killpg(process_group_id, signal.SIGTERM)
            logger.debug('SIGTERM Sent to pid: %s' % process_group_id)
        except OSError:
            logger.error('Could not find the process to kill')