"""
03_indobert.py
==============
Step 3 — IndoBERT Neural Feature Extractor & Interface
Pipeline: Instagram Indonesia Viral Intelligence & Research Platform

Provides a production interface for IndoBERT (e.g., indobenchmark/indobert-base-p1).
Adheres strictly to the research rule:
- Checks local model cache/directory (models/indobert/).
- If model artifacts (config.json, weights) are not locally present,
  status is flagged as MISSING.
- Does NOT perform automatic massive background downloads during audits.
- Documents exact steps for fine-tuning or loading pre-trained weights.

Run:
    python src/03_indobert.py
    python -m src.03_indobert
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
REPO = Path(__file__).resolve().parent.parent
INDOBERT_DIR = REPO / "models" / "indobert"
OUT_STATUS_JSON = REPO / "output" / "indobert_status.json"


class IndoBERTInterface:
    """Interface for IndoBERT embeddings, sentiment classification, and tokenization."""

    MODEL_NAME = "indobenchmark/indobert-base-p1"

    def __init__(self, model_dir: Path | str | None = None) -> None:
        self.model_dir = Path(model_dir) if model_dir else INDOBERT_DIR
        self.tokenizer = None
        self.model = None

    def check_local_artifacts(self) -> dict[str, Any]:
        """Inspects if weights and tokenizer files exist locally."""
        if not self.model_dir.exists():
            return {
                "status": "MISSING",
                "exists": False,
                "path": str(self.model_dir),
                "artifacts_found": [],
                "reason": f"Directory '{self.model_dir}' does not exist.",
            }

        files = [f.name for f in self.model_dir.iterdir() if f.is_file() and not f.name.startswith(".")]
        expected = ["config.json", "pytorch_model.bin", "model.safetensors", "vocab.txt"]
        found = [f for f in files if any(exp in f for exp in expected)]

        has_weights = any("model" in f or "pytorch" in f or "safetensors" in f for f in files)
        has_config = any("config.json" in f for f in files)

        if has_weights and has_config:
            status = "AVAILABLE"
        elif files:
            status = "PARTIAL"
        else:
            status = "MISSING"

        return {
            "status": status,
            "exists": True,
            "path": str(self.model_dir),
            "files_count": len(files),
            "artifacts_found": files,
            "target_architecture": "indobenchmark/indobert-base-p1",
            "reason": (
                "Local model weights not found in models/indobert/. "
                "Automatic heavy downloads are disabled to preserve data fidelity."
                if status == "MISSING"
                else "Artifacts detected."
            ),
            "deployment_guide": (
                "To deploy IndoBERT: place fine-tuned weights or run offline checkpoint extraction "
                "into models/indobert/ with config.json and pytorch_model.bin / model.safetensors."
            ),
        }

    def load_model(self, allow_download: bool = False) -> bool:
        """Loads tokenizer and model. If allow_download is False, only checks local files."""
        artifacts = self.check_local_artifacts()
        if artifacts["status"] == "MISSING" and not allow_download:
            return False

        try:
            from transformers import AutoTokenizer, AutoModelForSequenceClassification  # type: ignore
            source = str(self.model_dir) if artifacts["status"] == "AVAILABLE" else self.MODEL_NAME
            self.tokenizer = AutoTokenizer.from_pretrained(source, local_files_only=not allow_download)
            self.model = AutoModelForSequenceClassification.from_pretrained(source, local_files_only=not allow_download)
            return True
        except Exception:
            return False

    def extract_features(self, texts: list[str]) -> dict[str, Any]:
        """Extracts contextual sentence representations or reports missing state."""
        artifacts = self.check_local_artifacts()
        if artifacts["status"] != "AVAILABLE" and self.model is None:
            return {
                "status": "MISSING",
                "embeddings": None,
                "message": "IndoBERT weights not loaded. Status is MISSING.",
            }

        # If model is loaded, compute embeddings
        import torch  # type: ignore
        inputs = self.tokenizer(texts, padding=True, truncation=True, max_length=128, return_tensors="pt")
        with torch.no_grad():
            outputs = self.model.bert(**inputs)
            cls_embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy().tolist()

        return {
            "status": "AVAILABLE",
            "embeddings": cls_embeddings,
            "dimension": len(cls_embeddings[0]) if cls_embeddings else 0,
        }


def run(verbose: bool = True) -> dict[str, Any]:
    """Executes the IndoBERT interface audit."""
    if verbose:
        print("=" * 60)
        print("03_indobert.py | IndoBERT Neural Interface & Status Audit")
        print("=" * 60)

    interface = IndoBERTInterface()
    audit = interface.check_local_artifacts()

    if verbose:
        print(f"[STATUS]     IndoBERT Status: {audit['status']}")
        print(f"[DIRECTORY]  {audit['path']}")
        print(f"[ARTIFACTS]  Files detected: {audit['artifacts_found']}")
        print(f"[REASON]     {audit['reason']}")
        print(f"[GUIDE]      {audit['deployment_guide']}")

    # Save status
    OUT_STATUS_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_STATUS_JSON, "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    if verbose:
        print(f"\n[SAVE] Status saved to {OUT_STATUS_JSON}")
        print(f"✓ 03_indobert.py complete (Status: {audit['status']})")

    return audit


if __name__ == "__main__":
    run(verbose=True)
