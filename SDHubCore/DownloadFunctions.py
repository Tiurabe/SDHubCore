import os
import subprocess
from PathHandler import check_path
from urllib.parse import urlparse, unquote
import requests
import re
from colored import cprint


def get_filename(url, user_header=None) -> str:
    """
    Attempts to extract the filename from a URL. Also tries to handle possible errors and handling potential edge cases.

    Args:
        url (str): The target URL.
        user_header (str, optional): Optional user header for authentication. The default value is None.

    Returns:
        str: The extracted filename, or raises an exception if not found.

    Raises:
        requests.HTTPError: If the request fails with an HTTP error.
        ValueError: If the filename cannot be extracted from the URL or headers.
    """

    headers = {"Authorization": user_header} if user_header else {}  # Concise header assignment

    try:
        response = requests.get(url, stream=True, headers=headers)
        response.raise_for_status()

        filename = (
            response.headers.get("content-disposition")  # Use get() for optional headers
            and re.findall(r'filename="?([^"]+)"?', response.headers["content-disposition"])[0]
        ) or unquote(os.path.basename(urlparse(url).path))

        if not filename:
            raise ValueError("Filename could not be extracted from the URL or headers.")

        return filename

    except requests.HTTPError as err:
        raise requests.HTTPError(f"Failed to retrieve filename from URL: {err}") from err


def aria2_download(url: str, output_folder: str, file_name: str | None = None,
                   quiet: bool = False, safe_mode: bool = True, civitai_api_key: str = None):
    if safe_mode:
        if not check_path(output_folder):
            raise ValueError("The folder where you are trying to save the downloaded file does not exist.")
    if not file_name or file_name.find(".") == -1:
        if "civitai.com" in url:
            if civitai_api_key is not None:
                file_name = get_filename(url, user_header=f"Bearer {civitai_api_key}")
            else:
                cprint(text="Warning: The CivitAI API Key is missing. Some downloads might fail.", fore_rgb=(230, 57, 0))
        else:
            file_name = get_filename(url)

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
