# Disable the HomeFolderLocator from plone.app.iterate
from plone.app.iterate.containers import HomeFolderLocator
HomeFolderLocator.available = False
