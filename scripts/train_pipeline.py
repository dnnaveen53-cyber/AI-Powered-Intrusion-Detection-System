from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.training.model_trainer import train_model_from_dataset
from src.utils.logger import setup_logging

logger = setup_logging("train_pipeline")


if __name__ == "__main__":
    logger.info("Starting training pipeline")
    metrics = train_model_from_dataset()
    logger.info("Training pipeline complete")
    print("Training complete.")
    print(metrics)
