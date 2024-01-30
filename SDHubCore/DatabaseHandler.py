from pydantic import BaseModel
import ast
import requests


class Info(BaseModel):
    source: str
    version: str | None = ""
    last_update: str | None = ""
    comment: str | None = ""


class Model(BaseModel):
    name: str
    type: str
    format: str = "safetensors"
    info: Info


models: list[Model] = []


def fetch_models(url: str):
    if not url:
        raise Exception("The url parameter cannot be empty.")
    models.clear()
    response = requests.get(url).text
    custom_database = ast.literal_eval(response)
    for custom_model_data in custom_database:
        temp_custom_model = Model(**custom_model_data)
        models.append(temp_custom_model)
    return models


keys: list = [key.name for key in models]


# Usage example: temp = model_finder(models_list=models, index="name", value="YamersAnime")
def model_finder(index: str, value: str, models_list: list = None):
    if not models_list:
        models_list = models
    for model in models_list:
        dict_model = model.model_dump()
        if dict_model[index] == value:
            return model
