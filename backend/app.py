from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from bingo_game import BingoGame

app = FastAPI()
game = BingoGame()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:3000", "http://localhost:3000"],  # React URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the BINGO game API!"}

@app.post("/join/{player_id}")
def join_game(player_id: int):
    board = game.add_player(player_id)
    if board:
        return {"status": "success", "board": board}
    return {"status": "error", "message": "Player already joined."}

@app.post("/mark/{player_id}/{number}")
def mark_number(player_id: int, number: int):
    if game.mark_number(player_id, number):
        if game.check_bingo(player_id):
            return {"status": "success", "message": "BINGO!"}
        return {"status": "success", "message": f"Number {number} marked."}
    return {"status": "error", "message": "Number not found on board."}
