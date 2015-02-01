from flask_wtf import Form
from wtforms import TextField, RadioField, TextAreaField
from wtforms.fields.html5 import EmailField
from wtforms.validators import DataRequired, Email, Length
from flask.ext.babel import lazy_gettext as _


class ContactForm(Form):
    type_ = RadioField(_('Type'), choices=[('bug', _('Bug')),
                                           ('suggestion', _('Suggestion')),
                                           ('question', _('Question'))],
                       validators=[DataRequired()])
    subject = TextField(_('Subject'), validators=[Length(min=5), DataRequired()])
    description = TextAreaField(_('Description'), validators=[DataRequired()])
    name = TextField(_('Name'), validators=[DataRequired()])
    email = EmailField(_('E-mail'), validators=[Email(), DataRequired()])
