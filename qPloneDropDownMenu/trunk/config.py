from Products.CMFCore import CMFCorePermissions
 
VIEW_PERMISSION = CMFCorePermissions.ManagePortal

PROJECT_NAME = 'qPloneDropDownMenu'
UNIQUE_ID = "portal_dropdownmenu"
SKINS_DIR = 'skins'

GLOBALS = globals()

PROPERTY_SHEET = 'dropdownmenu_properties'
MENU_HTML = '''<ul><li><a class="first-item" href="http://www.bmc.com">Home</a></li><li><a href="http://www.bmc.com/products/">Solutions &amp; Products</a><ul>
        <li><a href="http://www.bmc.com/BMC/Common/Templates/hou_generic_tab/0,,19052_34957721,00.html">Business Service Management</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/Templates/hou_generic_tab/0,,19052_34829607,00.html">Best Practices &amp; Compliance</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/Templates/hou_generic_tab/0,,19052_34830527,00.html">Small &amp; Mid-Sized Business </a></li>
        <li><a href="http://www.bmc.comBMC/Common/Templates/hou_generic_tab/0,3846,19052_34818399,00.html">Industry Solutions</a></li>
        <li><a href="http://www.bmc.com/BMC/Products/CDA/hou_Products_Index/0,2830,19052_23655657,00.html">Product Families</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,3465,19052_19432,00.html">Services</a></li>
        <li><a href="http://www.bmc.com/products/productlist/0,,19052,00.html">Product List A to Z</a></li>
        <li><a href="http://www.bmc.com/BMC/Products/CDA/hou_Products_Index/0,2830,19052_23655660,00.html">Downloads &amp; Resources</a></li>
        <li><a href="http://www.bmc.com/pricelist/">Global Pricing</a></li>  	  
      </ul></li><li><a href="http://www.bmc.com/partners/">Partners</a><ul>
        <li><a href="http://www.bmc.com/BMC/Partners/CDA/hou_Partner_Generic/0,3319,5377102_5379132,00.html">Find a Partner</a></li>
        <li><a href="http://www.bmc.com/BMC/Partners/CDA/hou_Partner_Generic/0,3319,5377102_5379134,00.html">Become a Partner</a></li>
        <li><a href="http://www.bmc.com/BMC/Partners/CDA/hou_Partner_Generic/0,3317,5377102_5379136,00.html">Find a Market Zone Product</a></li>
      </ul></li><li><a href="http://www.bmc.com/support_home">Support</a><ul>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4736148,00.html">Case Tracking &amp; Reporting</a></li>
        <li><a href="http://www.bmc.com/support/vantive_bridge.cfm?path=http://selfserve.bmc.com/support/Forms/frmResolutionSearch.asp">Knowledge Database</a></li>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4736152,00.html">My Support Admin</a></li>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4736150,00.html">PTFs, FTP &amp; Installation</a></li>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4736154,00.html">Policies &amp; Guidelines</a></li>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4736144,00.html">Product Lists &amp; Manuals</a></li>
        <li><a href="http://www.bmc.com/info_center_support/overview/0,3252,19097_4718041,00.html">Support Contacts</a></li>
        <li><a href="http://www.bmc.com/info_center_support/All_News/0,2560,19097,00.html">Support News</a></li>
      </ul></li><li><a href="http://shop.bmc.com/">Store</a><ul>
        <li><a href="http://shop.bmc.com/shopping_support.cfm">Shopping Support</a></li>
        <li><a href="http://shop.bmc.com/licensing.cfm">Licensing Information</a></li>
        <li><a href="http://shop.bmc.com/download.cfm">Download Facility</a></li>
        <li><a href="http://shop.bmc.com/retrieve_cart.cfm">Retrieve Your Quote</a></li>
      </ul></li><li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,,11629550_11650861_11651561,00.html?c=products_header&amp;n=education_linksupport_homet=11503">Education</a><ul>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,3465,11629550_11650863,00.html">Certification Program</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,3465,11629550_11681301,00.html">Placement Tests</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,3465,11629550_11651556,00.html">Product Education</a></li>
      </ul></li><li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Detail/0,3464,9926222_10667925,00.html">Communities</a><ul>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Detail/0,3464,9926222_10636326,00.html">Thought Leadership Council</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Generic/0,3465,9926222_33961809,00.html">Enterprise Leadership</a></li>
        <li><a href="http://talk.bmc.com/">Blogs &amp; Podcasts @TalkBMC</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Detail/0,3464,9926222_33455235,00.html">External Communities</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/CDA/hou_Page_Detail/0,3464,9926222_10636328,00.html">User Groups</a></li>
        <li><a href="http://devcon.bmc.com/">Developer Connection</a></li>
        <li><a href="http://www.bmc.com/BMC/Common/Views/hou_vw_redirect_url/0,3411,9926222_34207904,00.html">Partner Network Login</a></li>
      </ul></li></ul>'''
