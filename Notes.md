# Notes

This file will be used to track notes, things to do, and things to fix in the project (outside of the version history document).

- Currently, H% numbers in Event, line 25 (elif b_rand >= 50 and p_rand >= 50:) are incorrect
    - These numbers are adjusted for AVG, not H% (i.e. H/PA)

V0.1.0 Notes: Can I store game-time team information (like score, bat_ind, etc.) into a dictionary? Could help ease information retrieval. Think about implementing this in a future version.
V0.4.0 Notes: I am implementing this dictionary now. It will be put into the Game class and will prevent me from needing to call get_pitcher every at-bat (or even every half-inning)