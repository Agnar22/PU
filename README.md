# ShareBNB
ShareBNB is an online marketplace and hospitality service which allows for users to arrange or offer lodging. The primary focus is to give hosts the opportunity to sublease their rented apartment(s), and for guests to search for lodging using filter such as dates and location. Apartment owners will be able to access rental information and be given the chance to decline requests for sublease.

### Motivation
In the subject TDT4140 at NTNU we will work together as a team to create an application. The product owner/customer requested that we developed an application which is accessible via a website. We manage the project using the agile management process Scrum.

### Requirements
This project requires the following technologies to be pre-installed:
* Git (can be installed from https://git-scm.com/downloads)
* Python 3 (can be installed from https://www.python.org/downloads)
# Installation and use
1. Open the CMD/terminal, navigate to a desired folder and clone the project to your computer with `git clone https://gitlab.stud.idi.ntnu.no/programvareutvikling-v19/gruppe-15.git`
2. Now navigate to the cloned directory by typing `cd gruppe-15` in command line
3. **(Optional)** Create a virtual environment and activate it before step *5.*<br>
*(Tip for PyCharm users):* Open this folder in PyCharm. Then File -> Settings -> Project interpreter -> add... -> velg python3
5. Type `pip install -r requirements.txt` in command line (with the virtual environment activated `source envname/bin/activate`)
6. Type `python manage.py makemigrations` in command line
7. Type `python manage.py migrate` in command line
8. Type `python manage.py createsuperuser` in command line
9. Type `python manage.py runserver` in command line
10. The product can now be accessed by typing `http://localhost:8000` in your web-browser 

# Tech/framework used
*  Heroku for web-hosting
*  Amazon S3 buckets for image hosting
*  Django as backend framework
    *  Django imagekit to process images
    *  Mixer to create test data
*  Jquery and Vue to handle front-end data
*  SCSS for a better and easier css structure

# Testing
* Open the CMD/terminal and navigate to the "gruppe-15" folder in the cloned project
    * Type `python manage.py test` in command line; runs all test
    * Type `python manage.py test <appname>`; runs all tests for a specific app

# Credits
**Gruppe 15:**<br>
Agnar Martin Bjørnstad<br>
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