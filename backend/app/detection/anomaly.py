from dataclasses import dataclass
import numpy as np


@dataclass
class DetectionResult:
    is_anomaly: bool
    baseline: float
    standard_deviation: float
    z_score: float


def detect_anomaly(
    history: list[float],
    current_value: float,
    min_samples: int = 8,
    z_threshold: float = 3.0,
) -> DetectionResult:
    if len(history) < min_samples:
        baseline = float(np.mean(history)) if history else float(current_value)
        return DetectionResult(False, baseline, 0.0, 0.0)

    values = np.asarray(history, dtype=float)
    baseline = float(np.mean(values))
    deviation = float(np.std(values))

    if deviation < 1e-9:
        is_anomaly = abs(current_value - baseline) > max(abs(baseline) * 0.25, 1.0)
        z_score = 0.0 if not is_anomaly else float("inf")
    else:
        z_score = abs(float(current_value) - baseline) / deviation
        is_anomaly = z_score >= z_threshold

    return DetectionResult(is_anomaly, baseline, deviation, z_score)
