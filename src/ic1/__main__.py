import argparse
from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd
from .analysis import fit_calibration


def main():
    parser = argparse.ArgumentParser(description='Ajusta sinal = a * concentração + b a um CSV de pares.')
    parser.add_argument('csv', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('O arquivo de saída já existe; escolha outro nome.')
    frame = pd.read_csv(args.csv)
    if not {'concentration', 'signal'} <= set(frame.columns):
        parser.error('CSV deve conter concentration e signal.')
    result = asdict(fit_calibration(frame.concentration, frame.signal))
    result['source'] = args.csv.name
    result['note'] = 'Ajuste aos pares fornecidos; não estabelece LOD, LOQ ou validação independente.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, allow_nan=False)+'\n', encoding='utf-8')
    print(json.dumps(result, indent=2, allow_nan=False))


if __name__ == '__main__':
    main()
