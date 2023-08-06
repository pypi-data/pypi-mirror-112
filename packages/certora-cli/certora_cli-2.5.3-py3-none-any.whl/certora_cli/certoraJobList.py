import os.path
from datetime import datetime
from shutil import copyfile
from typing import Any, Dict

from certora_cli.certoraUtils import debug_print_, get_certora_root_directory, is_windows, print_warning, \
    read_json_file, remove_file, write_json_file
from certora_cli.certoraUtils import RECENT_JOBS_FILE


class JobList:
    """
    Represents Recently executed jobs

    Structure is as follows:
    {
        "path_to_test/working_dir": [
            {
                "job_id": {JOB_ID},
                "output_url": {REPORT_URL: https://{DOMAIN}/output/.../data.json...},
                "notify_msg": {OPTIONAL: NOTIFICATION_MSG}
            },...
        ],...
    }

    Each path has a (FIFO) queue of up to {MAX_LENGTH} recently executed jobs
    The first element in the queue is the most recent one

    """

    jobs = {}  # type: Dict[str, Any]

    MAX_LENGTH = 10

    recent_jobs_path = ""
    temp_file_path = ""

    def __init__(self, current_path: str = os.getcwd(), debug: bool = False):
        self.current_path = current_path
        if is_windows():
            self.current_path = os.path.normcase(self.current_path)
        self.debug = debug
        self.recent_jobs_path = os.path.join(get_certora_root_directory(), RECENT_JOBS_FILE)
        self.temp_file_path = os.path.join(get_certora_root_directory(), f".tmp{RECENT_JOBS_FILE}")
        self.get_recent_jobs(self.recent_jobs_path)

    def add_job(self, job_id: str, output_url: str, notify_msg: str) -> None:
        if not self.current_path:
            debug_print_(f"Current path attribute is missing. Skipped adding job {job_id} to recent jobs list",
                         self.debug)
            return
        new_job = {
            "job_id": job_id,
            "output_url": output_url,
            "notify_msg": notify_msg
        }  # type: Dict[str, Any]
        try:
            if self.current_path not in self.jobs.keys():
                self.jobs[self.current_path] = []
            self.jobs[self.current_path].insert(0, new_job)  # insert at the front of the list
            if len(self.jobs[self.current_path]) > self.MAX_LENGTH:
                self.remove_oldest_job()
        except AttributeError as e:
            debug_print_(f"Couldn't add job {job_id}. Recent jobs file format may have changed: {e}", self.debug)
            self.rename_recent_jobs_file()

    def remove_oldest_job(self) -> None:
        if not self.current_path:
            debug_print_("Current path attribute is missing", self.debug)
            return
        if len(self.jobs[self.current_path]):
            removed_job = self.jobs[self.current_path].pop()  # remove the last element
            debug_print_(f"Removed job {removed_job.get('jobId', '')} from recent jobs list", self.debug)

    def get_data(self) -> Dict[str, Any]:
        return self.jobs

    def save_data(self) -> None:
        # backup
        succeeded = self.copy(self.recent_jobs_path, self.temp_file_path)
        if not succeeded:
            debug_print_("Couldn't create a backup file.", self.debug)

        try:
            write_json_file(self.get_data(), self.recent_jobs_path)
            # remove the backup file
            remove_file(self.temp_file_path)
        except (ValueError, OSError) as e:
            debug_print_(f"Error occurred when saving json data: {e}", self.debug)
            self.revert()

    def revert(self) -> None:
        """
        used when recent job file is corrupted
        overrides this file with the backup file (if exists)
        """
        if os.path.isfile(self.temp_file_path):
            succeeded = self.copy(self.temp_file_path, self.recent_jobs_path)
            if succeeded:
                # remove the backup file
                remove_file(self.temp_file_path)
        else:
            debug_print_("Couldn't revert recent jobs changes. Backup file does not exist", self.debug)

    def get_recent_jobs(self, file_path: str) -> None:
        """
        Sets the jobs attribute to be the JSON object stored in the supplied file_path
        If file_path format is wrong (on ValueError) renames the file
        """
        try:
            recent_jobs = read_json_file(file_path)
            self.jobs = recent_jobs
        except FileNotFoundError:
            debug_print_(f"Couldn't find recent jobs file in {file_path}", self.debug)
        except ValueError:
            debug_print_("Recent jobs file has incorrect format", self.debug)
            self.rename_recent_jobs_file()

    def copy(self, src_path: str, dst_path: str) -> bool:
        try:
            copyfile(src_path, dst_path)
            return True
        except OSError as e:
            debug_print_(f"Couldn't copy {src_path}: {e}", self.debug)
        return False

    def rename_recent_jobs_file(self) -> None:
        now = datetime.now()
        current_time = now.strftime("%Y-%m-%d_%H-%M-%S-%f")
        name = os.path.join(get_certora_root_directory(), f".incompatible.{current_time}{RECENT_JOBS_FILE}")
        try:
            os.rename(self.recent_jobs_path, name)
            print_warning(f"Recent jobs file was renamed. Please, see {name}")
        except (OSError, FileExistsError) as e:
            debug_print_(f"Couldn't rename the recent jobs file: {e}", self.debug)
