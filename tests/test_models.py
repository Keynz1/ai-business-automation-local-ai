from models import BusinessRequest, ProcessedRequest, normalize_payload


def test_normalize_payload_defaults_and_priority():
    item = normalize_payload({"customer_name": "Ada", "priority": "URGENT"})
    assert isinstance(item, BusinessRequest)
    assert item.customer_name == "Ada"
    assert item.priority == "urgent"
    assert item.company == "Unknown"
    assert item.email == ""
    assert item.request_type == "general"
    assert item.confidence == 0.0


def test_missing_fields_produce_valid_request():
    item = normalize_payload({})
    assert item.customer_name == "Unknown"
    assert item.summary == "No summary provided"
    assert item.requested_action == "Review request"


def test_unknown_priority_becomes_normal():
    item = normalize_payload({"priority": "banana"})
    assert item.priority == "normal"


def test_empty_email_is_preserved():
    item = normalize_payload({"email": ""})
    assert item.email == ""


def test_processed_request_contains_spec_fields():
    base = normalize_payload({})
    item = ProcessedRequest.from_business_request(
        base,
        api_status="demo-local",
        response_text="Thanks",
        processing_status="processed",
    )
    assert item.api_status == "demo-local"
    assert item.response_text == "Thanks"
    assert item.processing_status == "processed"
    assert item.request_id
    assert item.received_at
