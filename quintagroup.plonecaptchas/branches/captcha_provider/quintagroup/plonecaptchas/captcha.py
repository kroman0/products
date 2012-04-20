from plone.app.discussion.browser.captcha import CaptchaExtender
from quintagroup.z3cform.captcha.widget import CaptchaWidgetFactory
from plone.app.discussion import vocabularies
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from quintagroup.plonecaptchas.interfaces import IQGDiscussionCaptchas
from quintagroup.plonecaptchas.interfaces import ICaptchaProvider
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
                self.form.fields['captcha'].widgetFactory = \
                                                captcha_provider.widget_factory
                self.form.fields['captcha'].mode = None


def captcha_vocabulary(context):
    """ Extend captcha vocabulary with quintagroup.plonecaptchas"""
    terms = vocabularies.captcha_vocabulary(context)._terms
    captchas = [t.value for t in terms]

    adapters = getAdapters((context,), ICaptchaProvider)
    for name, adapter in adapters:
        if name and name not in captchas:
            terms.append(SimpleTerm(value=name.lower(),
                                    token=name.lower(),
                                    title=name[0].upper()+name[1:]))
    return SimpleVocabulary(terms)
