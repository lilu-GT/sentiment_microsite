import pandas as pd


def preprocess_df(df, text_field):
    # keep rows that are empty
    empty_responses_df = pd.DataFrame(columns=df.columns)
    empty_responses_df = pd.concat(
        [empty_responses_df, df[df[text_field].isnull()]])
    df = df[~df[text_field].isnull()]

    # drop rows that are empty before preprocessing
    df['word_count'] = df[text_field].str.split().str.len()

    empty_responses_df = pd.concat(
        [empty_responses_df, df[df['word_count'] < 1]])
    df = df[df['word_count'] >= 1]
    df = df.drop('word_count', axis=1)
    empty_responses_df = empty_responses_df.drop('word_count', axis=1)

    return df, empty_responses_df
