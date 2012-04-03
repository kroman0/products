import unittest
from unittest import TestSuite, makeSuite, TestCase
from itertools import izip
from PIL import ImageDraw

from quintagroup.analytics.browser.treemap import TreemapBTree, Treemap, \
                                                  TreemapControl, \
                                                  TreemapHtml, \
                                                  TreemapImage

#class TestQRectangle(unittest.TestCase):
#    def setUp(self):
#        self.rect = QRectangle(100,100,200,200,1000)
#        self.rect.append(QRectangle(size=10))
#        self.rect.append(QRectangle(size=20))
#    
#    def test_length(self):
#        """ Testing lengths 'self' object """
#        self.assertEqual(2, self.rect.length())
#
#    def test_coordinates(self):
#        """ Testing setCoordinates() and getCoordinates """
#        self.rect.setCoordinates((5,5,10,10))
#        self.assertEqual((5,5,10,10), self.rect.getCoordinates())
#
#    def test_size(self):
#        """ Testing getSize() and setSize() """
#        self.rect.setSize(10)
#        self.assertEqual(10.0, self.rect.getSize())
#    
#    def test_getWeight(self):
#        """ Tests method that returns size of QRectangle objects"""
#        self.assertEqual(30.0, self.rect.getWeight())
#    
#    def test_addItem(self):
#        """ Tests method that add QRectangle object in QRectangle list """
#        self.assertEqual(1, self.rect.addItem(QRectangle(size=10)))
#        self.assertEqual(0, self.rect.addItem(QRectangle(size=0)))
#
#    def test_layout(self):
#        """ Tests method that forms (x1, y1, x2, y2) for rectangles """
#        self.rect.layout()
#        isNumber = lambda x: abs(x - round(x, 1)) < 0.1
#        self.assertEqual((True, True, True, True),
#                             tuple(imap(isNumber, self.rect[0].getCoordinates())))
#        self.assertEqual((True, True, True, True),
#                             tuple(imap(isNumber, self.rect[1].getCoordinates())))


def createTreemap(cls=Treemap):
    """ Method dedicated to create tests instance """
    treemap = cls(x=0, y=0, w=100,h=100)
    treemap.addItems([Treemap(size=50, color='#ad3333', title='admin4'),
                      Treemap(size=30, color='#4af6a0', title='admin2'),
                      Treemap(size=20, color='#9c1b9c', title='admin3'),
                      Treemap(size=10, color='#fde5be', title='admin1')])
    return treemap

def getCoordinates(treemap, nominal):
     for i,x in enumerate(treemap):
          for coord in zip(x.coordinates, nominal[i]):
              yield coord
    

class StubSizeByPath:
    @staticmethod
    def getTreemapInfo():
        return [{'size': 10, 'id': 'admin1', 'type': 'Image'},
                {'size': 30, 'id': 'admin2', 'type': 'File'},
                {'size': 20, 'id': 'admin3', 'type': 'File'},
                {'size': 50, 'id': 'admin4', 'type': 'Image'}]
    
    
class TestTreemapBTree(unittest.TestCase):
    """ Class dedicated to test treemap binary tree """
    def createTreemap(self):
        """ Method dedicated to create tests instance """
        treemap = Treemap(size=100)
        for x in [10, 20, 30,40]: 
            treemap.append(Treemap(size=x))
        treemap[3].addItems([Treemap(size=20), Treemap(size=20)])
        return treemap

    def setUp(self):
        self.treemap = self.createTreemap()
        self.btree = TreemapBTree(data=self.treemap)

    def test_getWeight(self):
        """ Tests method that returns size of objects """
        self.assertEqual(100, self.btree.getWeight(self.treemap))

    def test_getHalfSize(self):
        """ Tests method that returns half size of objects"""
        self.assertEqual(3, self.btree.getHalfSize(self.treemap))
    
    def test_addNodes(self):
        """ Tests method adds treemap objects into TreemapBTree """
        def getItems(treemap):
            if not(treemap.left and treemap.right):
                return [treemap.data.size]
            res = [treemap.data.size] + getItems(treemap.left) + \
                    getItems(treemap.right)
            return res

        self.btree.addNodes(self.treemap)  
        self.assertEqual([100.0, 60.0, 30.0, 10.0, 20.0, 30.0, 40.0, 20.0, 20.0], getItems(self.btree))

        treemap = Treemap(title='Root')
        treemap.append(self.treemap) 
        btree = TreemapBTree(data=treemap)
        btree.addNodes(treemap)  
        self.assertEqual(1,len(btree.data))

class TestTreemapControl(unittest.TestCase):
    """ Class dedicated to test Treemap objects """
    def setUp(self):
        self.control = TreemapControl(None, None, Treemap(), StubSizeByPath())
        self.treemap = createTreemap()

    def test_setFieldColor(self):   
        """ Method dedicated to test treemap attributes """
        self.assertEqual([{'color': '#fde5be', 'type': 'Image', 'id': 'admin1', 'size': 10}, 
                         {'color': '#4af6a0', 'type': 'File', 'id': 'admin2', 'size': 30}, 
                         {'color': '#9c1b9c', 'type': 'File', 'id': 'admin3', 'size': 20},
                         {'color': '#ad3333', 'type': 'Image', 'id': 'admin4', 'size': 50}],
                         self.control.setFieldColor(StubSizeByPath.getTreemapInfo()))   

    def test_sortItems(self):
        """ Method dedicated to test fields """
        self.assertEqual([{'type': 'Image', 'id': 'admin4', 'size': 50}, 
                          {'type': 'File', 'id': 'admin2', 'size': 30}, 
                          {'type': 'File', 'id': 'admin3', 'size': 20}, 
                          {'type': 'Image', 'id': 'admin1', 'size': 10}],
                          self.control.sortItems(StubSizeByPath.getTreemapInfo()))

    def test_createRectangles(self):
        """ Method dedicated to test treemap rectangles """
        self.control.createRectangles(StubSizeByPath.getTreemapInfo())
        self.assertEqual(self.treemap, self.control.treemap)

    def test_setTreemapData(self):
        self.control.setTreemapData()
        self.assertEqual(self.treemap, self.control.treemap)
        
class TestTreemap(unittest.TestCase):
    """ Class dedicated to test rectangles """
    def setUp(self):
        self.treemap = createTreemap()
        self.btree = TreemapBTree(data=self.treemap)

    def test_coordinates(self):
        """ Method dedicated to test rectangle coordinates (set and get)  """
        self.treemap.coordinates = (1,2,3,4)
        self.assertEqual((1,2,3,4), self.treemap.coordinates)
    
    def test_addItem(self):
        """ Method dedicated to test treemap object (adding into root treemap) """ 
        self.treemap.addItem(Treemap(size=0.0, title = 'test'))
        self.assertNotEqual('test', self.treemap[-1].title)

        self.treemap.addItem(Treemap(size=1, title='test'))
        self.assertEqual('test', self.treemap[-1].title)

    def test_addItems(self):
        """ Method dedicated to test treemap objects (adding into root treemap) """ 
        self.treemap.addItems([Treemap(size=1, title='test1'), 
                               Treemap(size=2, title='test2')])    
        self.assertEqual('test2', self.treemap[-1].title)
        self.assertEqual('test1', self.treemap[-2].title)

    def test_setCoordinates(self):
        """ Method dedicated to test recursive method """
        nominal = [(0, 0, 100, 45.45), 
                   (0, 45.45, 50.0, 54.54),
                   (50.0, 45.45, 50.0, 36.36),
                   (50.0, 81.81, 50.0, 18.18)] 

        self.btree.addNodes(self.treemap)
        self.treemap.setCoordinates(self.btree)
        for x in getCoordinates(self.treemap, nominal):
            self.assertAlmostEqual(x[0], x[1], 1) 

class TestTreemapHtml(unittest.TestCase):
    """ Class dedicated to test Treemap objects """
    def setUp(self):
        self.treemap = createTreemap(cls=TreemapHtml)
        self.btree = TreemapBTree(data=self.treemap)
        self.btree.addNodes(self.treemap)
        self.treemap.setTreemapData(self.btree)

    def test_getClasses(self):
        """ Method dedicated to test html tag (<div>) """
        self.treemap.setCoordinates(self.btree)
        self.assertEqual('horizontal prop100',
                         self.treemap.getClasses(self.btree))
        self.assertEqual('', self.treemap.getClasses(self.btree.left))
        self.assertEqual('vertical prop40', 
                         self.treemap.getClasses(self.btree.right.right))

    def test_writeHtml(self):
        """ Method dedicated to test html tag (<div>) """
        self.assertEqual("", self.treemap._writeHtml(self.btree.left)) 
        self.assertEqual('<div class="" style="background-color:#4af6a0"></div>' + \
                          '<div class="horizontal prop70" style="background-color:None">' + \
                          '<div class="" style="background-color:#9c1b9c"></div>' + \
                          '<div class="" style="background-color:#fde5be"></div></div>',
                          self.treemap._writeHtml(self.btree.right)) 


    def test_createTreemap(self):
        """ Method dedicated to test html tag (treemap) """
        self.assertEqual('<div class="horizontal prop50"><div class="" ' +\
                         'style="background-color:#ad3333"></div>' +\
                         '<div class="vertical prop50" style="background-color:None">' +\
                         '<div class="" style="background-color:#4af6a0"></div>' +\
                         '<div class="horizontal prop70" style="background-color:None">' +
                         '<div class="" style="background-color:#9c1b9c"></div>' +\
                         '<div class="" style="background-color:#fde5be"></div>' +\
                         '</div></div></div>',
                         self.treemap.createTreemap(self.btree))
        
    def test_setTreemapData(self):
        """ Method dedicated to test coordinates """
        nominal = [(None, None, 45.45, 100), 
                   (None, None, 100, 50.0),
                   (None, None, 66.66, 100),
                   (None, None, 33.33, 100)] 

        for x in getCoordinates(self.treemap, nominal):
            if x[0] and x[1]:
                self.assertAlmostEqual(x[0], x[1], 1) 

class TestTreemapImage(unittest.TestCase):
    """ Class dedicated to test treemap image """
    def setUp(self):
        self.treemap = createTreemap(cls=TreemapImage)
        self.btree = TreemapBTree(data=self.treemap)
        self.btree.addNodes(self.treemap)
        self.treemap.setCoordinates(self.btree)

    def test_drawContainer(self):
        treemap = self.treemap.drawContainer()
        self.assertEqual(self.treemap.image.getbbox(), treemap.getbbox())
        self.assertEqual(('R', 'G', 'B'), treemap.getbands())
    
    def test_rgbHexToDecimal(self):
        self.assertEqual((253, 229, 190),
                          self.treemap.rgbHexToDecimal('#fde5be'))
        
    def test_getHlsPIL(self):
        self.assertEqual('hsl(10,10%,20%)', 
                          self.treemap.getHlsPIL(10,10,20))

    def test_getFontSize(self):
        self.assertEqual(15, self.treemap.getFontSize(self.treemap[0]))
        self.assertEqual(81, self.treemap.getFontSize(Treemap(w=900,h=700)))

    def test_createFont(self):
        import PIL
        font = self.treemap.createFont(15)
        self.assertEqual(True, isinstance(font, PIL.ImageFont.FreeTypeFont))

    def test_setMask(self):
        rgb =  self.treemap.image.getpixel((10,10))

        treemap = Treemap(w=1,h=1)
        self.treemap.setMask(treemap)
        self.assertEqual(rgb, self.treemap.image.getpixel((10,10)))

        self.treemap.setMask(self.treemap)
        self.assertNotEqual(rgb, self.treemap.setMask(self.treemap))
       
    def test_getPilColor(self):
        self.assertEqual('hsl(37,144%,56%)', 
                          self.treemap.getPilColor('#fde5be'))
        
#    def checkImage(self):
#        return len([x for x in self.treemap.image.tostring().split('\xff') 
#                               if x != ''])

    def test_writeText(self):
        def istitle(self, result, width, height):
            treemap = TreemapBTree(data=Treemap(w=width, h=height, x=0, y=0, 
                                                color='#fde5be', title = 'test'))
            self.treemap.writeText(treemap, image)
            self.assertEqual(result, self.treemap.writeText(treemap, image)) 
 
        image = ImageDraw.Draw(self.treemap.image)

        istitle(self, None, 10, 10)
        istitle(self, True, 40, 40)

    def test_drawTreemap(self):
        image = ImageDraw.Draw(self.treemap.image)
        self.assertEqual(None, self.treemap.drawTreemap(self.btree, image))
    

def test_suite():
    test_suite = unittest.TestSuite([])
    test_suite.addTest(makeSuite(TestTreemapControl))
    test_suite.addTest(makeSuite(TestTreemapBTree))
    test_suite.addTest(makeSuite(TestTreemap))
    test_suite.addTest(makeSuite(TestTreemapHtml))
    test_suite.addTest(makeSuite(TestTreemapImage))
    return test_suite
 
if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')

#    suite = unittest.TestLoader().loadTestsFromTestCase(TestTreemapControl)
#    unittest.TextTestRunner(verbosity=2).run(suite)
