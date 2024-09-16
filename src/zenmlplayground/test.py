from zenml.client import Client
from zenml.code_repositories import BaseCodeRepository


model = Client().get_code_repository("zenmlplayground")
repo = BaseCodeRepository.from_model(model)

repo.download_files(commit="main", directory="code_repo_download",repo_sub_directory="")