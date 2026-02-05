from dataclasses import dataclass
from typing import Optional, List, Dict
from uuid import UUID, uuid4
from datetime import datetime

@dataclass
class PokerHand:
    hand_id: UUID
    winnings: Dict[str, int]
    actions: List[str]
    player_hands: List[str]
    created_at: Optional[datetime] = None
