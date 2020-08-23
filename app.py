# импорт библиотек
from selenium import webdriver
from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
from flask import jsonify, render_template, request, redirect, flash
from .forms import WebsiteForm
# путь к драйверу chrome
chromedriver = '/usr/local/bin/chromedriver'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
address = request.form.get('address')

@app.route('/', methods=['POST', 'GET'])
@app.route('/add_website', methods=['POST', 'GET'])
def website():
    website_form = WebsiteForm()
    if request.method == 'POST':
        if website_form.validate_on_submit():
            address = request.form.get('address')
            task = Tasks(address=address, timestamp=datetime.now(), task_status='NOT_STARTED')
            db.session.add(task)
            db.session.commit()
            parse_website_text.delay(task._id)
            return redirect('/')
        error = "Form was not validated"
        browser.get(address)
        return render_template('error.html',form=website_form,error = error)
    return render_template('add_website.html', form=website_form)


@app.route('/results')
def get_results():
	with app.app_context():
        res = requests.get(address) 
        words_count=0
        if res.ok:
            words = res.text.split()
            words_count = words.count("Python")
            
        result = Results(address=address, words_count=words_count, http_status_code=res.status_code)
        task = Tasks.query.get(_id)
        task.task_status = 'FINISHED'
        db.session.add(result)
        db.session.commit()
  return render_template('results.html', results=results)       