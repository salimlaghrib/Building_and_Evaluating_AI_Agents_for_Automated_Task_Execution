from datetime import datetime

from app.models.order import Order,OrderStatus
from app.models.extracted_order import ExtractedOrder

from app.graph.workflowStatus import WorkflowStatus
from app.services.human_validation_service import HumanValidationService

def create_valid_order()->Order:
    """
    Returns a valid business order
    """
    return Order(
        client_name="Salim",
        phone="0688784609",
        email="laghribsalim@gmail.com",
        product="Matelas",
        quantity=2,
        height=20,
        length=100,
        width=200,
        status=OrderStatus.READY_FOR_VALIDATION,
        created_at=datetime.now()
    )

def create_valid_extracted_order() -> ExtractedOrder:
    """
    Returns a valid AI extraction.
    """

    return ExtractedOrder(
        client_name="Salim",
        product="Matelas",
        length=100,
        width=200,
        height=20,
        quantity=2,
        confidence=0.98,
    )
# ======================================================
# VALID ORDER
# ======================================================

def test_validate_success():

    order = create_valid_order()
    extracted = create_valid_extracted_order()

    validation_required, status, comment = (
        HumanValidationService.validate(
            order,
            extracted,
        )
    )

    assert validation_required is False
    assert status == WorkflowStatus.VALIDATED
    assert comment is None

# ======================================================
# MISSING PRODUCT
# ======================================================

def test_missing_product():

    order = create_valid_order()
    order.product = None

    extracted = create_valid_extracted_order()

    validation_required, status, comment = (
        HumanValidationService.validate(
            order,
            extracted,
        )
    )

    assert validation_required is True
    assert status == WorkflowStatus.WAITING_HUMAN_VALIDATION
    assert comment == "Product is missing."

# ======================================================
# MISSING WIDTH
# ======================================================

def test_missing_width():

    order = create_valid_order()
    order.width = None

    extracted = create_valid_extracted_order()

    validation_required, status, comment = (
        HumanValidationService.validate(
            order,
            extracted,
        )
    )

    assert validation_required is True
    assert status == WorkflowStatus.WAITING_HUMAN_VALIDATION
    assert comment == "Width is missing."

# ======================================================
# INVALID QUANTITY
# ======================================================

def test_invalid_quantity():

    order = create_valid_order()
    order.quantity = 0

    extracted = create_valid_extracted_order()

    validation_required, status, comment = (
        HumanValidationService.validate(
            order,
            extracted,
        )
    )

    assert validation_required is True
    assert status == WorkflowStatus.WAITING_HUMAN_VALIDATION
    assert comment == "Invalid quantity."

# ======================================================
# LOW CONFIDENCE
# ======================================================

def test_low_confidence():

    order = create_valid_order()

    extracted = create_valid_extracted_order()
    extracted.confidence = 0.45

    validation_required, status, comment = (
        HumanValidationService.validate(
            order,
            extracted,
        )
    )

    assert validation_required is True
    assert status == WorkflowStatus.WAITING_HUMAN_VALIDATION
    assert comment == "Low confidence."