# Controller Python Script "formmailer_send"
##bind context=context
##bind state=state
##parameters=
##title=Sends a formmailer form.
##


if context.getCPYAction():
    state.setNextAction('traverse_to:'+context.getCPYAction())

    # Need to change the state to something other than success, so that
    # FormController can notice our overriding of the action.

    state.set(status='scriptaction')

    return state

context.send_form()

if context.getSentRedirect():
    return state.set(next_action='redirect_to:string:'+context.getSentRedirect())

return state

