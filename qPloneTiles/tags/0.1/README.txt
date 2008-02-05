qPloneTiles

 #120: Support and use "Tile" links
 
One of the classic, testable usability laws is Fitt's
Law, which simply says that the efficiency of a user
interface item is directly proportional to its size.
Plone currently has a lot of user interface items that
could have bigger clickable areas without changing the
elements themselves.
		      
 Proposed by
      Alexander Limi
 Proposal type
      User interface
 Assigned to release
      * Plone 3.0
 State
      being-discussed

 
Motivation

 A lot of the user interface elements in Plone only work when you click the links they define instead of the entire UI
element. This is bad UI, although most web-based systems work this way.
 I have already experimented with changing this for a limited set of items in previous Plone versions; in Plone 2.0 I made
the entire item in the navigation tree clickable and it indicates when it is selected with a block of color around itself,
so you know you can click (this doesn't work in Internet Explorer because it's a buggy piece of crap, more about that
later ;). In Plone 2.1 I made all the portlet items be clickable in the entire area through a display:block definition of
the link tag.
 It's time to take this to the next level.


Proposal
					  
 Because of the limitations (as far as I have found, at least), it's hard to make certain elements entirely clickable
through re-defining the link tag only. In a separate project I was involved in, we used a tiny piece of JS to assign
clickable behaviour to an arbitrary element, which worked well.
 (Note that the normal "read more" or whatever link still remains, so it's not removing links for people that have JS
turned off or browsing via lynx or similar — this is merely augmenting the link behaviour, not moving it into JS.)
 This also has the advantage of being able to make any area clickable. My pet peeve is that Plone in "Summary view"
doesn't accept clicks anywhere within the area of one of the items listed, but only on the links. The interface would be
so much more efficient if we could click anywhere within that item's area.
					  
					  
Implementation
					  
 We should find a good way to define an area as clickable. In the project I was in, we defined that on the tag itself, and
did it explicitly, but this can possibly be improved.
