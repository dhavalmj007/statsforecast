import os.path

import pandas as pd
from datasetsforecast.losses import mse
from statsforecast import StatsForecast
from statsforecast.models import (
    AutoARIMA,
    HoltWinters,
    CrostonClassic as Croston,
    HistoricAverage,
    DynamicOptimizedTheta as DOT,
    SeasonalNaive,
)

from src.constants import SEASON_LENGTH, TRAIN_DATA, DATA_FOLDER
from src.utils.common_utils import evaluate_cross_validation, get_best_model_forecast
from src.utils.logging_utils import logger


def train_and_predict() -> pd.DataFrame:
    logger().info("Training and predict: STARTED")

    logger().info(f"Fetching training data from {TRAIN_DATA}")
    Y_df = pd.read_parquet(TRAIN_DATA)

    uids = Y_df["unique_id"].unique()[:10]  # Select 10 ids to make the example faster
    
    Y_df = Y_df.query("unique_id in @uids")
    
    Y_df = Y_df.groupby("unique_id").tail(
        7 * 24
    )  # Select last 7 days of data to make example faster
    logger().info(f"Total data to train on: {Y_df.shape}")
    Y_df.to_csv(os.path.join(DATA_FOLDER, "Y_df.csv"), index=False)

    # Create a list of models and instantiation parameters
    models = [
        AutoARIMA(season_length=SEASON_LENGTH),
        HoltWinters(),
        Croston(),
        SeasonalNaive(season_length=SEASON_LENGTH),
        HistoricAverage(),
        DOT(season_length=SEASON_LENGTH),
    ]
    
    # Instantiate StatsForecast class as sf
    sf = StatsForecast(
        df=Y_df,
        models=models,
        freq="H",
        n_jobs=-1,
        fallback_model=SeasonalNaive(season_length=7),
    )
    logger().info(f"Starting forecast")
    forecasts_df = sf.forecast(h=48, level=[90])

    logger().info(f"Starting cross validation")
    crossvaldation_df = sf.cross_validation(df=Y_df, h=24, step_size=24, n_windows=2)
    
    evaluation_df = evaluate_cross_validation(crossvaldation_df, mse)
    
    summary_df = evaluation_df.groupby("best_model").size().sort_values().to_frame()
    summary_df.reset_index().columns = ["Model", "Nr. of unique_ids"]
    
    prod_forecasts_df = get_best_model_forecast(forecasts_df, evaluation_df)
    prod_forecasts_df.to_csv(os.path.join(DATA_FOLDER, "final_forecast.csv"), index=False)
    logger().info("Training and predict: COMPLETED")

    return prod_forecasts_df
