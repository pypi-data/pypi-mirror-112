import pandas as pd


def intersectionalize(df: pd.DataFrame, identity_columns: list[str]) -> pd.DataFrame:
    """Generates a new dataframe with identity columns replaced by indicator variables
    for all combinations of identities present in the data.

    Args:
        df (pd.DataFrame): The input dataframe.
        identity_columns (list[str]): A list of the names of columns in the dataframe
            which contain identity information.

    Returns:
        pd.DataFrame: A new dataframe with the identity columns replaced by indicator
        variables.
    """
    return pd.concat(
        [
            df.drop(identity_columns, axis="columns"),
            pd.get_dummies(
                pd.Series(zip(*[df[col] for col in identity_columns]), index=df.index)
            ),
        ],
        axis="columns",
    )
