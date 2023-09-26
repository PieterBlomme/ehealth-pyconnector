import logging
from typing import List, Dict

logger = logging.getLogger(__name__)

def get_existing_agreements(token, eagreement_service, patient) -> Dict[str, List[str]]:
    response = eagreement_service.consult_agreement(
        token=token,
        input_model=patient
    )
    bundle = [e.resource.bundle for e in response.response.entry if e.resource.bundle is not None]
    assert len(bundle) == 1
    bundle = bundle[0]
    claim_response = [e.resource.claim_response for e in bundle.entry if e.resource.claim_response is not None]
    existing_agreements = {}
    for c in claim_response:
        if c.status.value != "active":
            logger.info(f"Status {c.status.value} != 'active'")
            continue
        code = c.add_item.product_or_service.coding.code.value
        if c.add_item.adjudication.category.coding.code.value != "agreement":
            logger.info(f"Adjudication {c.add_item.adjudication.category.coding.code.value} for {code} != 'agreement' for {c.pre_auth_ref.value}")

        existing_agreements[code] = existing_agreements.get(code, []) + [c.pre_auth_ref.value]
    return existing_agreements