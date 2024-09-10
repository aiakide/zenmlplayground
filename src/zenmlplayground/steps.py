import logging
from typing import Tuple, Annotated

import numpy as np
import pandas as pd
from sklearn.base import ClassifierMixin
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from zenml import step, get_step_context, ArtifactConfig, log_artifact_metadata, log_model_metadata

from zenmlplayground.models import iris_classifier_model


@step
def load_data() -> dict:
    """Simulates loading of training data and labels."""

    training_data = [[1, 2], [3, 4], [5, 6]]
    labels = [0, 1, 0]

    return {'features': training_data, 'labels': labels}


@step
def train_model(data: dict) -> None:
    """
    A mock 'training' process that also demonstrates using the input data.
    In a real-world scenario, this would be replaced with actual model fitting logic.
    """
    total_features = sum(map(sum, data['features']))
    total_labels = sum(data['labels'])

    print(f"Trained model using {len(data['features'])} data points. "
          f"Feature sum is {total_features}, label sum is {total_labels}")

@step
def training_data_loader() -> Tuple[
    # Notice we use a Tuple and Annotated to return
    # multiple named outputs
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
    Annotated[pd.DataFrame,"iris_dataset"]
]:
    """Load the iris dataset as a tuple of Pandas DataFrame / Series."""
    logging.info("Loading iris...")
    iris = load_iris(as_frame=True)
    logging.info("Splitting train and test...")
    X_train, X_test, y_train, y_test = train_test_split(
        iris.data, iris.target, test_size=0.2, shuffle=True, random_state=42
    )
    return X_train, X_test, y_train, y_test,iris.data


@step(model=iris_classifier_model)
def svc_trainer(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    gamma: float = 0.001,
) ->Annotated[ClassifierMixin, ArtifactConfig(name="trained_model")]:
    """Train a sklearn SVC classifier."""

    model = SVC(gamma=gamma)
    model.fit(X_train.to_numpy(), y_train.to_numpy())

    train_acc = model.score(X_train.to_numpy(), y_train.to_numpy())
    print(f"Train accuracy: {train_acc}")
    step_context = get_step_context()
    step_context.add_output_metadata(
        output_name="trained_model", metadata={"metadata_key": "metadata_value"}
    )
    step_context.add_output_tags(output_name="trained_model", tags=["tag_name"])

    log_artifact_metadata(artifact_name="trained_model",metadata={"accuracy":train_acc})

    return model


@step(model=iris_classifier_model)
def new_svc_trainer(    X_train: pd.DataFrame,
    y_train: pd.Series,
    gamma: float = 0.001)->Annotated[ClassifierMixin,ArtifactConfig(name="trained_classifier",is_model_artifact=True)]:
    technical_model = SVC(gamma=gamma)
    technical_model.fit(X_train.to_numpy(), y_train.to_numpy())
    model = get_step_context().model

    train_acc = technical_model.score(X_train.to_numpy(), y_train.to_numpy())
    log_model_metadata(
        # Model name can be omitted if specified in the step or pipeline context
        model_name=model.name,
        # Passing None or omitting this will use the `latest` version
        # Metadata should be a dictionary of JSON-serializable values
        metadata={"accuracy": float(train_acc)}
        # A dictionary of dictionaries can also be passed to group metadata
        #  in the dashboard
        # metadata = {"metrics": {"accuracy": accuracy}}

    )
    log_artifact_metadata(artifact_name="trained_classifier",metadata={"accuracy":train_acc})
    model.set_stage(stage="production",force=True)
    return technical_model


@step()
def fetch_svc_trainer(    X_train: pd.DataFrame,
    y_train: pd.Series,
    gamma: float = 0.001)->Annotated[ClassifierMixin,"trained_classifier"]:
    model = get_step_context().model
    technical_model=model.get_model_artifact(name="trained_classifier").load()

    train_acc = technical_model.score(X_train.to_numpy(), y_train.to_numpy())
    log_model_metadata(
        # Model name can be omitted if specified in the step or pipeline context
        model_name=model.name,
        # Passing None or omitting this will use the `latest` version
        model_version=f"{model.version}.1",
        # Metadata should be a dictionary of JSON-serializable values
        metadata={"accuracy": float(train_acc)}
        # A dictionary of dictionaries can also be passed to group metadata
        #  in the dashboard
        # metadata = {"metrics": {"accuracy": accuracy}}

    )
    #log_artifact_metadata(artifact_name="iris_classifier",metadata={"accuracy":train_acc})
    return technical_model


@step
def print_data(data: np.ndarray):
    print(data)


@step
def dummy_trainer(dataset:pd.DataFrame):
    print("Dummy trainer")