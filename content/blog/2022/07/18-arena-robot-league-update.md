---
Title: Arena Robot League Design Update
categories: [games]
Date: "2022-07-18"
Tags:
- game-design
Series: Bot Builders
---

Since my [last post], I've made a lot of progress on Arena Robot League!

I had to take a break for the first few months of the year, due to the FIRST build season consuming most of my time.
But once that was done, I had a bunch of time that I could devote to design.

I signed up to participate in [Protospiel Online], which is an online prototype playtesting convention.
In addition to trying some really fun concepts, I put my design out for more testing.

Some of the mechanics that I had tried worked well. Others needed some adjustment.
The first large issue that I noticed, was that Skill cards still ended up being not particularly helpful.
Student cards did everything a skill card does, and more.
With that in mind, I tried several variations, settling on eliminating skill cards entirely.
Players would draft cards from the central market ("The School") into their hand, and as a later action they could Recruit a student to their workshop.
After some testing, this felt like too many steps. The players were using two of their precious actions just for recruiting.
One tester suggested an idea that really helped make the team side of the game feel more cohesive - get rid of player hands.
This simple change fixed numerous issues.
Because there was no hand, players recruited directly from the school, using only one action.
This left more actions for robot development.
This change also meant that players couldn't use cards from their hand to assist actions.
This placed a greater emphasis on teamwork and resource management, since now you were limited by the students in your workshop.
These two changes together made the team aspect feel more cohesive and like every decision mattered.

I continued looking at recruiting to see how it could be adjusted.
I noticed in a play session that the player could spend several rounds only recruiting and building up a large workshop, then take a ton of actions in later rounds.
To mitigate this, I made a few additional changes.
First, I gave the players one additional Freshman card at the beginning of the game.
With a total of three students, the need to recruit in the beginning was reduced.
Second, I changed recruiting to be an action that only some students can take.
This helped reduce the chances of exponential growth in team size.
With these changes, team size felt important without feeling limited.
In testing so far, players have typically ended up with five to seven students, which means a sizeable number of actions per round.

Now that the student cards were in a much better place, I could turn my attention to the robot cards.
After all, what use is a team if there's nothing for them to make?
The biggest issue I had with robot cards is that actually scoring didn't feel interesting.
Each time the player scored, they would move a cube down a card.
That didn't have any suspense or intrigue, and felt very rote.
This also severely limited the number of abilities that I could come up with.
I tried a few approaches, but nothing seemed to really stick.
Finally, I was reading a book that talked about suspense, when it hit me.

I added dice.

After this change, every subsystem on the robot would add an ability, a die to the player's pool, or both.
When the player pilots a robot using a student, they roll all the dice, then use any robot abilities.
These abilities allow for rerolling die, mitigating failure, and boosting success.

As a bonus, this helped solve the interaction problem I was running into.
Some subsystems have the `Block` ability.
These now allow the player to give an opponent a Block Die - a black die with "cancel" symbols on it.
When a player pilots and has block die in front of them, they have to roll it as well, and it cancels out some number of symbols if it rolls well - or poorly, for that player.
This definitely felt a lot more suspenseful than the previous setup, and allowed some variability.

The last major change I've made is an improvement on the piloting score system.
Near the beginning of 2022 I had a rule where students could only pilot something if the number of subsystems was less than their pilot score.
This was alright, but ran into confusion quickly.
Did the subsystem on the chassis card count? I didn't intend it to.
So I replaced it with a mechanic that seems to work better - the Memory system.
Each subsystem and chassis now has a memory cost.
If the total cost visible on the robot is higher than the student's pilot score, then they can't pilot the robot.
This allows for special cards like `Autonomous Mode`, which has a high software cost but lowers Memory usage.
Thematically, the programming made it easier to pilot.
It's still not perfect - in the last playtest, we barely ran into the memory limit.
But it's a start.

My next steps are to start marketing the design on places like Twitter and Board Game Geek.
If I can raise interest, this will help viability for publishers.
At the same time, I'll continue play testing (and calibrating), to make the cards feel like they cost the right amounts and have appropriate abilities.
This calibration will take a lot of time, I suspect, but I've gotten good feedback that the game's mechanics are generally solid.
My dream is to get it signed with a publisher, so I won't have to worry about artwork and fulfillment.

At that point I'll have created and brought to life my passion project game!

[last post]: {{< ref "/blog/2021/08/21-arena-robot-league-first-design.md" >}}
[Protospiel Online]: https://protospiel.online/
