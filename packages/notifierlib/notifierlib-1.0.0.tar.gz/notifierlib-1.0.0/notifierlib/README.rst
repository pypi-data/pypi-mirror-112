===========
notifierlib
===========

A library that implements a kind of fan-out pattern, sending messages to very different endpoints.
Extendable through the implementation of custom Channels.


* Documentation: http://notifierlib.readthedocs.io/en/latest/

Features
--------

Introduced concepts are:

* Channels
    A channel is a communication endpoint capable of sending some type of message exposing a "notify" method.

* Groups
    A group is a construct bringing channels together under a common entrypoint showing up as a method call of the main Notifier object.

* Notifier
    The main object bringing together channels as broadcast by default and exposing methods to register and unregister channels and add and remove groups.

The payload of the notification methods is by convention a dictionary with at least a "subject" and a "message" key with the appropriate values.
It is designed like this so it can be very easy to implement much more complex structures like templates without needed any domain knowledge on all the channels.

Each channel can implement their own template as in instantiation argument in their class and handle the interpolation of variables in the notify method.

An example could be :

.. code-block:: python

    from notifierlib.channels import Email
    from notifierlib import Notifier, Group

    import logging
    logging.basicConfig(level=logging.DEBUG)
    template='<b>{{subject}}</b> <i>{{message}}</i> <a href="http://google.com">link</a>.'

    email=Email('email',
                sender='sender@gmail.com',
                recipient='recipient@gmail.com',
                smtp_address='smtp.domain.com',
                username='smtp_username',
                password='smtp_password',
                tls=True,
                ssl=False,
                port=587,
                template=template,
                content='html')

    notifier=Notifier()
    notifier.register(email)
    notifier.broadcast(subject='this is a test of a template', message="""this is a nice and long message""")

The above would render the template with the provided values on the notify method of the email channel before the mail gets sent.




For a more detailed explanation please see the USAGE.rst file.
