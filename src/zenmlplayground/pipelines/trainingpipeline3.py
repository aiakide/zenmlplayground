from zenml import pipeline, Model, get_pipeline_context

from zenmlplayground.steps import training_data_loader, fetch_svc_trainer


@pipeline(
    model=Model(
        # The name uniquely identifies this model
        name="iris_classifier",
        # Pass the stage you want to get the right model
        version="production",
    ),enable_cache=False,
name="training pipeline 3")
def training_pipeline(gamma: float = 0.002):
    # Now this pipeline will have the production `iris_classifier` model active.
    model = get_pipeline_context().model

    X_train, X_test, y_train, y_test,_ = training_data_loader()
    fetch_svc_trainer(gamma=gamma, X_train=X_train, y_train=y_train)

if __name__ == '__main__':
    training_pipeline()