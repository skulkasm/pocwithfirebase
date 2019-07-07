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
    for doc in docs:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    documents = docs

    return render_template(
        "listdocuments.html",
        documents=documents
       )


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


@crud.route('/search', methods=['GET','POST'])
def search():
    if request.method == 'POST':
        db = firestore.Client()
        region = request.form['region']
        country = request.form['country']

        return redirect(url_for('.searchresults', region=region, country=country))

    return render_template("search.html")


@crud.route('/searchresults')
def searchresults():
    db = firestore.Client()
    print('in search results function')
    region = request.args.get('region')
    print(region)
    country = request.args.get('country')
    print(country)
    qry = db.collection(u'kycdocs').where(u'region', u'==', region)
    documents = qry.get()
    for doc in documents:
        print(u'{} => {}'.format(doc.id, doc.to_dict()))

    return render_template("searchresults.html", documents=documents)
