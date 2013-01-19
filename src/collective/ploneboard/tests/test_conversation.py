from zope.component import createObject
from zope.component import queryUtility
from plone.dexterity.interfaces import IDexterityFTI
import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.ploneboard.interfaces import IConversation
from collective.ploneboard.testing import \
    COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING


class ConversationIntegrationTest(unittest.TestCase):

    layer = COLLECTIVE_PLONEBOARD_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.request['ACTUAL_URL'] = self.portal.absolute_url()
        setRoles(self.portal, TEST_USER_ID, ['Manager'])

    def test_fti(self):
        fti = queryUtility(
            IDexterityFTI,
            name='conversation'
        )
        schema = fti.lookupSchema()
        self.assertEquals(IConversation, schema)

    def test_factory(self):
        fti = queryUtility(
            IDexterityFTI,
            name='conversation'
        )
        factory = fti.factory
        new_object = createObject(factory)
        self.failUnless(IConversation.providedBy(new_object))

    def test_global_allow_not_allowed(self):
        self.assertRaises(
            ValueError,
            self.portal.invokeFactory,
            'conversation',
            'my-conversation',
        )

    def test_adding(self):
        self.portal.invokeFactory(
            'messageboard',
            'board'
        )
        self.portal.board.invokeFactory(
            'topic',
            'topic'
        )

        self.portal.board.topic.invokeFactory(
            'conversation',
            'conversation'
        )

        obj = self.portal.board.topic['conversation']
        self.failUnless(IConversation.providedBy(obj))