[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/yutianqing579/tiny-chess-01/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/yutianqing579/tiny-chess-01/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

# tiny-chess-01 — a chess engine in 4,074 bytes of Python

An entry for make.fun's bounty **“Build the strongest chess engine in 4 KB of Python.”**

`main.py` is the whole engine (Python 3 standard library only, no other file
is read). It plays through the env at `MAKEFUN_ENV_URL`: the env serves the
game and the legal moves, the engine answers with a UCI move.

Inside the byte budget:

- 0x88-style 120-square board as a plain string; move generation for all
  pieces, pawn pushes/captures, en passant and queen promotions (castling and
  underpromotions are the documented simplifications — root moves are filtered
  against the env's own legal-move list, so every played move is legal).
- Negamax alpha-beta search with iterative deepening under a fixed node
  budget (7,000 nodes — never a clock, so the same position always gets the
  same move), quiescence search over captures and promotions, MVV-LVA move
  ordering.
- Evaluation: material (100/320/330/500/900) plus positional terms computed
  from file/rank geometry — pawn advancement and centre files, knight and
  bishop centrality, rook on the seventh, queen centrality, king shelter in
  the middlegame and king centrality in the endgame, bishop pair.

Move generation is verified against the standard perft counts from the
starting position (20 / 400 / 8,902 / 197,281).

Licensed under the MIT License.
