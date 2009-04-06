from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from quills.app.portlets import archive

class Renderer(archive.Renderer):

    _template = ViewPageTemplateFile('archive.pt')
    
    @property
    def getSubArchives(self):
        res = []
        arch = super(Renderer, self).getSubArchives
        arch.reverse()
        for y in arch:
            ydata = {'title'  : y.Title(),
                     'months': []}
            months = y.getSubArchives()
            months.reverse()
            for m in months:
                ydata['months'].append(
                    {'murl':m.absolute_url() ,
                     'mid' :m.getId(),
                     'mlen':len(m)})
            res.append(ydata)
        return res
