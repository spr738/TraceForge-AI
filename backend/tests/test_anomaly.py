from app.detection.anomaly import detect_anomaly


def test_detector_waits_for_minimum_history():
    result = detect_anomaly([10, 11, 9, 10], 80)
    assert result.is_anomaly is False


def test_detector_flags_large_deviation():
    history = [100, 101, 99, 100, 102, 98, 101, 99, 100, 100]
    result = detect_anomaly(history, 180, min_samples=8, z_threshold=3.0)
    assert result.is_anomaly is True
    assert result.baseline == 100.0
