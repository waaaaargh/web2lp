from tempfile import mkdtemp
from os.path import join
from shutil import rmtree
from subprocess import STDOUT, check_output, CalledProcessError

from web2lp import app

from werkzeug import secure_filename
from flask import render_template
from flask_wtf.file import FileField, FileRequired
from flask.ext.wtf import Form


@app.route("/", methods=['GET', 'POST'])
def show_upload_form():
    class FileUploadForm(Form):
        document = FileField("document",
                             validators=[FileRequired()])

    form = FileUploadForm()

    if form.validate_on_submit():
        dirname = mkdtemp()
        filename = join(dirname,
                        secure_filename(form.document.data.filename))
        form.document.data.save(filename)

        try:
            check_output([app.config['LP_BINARY'], "-h",
                          app.config["CUPS_HOST"] + ":" +
                          str(app.config['CUPS_PORT']),
                          "-d", app.config["CUPS_PRINTER"], filename],
                         stderr=STDOUT)
            return render_template('result.html', error=False)
        except CalledProcessError as e:
            return render_template("result.html", error=True,
                                   cmd=" ".join(e.cmd), output=e.output)
        finally:
            rmtree(dirname)
    return render_template('upload.html', form=form)
