from asyncio import sleep
from asyncio.subprocess import create_subprocess_shell, PIPE


class AbstractDecryptionWorker:
    command_name = ""
    kwargs_separator = "="

    _running_kwargs = dict()
    _running_args = set()

    def setup_running_args(self, *args, **kwargs):
        """
        Method to set up process arguments
        """
        self._running_args = args
        self._running_kwargs = kwargs

    async def run(self) -> (bool, str):
        if not self.command_name:
            raise NotImplementedError("Property `command_name` must be implemented.")

        process = await create_subprocess_shell(self._get_complete_shell_command(), stdout=PIPE, stderr=PIPE)
        await sleep(5)
        stdout, stderr = await process.communicate()

        if stdout:
            return True, self.parse_process_response(stdout.decode())

        elif stderr:
            return False, f'[Error] {stderr.decode()}'

        else:
            return False, f"[Error] No response was received from process."

    def _get_complete_shell_command(self):
        kwargs_str = " ".join(f"{arg_key}{self.kwargs_separator}{arg_value}"
                              for arg_key, arg_value in self._running_kwargs.values())
        args_str = " ".join(self._running_args)
        return f"{self.command_name} {kwargs_str} {args_str}"

    def parse_process_response(self, response) -> str:
        return response


class AircrackNGWorker(AbstractDecryptionWorker):
    command_name = "aircrack-ng"
    kwargs_separator = " "

    def setup_running_args(self, target_file, dict_path, target_essid=None, target_bssid=None):
        if target_essid is None and target_bssid is None:
            raise RuntimeError("ESSID or BSSID must be passed")

        args = [target_file, "-q"]
        kwargs = {"-w": dict_path}

        if target_essid:
            kwargs["-e"] = target_essid
        else:
            kwargs["-b"] = target_bssid

        super(AircrackNGWorker, self).setup_running_args(*args, **kwargs)
