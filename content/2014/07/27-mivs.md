Title: MIVS: Medical Image Viewing System
Category: code

Last semester at school, I decided to take a course on software architecture. The class was heavily focused on two main assignments, exercises in creating a design for a program and refactoring an existing design into something that resembled sane.

The latter left me too scarred, but I felt like writing about the former. My teammate [Brian] had already posted about it, but I found his post in my big list of "things to talk about".

MIVS is a Medical Image Viewing System. The overall idea was that we had to create a tool that could theoretically be used to read in and view medical images, which was complicated by many requirements like:

- Nested studies
- Create a window to measure values over
- Reconstruct images by taking one column of each image and concatenating them
- Scroll through sets of images

Overall, it was an interesting exercise in design. Though my team had a bit of a rocky start, we managed to pull through to make something that we were pretty proud of. I created a [gource visualization] of our development, which was kind of interesting to see.

[Brian]: http://brianmartone.com/2014/04/10/meet-mivs-the-medical-image-viewing-system/
[gource visualization]: https://www.youtube.com/watch?v=giZLQdZQQH8
