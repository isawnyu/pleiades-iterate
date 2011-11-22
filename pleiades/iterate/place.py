#

from AccessControl import ClassSecurityInfo, getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
from AccessControl.User import nobody
from AccessControl.User import UnrestrictedUser as BaseUnrestrictedUser
from Products.CMFCore.utils import getToolByName

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
    
        # TODO: implement a new workflow for checked out items to replace
        # this hack. Also note that checkouts expose 
        sm = getSecurityManager()
        try:
            tmp_user = UnrestrictedUser(
                sm.getUser().getId(),
                '', 
                ['Manager'],
                '')
            newSecurityManager(None, tmp_user.__of__(event.object.acl_users))
            for oid, ob in event.working_copy.contentItems():
                baseline = event.object[oid]
                baseline_state = wftool.getInfoFor(baseline, 'review_state')
                if baseline_state in ('pending', 'published'):
                    wftool.doActionFor(ob, action="submit")
                if baseline_state in ('published'):
                    wftool.doActionFor(ob, action="publish")
            setSecurityManager(sm)
        except:
            setSecurityManager(sm)
            raise
    else:
        pass

