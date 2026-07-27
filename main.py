from flask import Flask, render_template, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField,EmailField
from wtforms.validators import DataRequired, Email
from flask_bootstrap import Bootstrap
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
EMAIL = os.environ["EMAIL"]
PASSWORD = os.environ["PASSWORD"]
SECRET_KEY = os.environ["SECRET_KEY"]

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    message= TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

def send_email(name,sender_email,message):
    my_email = EMAIL
    password = PASSWORD
    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=my_email, password=password)
        connection.sendmail(to_addrs=my_email,
                            msg=f"""Subject: New Portfolio Message

                            Name: {name}
                            Email: {sender_email}

                            Message:
                            {message}
                            """,
                            from_addr=my_email
                            )


app = Flask(__name__)
app.secret_key = SECRET_KEY
bootstrap = Bootstrap(app)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        email = form.email.data
        name = form.name.data
        message = form.message.data
        try:
            send_email(name, email, message)
            flash("Your message has been sent successfully", "success")

        except Exception as e:
                # flash("Something went wrong. Please try again later.", "error")
                print(e)
                flash(f"Error: {e}", "error")
        return redirect(url_for("contact"))
    return render_template('contact.html',form=form)

if __name__ == '__main__':
    app.run(debug=True)
