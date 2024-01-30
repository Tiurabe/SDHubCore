import subprocess
from PathHandler import check_path


def aria2_download(url: str, output_folder: str, file_name: str | None = None,
                   quiet: bool = False, safe_mode: bool = True, civitai_api_key: str = None):
    if safe_mode:
        if not check_path(output_folder):
            raise ValueError("The folder where you are trying to save the downloaded file does not exist.")

    def parse_parameters(config: dict | list) -> list:
        args_list = []
        for key, value in config.items():
            if key == "url":
                args_list.append(str(value))
            elif key == "out" and not file_name:
                continue
            elif value is not None and not isinstance(value, bool):
                args_list.append(f"--{key}={value}")
            elif isinstance(value, bool) and value:
                args_list.append(f"--{key}")

        return args_list

    parameters = {
        "console-log-level": "error",
        "summary-interval": 10,
        "quiet": quiet,
        "continue": True,
        "max-connection-per-server": 16,
        "split": 16,
        "min-split-size": "1M",
        "dir": output_folder,
        "out": file_name,
        "url": url,
    }

    if civitai_api_key and "civitai.com" in parameters['url']:
        parameters['url'] += f"&token={civitai_api_key}" if "?" in url else f"?token={civitai_api_key}"

    parsed_parameters = parse_parameters(parameters)
    subprocess.run(["aria2c", *parsed_parameters])
