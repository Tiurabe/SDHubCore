import os
from pydantic import BaseModel


class Dir(BaseModel):
    name: str
    path: str

    def __getattr__(self, item):
        if item == self.path:
            return self.path
        if item == self.name:
            return self.name
        raise AttributeError("Dir object has no attribute '{}'".format(item))


paths: list[Dir] = [
    Dir(name="root", path="/kaggle/working"),
    Dir(name="webui", path=os.path.join("/kaggle/working", "mlengine"))
]

paths.extend([
    Dir(name="model", path=os.path.join(paths[1].path, "models", "Stable-diffusion")),
    Dir(name="lora", path=os.path.join(paths[1].path, "models", "Lora")),
    Dir(name="vae", path=os.path.join(paths[1].path, "models", "VAE")),
    Dir(name="embedding", path=os.path.join(paths[1].path, "embeddings")),
    Dir(name="extension", path=os.path.join(paths[1].path, "extensions")),
])


def check_path(path: str):
    if path is None or path is False:
        return False
    if not os.path.exists(path):
        if not os.path.exists(f(paths, "webui")):
            print("Unable to locate your sd webui installation, aborting the download.")
            return False
        else:
            try:
                os.makedirs(path, exist_ok=True)
            except Exception as e:
                print(f"Something went wrong while trying to create the folder '{path}': \n{e}")
                return False
        return False
    return path


# Fetches a path based on the specified name parameter.
# Usage: f(paths, "Root")
def f(name_parameter: str = None, paths_list: list = None):
    if not paths_list:
        if not name_parameter:
            return None
        if paths and len(paths) != 0:
            paths_list = paths
        else:
            raise IndexError("Unable to fetch the directories from the paths List. Unsure what happened here.")

    for Object in paths_list:
        temp_dict = Object.model_dump()
        if name_parameter in temp_dict['name']:
            return temp_dict["path"]
    return None
