import logging
import os
import subprocess
from sys import platform

from asynchronousfilereader import AsynchronousFileReader


def run_snap_command(command):
    """
    Run a snap command.

    This will automatically log output from snap as it happens, rather than waiting for the end of the process.
    This should reduce the number of messages from snap where they can be generically avoided.
    This call will block until the snap command finishes.

    Expects an environment variable called SNAP_GPT to exist which holds the path to the snap gpt tool.

    :param command: the list of arguments to pass to snap
    :return: None, may raise an exception if snap errors in some way.
    """

    # if we need to prepend the snap executable.
    if command[0] != os.environ['SNAP_GPT']:
        full_command = [os.environ['SNAP_GPT']] + command
    else:
        full_command = command

    # on linux there is a warning message printed by snap if this environment variable is not set.
    base_env = os.environ.copy()
    if "LD_LIBRARY_PATH" not in base_env and platform.system() != "Windows":
        base_env["LD_LIBRARY_PATH"] = "."

    logging.debug(f"running {full_command}")

    process = subprocess.Popen(full_command, env=base_env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    snap_logger_out = logging.getLogger("snap_stdout")
    snap_logger_err = logging.getLogger("snap_stderr")
    std_out_reader = AsynchronousFileReader(process.stdout)
    std_err_reader = AsynchronousFileReader(process.stderr)

    def pass_logging():
        while not std_out_reader.queue.empty():
            line = std_out_reader.queue.get().decode()
            snap_logger_out.info(line.rstrip('\n'))
        while not std_err_reader.queue.empty():
            line = std_err_reader.queue.get().decode()
            snap_logger_err.info("stderr:" + line.rstrip('\n'))

    while process.poll() is None:
        pass_logging()

    std_out_reader.join()
    std_err_reader.join()

    if process.returncode != 0:
        raise Exception("Snap returned non zero exit status")
