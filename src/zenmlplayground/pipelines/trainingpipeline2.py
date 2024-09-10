import logging

from zenml import pipeline
from zenml.client import Client

from zenmlplayground.steps import dummy_trainer


@pipeline(name="training pipeline 2",enable_cache=False)
def training_pipeline():
    client = Client()

    # Fetch by name alone - uses the latest version of this artifact
    dataset_artifact = client.get_artifact_version(name_id_or_prefix="iris_dataset")

    # Fetch by name and version
    # = client.get_artifact_version(
     #   name_id_or_prefix="iris_dataset", version="1"
    #storage_size)

    logging.info("Dataset size %s",dataset_artifact.run_metadata["storage_size"].value)

    # Pass into any step
    dummy_trainer(dataset=dataset_artifact)


if __name__ == "__main__":
    training_pipeline()