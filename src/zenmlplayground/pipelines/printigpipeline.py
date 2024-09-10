import numpy as np
from zenml import ExternalArtifact, pipeline

from zenmlplayground.steps import print_data


@pipeline
def printing_pipeline():
    # One can also pass data directly into the ExternalArtifact
    # to create a new artifact on the fly
    data = ExternalArtifact(value=np.array([0]))

    print_data(data=data)


if __name__ == "__main__":
    printing_pipeline()