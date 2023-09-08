from src.model.post_process import post_process
from src.model.train_and_predict import train_and_predict
from src.utils.logging_utils import logger


def main():
    logger().info("Project init")
    forcast_df = train_and_predict()
    post_process(forcast_df)


if __name__ == "__main__":
    main()
