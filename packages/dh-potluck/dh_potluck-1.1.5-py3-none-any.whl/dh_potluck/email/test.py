from dh_potluck.email.email_service import EmailService

EmailService.send_email_html(
    'jake.delmas@dashhudson.com',
    'Jake Delmas',
    subject='Test Subject',
    html='<b>this is a test</b>',
)
EmailService.send_email_template(
    'jake.delmas@dashhudson.com',
    'Jake Delmas',
    'restore-password',
    [{'name': 'link', 'content': 'test'}, {'name': 'name', 'content': 'JAKEEE'}],
    subject='template test',
)
