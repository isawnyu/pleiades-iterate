
from unittest import TestCase, TestSuite, makeSuite

from plone.app.iterate.interfaces import ICheckinCheckoutPolicy

from pleiades.iterate.tests.base import PlacesIntegrationTestCase


class IteratePlaceTestCase(PlacesIntegrationTestCase):

    def test_nothing(self):
        self.setRoles(('Contributor',))
        p1 = self.places['1']
        self.failUnless('foo' in p1, p1.keys())
        wc = ICheckinCheckoutPolicy(p1).checkout(self.places)
        state = self.wf.getInfoFor(wc, 'review_state')
        self.failUnlessEqual(state, 'private')
        self.failUnlessEqual(len(wc.keys()), 0, wc.keys())
        # A child's history acquires its parent's history
        history = self.repo.getHistory(p1['foo'])
        self.failUnlessEqual(len(history), 1)
        p1 = ICheckinCheckoutPolicy(wc).checkin("updated")
        self.failUnless('foo' in p1, p1.keys())
        # A child's history acquires its parent's history
        history = self.repo.getHistory(p1['foo'])
        self.failUnlessEqual(len(history), 2)

    def test_cancel_checkout(self):
        self.setRoles(('Contributor',))
        p1 = self.places['1']
        self.failUnless('foo' in p1, p1.keys())
        wc = ICheckinCheckoutPolicy(p1).checkout(self.places)
        self.failUnlessEqual(len(wc.keys()), 0, wc.keys())
        p1 = ICheckinCheckoutPolicy(wc).cancelCheckout()
        self.failUnless('foo' in p1, p1.keys())
        # A child's history acquires its parent's history
        history = self.repo.getHistory(p1['foo'])
        self.failUnlessEqual(len(history), 1)

    def test_add_name_to_wc(self):
        self.setRoles(('Contributor',))
        p1 = self.places['1']
        self.failUnless('foo' in p1, p1.keys())
        wc = ICheckinCheckoutPolicy(p1).checkout(self.places)
        nid = wc.invokeFactory('Name', 'bar', nameTransliterated=u"Bar")
        self.failUnless('bar' in wc, wc.keys())
        p1 = ICheckinCheckoutPolicy(wc).checkin("updated")
        self.failUnless('foo' in p1, p1.keys())
        self.failUnless('bar' in p1, p1.keys())
        # A child's history acquires its parent's history
        history = self.repo.getHistory(p1['foo'])
        self.failUnlessEqual(len(history), 2)
        history = self.repo.getHistory(p1['bar'])
        self.failUnlessEqual(len(history), 1)

    def test_baseline_lock(self):
        self.setRoles(('Contributor',))
        p1 = self.places['1']
        wc = ICheckinCheckoutPolicy(p1).checkout(self.places)
        xx = ICheckinCheckoutPolicy(p1).checkout(self.places)

    def test_workingcopy_lock(self):
        self.setRoles(('Contributor',))
        p1 = self.places['1']
        wc = ICheckinCheckoutPolicy(p1).checkout(self.places)
        xx = ICheckinCheckoutPolicy(wc).checkout(self.places)

def test_suite():
    suite = TestSuite()
    suite.addTest(makeSuite(IteratePlaceTestCase))
    return suite
