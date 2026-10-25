"""Análise de sinais; implementação organizada após os experimentos históricos."""
from dataclasses import dataclass
from pathlib import Path
import math
import re
import statistics

import pandas as pd

POTENTIAL = 'Potential applied (V)'
CURRENT = 'WE(1).δ.Current (A)'


def _finite(values, name):
    result = [float(v) for v in values]
    if not result or not all(math.isfinite(v) for v in result):
        raise ValueError(f'{name}: esperada sequência não vazia de números finitos.')
    return result


def read_signal(path, x_column=POTENTIAL, y_column=CURRENT, encoding='utf-8-sig'):
    """Lê CSV ou XLSX, preservando os pares x/y. Não sobrescreve a entrada."""
    path = Path(path)
    if path.suffix.lower() == '.xlsx':
        frame = pd.read_excel(path)
    elif path.suffix.lower() == '.csv':
        frame = pd.read_csv(path, encoding=encoding)
    else:
        raise ValueError('Formato esperado: .csv ou .xlsx.')
    missing = {x_column, y_column} - set(frame.columns)
    if missing:
        raise ValueError(f'Colunas ausentes em {path.name}: {sorted(missing)}')
    x = _finite(frame[x_column], x_column)
    y = _finite(frame[y_column], y_column)
    return pd.DataFrame({'x': x, 'signal': y})


def consolidate_signals(paths, **read_options):
    """Une sinais apenas se as grades de x coincidirem, sem alinhamento implícito por índice."""
    paths = sorted(map(Path, paths), key=lambda p: p.name)
    if not paths:
        raise ValueError('Nenhum arquivo de entrada.')
    names = [p.stem for p in paths]
    if len(set(names)) != len(names):
        raise ValueError('Nomes de amostra duplicados.')
    reference = None
    result = None
    for path in paths:
        frame = read_signal(path, **read_options)
        grid = frame['x'].tolist()
        if reference is None:
            reference = grid
            result = pd.DataFrame({'x': grid})
        elif len(grid) != len(reference) or any(
            not math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-12)
            for a, b in zip(reference, grid)
        ):
            raise ValueError(f'Grade de x incompatível: {path.name}. Alinhe explicitamente antes de unir.')
        result[path.stem] = frame['signal'].to_numpy()
    return result


def signal_peak(x, y, lower=None, upper=None):
    """Máximo observado em uma janela explícita; não aplica suavização."""
    x, y = _finite(x, 'x'), _finite(y, 'y')
    if len(x) != len(y):
        raise ValueError('x e y devem ter o mesmo tamanho.')
    if lower is not None and not math.isfinite(lower):
        raise ValueError('Limite inferior não finito.')
    if upper is not None and not math.isfinite(upper):
        raise ValueError('Limite superior não finito.')
    if lower is not None and upper is not None and lower > upper:
        raise ValueError('Janela invertida.')
    pairs = [(a, b) for a, b in zip(x, y)
             if (lower is None or a >= lower) and (upper is None or a <= upper)]
    if not pairs:
        raise ValueError('A janela não contém observações.')
    return max(pairs, key=lambda pair: pair[1])


def subtract_signals(x_reference, y_reference, x_sample, y_sample):
    """Retorna amostra - referência, sem ordenar x e y separadamente."""
    xr, yr = _finite(x_reference, 'x_reference'), _finite(y_reference, 'y_reference')
    xs, ys = _finite(x_sample, 'x_sample'), _finite(y_sample, 'y_sample')
    if not (len(xr) == len(yr) == len(xs) == len(ys)):
        raise ValueError('Os sinais precisam ter o mesmo tamanho.')
    pairs = sorted(zip(xr, yr, xs, ys))
    if len(set(xr)) != len(xr):
        raise ValueError('Grade duplicada; selecione uma varredura antes da subtração.')
    if any(not math.isclose(a, c, rel_tol=1e-9, abs_tol=1e-12) for a, _, c, _ in pairs):
        raise ValueError('As grades de x devem coincidir na mesma ordem.')
    return [a for a, _, _, _ in pairs], [d-b for _, b, _, d in pairs]


@dataclass(frozen=True)
class Calibration:
    slope: float
    intercept: float
    r_squared: float | None
    rmse: float
    n: int
    concentration_min: float
    concentration_max: float

    def estimate(self, signal, allow_extrapolation=False):
        if self.slope == 0:
            raise ValueError('Inclinação nula: curva não invertível.')
        signal = _finite([signal], 'signal')[0]
        concentration = (signal - self.intercept) / self.slope
        if not allow_extrapolation and not self.concentration_min <= concentration <= self.concentration_max:
            raise ValueError('Estimativa fora da faixa de calibração.')
        return concentration


def fit_calibration(concentrations, signals):
    """OLS sinal = inclinação * concentração + intercepto; R² é ajuste, não validação externa."""
    x, y = _finite(concentrations, 'concentrations'), _finite(signals, 'signals')
    if len(x) != len(y) or len(x) < 3:
        raise ValueError('São necessários pelo menos três pares concentração/sinal.')
    xm, ym = statistics.mean(x), statistics.mean(y)
    sxx = sum((v-xm)**2 for v in x)
    if sxx == 0:
        raise ValueError('As concentrações devem variar.')
    slope = sum((a-xm)*(b-ym) for a, b in zip(x, y)) / sxx
    intercept = ym - slope*xm
    residual = sum((b-(slope*a+intercept))**2 for a, b in zip(x, y))
    total = sum((b-ym)**2 for b in y)
    return Calibration(slope, intercept, None if total == 0 else 1-residual/total,
                       math.sqrt(residual/len(x)), len(x), min(x), max(x))


def parse_sample_name(stem):
    """Formato explícito COMPOSTO-10uM; rejeita mistura de unidades no fluxo chamador."""
    match = re.fullmatch(r'(?P<analyte>[\w]+)-(?P<concentration>\d+(?:\.\d+)?)(?P<unit>[a-zA-Zµμ]+)', stem)
    if not match:
        raise ValueError(f'Nome inválido: {stem}. Esperado COMPOSTO-10uM.')
    return match['analyte'], float(match['concentration']), match['unit']
