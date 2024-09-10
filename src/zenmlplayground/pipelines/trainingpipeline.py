import os

from zenml import pipeline
from zenml.config import DockerSettings
from zenml.logger import get_logger
from zenml.orchestrators.local_docker.local_docker_orchestrator import \
    LocalDockerOrchestratorSettings

from zenmlplayground.models import iris_classifier_model
from zenmlplayground.steps import training_data_loader, svc_trainer, new_svc_trainer


logger = get_logger(__name__)

#ädocker_settings = DockerSettings(dockerfile="./docker/Dockerfile",build_context_root=".")
#orchestrator_settings = LocalDockerOrchestratorSettings(
       # run_args={"network_mode":"host"}
    #)

#docker_settings= DockerSettings(replicate_local_python_environment="pip_freeze")

#@pipeline(model=iris_classifier_model,enable_cache=False,settings={"docker":docker_settings,"orchestrator.local_docker":orchestrator_settings})
@pipeline()
def training_pipeline(gamma: float = 0.002):
    X_train, X_test, y_train, y_test,_ = training_data_loader()
    new_svc_trainer(gamma=gamma, X_train=X_train, y_train=y_train)


if __name__ == "__main__":
    #training_pipeline()
    pipeline_args = {}
    pipeline_args["config_path"] = os.path.join(
         "./configs","trainingpipeline.yaml"
    )
    training_pipeline.with_options(**pipeline_args)()
