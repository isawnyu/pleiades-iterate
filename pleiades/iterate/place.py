#

from Products.CMFCore.utils import getToolByName

def handleCheckout(event):
    # Change review state of all of a place's items to match the baseline
    wftool = getToolByName(event.object, "portal_workflow")
    for oid, ob in event.working_copy.contentItems():
        baseline = event.object[oid]
        baseline_state = wftool.getInfoFor(baseline, 'review_state')
        if baseline_state in ('pending', 'published'):
            wftool.doActionFor(ob, action="submit")
        if baseline_state in ('published'):
            wftool.doActionFor(ob, action="publish")

