---
Title: Group Advice
categories: [life]
Date: "2014-05-14"
Tags:
- hfoss
---

Sometimes, things just get to be too much.

Sometimes, "group projects" end up leaving you more alone than you would be with a "solo project".

Sometimes, everything happens to line up perfectly to cause problems.

There's no easy way to magically fix this - you can't wish away a project, you can only get it done or leave it untouched.

This last week was one of the least pleasant I've had in a while. I had, all due within one week:

- A language parser and analyzer in C++ (by far the easiest assignment)
- [Prim's Algorithm] in Java
- A level editor for the HFOSS project, written in Python
- A "group project" focused on refactoring in Java

This last one was, by far, the bane of my existence. Due to a lack of communication with my teammates, I spent significantly more time than I should have needed to doing a large portion of the project. Though I normally don't care to complain about these things publicly, by groupmates' behavior has made me angry enough that I feel the need to write down a few of the lessons I learned, for students who are in the kind of situation I had to deal with:

- If your groupmates don't show up to meetings, and don't explain why, send out reminders and ask them what's going on
    - If needed, include any supervisor/higher-up in the mailing list, that way they have records of your issues ahead of time
- Do NOT delete any of the messages sent or received. These can be used to remind teammates of things that they committed to, as well as keep a log of all plans and completed work.
- Use some sort of version control. As simple as this sounds, it can save a ton of time in the long run. [Git] is distributed, so it allows people to get started on a testing box, before moving the actual group project to a centralized location, and people can work without being connected to the server.
    - It also keeps logs. Like the first two points, this shows how much work each team member contributed to the project, or at least to the code portions.
	- Lock down access as much as possible. If you're using "feature-branch", try to find a way to prevent anybody but the "QA/SCM" person from pushing to master, for instance.
- Make sure that your group is on the same page with requirements and deadlines. In my project, the presentation was worth 15%, the implementation was worth 15%, and "Reverse Engineering, Refactoring, and Documentation" was worth 70% of the final grade. On the last day, when the largest refactoring wasn't done yet, my groupmates were complaining that I was spending too much time on the code and not enough on the documentation. As I was the one with the best understanding of the entire program architecture, to the point at which one teammate could ask about any class and I would say what it did and how it interacted, I felt that I was the only one suited to earning those "Reverse Engineering/Refactoring" points that we desperately needed. My group disagreed, believing that the point of the project was solely documenting "what would we do if we had time".
- Meet early, meet often. My "group meetings" had at most two people, up until a week before the deadline. (Not for a lack of trying, any time the other members showed up, there was inevitably some complication or other commitment that they had.) This was despite our early attempts to plan and organize meetings that would work for everyone. This could have been mitigated by trying to organize meetings at other times as well.
- Make sure all members are aware of the things that still need to be done. GitHub issues are useful for code portions of this. For other components (design documentation, art, etc.), make sure you have a list accessible to all group members. Go over this list at every group meeting, making sure people are aware of the tasks required and are working on them. Publish anything that changed on this list in the meeting notes.
- Speaking of meeting notes, HAVE THEM. Distribute them via email after EVERY meeting, and store them in your group's central documents area for future reference, and to avoid the "oh, I didn't get that email".
- Make sure that the supervisors/professor/manager/higher-ups are aware of your group situation. If there is a problem, they should be able to give advice on how to deal with it, especially in a college setting.
- Sometimes, a group member is just too difficult to deal with. I had some experience with an extremely argumentative group member last year, and despite my attempts to get her to participate she spent more time complaining about how the rest of the group wasn't being inclusive of her. There was absolutely nothing that I could do that would make the situation any better, so I ended up trying to mitigate the damage to the team as much as possible by reducing the work required of her and prevent her from getting into a position where she would "mess something up". This backfired during our final presentation when she refused, in front of the class, to present the portion she had agreed to present, stating that other group members had done "her" work and so they should present it. I don't know of a good solution for this kind of teammate, except to try to appease them and prevent them from intentionally sabotaging the project.
- When uncooperative group members finally decide to participate, you may be bitter and want to brush them off. This will hurt the team even more, as now you're trying to do your work, do the work you're covering for them on, and keep them from messing up your work, resulting in stress and frustration. Instead, pull them aside, attempt to get them as caught up as needed, and then continue on your earlier path. Worst case, you don't need to avoid them. Best case, they're taking work off of your workload.

Most of these might be seen as rambling, this entire post is really about dumping my thoughts on group projects and how not to deal with them.

[Prim's Algorithm]: http://en.wikipedia.org/wiki/Prim%27s_algorithm
[Git]: http://git-scm.com
