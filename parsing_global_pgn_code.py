import chess
import chess.pgn
import chess.engine

user_name="ParthMarathe" # provide the name of the user here 
#give path of lichess pgn file
path=r"C:\Users\kaush\Downloads\stockfish\stockfish\stockfish-windows-x86-64-avx2.exe"
user=user_name
threshold=150
pgn_file = open(r"C:\Users\kaush\Downloads\lichess_pgn_2025.12.04_jimpostak_vs_ParthMarathe.9CgPy4Lq.pgn",encoding="utf-8")
list_blunders=[]

game = chess.pgn.read_game(pgn_file)
engine = chess.engine.SimpleEngine.popen_uci(path)

while game is not None:
    board = game.board()
    if game.headers["White"]==user_name:
        i = 0 
        previous_eval = 0
        for move in game.mainline_moves():
            board.push(move)
            i += 1
            info = engine.analyse(board, chess.engine.Limit(depth=20))
            
            current_score_obj = info['score'].white().score(mate_score=10000)
            
            if i % 2 == 1: 
                current_eval = current_score_obj
                if previous_eval - current_eval >= threshold: 
                    board.pop()
                    list_blunders.append(board.fen())
                    board.push(move)
            else: 
                previous_eval = current_score_obj
    else: 
        i = 1 
        previous_eval = 0
        for move in game.mainline_moves():
            board.push(move)
            i += 1
            info = engine.analyse(board, chess.engine.Limit(depth=20))
            current_score_obj = info['score'].black().score(mate_score=10000)
            
            if i % 2 == 1: 
                current_eval = current_score_obj
                if previous_eval - current_eval >= threshold: 
                    board.pop()
                    mirrored_board = board.mirror()
                    list_blunders.append(mirrored_board.fen())
                    board.push(move)
            else: 
                previous_eval = current_score_obj
                
    game = chess.pgn.read_game(pgn_file)
            
print(list_blunders)
engine.quit()