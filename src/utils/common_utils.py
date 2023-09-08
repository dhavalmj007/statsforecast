import pandas as pd


def evaluate_cross_validation(df: pd.DataFrame, metric) -> pd.DataFrame:
    models = df.drop(columns=["ds", "cutoff", "y"]).columns.tolist()
    evals = []
    for model in models:
        eval_ = (
            df.groupby(["unique_id", "cutoff"])
            .apply(lambda x: metric(x["y"].values, x[model].values))
            .to_frame()
        )  # Calculate loss for every unique_id, model and cutoff.
        eval_.columns = [model]
        evals.append(eval_)
    evals = pd.concat(evals, axis=1)
    evals = evals.groupby(["unique_id"]).mean(
        numeric_only=True
    )  # Averages the error metrics for all cutoffs for every combination of model and unique_id
    evals["best_model"] = evals.idxmin(axis=1)
    return evals


def get_best_model_forecast(forecasts_df: pd.DataFrame, evaluation_df: pd.DataFrame) -> pd.DataFrame:
    df = (
        forecasts_df.set_index("ds", append=True)
        .stack()
        .to_frame()
        .reset_index(level=2)
    )  # Wide to long
    df.columns = ["model", "best_model_forecast"]
    df = df.join(evaluation_df[["best_model"]])
    df = df.query(
        'model.str.replace("-lo-90|-hi-90", "", regex=True) == best_model'
    ).copy()
    df.loc[:, "model"] = [
        model.replace(bm, "best_model")
        for model, bm in zip(df["model"], df["best_model"])
    ]
    df = df.drop(columns="best_model").set_index("model", append=True).unstack()
    df.columns = df.columns.droplevel()
    df = df.reset_index(level=1)
    return df
