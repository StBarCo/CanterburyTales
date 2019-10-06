# CanterburyTales
Uses Django in Python and Postgresql (check official documentation for installation)

## Purpose
To create a space where both clergy and laity can find teaching resources which are faithful to the Anglican way of Christianity. Users will share a course, write a brief description and upload all files (multiple files will be zipped together?). Courses use tags for categories and are targeted to a certain age of learners (audience).

Registered users can upvote any course

## Basic Structure
+ Authentication is handled by the standard User model.
+ Profile model is a proxy model extending the user via a 1-1 relationship
+ Courses model is the centerpiece. All data for a course is stored here:
  + tags is a ManytoMany relationship with Tag table
  + upvotes is ManytoMany relationship with Profile (users can only upvote a single course one time)

## Style Inspiration
I am unashamed to admit that the style is largely borrowed from http://hackr.io. Canterbury tales needs to find its own color scheme. I want it to be consistent, simple, and easy to read - whatever is best to that end is good. Just happen to like the hackr.io UI a lot.

Uses Bootstrap4 via the django-bootstrap4 plugin, and also material icons.


## To-Do
#### Course
##### #index
- [X] Chage the field Course.audience to be an Integer Range.
- [X] Style age range slider and add JS to display readable ages: [0: 0, 4: Pre-K, 5: Kindergarten.... 15-18: High School... Etc]
      e.g. a slider from 15-60 would have readable display "High Shool through Adults" or similar.

- [ ] Complete styling for Course.index view (especially course list and filters) based on 
      https://hackr.io/tutorials/learn-python 
- [ ] Add AJAX calls to filter course list.

- [ ] Add search bar and function to search course title, description and tags.

- [ ] Extract the course list into its own template so that it can be used to also list all of a User's shared courses and upboted courses (to templates/courses/course_list.html)
- [ ] Create AJAX call for new upovte.

- [ ] Imitate the welcome banner of http://hackr.io. Canterbury tales is... Here's how it works...

##### #new/edit
- [X] Implement the age range slider for course creation.
- [ ] Add appropriate div container and formatting.
- [ ] Show files input and impletent file storage and zipping multiples(?)
- [ ] Create good way for user to seamlessly create new tags while selecting.

##### #detail
- [ ] Create detail view. Perhaps based on profile view? Don't have specific vision for how it looks.

##### #delete
- [ ] Create function and add button with warning.

#### Profile
##### #detail
- [ ] Finish styling detail page
- [ ] Add related lists/tabs for courses submitted, & courses upvoted.

##### #edit
- [ ] Make edit page (inline editing of profile page?) or reuse signup form.

#### User
- [ ] Add forgot password function(?).
- [ ] Add basic styling to login and registration forms.
     
#### General
- [ ] use templates well
- [ ] Add better style to header /template/base.html

#### Permissions
- [ ] implement all permissions
- [ ] logged out: view all users (not emails) and all courses. Propmted to login/create account on upvote or download.
- [ ] logged in: Same as logged out, but can upvote/download. Also can edit own profile and own courses (eventually can comment)
- [ ] editor: Same as logged in, but can... um... ban users? Not sure.

### Beautification
- [ ] general beautification



## General Deploy Notes for Django (Deploying to Google Cloud)
+ Change USE_CLOUD_PROXY => True, start proxy server and run any migrations (manage.py makemigrations + migrate)
+ Organize any new static files (manage.py collectstatic)
+ Deploy to cloud (gcloud app deploy)



