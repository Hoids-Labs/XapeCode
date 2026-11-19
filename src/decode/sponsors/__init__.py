"""B2B sponsorship and developer-focused monetization module.

Provides non-intrusive, privacy-preserving sponsor rotation in the CLI status spinner
during thinking and executing states.
"""

from xape.sponsors.client import SponsorClient
from xape.sponsors.config import get_anonymized_metadata, is_sponsors_enabled
from xape.sponsors.hook import SponsorStateMachineHook
from xape.sponsors.rotator import SponsorRotator
from xape.sponsors.types import ClientMetadata, HarnessState, SponsorCampaign

__all__ = [
    "ClientMetadata",
    "HarnessState",
    "SponsorCampaign",
    "SponsorClient",
    "SponsorRotator",
    "SponsorStateMachineHook",
    "get_anonymized_metadata",
    "is_sponsors_enabled",
]
