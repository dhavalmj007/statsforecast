import pandas as pd

from src.utils.logging_utils import logger


def post_process(df: pd.DataFrame):
    """
    Code to do anything on the final dataframe. E.g. push to s3 or similar activity
    :param df:
    :return:
    """
    logger().info("Post Processing: STARTED")

    logger().info("Pushing final prediction to s3")

    logger().info("Post Processing: COMPLETED")

    pass
