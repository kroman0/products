from plone.app.discussion.browser.captcha import CaptchaExtender
from quintagroup.z3cform.captcha.widget import CaptchaWidgetFactory
from plone.app.discussion import vocabularies
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import interfaces
from quintagroup.plonecaptchas.config import CAPTCHA_NAME
from quintagroup.plonecaptchas.interfaces import IQGDiscussionCaptchas, ICaptchaProvider
from zope.interface import Interface
from zope.component import adapts, getAdapters, queryAdapter
from plone.app.discussion.browser.comments import CommentForm


class CaptchaProvider(object):

    def __init__(self, context):
        self.widget_factory = CaptchaWidgetFactory


class CaptchaExtender(CaptchaExtender):
    adapts(Interface, IQGDiscussionCaptchas, CommentForm)

    def update(self):
        super(CaptchaExtender, self).update()
        providers = getAdapters((self.context,), ICaptchaProvider)
        if self.captcha in (n for n, a in providers) and self.isAnon:
            captcha_provider = queryAdapter((self.context,), name=self.captcha)
            if captcha_provider:
                self.form.fields['captcha'].widgetFactory = captcha_provider.widget_factory
                self.form.fields['captcha'].mode = None


def captcha_vocabulary(context):
    """ Extend captcha vocabulary with quintagroup.plonecaptchas"""
    terms = vocabularies.captcha_vocabulary(context)._terms

    adapters = getAdapters((context,), ICaptchaProvider)
    for name, adapter in adapters:
        terms.append(SimpleTerm(value=name,
                                token=name,
                                title=name))
    return SimpleVocabulary(terms)
