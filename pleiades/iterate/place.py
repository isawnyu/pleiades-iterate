#

from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import (
    newSecurityManager, setSecurityManager)
from AccessControl.User import system
from Products.CMFCore.utils import getToolByName

def handleCheckout(event):
    # Change review state of all of a place's items to match the baseline
    wftool = getToolByName(event.object, "portal_workflow")
    mtool = getToolByName(event.object, "portal_membership")

    # TODO: implement a new workflow for checked out items to replace
    # this ugly security hack. Also note that checkouts expose 
    sm = getSecurityManager()
    admin = mtool.getMemberById("admin").getUser()
    try:
        newSecurityManager(None, admin.__of__(event.object.acl_users))
        for oid, ob in event.working_copy.contentItems():
            baseline = event.object[oid]
            baseline_state = wftool.getInfoFor(baseline, 'review_state')
            if baseline_state in ('pending', 'published'):
                wftool.doActionFor(ob, action="submit")
            if baseline_state in ('published'):
                wftool.doActionFor(ob, action="publish")
    except:
        setSecurityManager(sm)
        raise

