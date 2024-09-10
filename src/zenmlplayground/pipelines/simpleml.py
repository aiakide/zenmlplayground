from zenml import pipeline

from zenmlplayground.steps import load_data, train_model


@pipeline
def simple_ml_pipeline():
    """Define a pipeline that connects the steps."""
    dataset = load_data()
    train_model(dataset)


if __name__ == "__main__":
    run = simple_ml_pipeline()
    # You can now use the `run` object to see steps, outputs, etc.