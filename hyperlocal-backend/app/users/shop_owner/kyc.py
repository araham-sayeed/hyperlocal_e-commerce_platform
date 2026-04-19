"""KYC stubs — integrate UIDAI-compliant vendor before production."""


def verify_aadhaar_stub(aadhaar_last_four: str, full_name: str) -> dict:
    if len(aadhaar_last_four) != 4 or not aadhaar_last_four.isdigit():
        return {"verified": False, "reason": "Invalid last four digits"}
    return {"verified": True, "reference": f"KYC-DEMO-{aadhaar_last_four}", "name_match": True}
