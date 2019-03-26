# ShareBNB
ShareBNB is an online marketplace and hospitality service which allows for users to arrange or offer lodging. The primary focus is to give hosts the opportunity to sublease their rented apartment(s), and for guests to search for lodging using filter such as dates and location. Apartment owners will be able to access rental information and be given the chance to decline requests for sublease.

### Motivation
In the subject TDT4140 at NTNU we will work together as a team to create an application. The product owner/customer requested that we developed an application which is accessible via a website. We manage the project using the agile management process Scrum.

# Installation and use
1. Clone the project to your computer with `git clone <url>`
2. Navigate to the cloned directory
3. **(Optional)** Create a virtual environment and activate it before step *5.*<br>
*(Tip for PyCharm users):* Open this folder in PyCharm. Then Settings -> Project interpreter -> add... -> velg python3
5. Type `pip install -r requirements.txt` in command line (with the virtual environment activated `source envname/bin/activate`)
6. `python manage.py makemigrations`
7. `python manage.py migrate`
8. `python manage.py createsuperuser`
9. `python manage.py runserver`

# Tech/framework used
*  Heroku for hosting
*  Amazon S3 buckets for image hosting
*  Django as backend framework
    *  Django imagekit to process images
    *  Mixer to create test data
*  Jquery and Vue to handle front-end data
*  SCSS for a better and easier css structure

# Credits
**Gruppe 15:**<br>
Agnar Bjørnstad<br>
Ingvild Telle Finsås<br>
Joel Nicolaysen<br>
Markus Vagstad<br>
Tor Martin Wang<br>
Tobias Wulvik<br>

# License
The MIT License (MIT)

Copyright © 2019 Gruppe 15 (see above)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.