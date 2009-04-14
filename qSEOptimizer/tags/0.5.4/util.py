def createMultiColumnList(self,slist, numCols, sort_on='title_or_id'):
    try:
        mcl = self.createMultiColumnList(slist, numCols, sort_on=sort_on)
        return mcl
    except AttributeError:
        return [slist]