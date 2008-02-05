## Script (Python) "getSynProp"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=customer_id='',adsense_width='',adsense_height='',adsense_format=''
##title=
##
return """<script type="text/javascript"> <!--
  google_ad_client="%s";
  google_ad_width=%s;
  google_ad_height=%s;
  google_ad_format="%s";
  google_color_border="FFFFFF";
  google_color_bg="FFFFFF";
  google_color_link="0000FF";
  google_color_url="008000";
  google_color_text="000000";
  //--></script>
<script type="text/javascript" src="http://pagead2.googlesyndication.com/pagead/show_ads.js"></script>""" % (customer_id,adsense_width,adsense_height,adsense_format)