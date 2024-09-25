"""
Leaderboard data manipulation
"""
import datetime

import pandas as pd

from rives import Notice


def _dataframe_from_notices(notices: list[Notice]):
    """
    Create a DataFrame from the notices
    """
    records = [
        {
            'input_index': x.input_index,
            'output_index': x.output_index,
            'block_number': x.block_number,
            'verification_timestamp': x.block_timestamp,
            'submission_timestamp': datetime.datetime.fromtimestamp(
                x.payload.timestamp, tz=datetime.timezone.utc
            ),
            'cartridge_id': x.payload.cartridge_id.hex(),
            'rule_id': x.payload.rule_id[:20].hex(),
            'tape_id': x.payload.tape_id.hex(),
            'score': x.payload.score,
            'user_address': x.payload.user_address,
            'error_code': x.payload.error_code,
            'proof': x.proof,
        }
        for x in notices
    ]
    df = (
        pd.DataFrame.from_records(records)
        .query('error_code == 0')
    )
    return df


def _points_by_rank(rank: int):
    if rank <= 10:
        return 1000 - 3 * (rank - 1)
    if rank <= 100:
        return 973 - 2 * (rank - 10)
    return 793 - (rank - 100)


def _score_contest(group):
    """
    Create scores for a single contest
    """
    return (
        group
        .sort_values(by='score', ascending=False)
        .drop_duplicates(subset=['user_address'], keep='first')
        .query('score > 0')
        .assign(rank=lambda x: range(1, x.shape[0] + 1))
        .assign(points=lambda x: x['rank'].apply(_points_by_rank))
    )


def _compute_contest_scores(df_notices: pd.DataFrame) -> pd.DataFrame:
    """
    Transforma a DataFrame of notices into a narrow-form dataframe of contest
    scores.
    """
    return (
        df_notices
        .groupby('rule_id')
        .apply(_score_contest, include_groups=False)
        .reset_index()
    )


def _pivot_scores(
    df_scores: pd.DataFrame,
    contest_ids: list[str]
) -> pd.DataFrame:
    """
    Transform a narrow-form dataframe of contest scores into the final pivoted
    leaderboard.
    """
    title_order = contest_ids + ['rank', 'points', 'score', 'tape_id']

    pivoted = (
        pd.pivot(
            df_scores,
            columns='rule_id',
            index='user_address',
            values=['points', 'score', 'rank', 'tape_id']
        )
        .assign(
            total_points=lambda x: x['points'].fillna(0.0).sum(axis=1),
            total_score=lambda x: x['score'].fillna(0.0).sum(axis=1)
        )
        .sort_values(by='total_points', ascending=False)
        .swaplevel(axis=1)
        .sort_index(
            axis=1,
            kind='stable',
            key=lambda x: x.map(
                lambda y: title_order.index(y) if y in title_order else -1)
            )
    )
    pivoted.index.name = None
    pivoted.columns.names = [None, None]

    return pivoted


def compute_leaderboard(
    notices: list[Notice],
    contest_ids: list[str]
) -> pd.DataFrame:
    """
    Return the pivoted leaderboard based on a list of notices
    """

    df_notices = _dataframe_from_notices(notices)
    df_scores = _compute_contest_scores(df_notices=df_notices)
    df_pivoted = _pivot_scores(df_scores=df_scores, contest_ids=contest_ids)
    return df_pivoted
