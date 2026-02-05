from typing import List, Optional
from uuid import UUID
import psycopg2
from psycopg2.extras import RealDictCursor
from src.db.dataclass import PokerHand
import json

class PokerHandRepository:
    def __init__(self, conn):
        self.conn = conn

    def save(self, hand: PokerHand) -> PokerHand:
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO poker_hands (hand_id, winnings, actions, player_hands)
                VALUES (%s, %s, %s, %s)
                RETURNING created_at
                """,
                (
                    str(hand.hand_id),
                    json.dumps(hand.winnings),
                    hand.actions,
                    hand.player_hands
                )
            )
            created_at = cur.fetchone()[0]
            self.conn.commit()
            hand.created_at = created_at
            return hand

    def get_by_id(self, hand_id: UUID) -> Optional[PokerHand]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM poker_hands WHERE hand_id = %s", (str(hand_id),))
            row = cur.fetchone()
            if row:
                return PokerHand(
                    hand_id=UUID(row['hand_id']),
                    winnings=row['winnings'],
                    actions=row['actions'],
                    player_hands=row['player_hands'],
                    created_at=row['created_at']
                )
            return None

    def list_all(self) -> List[PokerHand]:
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute("SELECT * FROM poker_hands ORDER BY created_at DESC")
            rows = cur.fetchall()
            return [
                PokerHand(
                    hand_id=UUID(row['hand_id']),
                    winnings=row['winnings'],
                    actions=row['actions'],
                    player_hands=row['player_hands'],
                    created_at=row['created_at']
                )
                for row in rows
            ]
