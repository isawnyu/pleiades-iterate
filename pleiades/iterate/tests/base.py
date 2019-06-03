from Products.Five import fiveconfigure
from Products.Five import zcml
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import onsetup
from Testing import ZopeTestCase as ztc
from zope.component import eventtesting

ztc.installProduct('Products.ATBackRef')
ztc.installProduct('Products.CompoundField')
ztc.installProduct('Products.OrderableReferenceField')
ztc.installProduct('pleiades.vocabularies')
ztc.installProduct('PleiadesEntity')


@onsetup
def setup_pleiades():
    fiveconfigure.debug_mode = True
    import pleiades.iterate
    zcml.load_config('configure.zcml', pleiades.iterate)
    fiveconfigure.debug_mode = False
    ztc.installPackage('pleiades.vocabularies')
    ztc.installPackage('plone.app.iterate')
    ztc.installPackage('Products.PleiadesEntity')

setup_pleiades()
ptc.setupPloneSite(products=['PleiadesEntity'])


class PlacesIntegrationTestCase(ptc.PloneTestCase):

    def setUp(self):
        super(PlacesIntegrationTestCase, self).setUp()
        eventtesting.setUp()

    def afterSetUp(self):
        self.wf = self.portal.portal_workflow
        self.repo = self.portal.portal_repository
        self.setRoles(('Manager',))
        self.portal.invokeFactory('PlaceContainer', id='places')
        self.places = self.portal['places']
        self.wf.doActionFor(self.places, 'submit')
        self.wf.doActionFor(self.places, 'publish')
        self.setRoles(('Contributor',))
        pid = self.places.invokeFactory('Place', '1')
        p1 = self.places[pid]
        self.wf.doActionFor(p1, 'submit')
        nid = p1.invokeFactory(
            'Name', 'foo', nameAttested=u"Foo", nameTransliterated=u"Foo")
        n1 = p1[nid]
        self.wf.doActionFor(n1, 'submit')
        self.setRoles(('Reviewer',))
        self.wf.doActionFor(p1, 'publish')
        self.wf.doActionFor(n1, 'publish')
