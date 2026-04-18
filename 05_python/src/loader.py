import json
import os


def load_json(filepath: str) -> dict:
    """
    Loads a JSON file and returns it as a Python dictionary.
    Used to load controls, vendor responses, and SAQ data.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Data file not found: {filepath}")

    with open(filepath, "r") as f:
        return json.load(f)


def load_controls(base_path: str = "data") -> list:
    """Loads the ISO 27001 controls catalog."""
    data = load_json(os.path.join(base_path, "controls.json"))
    return data["controls"]


def load_vendor_responses(base_path: str = "data") -> dict:
    """Loads vendor scored responses."""
    return load_json(os.path.join(base_path, "vendor_responses.json"))


def load_saq_responses(base_path: str = "data") -> dict:
    """Loads SAQ questionnaire responses."""
    return load_json(os.path.join(base_path, "saq_responses.json"))