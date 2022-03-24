import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from canteen import mail


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='noreply@kjhs.com', recipients=[user.email])
    msg.body = f'''To reset your password visit the following link:\n\n
{url_for('users.reset_token', token=token, _external=True)}
\n\nIf you did not make this request then just ingnore this email
    '''
    mail.send(msg)


def save_picture(form_picture):

    # generating a random hex filename for the profile picture
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)

    # resizing the image to the output size
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # saving image to the file system and returning the filename of the image
    i.save(picture_path)
    return picture_fn