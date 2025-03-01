"""
Sending Messages over XMPP
==========================

.. versionadded:: 2014.1.0

This state is useful for firing messages during state runs, using the XMPP
protocol

.. code-block:: yaml

    server-warning-message:
      xmpp.send_msg:
        - name: 'This is a server warning message'
        - profile: my-xmpp-account
        - recipient: admins@xmpp.example.com/salt
"""


def __virtual__():
    """
    Only load if the XMPP module is available in __salt__
    """
    if "xmpp.send_msg" in __salt__:
        return "xmpp"
    return (False, "xmpp module could not be loaded")


def send_msg(name, recipient, profile):
    """
    Send a message to an XMPP user

    .. code-block:: yaml

        server-warning-message:
          xmpp.send_msg:
            - name: 'This is a server warning message'
            - profile: my-xmpp-account
            - recipient: admins@xmpp.example.com/salt

    name
        The message to send to the XMPP user
    """
    ret = {"name": name, "changes": {}, "result": None, "comment": ""}
    if __opts__["test"]:
        ret["comment"] = "Need to send message to {}: {}".format(recipient, name,)
        return ret
    __salt__["xmpp.send_msg_multi"](
        message=name, recipients=[recipient], profile=profile,
    )
    ret["result"] = True
    ret["comment"] = "Sent message to {}: {}".format(recipient, name)
    return ret


def send_msg_multi(name, profile, recipients=None, rooms=None):
    """
    Send a message to an list of recipients or rooms

    .. code-block:: yaml

        server-warning-message:
          xmpp.send_msg:
            - name: 'This is a server warning message'
            - profile: my-xmpp-account
            - recipients:
              - admins@xmpp.example.com/salt
            - rooms:
              - qa@conference.xmpp.example.com

    name
        The message to send to the XMPP user
    """
    ret = {"name": name, "changes": {}, "result": None, "comment": ""}

    if recipients is None and rooms is None:
        ret["comment"] = "Recipients and rooms are empty, no need to send"
        return ret

    comment = ""
    if recipients:
        comment += " users {}".format(recipients)
    if rooms:
        comment += " rooms {}".format(rooms)
    comment += ", message: {}".format(name)

    if __opts__["test"]:
        ret["comment"] = "Need to send" + comment
        return ret

    __salt__["xmpp.send_msg_multi"](
        message=name, recipients=recipients, rooms=rooms, profile=profile,
    )
    ret["result"] = True
    ret["comment"] = "Sent message to" + comment

    return ret
