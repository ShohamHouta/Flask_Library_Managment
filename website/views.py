from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

import json

views = Blueprint("views", __name__)


@views.route("/", methods=['GET', 'POST'])
@login_required
def Home():
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is to short!", category="error")
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note Created!", category='success')

    return render_template("Home.html", user=current_user)


@views.route("/delete-note", methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note["noteId"]
    note = Note.query.get(noteId)

    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            flash("Note Deleted!", category="success")

    return jsonify({})
