#

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import nobody
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from Products.CMFCore.utils import getToolByName

from plone.app.iterate.interfaces import CheckinException

from Products.PleiadesEntity.content.interfaces import IPlace

class UnrestrictedUser(BaseUnrestrictedUser):
    """Unrestricted user that still has an id.
    """
    def getId(self):
        """Return the ID of the user.
        """
        return self.getUserName()

def handleCheckout(event):
    # Change review state of all of a place's items to match the baseline
    context = event.object
    if IPlace.providedBy(context):
        wftool = getToolByName(event.object, "portal_workflow")
        mtool = getToolByName(event.object, "portal_membership")
        sm = getSecurityManager()
        try:
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(),
                '', 
                ['Manager'],
                '')
            newSecurityManager(None, tmp_user.__of__(event.object.acl_users))
            for oid, ob in event.working_copy.contentItems():
                # Set review state and ownership to that of the baseline
                baseline = event.object[oid]
                baseline_state = wftool.getInfoFor(baseline, 'review_state')
                if baseline_state in ('pending', 'published'):
                    wftool.doActionFor(ob, action="submit")
                if baseline_state in ('published'):
                    wftool.doActionFor(ob, action="publish")
                if baseline.owner_info().get('id') is not None:
                    ob.changeOwnership(baseline.getOwner())

            setSecurityManager(sm)
        except:
            setSecurityManager(sm)
            raise
    else:
        pass


def handleCheckin(event):
    context = event.object # working copy
    if IPlace.providedBy(context):
        baseline_keys, baseline_values = zip(
            *event.baseline.contentItems()) or [(), ()]
        keys, values = zip(*context.contentItems()) or [(), ()]
        baseline_diff = set(baseline_keys) - set(keys)
        if baseline_diff:
            raise CheckinException("Items present in the baseline, %s, were not found in the working copy. A checkin of the working copy would have corrupted the baseline. Review the working copy and restore deleted items or cancel the checkout." % list(baseline_diff))
    else:
        pass

