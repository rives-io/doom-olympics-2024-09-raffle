# DOOM Olympics 2024-09 Raffle

The September 2024 [DOOM Olympics](https://rives.io/blog/doom-olympics) was the event that marked the launch of [Rives](https://rives.io) on Base Mainnet. A series of seven contests were created between September 12th and 19th challenging different aspects of playing DOOM, in a verifiable manner.

By participating in these events, the players can win prizes, including a sum that will be distributed among the players in the Global Leaderboard. This repository contains the code for selecting the raffle participants and perform the distribution of points, for reproducibility and auditing purposes.

## Eligibility and How to Enter

You are eligible for by submitting tapes and earning certain achievements during the DOOM Olympics. Here are the conditions for entering and the number of tickets earned.

- Members of the Rives and Cartesi staff and their immediate family are **not** eligible.
- After removing non-eligible players, the remaining participants will enter the raffle.
- The number of tickets in the raffle is the number of achievements earned by the players across all of the seven DOOM Olympic contests. The valid achievements for this raffle are:
  - Tape Creator: the player earns this achievement by submitting a tape to DOOM Olympics. Rewarded only for the first tape
  - DOOM Olympian: the player has submitted a tape for a contest of DOOM Olympics. This achievement is rewarded only once, regardless of the number of tapes submitted
  - Contest Participants: the player has submitted a tape for a contest of DOOM Olympics. This achievement is rewarded only once, regardless of the number of tapes submitted
  - Contest Gold: the player earns this achievement if he ranked 1st in any of the DOOM Olympics contests
  - Contest Silver: the player earns this achievement if he ranked 2nd in any of the DOOM Olympics contests
  - Contest Bronze: the player earns this achievement if he ranked 3rd in any of the DOOM Olympics contests
  - DOOM Olympics Global Gold: the player earns this achievement if he ranked 1st in the Global Leaderboard
  - DOOM Olympics Global Silver: the player earns this achievement if he ranked 2nd in the Global Leaderboard
  - DOOM Olympics Global Bronze: the player earns this achievement if he ranked 3rd in the Global Leaderboard
  - DOOM Olympics Completionist: the player earns this achievement if he submitted a tape to all 7 contests of DOOM Olympics
  - DOOM Olympics Top 100: the player earns this achievement if he was in the top 100 in the Global Leaderboard

The script get_participants.py will generate a JSON file containing a list of participants and how many tickets each one earned.

## Drawing

The winners will be drawn with the following procedure:

- A random number will be generated and registered on chain
- This random number will be the seed for a Mersenne Twister pseudo-random number generator (pRNG).
- The pRNG will be used to draw 100 players, without replacement, and with probabilities proportional to the number of tickets.

The script draw_winners.py will read the previously generated JSON file and output another JSON file with the winners.
