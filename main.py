import random
import re
import os

from flask import render_template, request, jsonify, redirect

from __init__ import app, Field
from dbdata import URLData


@app.route('/', methods=['POST', 'GET'])
def main():
    form = Field()
    if form.validate_on_submit():
        url_root = request.url_root
        clean_url = re.compile(r'^(?:http|ftp)s?|://|www.| ', re.IGNORECASE)
        long_url = re.sub(clean_url, '', request.form.get('short_url_field'))
        shorted_url = url_root + '{}'.format(random.randint(100, 999))
        url_data_from_db = URLData(long_url=long_url, short_url=shorted_url, host_url=url_root)

        return jsonify(data={'message': '{}'.format(url_data_from_db.get_short_url())})
    return render_template('index.html', form=form)


@app.route('/<int:url_id>')
def redirect_url(url_id):
    url_id = request.url
    host_url = request.host
    getting_long_url = URLData(long_url='', short_url=url_id, host_url=host_url)

    return redirect('http://' + '{}'.format(getting_long_url.get_long_url()))

@app.errorhandler(404)
def page_not_found(e):
    page_not_found_image = os.path.join(app.config['UPLOAD_FOLDER'], '404.png')
    return render_template('404.html', image=page_not_found_image), 404

if __name__ == '__main__':
    app.run()
