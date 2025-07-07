# Notes

This file will be used to track notes, things to do, and things to fix in the project (outside of the version history document).

- Currently, H% numbers in Event, line 25 (elif b_rand >= 50 and p_rand >= 50:) are incorrect
    - These numbers are adjusted for AVG, not H% (i.e. H/PA)

Resolved - V0.1.0 Notes: Can I store game-time team information (like score, bat_ind, etc.) into a dictionary? Could help ease information retrieval. Think about implementing this in a future version.
Resolved - V0.4.0 Notes: I am implementing this dictionary now. It will be put into the Game class and will prevent me from needing to call get_pitcher every at-bat (or even every half-inning)
V0.5.0 Notes: I might need to brush up on some "official rulings" in regards to how groundouts, air outs, etc. get counted
V0.6.0 Notes: Should I completely abolish the hitter/pitcher viewpoint? What's stopping any pitcher from hitting (or position players from pitching)?
Is there a way that I can combine the single/double/triple/homerun methods and/or the groundout/airout/strikeout methods? They share a lot of the same accumulation methods and could do something similar to the gidp function in Events
Resolved - V0.7.0 Notes: I will need a more official Menu class as opposed to the loop that is currently implemented in the Game class. For now, the loop functions fine since there are only two teams playing