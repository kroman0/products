qPloneTiles


Usage

  Plone Product for creating "Tile" links.
  
  Provide class 'tile' for html element you want to 
  have link behaviour. Then select one of the anchor 
  elements inside that tile by adding it class =
  = 'primary'. Thus, our tile element will redirect
  you to primary anchor target. So all tile area,
  except anchors within it, is linkable and behave 
  like a link! If you define your tile element, but
  not select your primary link inside tile, href 
  attribute of the first anchor will be taken by 
  default.
  
  Example 1:
    
    <div class="tile">
      <a href="www.example1.com">First link</a>
      <a href="www.example2.com">Second link</a>
    </div>
  Here we have div element with class 'tile'. But any
  element inside div haven't class 'primary'. So by
  default will be used href of the first link. And 
  when you click in scopes div element and outside a
  element you'll be redirected to www.example1.com.
      
  Example 2:
  
    <div class="tile">
      <a href="www.example1.com">First link</a>
      <a class="primary"
         href="www.example2.com">Second link</a>
    </div>
  In this case we have (in addition all we have in previous
  example) second link with primary class. So div element
  have "www.example2.com" location.
  
  Example 3:
  
    <div class="tile">
      <a href="www.example1.com">First link</a>
      <div class="tile">
        <a href="www.example1.com">First link</a>
        <a class="primary"
           href="www.example2.com">Second link</a>
      </div>
    </div>
  This last example show us that we could have nested
  tile elements. In practice, everything works like in
  previous examples except one. Tile element look for
  primary link. In this example primary element is 
  inside both tiles. But if you want to have for outer
  div first link as primary, you could simply add 
  class 'primary' to 'First link'. In this case tile'll
  search only to first primary link. And it won't
  affect inner div element.
  So remember that tile element could inherite href
  attribute only from inner anchors.
  
  
Inspiration

  "#120: Support and use "Tile" links":
 
  One of the classic, testable usability laws is Fitt's
  Law, which simply says that the efficiency of a user
  interface item is directly proportional to its size.
  Plone currently has a lot of user interface items that
  could have bigger clickable areas without changing the
  elements themselves.
		      
  Proposed by::
    Alexander Limi
  Proposal type::
    User interface
  Assigned to release::
    Plone 3.0
  State::
    being-discussed

Motivation

  A lot of the user interface elements in Plone only 
  work when you click the links they define instead 
  of the entire UI element. This is bad UI, although
  most web-based systems work this way.

  I have already experimented with changing this for 
  a limited set of items in previous Plone versions; 
  in Plone 2.0 I made the entire item in the 
  navigation tree clickable and it indicates when it
  is selected with a block of color around itself,
  so you know you can click (this doesn't work in 
  Internet Explorer because it's a buggy piece of
  crap, more about that later ;). In Plone 2.1 I made
  all the portlet items be clickable in the entire
  area through a display:block definition of the link
  tag.
  It's time to take this to the next level.


Proposal
					  
  Because of the limitations (as far as I have found, 
  at least), it's hard to make certain elements
  entirely clickable through re-defining the link tag
  only. In a separate project I was involved in, we
  used a tiny piece of JS to assign clickable behaviour
  to an arbitrary element, which worked well.
  (Note that the normal "read more" or whatever link
  still remains, so it's not removing links for people
  that have JS turned off or browsing via lynx or
  similar — this is merely augmenting the link behaviour,
  not moving it into JS.)
  This also has the advantage of being able to make any
  area clickable. My pet peeve is that Plone in "Summary
  view" doesn't accept clicks anywhere within the area
  of one of the items listed, but only on the links. The
  interface would be so much more efficient if we could
  click anywhere within that item's area.
  
  					  
Implementation
					  
  We should find a good way to define an area as clickable.
  In the project I was in, we defined that on the tag
  itself, and did it explicitly, but this can possibly be
  improved.
