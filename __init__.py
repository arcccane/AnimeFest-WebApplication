import os
import shelve
import sys

from flask import Flask, render_template, request, redirect, url_for, session, flash, \
    send_from_directory

import Art
import Cart
import DisplayNames
import Enquiry
import Event
import Feedback
import Product
import User
from Cart import Cart
from Forms import CreateProductForm, CreateFeedbackForm, CreateUserForm, CreatePostForm, LoginForm, CreateArtForm, \
    CreateEnquiryForm, CreateEventForm, AdminLoginForm, CreateAdminForm

app = Flask(__name__)

if os.path.exists('arts'):
    print('folder exists')
else:
    os.mkdir('arts')

if os.path.exists('posts'):
    print('folder exists')
else:
    os.mkdir('posts')

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif', '.mp4']
app.config['UPLOAD_PATH'] = 'arts'
app.config['UPLOAD_PATH2'] = 'posts'

app.secret_key = 'any_random_string'


@app.route('/home')
def home():
    events_dict = {}
    db = shelve.open('storage.db', 'r')
    try:
        events_dict = db['Events']
    except:
        print("Error in retrieving Event from storage.db.")

    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('home.html', count=len(events_list), events_list=events_list)


@app.route('/createFeedback', methods=['GET', 'POST'])
def create_feedback():
    create_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and create_feedback_form.validate():
        feedback_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            feedback_dict = db['Feedback']
        except:
            print("Error in retrieving Feedback from storage.db.")

        current_id = 0
        for id in feedback_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Feedback.Feedback.count_id = current_id
        user = Feedback.Feedback(create_feedback_form.ratings.data, create_feedback_form.remarks.data)
        feedback_dict[user.get_feedback_id()] = user
        db['Feedback'] = feedback_dict

        db.close()

        session['feedback_created'] = user.get_feedback_id()

        return redirect(url_for('Submit_Successfully'))
    return render_template('createFeedback.html', form=create_feedback_form)


@app.route('/retrieveFeedback')
def retrieve_feedback():
    feedback_dict = {}
    db = shelve.open('storage.db', 'r')

    try:
        feedback_dict = db['Feedback']
    except:
        print("Error in retrieving Feedback from storage.db.")

    db.close()

    feedback_list = []
    for key in feedback_dict:
        user = feedback_dict.get(key)
        feedback_list.append(user)

    ratings_dict = {
        '1': 'Very unsatisfied',
        '2': 'unsatisfied',
        '3': 'Neutral',
        '4': 'Satisfied',
        '5': 'Very Satisfied'
    }
    return render_template('retrieveFeedback.html', count=len(feedback_list), feedback_list=feedback_list,
                           ratings=ratings_dict)


@app.route('/updateFeedback/<int:id>/', methods=['GET', 'POST'])
def update_feedback(id):
    update_feedback_form = CreateFeedbackForm(request.form)
    if request.method == 'POST' and update_feedback_form.validate():
        db = shelve.open('storage.db', 'w')
        feedback_dict = db['Feedback']

        feedback = feedback_dict.get(id)
        feedback.set_ratings(update_feedback_form.ratings.data)
        feedback.set_remarks(update_feedback_form.remarks.data)

        db['Feedback'] = feedback_dict
        db.close()

        session['feedback_updated'] = feedback.get_feedback_id()

        return redirect(url_for('retrieve_feedback'))
    else:
        feedback_dict = {}
        db = shelve.open('storage.db', 'r')
        feedback_dict = db['Feedback']
        db.close()

        feedback = feedback_dict.get(id)
        update_feedback_form.ratings.data = feedback.get_ratings()
        update_feedback_form.remarks.data = feedback.get_remarks()

        return render_template('updateFeedback.html', form=update_feedback_form)


@app.route('/deleteFeedback/<int:id>', methods=['GET', 'POST'])
def delete_feedback(id):
    feedback_dict = {}
    db = shelve.open('storage.db', 'w')
    feedback_dict = db['Feedback']

    feedback_dict.pop(id)

    db['Feedback'] = feedback_dict
    db.close()

    return redirect(url_for('retrieve_feedback'))


@app.route('/createEnquiry', methods=['GET', 'POST'])
def create_enquiry():
    create_enquiry_form = CreateEnquiryForm(request.form)
    if request.method == 'POST' and create_enquiry_form.validate():
        enquirys_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            enquirys_dict = db['Enquirys']
        except:
            print("Error in retrieving Enquiries from enquiry.db.")

        current_id = 0
        for id in enquirys_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Enquiry.Enquiry.count_id = current_id
        enquiry = Enquiry.Enquiry(create_enquiry_form.name.data, create_enquiry_form.email.data,
                                  create_enquiry_form.topic.data, create_enquiry_form.enquirys.data)
        enquirys_dict[enquiry.get_enquiry_id()] = enquiry
        db['Enquirys'] = enquirys_dict

        db.close()

        session['enquiry_created'] = enquiry.get_name()

        return redirect(url_for('Enquiry_Successfully'))
    return render_template('createEnquiry.html', form=create_enquiry_form)


@app.route('/retrieveEnquiry')
def retrieve_enquirys():
    enquirys_dict = {}
    db = shelve.open('storage.db', 'r')

    try:
        enquirys_dict = db['Enquirys']
    except:
        print("Error in retrieving Enquiries from enquiry.db.")

    db.close()

    enquirys_list = []
    for key in enquirys_dict:
        enquiry = enquirys_dict.get(key)
        enquirys_list.append(enquiry)

    return render_template('retrieveEnquiry.html', count=len(enquirys_list), enquirys_list=enquirys_list)


@app.route('/updateEnquiry/<int:id>/', methods=['GET', 'POST'])
def update_enquiry(id):
    update_enquiry_form = CreateEnquiryForm(request.form)
    if request.method == 'POST' and update_enquiry_form.validate():
        db = shelve.open('storage.db', 'w')
        enquirys_dict = db['Enquirys']

        enquiry = enquirys_dict.get(id)
        enquiry.set_name(update_enquiry_form.name.data)
        enquiry.set_email(update_enquiry_form.email.data)
        enquiry.set_topic(update_enquiry_form.topic.data)
        enquiry.set_enquirys(update_enquiry_form.enquirys.data)

        db['Enquirys'] = enquirys_dict
        db.close()

        session['enquiry_updated'] = enquiry.get_name()

        return redirect(url_for('retrieve_enquirys'))
    else:
        enquirys_dict = {}
        db = shelve.open('storage.db', 'r')
        enquirys_dict = db['Enquirys']
        db.close()

        enquiry = enquirys_dict.get(id)
        update_enquiry_form.name.data = enquiry.get_name()
        update_enquiry_form.email.data = enquiry.get_email()
        update_enquiry_form.topic.data = enquiry.get_topic()
        update_enquiry_form.enquirys.data = enquiry.get_enquirys()

        return render_template('updateEnquiry.html', form=update_enquiry_form)


@app.route('/deleteEnquiry/<int:id>', methods=['POST'])
def delete_enquiry(id):
    enquirys_dict = {}
    db = shelve.open('storage.db', 'w')
    enquirys_dict = db['Enquirys']

    enquiry = enquirys_dict.pop(id)

    db['Enquirys'] = enquirys_dict
    db.close()

    session['enquiry_deleted'] = enquiry.get_name()

    return redirect(url_for('retrieve_enquirys'))


@app.route('/createEvent', methods=['GET', 'POST'])
def create_event():
    create_event_form = CreateEventForm(request.form)
    if request.method == 'POST' and create_event_form.validate():
        events_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            events_dict = db['Events']
        except:
            print("Error in retrieving Events from event.db.")

        current_id = 0
        for id in events_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Event.Event.count_id = current_id
        event = Event.Event(create_event_form.title.data, create_event_form.date.data, create_event_form.starttime.data,
                            create_event_form.endtime.data, create_event_form.url.data)
        events_dict[event.get_event_id()] = event
        db['Events'] = events_dict

        db.close()

        session['event_created'] = event.get_title()

        return redirect(url_for('home'))
    return render_template('createEvent.html', form=create_event_form)


@app.route('/retrieveEvent')
def retrieve_events():
    events_dict = {}
    db = shelve.open('storage.db', 'r')

    try:
        events_dict = db['Events']
    except:
        print("Error in retrieving Events from event.db.")
    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('retrieveEvent.html', count=len(events_list), events_list=events_list)


@app.route('/updateEvent/<int:id>/', methods=['GET', 'POST'])
def update_event(id):
    update_event_form = CreateEventForm(request.form)
    if request.method == 'POST' and update_event_form.validate():
        db = shelve.open('storage.db', 'w')
        events_dict = db['Events']

        event = events_dict.get(id)
        event.set_title(update_event_form.title.data)
        event.set_date(update_event_form.date.data)
        event.set_starttime(update_event_form.starttime.data)
        event.set_endtime(update_event_form.endtime.data)
        event.set_url(update_event_form.url.data)

        db['Events'] = events_dict
        db.close()

        session['event_updated'] = event.get_title()

        return redirect(url_for('retrieve_events'))
    else:
        events_dict = {}
        db = shelve.open('storage.db', 'r')
        events_dict = db['Events']
        db.close()

        event = events_dict.get(id)
        update_event_form.title.data = event.get_title()
        update_event_form.date.data = event.get_date()
        update_event_form.starttime.data = event.get_starttime()
        update_event_form.endtime.data = event.get_endtime()
        update_event_form.url.data = event.get_url()

        return render_template('updateEvent.html', form=update_event_form)


@app.route('/deleteEvent/<int:id>', methods=['POST'])
def delete_event(id):
    events_dict = {}
    db = shelve.open('storage.db', 'w')
    events_dict = db['Events']

    event = events_dict.pop(id)

    db['Events'] = events_dict
    db.close()

    session['event_deleted'] = event.get_title()

    return redirect(url_for('retrieve_events'))


@app.route('/SubmitSuccessfully')
def Submit_Successfully():
    return render_template('SubmitSuccessfully.html')


@app.route('/EnquirySuccessfully')
def Enquiry_Successfully():
    return render_template('EnquirySuccessfully.html')


# chen

@app.route('/createProduct', methods=['GET', 'POST'])
def create_product():
    create_product_form = CreateProductForm(request.form)
    if request.method == 'POST' and create_product_form.validate():
        products_dict = {}
        db = shelve.open('storage.db', 'c')

        try:
            products_dict = db['Products']
        except:
            print("Error in retrieving Products from storage.db.")

        product_id = 0
        for id in products_dict:
            if id >= product_id and id < sys.maxsize:
                product_id = id
            else:
                product_id = 0

        Product.Product.count_id = product_id

        product = Product.Product(create_product_form.product_name.data,
                                  create_product_form.product_description.data,
                                  create_product_form.price.data,
                                  create_product_form.promotion.data,
                                  create_product_form.company.data,
                                  create_product_form.category.data)
        products_dict[product.get_product_id()] = product
        db['Products'] = products_dict

        db.close()

        session['product_created'] = product.get_product_name()

        return redirect(url_for('retrieve_product'))
    return render_template('createProduct.html', form=create_product_form)


@app.route('/deleteProduct/<int:id>', methods=['POST'])
def delete_product(id):
    products_dict = {}
    db = shelve.open('storage.db', 'w')
    products_dict = db['Products']

    product = products_dict.get(id)

    products_dict.pop(id)

    db['Products'] = products_dict
    db.close()
    session['product_deleted'] = product.get_product_name()

    return redirect(url_for('retrieve_product'))


@app.route('/updateProduct/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    update_product_form = CreateProductForm(request.form)

    if request.method == 'POST' and update_product_form.validate():
        products_dict = {}
        db = shelve.open('storage.db', 'w')
        products_dict = db['Products']

        product = products_dict.get(id)
        product.set_product_name(update_product_form.product_name.data)
        product.set_product_description(update_product_form.product_description.data)
        product.set_price(update_product_form.price.data)
        product.set_promotion(update_product_form.promotion.data)
        product.set_company(update_product_form.company.data)
        product.set_category(update_product_form.category.data)

        db['Products'] = products_dict
        db.close()
        session['product_updated'] = product.get_product_name()

        return redirect(url_for('retrieve_product'))
    else:
        products_dict = {}
        db = shelve.open('storage.db', 'w')
        products_dict = db['Products']
        db.close()

        product = products_dict.get(id)

        update_product_form.product_name.data = product.get_product_name()
        update_product_form.product_description.data = product.get_product_description()
        update_product_form.price.data = product.get_price()
        update_product_form.promotion.data = product.get_promotion()
        update_product_form.company.data = product.get_company()
        update_product_form.category.data = product.get_category()

        return render_template('updateProduct.html', form=update_product_form)


@app.route('/retrieveProduct')
def retrieve_product():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('retrieveProduct.html', count=len(products_list), products_list=products_list)


@app.route('/shoppingCart/<int:product_id>', methods=['GET', 'POST'])
def shopping_cart(product_id):
    if request.method == 'POST' or 'GET':
        cart_dict = {}
        cart_db = shelve.open('cart.db', 'c')

        try:
            cart_dict = cart_db['Product']
        except:
            print("Error in retrieving Cart from cart.db.")

        cart = Cart()
        cart.add_product_id(product_id)
        cart.set_user_id(session['user_id'])
        cart_dict[cart.get_cart_id()] = cart
        cart_db['Product'] = cart_dict
        cart_db.close()

        cart_list = []
        product_dict = {}

        product_db = shelve.open('storage.db', 'c')

        try:
            product_dict = product_db['Products']
        except:
            print("Error in retrieving Cart from cart.db.")

        for cart_key in cart_dict:
            product_list = cart_dict[cart_key].get_product_list()
            for product in product_list:
                cart_list.append(product_dict[product])

    return render_template('shoppingCart.html', count=len(cart_list), cart_list=cart_list)


@app.route('/testcart')
def test_cart():
    products_dict = {}
    db = shelve.open('storage.db', 'c')

    try:
        products_dict = db['Products']
    except:
        print("Error in retrieving Products from storage.db.")

    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('testcart.html', count=len(products_list), products_list=products_list)


@app.route('/bs')
def bs():
    products_dict = {}
    db = shelve.open('storage.db', 'c')

    try:
        products_dict = db['Products']
    except:
        print("Error in retrieving Products from storage.db.")

    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('bs.html', count=len(products_list), products_list=products_list)


@app.route('/na')
def na():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('na.html', count=len(products_list), products_list=products_list)


@app.route('/n')
def n():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('n.html', count=len(products_list), products_list=products_list)


@app.route('/f')
def f():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('f.html', count=len(products_list), products_list=products_list)


@app.route('/p')
def p():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('p.html', count=len(products_list), products_list=products_list)


@app.route('/c')
def c():
    products_dict = {}
    db = shelve.open('storage.db', 'r')
    products_dict = db['Products']
    db.close()

    products_list = []
    for key in products_dict:
        product = products_dict.get(key)
        products_list.append(product)

    return render_template('c.html', count=len(products_list), products_list=products_list)


# ronald
@app.route('/ehome')
def ehome():
    return render_template('ehome.html')


@app.route('/createArt', methods=['GET', 'POST'])
def create_art():
    create_user_form = CreateArtForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        uploaded_file = request.files['file']
        filename, fileExtension = os.path.splitext(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_PATH'], filename + fileExtension)
        print(filename)
        print(fileExtension)
        print(filepath)
        uploaded_file.save(filepath)

        # store form data into shelve
        users_dict = {}
        db = shelve.open('arts.db', 'c')

        try:
            users_dict = db['Arts']
        except:
            print("Error in retrieving Users from arts.db.")

        current_id = 0
        for id in users_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        Art.Art.countid = current_id
        user = Art.Art(filepath, create_user_form.first_name.data, create_user_form.last_name.data,
                       create_user_form.email.data, create_user_form.phone.data, create_user_form.age.data,
                       create_user_form.gender.data, create_user_form.sname.data)
        users_dict[user.get_userid()] = user
        db['Arts'] = users_dict

        users_dict = db['Arts']
        user = users_dict[user.get_userid()]
        print(user.get_firstname(), user.get_lastname(), "was stored in arts.db successfully with user_id ==",
              user.get_userid())

        db.close()

        session['art_created'] = user.get_firstname() + ' ' + user.get_lastname()

        return redirect(url_for('view'))
    return render_template('createArt.html', form=create_user_form)


# User display POV (Fan Art Contest)
@app.route('/view')
def view():
    users_dict = {}
    db = shelve.open('arts.db', 'c')
    try:
        users_dict = db['Arts']
    except:
        print("Error in retrieving Feedback from arts.db.")

    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('view.html', count=len(users_list), users_list=users_list)


@app.route('/arts/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


# Employee POV (Fan Art Contest)
@app.route('/manage')
def manage():
    # print all shelve data
    users_dict = {}
    db = shelve.open('arts.db', 'c')
    try:
        users_dict = db['Arts']
    except:
        print("Error in retrieving Users from arts.db.")

    db.close()

    users_list = []
    for key in users_dict:
        user = users_dict.get(key)
        users_list.append(user)

    return render_template('manage.html', count=len(users_list), users_list=users_list)


@app.route('/updateArt/<int:id>/', methods=['GET', 'POST'])
def update_art(id):
    update_user_form = CreateArtForm(request.form)
    if request.method == 'POST' and update_user_form.validate():

        users_dict = {}
        db = shelve.open('arts.db', 'c')
        try:
            users_dict = db['Arts']
        except:
            print("Error in retrieving Users from arts.db.")

        user = users_dict.get(id)
        user.set_firstname(update_user_form.first_name.data)
        user.set_lastname(update_user_form.last_name.data)
        user.set_email(update_user_form.email.data)
        user.set_phone(update_user_form.phone.data)
        user.set_age(update_user_form.age.data)
        user.set_gender(update_user_form.gender.data)
        user.set_sname(update_user_form.sname.data)

        db['Arts'] = users_dict
        db.close()
        session['art_updated'] = user.get_firstname() + ' ' + user.get_lastname()

        return redirect(url_for('manage'))
    else:

        users_dict = {}
        db = shelve.open('arts.db', 'r')
        users_dict = db['Arts']
        db.close()

        user = users_dict.get(id)
        update_user_form.first_name.data = user.get_firstname()
        update_user_form.last_name.data = user.get_lastname()
        update_user_form.email.data = user.get_email()
        update_user_form.phone.data = user.get_phone()
        update_user_form.age.data = user.get_age()
        update_user_form.gender.data = user.get_gender()
        update_user_form.sname.data = user.get_sname()

        return render_template('updateArt.html', form=update_user_form)


@app.route('/deleteArt/<int:id>', methods=['POST'])
def delete_art(id):
    users_dict = {}
    db = shelve.open('arts.db', 'c')
    try:
        users_dict = db['Arts']
    except:
        print("Error in retrieving Users from arts.db.")

    user = users_dict.pop(id)

    db['Arts'] = users_dict
    db.close()
    session['art_deleted'] = user.get_firstname() + ' ' + user.get_lastname()

    return redirect(url_for('manage'))


@app.route('/createPost', methods=['GET', 'POST'])
def createPost():
    create_name_form = CreatePostForm(request.form)
    if request.method == 'POST' and create_name_form.validate():

        uploaded_file = request.files['file']
        filename, fileExtension = os.path.splitext(uploaded_file.filename)
        filepath = os.path.join(app.config['UPLOAD_PATH2'], filename + fileExtension)
        print(filename)
        print(fileExtension)
        print(filepath)
        uploaded_file.save(filepath)

        names_dict = {}
        namedb = shelve.open('posts.db', 'c')

        try:
            names_dict = namedb['Names']
        except:
            print("Error in retrieving Users from posts.db.")

        current_id = 0
        for id in names_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        DisplayNames.DisplayNames.countid = current_id
        name = DisplayNames.DisplayNames(filepath, create_name_form.dname.data, create_name_form.caption.data)
        names_dict[name.get_nameid()] = name
        namedb['Names'] = names_dict

        names_dict = namedb['Names']
        name = names_dict[name.get_nameid()]
        print(name.get_dname(), "was stored in posts.db successfully with name_id ==", name.get_nameid())

        namedb.close()
        session['post_created'] = name.get_dname()

        return redirect(url_for('animedia'))
    return render_template('createPost.html', form=create_name_form)


@app.route('/animedia')
def animedia():
    names_dict = {}
    namedb = shelve.open('posts.db', 'c')
    try:
        names_dict = namedb['Names']
    except:
        print("Error in retrieving Users from posts.db.")

    namedb.close()

    names_list = []
    for key in names_dict:
        name = names_dict.get(key)
        names_list.append(name)

    return render_template('animedia.html', count=len(names_list), names_list=names_list)


@app.route('/posts/<filename>')
def upload2(filename):
    return send_from_directory(app.config['UPLOAD_PATH2'], filename)


@app.route('/animediamanage')
def animediamanage():
    # print all shelve data
    names_dict = {}
    namedb = shelve.open('posts.db', 'c')
    try:
        names_dict = namedb['Names']
    except:
        print("Error in retrieving Users from posts.db.")

    namedb.close()

    names_list = []
    for key in names_dict:
        name = names_dict.get(key)
        names_list.append(name)

    return render_template('animediamanage.html', count=len(names_list), names_list=names_list)


@app.route('/updatePost/<int:id>/', methods=['GET', 'POST'])
def updatePost(id):
    update_post_form = CreatePostForm(request.form)
    if request.method == 'POST' and update_post_form.validate():
        names_dict = {}
        namedb = shelve.open('posts.db', 'c')
        try:
            names_dict = namedb['Names']
        except:
            print("Error in retrieving Users from posts.db.")

        name = names_dict.get(id)
        name.set_dname(update_post_form.dname.data)
        name.set_caption(update_post_form.caption.data)

        namedb['Names'] = names_dict
        namedb.close()

        session['post_updated'] = name.get_dname()

        return redirect(url_for('animediamanage'))
    else:
        names_dict = {}
        namedb = shelve.open('posts.db', 'r')
        names_dict = namedb['Names']
        namedb.close()

        name = names_dict.get(id)
        update_post_form.dname.data = name.get_dname()
        update_post_form.caption.data = name.get_caption()

        return render_template('updatePost.html', form=update_post_form)


@app.route('/deletePost/<int:id>', methods=['POST'])
def delete_post(id):
    names_dict = {}
    namedb = shelve.open('posts.db', 'c')
    try:
        names_dict = namedb['Names']
    except:
        print("Error in retrieving Users from posts.db.")

    name = names_dict.pop(id)

    namedb['Names'] = names_dict
    namedb.close()

    session['post_deleted'] = name.get_dname()

    return redirect(url_for('animediamanage'))


# Jiayu

@app.route('/')
def main():
    session["admin_account"] = False
    session["customer_account"] = False
    session["Account_Status"] = False
    return render_template('home.html')


@app.route('/contactUs')
def contact_us():
    return render_template("contactUs.html")


@app.route('/createUser', methods=['GET', 'POST'])
def create_user():
    create_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and create_user_form.validate():
        userz_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        current_id = 0
        for id in userz_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        User.User.count_id = current_id
        user = User.User(create_user_form.first_name.data, create_user_form.last_name.data,
                         create_user_form.gender.data, create_user_form.username.data, create_user_form.password.data)
        userz_dict[user.get_user_id()] = user
        db['Userz'] = userz_dict

        db.close()

        session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('login'))
    return render_template('createUser.html', form=create_user_form)


@app.route('/createAdmin', methods=['GET', 'POST'])
def create_admin():
    create_admin_form = CreateAdminForm(request.form)
    if request.method == 'POST' and create_admin_form.validate():
        adminz_dict = {}
        db = shelve.open('storage.db', 'c')
        try:
            adminz_dict = db['adminz']
        except:
            print("Error in retrieving Users from storage.db.")

        current_id = 0
        for id in adminz_dict:
            if id >= current_id and id < sys.maxsize:
                current_id = id
            else:
                current_id = 0

        User.User.count_id = current_id
        user = User.User(create_admin_form.first_name.data, create_admin_form.last_name.data,
                         create_admin_form.gender.data, create_admin_form.username.data,
                         create_admin_form.password.data)
        adminz_dict[user.get_user_id()] = user
        db['adminz'] = adminz_dict

        db.close()

        session['user_created'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('adminlogin'))
    return render_template('createAdmin.html', form=create_admin_form)


@app.route('/retrieveUsers')
def retrieve_users():
    if session.get('admin_account') == True:

        adminz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            adminz_dict = db['adminz']
        except:
            print("Error in retrieving Admins from storage.db.")

        db.close()

        adminz_list = []
        for key in adminz_dict:
            admin = adminz_dict.get(key)
            adminz_list.append(admin)

        userz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")
        db.close()

        userz_list = []
        for key in userz_dict:
            user = userz_dict.get(key)
            userz_list.append(user)

        return render_template('retrieveUsers.html', count=len(userz_list), userz_list=userz_list,
                               countz=len(adminz_list), adminz_list=adminz_list)
    return redirect(url_for('profile'))


@app.route('/updateUser/<int:id>/', methods=['GET', 'POST'])
def update_user(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        userz_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        user = userz_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_username(update_user_form.username.data)
        user.set_password(update_user_form.password.data)

        db['Userz'] = userz_dict
        db.close()

        session['user_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))
    else:
        userz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        db.close()

        user = userz_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.username.data = user.get_username()
        update_user_form.password.data = user.get_password()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/updateAdmin/<int:id>/', methods=['GET', 'POST'])
def update_Admin(id):
    update_user_form = CreateUserForm(request.form)
    if request.method == 'POST' and update_user_form.validate():
        adminz_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            adminz_dict = db['adminz']
        except:
            print("Error in retrieving Admins from storage.db.")

        user = adminz_dict.get(id)
        user.set_first_name(update_user_form.first_name.data)
        user.set_last_name(update_user_form.last_name.data)
        user.set_gender(update_user_form.gender.data)
        user.set_username(update_user_form.username.data)
        user.set_password(update_user_form.password.data)

        db['adminz'] = adminz_dict
        db.close()

        session['admin_updated'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))
    else:
        adminz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            adminz_dict = db['adminz']
        except:
            print("Error in retrieving Admins from storage.db.")

        db.close()

        user = adminz_dict.get(id)
        update_user_form.first_name.data = user.get_first_name()
        update_user_form.last_name.data = user.get_last_name()
        update_user_form.gender.data = user.get_gender()
        update_user_form.username.data = user.get_username()
        update_user_form.password.data = user.get_password()

        return render_template('updateUser.html', form=update_user_form)


@app.route('/deleteUser/<int:id>', methods=['POST'])
def delete_user(id):
    if session["admin_account"] == True:
        userz_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        user = userz_dict.pop(id)

        db['Userz'] = userz_dict
        db.close()

        session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

        return redirect(url_for('retrieve_users'))

    elif session["customer_account"] == True:
        userz_dict = {}
        db = shelve.open('storage.db', 'w')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        user = userz_dict.pop(id)

        db['Userz'] = userz_dict
        db.close()

        session['user_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

        session["customer_account"] = True
        session["admin_account"] = False
        session["Account_Status"] = False

        return redirect(url_for('accountdeleted'))


@app.route('/deleteAdmin/<int:id>', methods=['POST'])
def delete_admin(id):
    adminz_dict = {}
    db = shelve.open('storage.db', 'w')
    try:
        adminz_dict = db['adminz']
    except:
        print("Error in retrieving Admins from storage.db.")

    user = adminz_dict.pop(id)

    db['adminz'] = adminz_dict
    db.close()

    session['admin_deleted'] = user.get_first_name() + ' ' + user.get_last_name()

    return redirect(url_for('retrieve_users'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/login', methods=["GET", "POST"])
def login():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        userz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        db.close()

        for userid in userz_dict:
            user = userz_dict.get(userid)
            if login_form.username.data == user.get_username() and login_form.password.data == user.get_password():
                LoginForm.profileuser = login_form.username.data
                session["Account_Status"] = True
                if user.get_username() == "admin" and user.get_password() == "admins":
                    flash('Welcome! ' + login_form.username.data)
                    session['admin_account'] = True
                    session["customer_account"] = False
                    session["user_id"] = user.get_user_id()
                    print("Admin has logged in.")
                    return redirect(url_for('home'))
                elif user.get_username() == login_form.username.data and user.get_password() == login_form.password.data:
                    flash('Welcome! ' + login_form.username.data)
                    session["customer_account"] = True
                    session["admin_account"] = False
                    session["user_id"] = user.get_user_id()
                    print("Customer: " + user.get_first_name() + " " + user.get_last_name() + " has logged in.")
                    return redirect(url_for('home'))

        flash('Wrong Username of Password. Please try again.')
        # error = 'Invalid Credentials. Please try again.'
        # print(user.get_username())
        # print(user.get_password())
        # print(error)
        return render_template('login.html', form=login_form)

    return render_template('login.html', form=login_form)


@app.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    login_form = AdminLoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        adminz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            adminz_dict = db['adminz']
        except:
            print("Error in retrieving Admins from storage.db.")

        db.close()

        for userid in adminz_dict:
            user = adminz_dict.get(userid)
            if login_form.username.data == user.get_username() and login_form.password.data == user.get_password():
                LoginForm.profileuser = login_form.username.data
                session["Account_Status"] = True
                if user.get_username() == login_form.username.data and user.get_password() == login_form.password.data:
                    flash('Welcome! ' + login_form.username.data)
                    session['admin_account'] = True
                    session["customer_account"] = False
                    session["user_id"] = user.get_user_id()
                    print("Admin: " + user.get_first_name() + " " + user.get_last_name() + " has logged in.")
                    return redirect(url_for('home'))
                else:
                    print("Admin Login Error")
                    flash("Invalid Admin Account. Please try again.")
                    return render_template('adminlogin.html', form=login_form)

        flash('Wrong Username of Password. Please try again.')
        # error = 'Invalid Credentials. Please try again.'
        # print(user.get_username())
        # print(user.get_password())
        # print(error)
        return render_template('adminlogin.html', form=login_form)

    return render_template('adminlogin.html', form=login_form)


@app.route('/customerlogin', methods=['GET', 'POST'])
def customerlogin():
    login_form = LoginForm(request.form)
    if request.method == 'POST' and login_form.validate():
        userz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        db.close()

        for userid in userz_dict:
            user = userz_dict.get(userid)
            if login_form.username.data == user.get_username() and login_form.password.data == user.get_password():
                LoginForm.profileuser = login_form.username.data
                session["Account_Status"] = True
                if user.get_username() == login_form.username.data and user.get_password() == login_form.password.data:
                    flash('Welcome! ' + login_form.username.data)
                    session["customer_account"] = True
                    session["admin_account"] = False
                    session["user_id"] = user.get_user_id()
                    print("Customer: " + user.get_first_name() + " " + user.get_last_name() + " has logged in.")
                    return redirect(url_for('home'))
                else:
                    flash("Invalid Customer Account. Please try again.")
                    return render_template('customerlogin.html', form=login_form)

        flash('Wrong Username of Password. Please try again.')
        # error = 'Invalid Credentials. Please try again.'
        # print(user.get_username())
        # print(user.get_password())
        # print(error)
        return render_template('customerlogin.html', form=login_form)

    return render_template('customerlogin.html', form=login_form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    login_form = LoginForm(request.form)
    if session.get('customer_account') == True:
        userz_dict = {}
        db = shelve.open('storage.db', 'r')
        try:
            userz_dict = db['Userz']
        except:
            print("Error in retrieving Users from storage.db.")

        db.close()

        userz_list = []
        for userid in userz_dict:
            user = userz_dict.get(userid)
            if user.get_username() == login_form.profileuser:
                userz_list.append(user)
        return render_template('profile.html', count=len(userz_list), userz_list=userz_list)
    return render_template('profile.html')


@app.route("/Logout", methods=["GET", "POST"])
def logout():
    if request.method == 'GET':
        session["customer_account"] = True
        session["admin_account"] = False
        session["Account_Status"] = False
        return render_template("Logout.html")


@app.route("/accountdeleted", methods=["GET", "POST"])
def accountdeleted():
    if request.method == 'GET':
        session["customer_account"] = True
        session["admin_account"] = False
        session["Account_Status"] = False
        return render_template("accountdeleted.html")


@app.route('/Event1')
def event1():
    events_dict = {}
    db = shelve.open('storage.db', 'r')
    events_dict = db['Events']
    db.close()

    events_list = []
    for key in events_dict:
        event = events_dict.get(key)
        events_list.append(event)

    return render_template('Event1.html', count=len(events_list), events_list=events_list)


if __name__ == '__main__':
    app.run()
