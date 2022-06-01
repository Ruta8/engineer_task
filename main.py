from workflow.combine_files import combine_files
from workflow.transform_data import transform
from data_quality.check_quality import check_data_quality
import logging

def logger(file_name: str) -> None:
    logging.basicConfig(
        filename=f"logs/{file_name}",
        format="%(asctime)s - %(filename)s - %(message)s",
        level=logging.DEBUG,
        datefmt="%m/%d/%Y %I:%M:%S %p",
    )


def app() -> None:
    
    df = combine_files()

    check_data_quality(df)

    df = transform(df)

    df.to_csv("data/processed/task_data.csv", index=False)


if __name__ == "__main__":
    logger("data_quality")
    app()
