from docpoc import get_model
from google.cloud import firestore
from docpoc import storage
from flask import Blueprint, current_app, redirect, render_template, request, \
    url_for


crud = Blueprint('crud', __name__,
                 template_folder='templates')


def upload_image_file(file):

    if not file:
        return None
    print ('reached upto here')
    print (file.filename)
    print (file.content_type)
    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )
    print ('after file upload')
    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url


@crud.route("/")
def logged_in():
    return render_template('login_page.html')


@crud.route("/documents")
def list():
    db = firestore.Client()
    #db = firebase.database()

    docs = db.collection(u'kycdocs').get()
    print (docs)
    documents = docs

    return render_template(
        "listdocuments.html",
        documents=documents
       )


@crud.route('/<id>')
def view():
    #doc = get_model().read(id)
    return render_template("view.html")


@crud.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        data = request.form.to_dict(flat=True)

        print (data)
        image_url = upload_image_file(request.files.get('image'))

        if image_url:
            data['imageUrl'] = image_url

        doc = get_model().add_data(data)

        return redirect(url_for('.list'))

    return render_template("mainform.html", action="Add", doc={})

