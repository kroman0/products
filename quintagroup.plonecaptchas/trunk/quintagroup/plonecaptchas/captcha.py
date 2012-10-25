from plone.app.discussion.browser.captcha import CaptchaExtender
from quintagroup.z3cform.captcha.widget import CaptchaWidgetFactory
from plone.app.discussion import vocabularies
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from quintagroup.plonecaptchas.interfaces import IQGDiscussionCaptchas
from quintagroup.plonecaptchas.interfaces import ICaptchaProvider
from zope.interface import Interface
from zope.component import adapts, getUtilitiesFor, queryUtility
from plone.app.discussion.browser.comments import CommentForm


class CaptchaProvider(object):

    def __init__(self):
        self.widget_factory = CaptchaWidgetFactory


class CaptchaExtender(CaptchaExtender):
    adapts(Interface, IQGDiscussionCaptchas, CommentForm)

    def update(self):
        super(CaptchaExtender, self).update()
        if self.isAnon:
            cp = queryUtility(ICaptchaProvider, name=self.captcha)
            if cp:
                self.form.fields['captcha'].widgetFactory = cp.widget_factory
                self.form.fields['captcha'].mode = None


def captcha_vocabulary(context):
    """ Extend captcha vocabulary with quintagroup.plonecaptchas"""
    terms = vocabularies.captcha_vocabulary(context)._terms
    captchas = set((t.value for t in terms))

    providers = getUtilitiesFor(ICaptchaProvider)
    for name, util in providers:
        if name and name not in captchas:
            terms.append(SimpleTerm(value=name,
                                    token=name,
                                    title=name.capitalize()))
    return SimpleVocabulary(terms)
