from datetime import datetime

from django.shortcuts import render, redirect, get_object_or_404
from .models import Product, Contact, Orders, OrderUpdate, User, Admin, ProductReview, Address
# from mac.loginapp.models import UserModel

from math import ceil
import json
from django.db.models import Avg
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
from django.http import HttpResponse
#

from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    return render(request, 'template.html')

import os
import streamlit as st
import pickle
import time
import langchain
from langchain_openai import OpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.chains.qa_with_sources.loading import load_qa_with_sources_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import UnstructuredURLLoader
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

from dotenv import load_dotenv
load_dotenv()

from .models import Session, Url, Question


def index(request):
    username = request.session.get('username')
    sessions = Session.objects.filter(userName=username)
    context = {
        'sessions': sessions
    }
    return render(request, 'shop/index.html', context)

def getsession(request, session_id):
    psession = Session.objects.filter(id=session_id).first()
    username = request.session.get('username')
    sessions = Session.objects.filter(userName=username)

    urls = Url.objects.filter(sessionId=psession.id)

    context = {
        'sessions': sessions,
        'psession': psession,
        'urls': urls
    }

    # print(psession.id)
    # print("aaaaaa")
    # return HttpResponse("ok")
    return render(request, 'shop/index.html', context)

from django.conf import settings
def process(request):
    if request.method == "POST":
        sessionName = request.POST.get('session')
        userName = request.session.get("username")

        session, created = Session.objects.get_or_create(sessionName=sessionName, userName=userName)
        request.session["sessionname"] = sessionName
        request.session["sessionid"] = session.id

        # urls = request.POST.getlist('urls[]')
        # names = request.POST.getlist('names[]')
        #
        # for url, urlName in zip(urls, names):
        #     Url.objects.get_or_create(
        #         urlName=urlName,
        #         userName = userName,
        #         url=url,
        #         sessionId = session.id
        #     )
        #
        # # for url in urls:
        # #     print(url)
        #
        # file_path = "faiss_store_openai.pkl"
        # string_list = []
        # from bs4 import BeautifulSoup
        # import requests
        # class MyObject:
        #     def __init__(self, page_content, metadata):
        #         self.page_content = page_content
        #         self.metadata = metadata
        #
        # def get_page_data(url):
        #     try:
        #         response = requests.get(url)
        #         response.raise_for_status()  # Raise an HTTPError for bad responses
        #
        #         soup = BeautifulSoup(response.text, 'html.parser')
        #         page_content = soup.get_text()
        #         meta_url = soup.find('meta', {'property': 'og:url'})
        #
        #         if meta_url:
        #             url = meta_url.get('content')
        #
        #         metadata = {'source': url}
        #         string_list.append(page_content)
        #         print(page_content)
        #         print(metadata)
        #         return MyObject(page_content, metadata)
        #
        #     except requests.exceptions.HTTPError as http_err:
        #         print(f"HTTP error occurred: {http_err}")
        #     except requests.exceptions.RequestException as req_err:
        #         print(f"Request error occurred: {req_err}")
        #     except Exception as e:
        #         print(f"An unexpected error occurred: {e}")
        #
        #     return None
        #
        # data = []
        # for url in urls:
        #     page_data = get_page_data(url)
        #     data.append(page_data)
        #     # print(page_data.page_content)
        #     # print(page_data.metadata)
        #
        # for url, urlName in zip(urls, names):
        #     Url.objects.get_or_create(
        #         urlName=urlName,
        #         userName = userName,
        #         url=url,
        #         sessionId = session.id
        #     )
        #
        #
        # images = request.FILES.getlist('images[]')
        # save_dir = os.path.join(settings.BASE_DIR, 'shop', 'info_images')
        # if not os.path.exists(save_dir):
        #     os.makedirs(save_dir)
        #
        # for image in images:
        #     image_path = os.path.join(save_dir, image.name)
        #     with open(image_path, 'wb') as f:
        #         for chunk in image.chunks():
        #             f.write(chunk)
        #     from PIL import Image
        #     from pytesseract import pytesseract
        #     path_to_tesseract = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
        #     img = Image.open(image_path)
        #     pytesseract.tesseract_cmd = path_to_tesseract
        #     text = pytesseract.image_to_string(img)
        #     page_content = text[:-1]
        #     metadata = {'source': image_path }
        #     # print(image_path)
        #     # print(text[:-1])
        #     data.append(MyObject(page_content, metadata))
        #
        #     Url.objects.get_or_create(
        #         urlName=image.name,
        #         userName=userName,
        #         url=image_path,
        #         sessionId=session.id
        #     )
        #
        # text_splitter = RecursiveCharacterTextSplitter(
        #     chunk_size=1000,
        #     chunk_overlap=200
        # )
        #
        # docs = text_splitter.split_documents(data)
        # # print(type(docs))
        # for ind, el in enumerate(docs):
        #     print(ind , el, sep="\n\n")
        # print(docs)
        #
        # embeddings = OpenAIEmbeddings()
        #
        # vectorIndex = FAISS.from_documents(docs, embeddings)
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(current_dir, 'vector_index')
        # vectorIndex.save_local(filename)
        # #     vectorstore_openai = FAISS.from_documents(docs, embeddings)
        # time.sleep(2)

        # return HttpResponse("URLs processed successfully")

        username = request.session.get('username')
        sessions = Session.objects.filter(userName=username)
        questions = Question.objects.filter(sessionId=session.id)
        context = {
            'questions': questions,
            'sessions': sessions
        }
        return render(request, 'shop/answer.html', context)
    else:
        print(request.session["sessionname"])
    return HttpResponse("URLs processed successfully")

def answer(request):
    if request.method == "POST":
        query = request.POST.get('question')
        # print(query)
        # import os
        # from langchain.vectorstores import FAISS
        # current_dir = os.path.dirname(os.path.realpath(__file__))
        # filename = os.path.join(current_dir, 'vector_index')
        # embeddings = OpenAIEmbeddings()
        # vectorIndex = FAISS.load_local(filename, embeddings)
        # llm = OpenAI(temperature=0.9, max_tokens=500)
        #
        # chain = RetrievalQAWithSourcesChain.from_llm(llm=llm, retriever=vectorIndex.as_retriever())
        #
        # langchain.debug = True
        # chain({"question": query})
        #
        # result = chain({"question": query})
        #
        # answer = result["answer"]
        # url = result["sources"]
        #
        # print(result["answer"])
        # print(result["sources"])

        return HttpResponse("Okay")

        answer = "Silicon Valley"
        url = "SV url"

        sessionid = request.POST.get('sessionid')
        sessionname = request.POST.get('sessionname')
        # print(sessionid)
        # print(sessionname)
        # return JsonResponse({'error': 'Invalid request method'})

        question = Question(
            question=query,
            answer=answer,
            url=url,
            sessionId=sessionid # Associate the question with the session
        )
        question.save()

        questions = Question.objects.filter(sessionId=sessionid)
        username = request.session.get('username')
        sessions = Session.objects.filter(userName=username)
        context = {
            'sessions': sessions,
            'questions': questions
        }

        return render(request, 'shop/answer.html', context)
    else:
        print(request.session["sessionname"])
        print("aaa")
        return JsonResponse({'error': 'Invalid request method'})


def sessions(request):
    username = request.session.get("username")
    print(username)
    sessions = Session.objects.filter(userName=username)

    sessions_data = []
    for session in sessions:
        urls = Url.objects.filter(sessionId=session.id)
        questions = Question.objects.filter(sessionId=session.id)
        sessions_data.append({
            'sessionName': session.sessionName,
            'urls': urls,
            'questions': questions
        })

    context = {
        'sessions' : sessions,
        'sessiondetails': sessions_data
    }
    return render(request, 'shop/sessions.html', context)


def searchMatch(query, item):
    '''return true only if query matches the item'''
    if query in item.desc.lower() or query in item.product_name.lower() or query in item.category.lower():
        return True
    else:
        return False

def search(request):
    query = request.GET.get('search','')
    query = query.lower()
    print(query)
    # return HttpResponse("ok")
    allProds = []
    catprods = Product.objects.values('category', 'id')
    cats = {item['category'] for item in catprods}
    for cat in cats:
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]

        n = len(prod)
        nSlides = n // 4 + ceil((n / 4) - (n // 4))
        if len(prod) != 0:
            allProds.append([prod, range(1, nSlides), nSlides])
    params = {'allProds': allProds, "msg": "", "query": query}
    if len(allProds) == 0 or len(query)<3:
        params = {'msg': "Please make sure to enter relevant search query"}

    return render(request, 'shop/search.html', params)


def about(request):
    return render(request, 'shop/answer.html')


def contact(request):
    if request.method=="POST":
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        phone = request.POST.get('phone', '')
        desc = request.POST.get('desc', '')
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        print(orderId)
        print(email)
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})

                order = order[0]
                porder = {
                    "order_id" : order.order_id,
                    "items_json" : order.items_json,
                    "shipto" : order.shipto,
                    "shipfrom" : order.shipfrom,
                    "email" : order.email,
                    "address" : order.address,
                    "state" : order.state,
                    "city" : order.city,
                    "zip_code" : order.zip_code,
                    "phone" : order.phone,
                    "amount" : order.amount,
                }
                #
                # print(updates);
                response = json.dumps([updates, porder], default=str)
                # response = json.dumps([updates, order], default=str)
                return HttpResponse(response)
            else:
                print("noo")
                return HttpResponse('{}')
        except Exception as e:
            print("lnbcdl")
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')



# def productView(request, myid):
#
#     # Fetch the product using the id
#     product = Product.objects.filter(id=myid)
#     return render(request, 'shop/prodView.html', {'product':product[0]})


def checkout(request):
    if request.method=="POST":
        items_json = request.POST.get('itemsJson', '')
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        address = request.POST.get('address1', '') + " " + request.POST.get('address2', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        zip_code = request.POST.get('zip_code', '')
        phone = request.POST.get('phone', '')
        amount = request.POST.get('amount', '')
        print(amount)
        order = Orders(items_json=items_json, shipfrom= request.session.get("username"), shipto=name, email=email, address=address, city=city,
                       state=state, zip_code=zip_code, phone=phone, amount = amount)
        order.save()
        update = OrderUpdate(order_id=order.order_id, update_desc="The order has been placed")
        update.save()
        thank = True
        id = order.order_id
        return render(request, 'shop/checkout.html', {'thank':thank, 'id': id})
    try:
        request.session.get("username")
        addresses = Address.objects.filter(user=request.session.get("username"))
        return render(request, 'shop/checkout.html', {'addresses': addresses})
    except:
        return render(request, 'shop/login.html')

# def orders(request):
#     # Retrieve orders for the current user (filtered by shipfrom)
#     username = request.session.get("username", "")
#     user_orders = Orders.objects.filter(shipfrom=username)
#
#     # Loop through orders and modify item_json to include product.image
#     for order in user_orders:
#         print(type(order.items_json))
#         print(order.items_json)
#         order.items_json = json.loads(order.items_json)
#         print(type(order.items_json))
#         print(order.items_json)
#
#
#
#         for key, item_data in order.items_json.items():
#             product_id = key[2:]  # Assuming your product key is in the format "pr10", "pr11", etc.
#             product = Product.objects.get(id=product_id)
#             item_data.append(str(product.image))  # Add product.image URL to the item_data
#
#     # Pass the orders data to the template
#     context = {'orders': user_orders}
#     return render(request, 'shop/orders.html', context)


def orders(request):
    # Retrieve orders for the current user (filtered by shipfrom)
    username = request.session["username"]
    user_orders = Orders.objects.filter(shipfrom=username)
    # print(username)

    # Loop through orders and modify item_json to include product.image
    for order in user_orders:
        # print(type(order.items_json))
        # print(order.items_json)
        order.items_json = json.loads(order.items_json)
        # print(type(order.items_json))
        # print(order.items_json)



        for key, item_data in order.items_json.items():
            product_id = key[2:]  # Assuming your product key is in the format "pr10", "pr11", etc.
            product = Product.objects.get(id=product_id)
            item_data.append(str(product.image))  # Add product.image URL to the item_data
            rating = -1
            if ProductReview.objects.filter(product=product, username=username).exists():
                product_reviev  = ProductReview.objects.filter(product=product, username=username)[0]
                # print(product_reviev.product, product_reviev.rating)
                rating = product_reviev.rating
            # print(product_id, username)
            # print(product_reviev)
            item_data.append(rating)

    # Pass the orders data to the template
    context = {'orders': user_orders, 'len': len(user_orders)}
    return render(request, 'shop/orders.html', context)


def productView(request, myid):
    # Fetch the product using the id
    product = get_object_or_404(Product, id=myid)

    # Fetch product reviews including comments
    reviews = ProductReview.objects.filter(product=product)
    reviewCount = len(reviews)


    # Calculate average rating
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']

    return render(request, 'shop/prodView.html',
                  {'product': product, 'reviews': reviews,'reviewCount': reviewCount, 'average_rating': average_rating})

def add_rating(request, order_id, product_key):
    if request.method == 'POST':
        # order = # Fetch the order based on order_id (if needed)
        product_id = int(product_key[2:])  # Extract product_id from "pr" + product_id
        product = get_object_or_404(Product, id=product_id)

        username = request.session["username"]  # Adjust this based on your authentication logic
        rating = int(request.POST.get('rating', 0))

        print(product, username, rating, "eee")
        # comment = "None"
        # if ProductReview.objects.filter(product=product, username=username).exists():
        #     if ProductReview.objects.filter(product=product, username=username)[0].comment:
        #         comment = ProductReview.objects.filter(product=product, username=username)[0]
        #     ProductReview.objects.filter(product=product, username=username)[0].delete()
        # pr = ProductReview()
        # pr.product = product
        # pr.username = username
        # pr.rating = rating
        # pr.comment = comment
        # pr.save()

        existing_review = ProductReview.objects.filter(product=product, username=username).first()

        if existing_review:
            # Update the existing ProductReview instance with a new comment
            existing_review.rating = rating
            existing_review.save()
        else:
            # Create a new ProductReview instance with a new comment
            pr = ProductReview(product=product, username=username, rating=rating)
            pr.save()

    return redirect('/orders')

def add_comment(request, order_id, product_key):
    if request.method == 'POST':

        product_id = int(product_key[2:])  # Extract product_id from "pr" + product_id
        product = get_object_or_404(Product, id=product_id)

        username = request.session.get("username")  # Adjust this based on your authentication logic
        comment_text = request.POST.get('comment', '')
        print("aaa")
        print(comment_text)

            # Check if a ProductReview instance exists for the given product and username
        existing_review = ProductReview.objects.filter(product=product, username=username).first()

        if existing_review:
            # Update the existing ProductReview instance with a new comment
            existing_review.comment = comment_text
            existing_review.save()
        else:
            # Create a new ProductReview instance with a new comment
            pr = ProductReview(product=product, username=username, comment=comment_text)
            pr.save()

    return redirect('/orders')


def invoice(request, order_id):
    username = request.session["username"]
    order = Orders.objects.filter(order_id = order_id)
    order = order[0]
    print(order)

    order.items_json = json.loads(order.items_json)

    for key, item_data in order.items_json.items():
        product_id = key[2:]  # Assuming your product key is in the format "pr10", "pr11", etc.
        product = Product.objects.get(id=product_id)
        item_data.append(str(product.image))  # Add product.image URL to the item_data
        item_data.append(int(item_data[0])*int(item_data[2]))
    # Pass the orders data to the template
    print(order)
    context = {'order': order}
    return render(request, 'shop/invoice.html', context)



def search_recommendations(request):
    if request.method == 'GET':
        search_input = request.GET.get('search_input', '')
        if len(search_input)<2:
            return JsonResponse([], safe=False)
        print(search_input)

        # Perform a case-insensitive search on both product_name and category
        results = Product.objects.filter(
            Q(product_name__icontains=search_input)
        ).values('product_name')[:5]

        recommendations = [result['product_name'] for result in results]
        print(recommendations)

        return JsonResponse(recommendations, safe=False)
    else:
        return JsonResponse([], safe=False)


from django.shortcuts import redirect
def my_logout_page(request):
    if "username" in request.session:
        print(request.session["username"])
        request.session.clear()


    if "adminusername" in request.session:
        request.session.clear()
    return redirect("/login")


from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Orders

def adminpage(request):
    if request.session["adminusername"]:
        # Calculate total number of unique ship_from values
        ship_from_count = Orders.objects.values('shipfrom').distinct().count()

        # Calculate total number of orders
        total_orders = Orders.objects.count()

        # Calculate total revenue
        total_revenue = Orders.objects.aggregate(Sum('amount'))['amount__sum'] or 0

        context = {
            'ship_from_count': ship_from_count,
            'total_orders': total_orders,
            'total_revenue': total_revenue,
        }

        return render(request, 'shop/adminpage.html', context)
    else:
        return redirect("/login/admin")



from django.shortcuts import render
from .models import Orders
import json

def allOrders(request):
    if request.session.get("adminusername"):
        # Fetch all orders in descending order of timestamp
        all_orders = Orders.objects.all().order_by('-timestamp')

        # Parse items_json to extract product names
        for order in all_orders:
            items_data = json.loads(order.items_json)
            product_names = [item_data[1] for item_data in items_data.values()]
            order.product_names = ', '.join(product_names)

        context = {
            'all_orders': all_orders,
        }

        return render(request, 'shop/allOrders.html', context)
    else:
        return redirect("/login/admin")


def addProductPage(request):
    return render(request, 'shop/addProduct.html', {})

def updateStatusPage(request):
    return render(request, 'shop/updateProduct.html', {})

from .models import Product


def addtoDB(request):
    if request.method == 'POST' and request.session.get("adminusername"):
        if request.method == 'POST':
            # Process the form data and save it to the database
            product_name = request.POST['product_name']
            category = request.POST['category']
            subcategory = request.POST['subcategory']
            price = request.POST['price']
            desc = request.POST['desc']
            pub_date_str = request.POST['pub_date']
            image = request.FILES.get('image', None)

            try:
                # Validate and convert pub_date to a datetime object
                pub_date = datetime.strptime(pub_date_str, "%Y-%m-%d").date()
            except ValueError:
                # Handle invalid date format
                return render(request, 'adminpage.html', {'error_message': 'Invalid date format'})

            # Check if required fields are filled correctly
            if not (product_name and category and price and desc and pub_date):
                return render(request, 'adminpage.html', {'error_message': 'All fields are required'})

            # Save the product to the database
            Product.objects.create(
                product_name=product_name,
                category=category,
                subcategory=subcategory,
                price=price,
                desc=desc,
                pub_date=pub_date,
                image=image
            )

        # Redirect to a success page or any other desired page
        return redirect('/adminpage/addProduct/?success=1')

    # Render the form or any other page if not a POST request
    return redirect('/login')

from django.utils import timezone
def updatecurrentStatus(request):
    if request.method == 'POST' and request.session.get("adminusername") :
        order_id = request.POST.get('order_id')
        update_desc = request.POST.get('update_desc')

        # Perform any additional validation if needed

        # Save the order update
        order_update = OrderUpdate(order_id=order_id, update_desc=update_desc, timestamp=timezone.now())
        order_update.save()

        # Redirect to a success page or the same page
        return redirect('/adminpage/updateStatus/?success=1')  # Adjust the URL name or use a specific URL

    return redirect('/login')


def address(request):
    username = request.session["username"]
    print(username)

    # Retrieve user details
    # user = UserModel.objects.get(username=username)

    # Retrieve all addresses for the given username
    addresses = Address.objects.filter(user=username)

    # for address in addresses:
    #     print(address.address_id)

    context = {'addresses': addresses}
    return render(request, 'shop/address.html', context)


def add_address(request):
    if request.method == 'POST':
        # Retrieve form data from POST request
        shipto = request.POST.get('shipto')
        email = request.POST.get('email')
        address_text = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip_code = request.POST.get('zip_code')
        phone = request.POST.get('phone')


        # Create a new Address instance and save it to the database
        new_address = Address(
            shipto=shipto,
            email=email,
            address=address_text,
            city=city,
            state=state,
            zip_code=zip_code,
            phone=phone,
            user=request.session["username"]
        )
        new_address.save()

        return redirect('/profile/address')  # Adjust the redirect URL as needed

    return render(request, '/profile/address')


def delete(request, address_id):
    address = Address.objects.get(address_id=address_id)
    address.delete()
    return redirect('/profile/address')






