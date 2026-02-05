from fastapi import APIRouter, HTTPException
from src.models.models import PlayerActionRequest, StartGameRequest
from src.services.game_state_manager import GameStateManager
from math import inf

router = APIRouter()

@router.post("/start/game", status_code=200)
def start_game(req: StartGameRequest):
    manager = GameStateManager.get_instance()
    state = manager.start_game(stack_size=req.stack_size)
    preflop_response = GameStateManager.get_instance().preflop_response()

    print(req)
    try:
        return {"message": "Hole cards dealt successfully", "cards": preflop_response}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to deal hole cards: {str(e)}")

@router.post("/action/fold")
def fold_action(req: PlayerActionRequest):
    manager = GameStateManager.get_instance()
    try:
        return manager.fold(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/action/check_or_call")
def check_or_call_action(req: PlayerActionRequest):
    manager = GameStateManager.get_instance()
    try:
        return manager.check_or_call(req.action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/action/complete_bet_or_raise_to")
def complete_bet_or_raise_to_action(req: PlayerActionRequest):
    manager = GameStateManager.get_instance()
    try:
        if req.amount is None:
            raise HTTPException(status_code=400, detail="Amount is required for betting or raising.")
        return manager.complete_bet_or_raise_to(req.action, req.amount)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Game state management in one endpoint
# @router.post("/action/player")
# def player_action(req: PlayerActionRequest):
#     manager = GameStateManager.get_instance()
#     state = manager.state

#     if state is None:
#         raise HTTPException(status_code=400, detail="Game not started.")

#     print(state.actor_indices, state.stacks)
#     try:
#         if req.action == "fold":
#             state.fold()

#         elif req.action == "check_or_call":
#             if not state.can_check_or_call():
#                 raise HTTPException(status_code=400, detail="Cannot check or call right now.")
#             state.check_or_call()

#         elif req.action == "complete_bet_or_raise_to":
#             if not state.can_complete_bet_or_raise_to():
#                 print(state.can_complete_bet_or_raise_to())
#                 raise HTTPException(status_code=400, detail="Cannot bet or raise right now.")
#             if req.amount is None:
#                 raise HTTPException(status_code=400, detail="Amount is required for betting or raising.")
#             state.complete_bet_or_raise_to(req.amount)

#         else:
#             raise HTTPException(status_code=400, detail="Invalid action.")

#         # Advance to next round if actor_indices is empty
#         if not state.actor_indices:
#             # Only deal next street if hand is still alive
#             if state.street_index == 1:
#                 state.burn_card()
#                 state.deal_board("3c4d5s")  # placeholder flop
#             elif state.street_index == 2:
#                 state.burn_card()
#                 state.deal_board("Kh")  # turn
#             elif state.street_index == 3:
#                 state.burn_card()
#                 state.deal_board("9d")  # river
#             elif state.street_index == None:
#                 raise HTTPException(status_code=400, detail="Game has ended.")

#         return {
#             # "next_actor": actor,
#             # "legal_actions": actions,
#             "indices": list(state.actor_indices),
#             "street_index": state.street_index,
#             "board": list(state.board_cards),
#             "status": state.status,
#             "bets": list(state.bets),
#             "stacks": list(state.stacks)
#         }

#     except Exception as e:
#         raise HTTPException(status_code=400, detail=f"Action failed: {str(e)}")