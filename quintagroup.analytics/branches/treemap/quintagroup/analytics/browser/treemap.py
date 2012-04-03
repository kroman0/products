""" Module dedicated to create treemap """

import colorsys
from StringIO import StringIO

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from Products.Five.browser import BrowserView
from views import SizeByPath
from const import FONT_PATH, IMAGE_MASK, USER_FONT, WIDTH, HEIGHT, \
                  TEXT_SATURATION, TEXT_LIGHT, MAX_PERCENT, MAX_ANGLE, \
                  DIV_RGB, DIV_SIDE, DIVERSION_FATHER, DIVERSION_CHILD, \
                  DIVERSION_TEXT_CHILD_V, DIVERSION_TEXT_CHILD_H, \
                  FONT_SIZE_FATHER, FONT_SIZE_CHILDREN_MIN, FRAME_COLOR, \
                  USER_COLOR, COLOR_FIELD, DIVERSION_TEXT_BORDER, \
                  DIVERSION_CHILD, DIVERSION_VERTICAL, FRAME_DIVERSION

class TreemapBTree:
    """ Class dedicated to create treemap binary tree """
    def __init__(self, left=None, right=None, data=None):
        self.left = left
        self.right = right
        self.data = data
        
    def getWeight(self, treemap):
        """ Method gets size of treemap objects """
        return float(sum(x.size for x in treemap))
    
    def getHalfSize(self, items):
        """  Method gets index of treemap objects (half size) """
        half_size = self.getWeight(items) / 2
        pre_size = next_size = 0.0
        for i,treemap in enumerate(items):
            next_size = pre_size + treemap.size
            if abs(half_size - next_size) > abs(half_size - pre_size):
                return i
            pre_size = next_size

        
    def addNodes(self, treemap_data):
        """  Recursive method adds treemap objects into TreemapBTree """
        def leaf(self,treemap_data):
            """ Method sets leaf into treemap tree """
            if len(treemap_data) == 0:
                return True
            
            elif isinstance(treemap_data, Treemap) and treemap_data.title == 'Root':
                self.addNodes(treemap_data[0])
                return False 

            elif len(treemap_data) == 1:
                if len(treemap_data[0]) >= 1:
                    self.data = treemap_data[0]
                    self.addNodes(treemap_data[0])
                elif type(treemap_data[0]) is Treemap:
                    self.data = treemap_data[0]
                return True

        if leaf(self, treemap_data):
            return

        half = self.getHalfSize(treemap_data)
        treemap1 = treemap_data[0:half]
        treemap2 = treemap_data[half:]
        weight1 = self.getWeight(treemap1)
        weight2 = self.getWeight(treemap2)
        
        self.left = TreemapBTree(data=Treemap(size=weight1))
        self.right = TreemapBTree(data=Treemap(size=weight2))
        
        self.left.addNodes(treemap1)
        self.right.addNodes(treemap2)
    
class TreemapControl(BrowserView):
    """ Class dedicated to control Treemap objects """
    def __init__(self, context, request, treemap, data):
        super(BrowserView, self).__init__(context, request)

        # eg: self.data = SizeByPath(context, request)
        self.data = data
        self.treemap = treemap
        self.binary_tree = TreemapBTree(data=self.treemap) 

    def setFieldColor(self, data):
        """
        >>> x = TreemapControl()
        >>> x.setFieldColor([{'id': 'admin'}, {'id': 'admin2'}])
        [{'color': '#fde5be', 'id': 'admin'}, {'color': '#4af6a0', 'id': 'admin2'}]
        """
        colors_list = COLOR_FIELD[0:len(data)]
        for i,x in enumerate(data):
            x['color'] = colors_list[i]
        return data
        
    def sortItems(self, data):
        """ Method sorts fields for treemap 
        >>> TreemapControl().sortItems([{'id': 'admin', 'size': 10}, {'id': 'admin2', 'size': 20}])
        [{'id': 'admin2', 'size': 20}, {'id': 'admin', 'size': 10}]
        """
        getWeight = lambda x: x.get('size')
        return sorted(data, key=getWeight, reverse=True)

    def createRectangles(self, data):
        """ Method create treemap rectangles """
        for field_data in self.sortItems(data):
             self.treemap.addItem(Treemap(size=field_data.get('size'),
                                          color=field_data.get('color'),
                                          title=field_data.get('id')))
    def setTreemapData(self):
        """ Method sets treemap attributes """
        # self.data.getTreemapInfo() -> [{'id': 'admin', size: '10', 'type': 'Image'},...]
        data = self.data.getTreemapInfo()
        self.setFieldColor(data)
        self.createRectangles(data)

class Treemap(list):
    """ Class dedicated to create rectangle """
    def __init__(self, x=None, y=None, w=None, h=None, color=None, title="", size=0):
        self.x = x
        self.y = y
        self.w = w    # width
        self.h = h    # hight
        self.color = color
        self.size = float( size )
        self.title = title

    def coordinates_get(self):
        """ Method gets rectangle coordinates """
        return (self.x, self.y, self.w, self.h)
    def coordinates_set(self, value):
        """ Method sets rectangle coordinates """
        (self.x, self.y, self.w, self.h) = value
    coordinates = property(fget=coordinates_get, fset=coordinates_set)

    def addItem(self, item):
        """ Method adds treemap object into root treemap """
        if float(item.size) != 0.0:
            self.append(item)
        
    def addItems(self, items):
        """ Method adds treemap objects into root treemap """
        for item in items:
            self.addItem(item)

    def setCoordinates(self, treemap):
        """  Recursive method adds coordinates into rectangles """
        if not(treemap.left and treemap.right):
            return

        if treemap.data.w > treemap.data.h:
            treemap.left.data.coordinates = (treemap.data.x, treemap.data.y,
                                             treemap.data.w * (treemap.left.data.size/
                                            (treemap.left.data.size + treemap.right.data.size)), 
                                             treemap.data.h)
            treemap.right.data.coordinates = (treemap.data.x + treemap.left.data.w,
                                              treemap.data.y, 
                                              treemap.data.w - treemap.left.data.w,
                                              treemap.data.h)
        else:
            treemap.left.data.coordinates = (treemap.data.x, treemap.data.y, 
                                             treemap.data.w,
                                             treemap.data.h * (treemap.left.data.size/
                                             (treemap.left.data.size + treemap.right.data.size)))
            treemap.right.data.coordinates = (treemap.data.x, treemap.data.y + treemap.left.data.h, 
                                              treemap.data.w,
                                              treemap.data.h - treemap.left.data.h)

        self.setCoordinates(treemap.left)
        self.setCoordinates(treemap.right)


          

class TreemapHtmlControl(TreemapControl):
    """ Class dedicated to control Treemap objects """
    def __init__(self, context, request):
        data = SizeByPath(context, request)
        super(TreemapHtmlControl, self).__init__(context, request, 
                                                 TreemapHtml(), 
                                                 data)

    def getTreemap(self):
        """ Method generates treemap (using html) """
        self.setTreemapData()
        self.binary_tree.addNodes(self.treemap)
        self.treemap.setTreemapData(self.binary_tree)
        return self.treemap.createTreemap(self.binary_tree)

class TreemapImageControl(TreemapControl):
    """ Class dedicated to control Treemap objects """
    def __init__(self, context, request):
        super(TreemapImageControl, self).__init__(context, request, 
                                             TreemapImage(),
                                             SizeByPath(context, request))
    def getTreemap(self):
        """ Method generates treemap view (PIL)"""
        self.setTreemapData()
        self.binary_tree.addNodes(self.treemap)
        self.treemap.setCoordinates(self.binary_tree)

        treemap = ImageDraw.Draw(self.treemap.image)
        self.treemap.drawTreemap(self.binary_tree, treemap)
        self.treemap.image = self.treemap.drawContainer()
        self.treemap.image = self.treemap.createFrame()
        self.treemap.image.show()

        output_file = StringIO()
        self.treemap.image.save(output_file,"PNG")
        try:
            return output_file.getvalue()
        finally:
            output_file.close()


class TreemapHtml(Treemap):
    """ Class dedicated to create Treemap objects """
    def __init__(self, x = 0, y = 0, w = 100, h = 100, title = "Root", 
                                               position=""):
        Treemap.__init__(self, x, y, w, h, title = title)
#        self.__position = position

#    def position_get(self):
#        """ Method gets rectangle position """
#        return self.__position
#    def position_set(self, value):
#        """ Method sets rectangle position """
#        if value in ['horizontal', 'vertical']:
#            self.__position = value 
#    position = property(fget=position_get, fset=position_set)

    def getClasses(self, treemap):
        """ Method provides classes for html tag """
        if not(treemap.left and treemap.right):
            return "" 

        elif treemap.data.w >= treemap.data.h:
            return 'horizontal prop%d' % int(round(treemap.left.data.w, -1))
        else:
            return 'vertical prop%d' % int(round(treemap.left.data.h, -1))

            
    def _writeHtml(self, treemap):
        """ Method generates html tag (<div>) """
        if not(treemap.left and treemap.right):
            return "" 
    
        return  '<div class="%s" style="background-color:%s">' % \
                              (self.getClasses(treemap.left), treemap.left.data.color) + \
                              self._writeHtml(treemap.left) + '</div>' + \
                '<div class="%s" style="background-color:%s">'% \
                              (self.getClasses(treemap.right), treemap.right.data.color) + \
                               self._writeHtml(treemap.right) +'</div>'

    def createTreemap(self, treemap):
        """ Method generates html tag (treemap) """
        return  '<div class="%s">' % \
                       self.getClasses(treemap) + \
                       self._writeHtml(treemap) + \
                '</div>'
               
        
    def setTreemapData(self, treemap):
        """  Recursive method adds coordinates into rectangles """
        if not(treemap.left and treemap.right):
            return
        if treemap.data.w >= treemap.data.h:
            treemap.left.data.coordinates = (None, None,
                                             100 * (treemap.left.data.size/
                                            (treemap.left.data.size + treemap.right.data.size)), 
                                             100)
            treemap.right.data.coordinates = (None,
                                              None, 
                                              treemap.data.w - treemap.left.data.w,
                                              100)
        else:
            treemap.left.data.coordinates = (None, None, 
                                             100,
                                             100 * (treemap.left.data.size/
                                             (treemap.left.data.size + treemap.right.data.size)))
            treemap.right.data.coordinates = (None, None, 
                                              100,
                                              treemap.data.h - treemap.left.data.h)

        self.setTreemapData(treemap.left)
        self.setTreemapData(treemap.right)

class TreemapImage(Treemap):
    """ Class dedicated to create treemap image """
    def __init__(self, x = 0, y = 0, w = WIDTH, h = HEIGHT, title = "Root"):
        Treemap.__init__(self, x, y, w, h, title = title)
        self.image = Image.new("RGB", (w, h), "white")
        self.size = (w, h)

    def drawContainer(self):
        """ Method draws treemap (name of item in the top) """
        font = self.createFont(FONT_SIZE_FATHER, USER_FONT)
        treemap = Image.new( "RGB", self.size, "white")
        rectangle = ImageDraw.Draw(treemap)
        for main in self:
             rectangle.rectangle((main.x, main.y, main.x + main.w, 
                                        main.h + main.y),
                                        fill=main.color)
             if font.getsize(main.title)[0] < main.w:
                 rectangle.text((main.x, main.y), text = main.title, 
                                       font = font)
             region = self.image.crop((int(round(main.x)) + DIVERSION_CHILD, 
                                               int(round(main.y)) + DIVERSION_CHILD,
                                               int(round(main.x + main.w) - DIVERSION_CHILD), 
                                               int(round(main.h + main.y)) - DIVERSION_CHILD))
             try:
                 region = region.resize((int(round(main.w - DIVERSION_FATHER * 2)),
                                        int(round(main.h - DIVERSION_FATHER * 2 - DIVERSION_VERTICAL))))
             except MemoryError:
                 continue
             treemap.paste(region,(int(round( main.x + DIVERSION_FATHER)),
                           int(round( main.y + DIVERSION_FATHER + DIVERSION_VERTICAL))))
        return treemap

    def rgbHexToDecimal(self, hex_str):
        """
        >>> TreemapImage().rgbHexToDecimal('#fde5be')
        (253, 229, 190)
        """
        hex_str = hex_str[1:]
        R = int(hex_str[0:2], 16)
        G = int(hex_str[2:4], 16)
        B = int(hex_str[4:], 16)
        return R,G,B

    def getHlsPIL(self, r, g, b):
        """
        >>> TreemapImage().getHlsPIL(10,10,20)
        'hsl(10,10%,20%)'
        """
        return "hsl(%d,%d%%,%d%%)"%(r, g, b)

    def getFontSize(self, field):
        """ Method gets font size for rectangles """
#        font_size = field.w/DIV_SID if field.h < field.w else field.h / DIV_SIDE

        if field.h < field.w:
            font_size =  field.w / DIV_SIDE
        else:
            font_size =  field.h / DIV_SIDE
        if font_size < FONT_SIZE_CHILDREN_MIN:
            return FONT_SIZE_CHILDREN_MIN
        else:
            return font_size

    def createFont(self, font_size, font=''):
        """ Method creates font for treemap """
        return ImageFont.truetype( FONT_PATH + '/vera/Vera%s.ttf'%font, font_size)

    def setMask(self, field):
        """ Method sets mask on rectangle """
        try:
            image_mask = IMAGE_MASK.resize((field.w - DIVERSION_CHILD,
                                            field.h - DIVERSION_CHILD))
        except MemoryError:
            return
        self.image.paste("white", (field.x + DIVERSION_CHILD,
                                 field.y + DIVERSION_CHILD),
                                 mask = image_mask)

    def getPilColor(self, color):
        """ 
        >>> TreemapImage().getPilColor('#fde5be')
        'hsl(37,144%,56%)'
        """
        r, g, b = self.rgbHexToDecimal(color)
        h, l, s = colorsys.rgb_to_hls(r / DIV_RGB, g / DIV_RGB, b / DIV_RGB)
        l -= TEXT_LIGHT
        s += TEXT_SATURATION
        return self.getHlsPIL(int(h * MAX_ANGLE), int(s * MAX_PERCENT), 
                              int(l * MAX_PERCENT))

    def writeText(self, treemap, image):
        """ Method dedicated to write text in treemap rectangles """
        field_name = treemap.data.title
        font = self.createFont(self.getFontSize(treemap.data))
    
        # font_size = (126, 47); font_size[0] - width, font_size[1] - height
        font_size = font.getsize(field_name)
        if treemap.data.w - DIVERSION_TEXT_CHILD_H + DIVERSION_TEXT_BORDER > font_size[0] and \
              font_size[1] < treemap.data.h - DIVERSION_TEXT_CHILD_V + DIVERSION_TEXT_BORDER:
            image.text((treemap.data.x + DIVERSION_TEXT_CHILD_H ,
                        treemap.data.y + DIVERSION_TEXT_CHILD_V),
                        text = field_name, font = font, 
                        fill = self.getPilColor(treemap.data.color))
            return True

    def drawTreemap(self, treemap, image):
        """ Method generates treemap image """
        if treemap.data.color:
            image.rectangle((treemap.data.x + DIVERSION_CHILD, treemap.data.y + DIVERSION_CHILD, 
                             treemap.data.x + treemap.data.w - DIVERSION_CHILD, 
                             treemap.data.h + treemap.data.y - DIVERSION_CHILD),
                             fill= treemap.data.color )
    
            self.setMask(treemap.data)
            self.writeText(treemap, image)

        if not(treemap.left and treemap.right):
            return  
       
        self.drawTreemap(treemap.left, image)
        self.drawTreemap(treemap.right, image)
        
    def createFrame(self):
        """ Method creates frame for treemap image """
        treemap = Image.new("RGB", 
                           (WIDTH + FRAME_DIVERSION,HEIGHT + FRAME_DIVERSION),
                            FRAME_COLOR)
        treemap.paste(self.image,(FRAME_DIVERSION/2, FRAME_DIVERSION/2))
        return treemap
