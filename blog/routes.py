
# blog/routes.py

from flask import render_template, request, redirect, flash
from blog import app
from blog.models import Entry, db
from blog.forms import EntryForm


@app.route("/")
def index():
      all_posts = Entry.query.filter_by(is_published=True).order_by(Entry.pub_date.desc())
      return render_template("homepage.html", all_posts=all_posts)

#   return render_template("base.html")


@app.route("/new-post/", methods=["GET", "POST"])
@app.route("/edit-post/<int:entry_id>", methods=["GET", "POST"])
def manage_entry(entry_id=None):
    entry = Entry.query.get_or_404(entry_id) if entry_id else None
    form = EntryForm(obj=entry) if entry else EntryForm()
    errors = None

    if request.method == 'POST':
        if form.validate_on_submit():
            if entry:
                form.populate_obj(entry)
            else:
                entry = Entry(
                    title=form.title.data,
                    body=form.body.data,
                    is_published=form.is_published.data
                )
                db.session.add(entry)
            db.session.commit()
            flash('Wpis został zaktualizowany pomyślnie!' if entry_id else 'Wpis został opublikowany pomyślnie!', 'success')
            return redirect('/')
        else:
            errors = form.errors

    return render_template("entry_form.html", form=form, errors=errors)
   
   
 