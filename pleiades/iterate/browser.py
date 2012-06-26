
from plone.app.iterate.relation import WorkingCopyRelation
from plone.memoize.instance import memoize
from Products.Five.browser import BrowserView


class IterateInfoView(BrowserView):

    def working_copy(self):
        refs = self.context.getBRefs( WorkingCopyRelation.relationship )
        if len( refs ) > 0:
            return refs[0]
        else:
            return None

    def baseline( self ):
        refs = self.context.getReferences( WorkingCopyRelation.relationship )
        if len( refs ) > 0:
            return refs[0]
        else:
            return None

    def __call__(self):
        return {
            'working_copy': self.working_copy(),
            'baseline': self.baseline() }

