#!/usr/bin/env python
import hashlib
import json
from pathlib import Path
from typing_extensions import Annotated
import zlib

import pandas as pd
import numpy as np
import typer


def main(
    filename: Annotated[
        Path,
        typer.Argument(
            help='Raffle entries JSON file',
            exists=True,
            dir_okay=False,
            readable=True,
        )
    ],
    seed: Annotated[
        str,
        typer.Argument(
            help='Seed for the pRNG. This must have been generated securely.',
        )
    ],
    n_winners: Annotated[
        int,
        typer.Option(
            help='Number of winners to be selected',
            min=1,
        )
    ] = 100,
    winners_filename: Annotated[
        Path | None,
        typer.Option(
            help='Output JSON file with the winners',
            exists=False,
            dir_okay=False,
            writable=True,
        )
    ] = None,
):
    df = pd.read_json(filename)

    with filename.open('rb') as fin:
        file_hash = hashlib.sha256(fin.read()).hexdigest()

    population = df['user_address'].values
    weights = df['count'].values
    prob = weights / weights.sum()

    seed_crc = zlib.crc32(seed.encode())
    print(seed_crc)

    prng = np.random.RandomState(seed_crc)
    prng

    winners = prng.choice(population, p=prob, size=n_winners, replace=False)
    winners = winners.tolist()

    output_data = {
        'input_file_sha256': file_hash,
        'seed': seed,
        'winners': winners
    }

    if winners_filename is None:
        winners_filename = filename.parent / (filename.stem + '_winners.json')

    if winners_filename.exists():
        print(f'File {str(winners_filename)} already exists.')
        raise typer.Abort()

    print(f"Generating report on {str(winners_filename)}")

    with winners_filename.open('w') as fout:
        json.dump(output_data, fout, indent=4)


if __name__ == '__main__':
    typer.run(main)
