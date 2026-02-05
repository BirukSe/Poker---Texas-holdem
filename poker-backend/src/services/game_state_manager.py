import random
from uuid import uuid4
from pokerkit import Automation, NoLimitTexasHoldem
from typing import List, Optional
from src.models.models import PreflopResponse, GameStateResponse

class GameStateManager:
    _instance = None

    def __init__(self):
        self.state: Optional[NoLimitTexasHoldem] = None
        self.hand_id: Optional[str] = uuid4()
        self.winnings : Optional[dict] = 0  # Total winnings for the hand
        self.actions : List[str] = []
        self.player_hands: List[str] = []

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def start_game(self, stack_size: int, num_players: int = 6):
        """
        Initializes the game state with the given stack size and number of players.
        Args:
            stack_size (int): The initial stack size for each player.
            num_players (int): The number of players in the game.
            Returns:
            
            NoLimitTexasHoldem: The initialized game state.
        """

        self.state = NoLimitTexasHoldem.create_state(
            (
                Automation.BET_COLLECTION,
                Automation.BLIND_OR_STRADDLE_POSTING,
                Automation.HOLE_CARDS_SHOWING_OR_MUCKING,
                Automation.HAND_KILLING,
                Automation.CHIPS_PUSHING,
                Automation.CHIPS_PULLING,
            ),
            True,  # Uniform antes
            0,     # No ante
            (20, 40),  # SB/BB
            80,    # Min-bet
            tuple([stack_size] * num_players),
            num_players
        )
        return self.state

    def generate_unique_hole_cards(self, num_players: int = 6) -> list[str]:
        """
        Generates unique hole cards for each player.
        Args:
            num_players (int): The number of players in the game.
        Returns:
            list[str]: A list of unique hole cards for each player.
        """

        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A']
        suits = ['c', 'd', 'h', 's']
        full_deck = [rank + suit for rank in ranks for suit in suits]
        print(f"full_deck: {full_deck}")
        random.shuffle(full_deck)

        hole_cards = []
        for _ in range(num_players):
            card1 = full_deck.pop()
            card2 = full_deck.pop()
            hole_cards.append(card1 + card2)
        
        print("hh", hole_cards)
        return hole_cards
    
    def deal_flop(self):
        """
        Deals the flop by burning a card and dealing 3 cards to the board.
        Raises:
            Exception: If the game has not started or if the state is None.
        """
        if self.state is None:
            raise Exception("Game not started.")
        self.state.burn_card()
        return self.state.deal_board()  # Deals 3 cards for the flop

    def deal_turn(self):
        """
        Deals the turn by burning a card and dealing 1 card to the board.
        Raises:
            Exception: If the game has not started or if the state is None.
        """
        if self.state is None:
            raise Exception("Game not started.")
        self.state.burn_card()
        return self.state.deal_board()  # Deals 1 card for the turn

    def deal_river(self):
        if self.state is None:
            raise Exception("Game not started.")
        self.state.burn_card()
        return self.state.deal_board()  # Deals 1 card for the river

    def card_formatter(self, cards: tuple[str]) -> str:
        return ''.join(cards)

    def fold(self, action:str):
        if self.state is None:
            raise Exception("Game not started.")
        if not self.state.can_fold():
            raise Exception("Cannot fold right now.")
        self.state.fold()
        self.actions.append(f"{action}:")
        return self.advance_game_state()

    def check_or_call(self, action:str):
        if self.state is None:
            raise Exception("Game not started.")
        try:
            self.state.check_or_call()
            self.actions.append(f"{action}:")
        except ValueError as e:
            raise Exception(f"Cannot check or call: {str(e)}")
        
        return self.advance_game_state()

    def complete_bet_or_raise_to(self, action: str, amount: int):
        if self.state is None:
            raise Exception("Game not started.")
        if not self.state.can_complete_bet_or_raise_to():
            raise Exception("Cannot bet or raise right now.")

        try:
            self.state.complete_bet_or_raise_to(amount)
            if action == "allin":
                self.actions.append(f"{action}:")
            else:
                self.actions.append(f"{action}{amount}")
        except ValueError as e:
            raise Exception(f"Cannot complete bet or raise to {amount}: {str(e)}")

        return self.advance_game_state()


    def preflop_response(self):
        """
        Deals hole cards to players and returns the preflop response.
        Returns:
            PreflopResponse: Contains indices of small blind, big blind, dealer, and the dealt hole cards.
        """

        num_players = 6
        hole_cards = self.generate_unique_hole_cards(num_players)
        self.actions = hole_cards
        if self.state is None:
            raise Exception("Game state is not initialized")

        for cards in hole_cards:
            self.state.deal_hole(cards)

        actor_indices = self.state.actor_indices
        first_actor = actor_indices[0]
        dealer_index = (first_actor - 2) % num_players
        small_blind_index = (dealer_index + 1) % num_players
        big_blind_index = (dealer_index + 2) % num_players

        preflop_dealings = hole_cards

        print(f"Dealer index: {dealer_index}, Small blind index: {small_blind_index}, Big blind index: {big_blind_index}")
        print(f"Preflop dealings: {preflop_dealings}")
        print(type(preflop_dealings[0]))

        return PreflopResponse(
            small_blind_index=small_blind_index,
            big_blind_index=big_blind_index,
            dealer_index=dealer_index,
            preflop_dealings=preflop_dealings
        )
    
    def advance_game_state(self) -> GameStateResponse:
        """
        Advances the game state to the next round if applicable.
        Returns:
            GameStateResponse: The current game state after advancing.
        """
        is_round_changed = False
        if self.state is None:
            raise Exception("Game not started.")

        if not self.state.actor_indices:
            if self.state.street_index is not None:
                public_card = None
                if self.state.street_index == 1:
                    public_card = self.deal_flop()
                elif self.state.street_index == 2:
                    public_card = self.deal_turn()
                elif self.state.street_index == 3:
                    public_card = self.deal_river()
                is_round_changed = True
                card_str = self.card_formatter(public_card.cards)
                self.actions.append(f" {card_str} ")
            else:
                raise Exception("Game has ended.")

        return GameStateResponse(
            indices=list(self.state.actor_indices),
            is_round_changed=is_round_changed,
            street_index=self.state.street_index,
            board=list(self.state.board_cards),
            status=str(self.state.status),
            bets=list(self.state.bets),
            stacks=list(self.state.stacks)
        )
