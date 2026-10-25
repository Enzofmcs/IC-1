"""Recalcula a série VIN fornecida, preservando os rótulos nmol dos arquivos."""
import argparse
from dataclasses import asdict
import json
from pathlib import Path

import pandas as pd
from .analysis import consolidate_signals, fit_calibration, parse_sample_name, signal_peak

LOWER_POTENTIAL = -0.025177002


def analyze_vincristine(folder):
    """Aplica a janela histórica de B01 aos seis sinais transcritos de XLSX."""
    folder = Path(folder)
    paths = list(folder.glob('VIN-*.csv'))
    if len(paths) != 6:
        raise ValueError('Esperados seis arquivos VIN para a série histórica fornecida.')
    signals = consolidate_signals(paths)
    selected = signals.loc[signals.x >= LOWER_POTENTIAL].reset_index(drop=True)
    peaks = []
    for name in signals.columns[1:]:
        analyte, amount, unit = parse_sample_name(name)
        if analyte != 'VIN' or unit != 'nmol':
            raise ValueError('Série deve usar exclusivamente os rótulos VIN-nmol.')
        x, y = signal_peak(signals.x, signals[name], lower=LOWER_POTENTIAL)
        peaks.append({'sample':name, 'amount_label_nmol':amount,
                      'peak_potential_V':x, 'peak_current_A':y})
    peaks = pd.DataFrame(peaks).sort_values('amount_label_nmol').reset_index(drop=True)
    selected = selected[['x', *peaks['sample'].tolist()]]
    fit = asdict(fit_calibration(peaks.amount_label_nmol, peaks.peak_current_A))
    fit['amount_label_min_nmol'] = fit.pop('concentration_min')
    fit['amount_label_max_nmol'] = fit.pop('concentration_max')
    report = {'analyte_label':'VIN', 'x_variable':'amount_label_nmol', 'y_variable':'peak_current_A',
              'window':{'lower_potential_V':LOWER_POTENTIAL,'upper_potential_V':None},
              'source_rows_per_signal':len(signals), 'selected_rows_per_signal':len(selected),
              'fit':fit, 'historical_B01_R2_rounded':0.985,
              'matches_recorded_R2_at_three_decimals':round(fit['r_squared'],3)==0.985,
              'limitations':[
                  'nmol é o rótulo de quantidade dos arquivos; sem volume não foi convertido em concentração.',
                  'Há uma série por rótulo; não foram fornecidas réplicas independentes para este ajuste.',
                  'R² descreve o ajuste aos seis pontos e não estabelece LOD, LOQ ou validação externa.',
              ]}
    return selected, peaks, report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data',type=Path,default=Path('data/source_tables/vincristine'))
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if args.output.exists():
        parser.error('Escolha uma pasta de saída nova.')
    signals, peaks, report = analyze_vincristine(args.data)
    args.output.mkdir(parents=True)
    signals.to_csv(args.output/'signals_in_window.csv',index=False,float_format='%.17g')
    peaks.to_csv(args.output/'peaks.csv',index=False,float_format='%.17g')
    (args.output/'fit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False))


if __name__ == '__main__':
    main()
