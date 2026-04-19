def verify_rider_documents(aadhaar_last_four: str, reason: str) -> dict:
    if len(aadhaar_last_four) != 4 or not aadhaar_last_four.isdigit():
        return {"ok": False, "message": "Invalid Aadhaar last four"}
    if len(reason.strip()) < 10:
        return {"ok": False, "message": "Please provide a clearer reason to join (min 10 chars)"}
    return {"ok": True, "reference": f"RIDER-KYC-{aadhaar_last_four}"}
