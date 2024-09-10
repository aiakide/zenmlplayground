from zenml import Model

iris_classifier_model = Model(
    # The name uniquely identifies this model
    # It usually represents the business use case
    name="iris_classifier",
    # The version specifies the version
    # If None or an unseen version is specified, it will be created
    # Otherwise, a version will be fetched.
    version="prod",
    # Some other properties may be specified
    license="Apache 2.0",
    description="A classification model for the iris dataset.",
)