from libabr import Control, Files, Protocol

files = Files()
control = Control()
locale = control.read_record("locale", "/etc/gui")
url = Protocol()


def get_string(name):
    return control.read_record(name, f'/srv/com/pyabr/data/{locale}.locale')


if locale == 'fa' or locale == 'ar':
    alignment = 'rtl'
else:
    alignment = 'ltr'

style = '''
p {
    font: menu;
    font-size: 120%;
}
'''

print(f'''
<html dir='{alignment}'>
    <head>
        <title>{get_string('invalid_url')}</title>
        <style>
        {style}
        </style>
    </head>
    <body>
        <p>{get_string('invalid_url')}</p>
    </body>
</html>
''')