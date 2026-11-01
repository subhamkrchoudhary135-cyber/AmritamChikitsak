"""Script to train all Sanjivani AI models, calibrate probabilities, tune thresholds, and persist to cache."""

import logging
import sys
from pathlib import Path

# Ensure project root is in sys.path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core.audit import setup_structured_logging
from src.ml.registry import model_registry

logger = setup_structured_logging()


def main():
    logger.info("Starting complete model training pipeline for Sanjivani AI...")
    model_registry.train_and_cache_all(n_samples=3000)
    logger.info("Training complete. Artifacts successfully persisted to models_cache/.")

    # Print summary of trained models
    summary = model_registry.get_model_versions_info()
    for m in summary:
        logger.info(
            f"Model: {m.condition} | Algo: {m.algorithm} | Threshold: {m.decision_threshold:.3f} | Metrics: {m.metrics}"
        )


if __name__ == "__main__":
    main()
