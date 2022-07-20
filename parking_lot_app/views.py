from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from .models import Parking, Slot
from datetime import datetime
from .utility_functions import get_number_of_digits
import pyqrcode
import png
from pyqrcode import QRCode
from parking_lot_project.settings import BASE_DIR
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os


# Create your views here.


def index(request):
    parking = Parking.objects.all()
    slots = Slot.objects.all()
    context = {
        "parking": parking,
        "slots": slots[0]
    }
    return render(request, 'parking_lot_app/index.html', context)


def entry(request):
    slots = Slot.objects.get(id=1)
    if request.method == 'POST':
        current_id = slots.counter
        num_of_digits = get_number_of_digits(current_id)
        rem = 19 - num_of_digits
        vehicle_type = request.POST['vehicle_type']
        if vehicle_type == '2-WHEELER':
            if slots.two_wheeler_count == 0:
                return render(request, 'parking_lot_app/index.html', {'slots': slots, 'message': "2-Wheeler Parking is Full"})
            start = 'T'
            amount = 30
        elif vehicle_type == '4-WHEELER':
            if slots.four_wheeler_count == 0:
                return render(request, 'parking_lot_app/index.html', {'slots': slots, 'message': "4-Wheeler Parking is Full"})
            start = 'F'
            amount = 50
        ref_id = start + str('0'*rem) + str(current_id)
        obj = Parking(in_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                      out_time=None, vehicle_type=vehicle_type, amount=amount, reference_id=ref_id)
        obj.save()
        slots.counter = current_id + 1
        if vehicle_type == '2-WHEELER':
            slots.two_wheeler_count -= 1
        elif vehicle_type == '4-WHEELER':
            slots.four_wheeler_count -= 1
        slots.save()
        print(BASE_DIR)
        pyqrcode.create(ref_id).png(
            str(BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/" + str(ref_id) + ".png", scale=6)
        context = {
            'parking': obj,
            'slots': slots,
            'path': str(BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/" + str(ref_id) + ".png"
        }
        return render(request, "parking_lot_app/entry_details.html", context)
    return render(request, 'parking_lot_app/entry.html', {'current_datetime': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                                                          "slots": slots
                                                          })


def print_ticket(request, ref):
    slots = Slot.objects.get(id=1)
    parking = Parking.objects.get(reference_id=ref)
    print("            WELCOME TO XYZ            ")
    print("--------------------------------------")
    print("  In-time:", parking.in_time)
    print("  Vehicle Type:", parking.vehicle_type)
    print("  QR Image Here")
    # try:
    #     img = mpimg.imread(str(
    #         BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/" + str(ref) + ".png")
    #     imgplot = plt.imshow(img)
    #     plt.show()
    # except NSInternalInconsistencyException:
    #     print("QR Image Here")
    # except NSException:
    #     print("QR Image Here")
    # except Exception:
    #     print("QR Image Here")
    print("  Parking ID:", parking.reference_id)
    if parking.vehicle_type == "2-WHEELER":
        print("  First Hour ₹30")
    elif parking.vehicle_type == "4-WHEELER":
        print("  First Hour ₹50")
    print("  Additional ₹20/hour")
    print("--------------------------------------")
    print("  Ticket Lost Charges ₹200")
    context = {
        'parking': parking,
        'slots': slots
    }
    os.remove(str(BASE_DIR) +
              "/parking_lot_app/static/parking_lot_app/images/" + str(ref) + ".png")
    return render(request, "parking_lot_app/index.html", context)


def exit(request):
    slots = Slot.objects.get(id=1)
    context = {}
    context['slots'] = slots
    if request.method == 'POST':
        ref_id = request.POST['referenceid']
        parking = Parking.objects.get(reference_id=ref_id)
        if not parking.amount_received:
            if parking.vehicle_type == '2-WHEELER':
                slots.two_wheeler_count += 1
            elif parking.vehicle_type == '4-WHEELER':
                slots.four_wheeler_count += 1
            parking.amount_received = True
            slots.save()
            parking.save()
            os.remove(str(
                BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/" + str(ref_id) + ".png")
            context['message'] = "Exit Successful"
            return render(request, 'parking_lot_app/index.html', context)
        else:
            context['message'] = "Vehicle amount already received!"
            return render(request, 'parking_lot_app/index.html', context)
    files = os.listdir(
        str(BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/")
    if len(files) > 0:
        filename = files[0]
        reference = filename.split('.')[0]
        parking = Parking.objects.get(reference_id=reference)
        in_time = str(parking.in_time).split('+')[0]
        in_time = datetime.strptime(in_time, "%Y-%m-%d %H:%M:%S")
        parking.out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        out_time = datetime.strptime(
            str(parking.out_time), "%Y-%m-%d %H:%M:%S")
        difference = out_time - in_time
        hours = difference.total_seconds() / 3600
        if int(str(hours).split('.')[1]) / 60 > 5:
            hours = int(str(hours).split('.')[0]) + 1
        else:
            hours = int(str(hours).split('.')[0])
        if parking.vehicle_type == '2-WHEELER':
            parking.amount = 30 + (hours - 1) * 20
        elif parking.vehicle_type == '4-WHEELER':
            parking.amount = 50 + (hours - 1) * 20
        parking.save()
        parking = Parking.objects.get(reference_id=reference)
        context['parking'] = parking
    else:
        return render(request, 'parking_lot_app/index.html', {'slots': slots, 'message': "Could not find a valid QR, scan again!"})
    return render(request, 'parking_lot_app/exit.html', context)


def ticket_lost(request):
    slots = Slot.objects.get(id=1)
    context = {
        'slots': slots
    }
    if request.method == "POST":
        vehicle_type = request.POST['vehicle_type']
        if vehicle_type == "2-WHEELER":
            if slots.two_wheeler_count < 5:
                slots.two_wheeler_count += 1
            else:
                context['message'] = "That's not possible. 2-Wheeler parking as per system was empty. He might have entered wrongfully. Charge him ₹200 anyway and let him go!!"
                return render(request, 'parking_lot_app/index.html', context)
        elif vehicle_type == "4-WHEELER":
            if slots.four_wheeler_count < 5:
                slots.four_wheeler_count += 1
            else:
                context['message'] = "That's not possible. 4-Wheeler parking as per system was empty. He might have entered wrongfully. Charge him ₹300 anyway and let him go!!"
                return render(request, 'parking_lot_app/index.html', context)
        slots.save()
        slots = Slot.objects.get(id=1)
        context['slots'] = slots
        context['message'] = "Exit Successful! Ha ha that was fun :D"
        return render(request, 'parking_lot_app/index.html', context)
    return render(request, 'parking_lot_app/ticket_lost.html', context)


def manual_exit(request):
    slots = Slot.objects.get(id=1)
    context = {}
    context['slots'] = slots
    if request.method == 'POST':
        ref_id = request.POST['referenceid']
        try:
            parking = Parking.objects.get(reference_id=ref_id)
        except Exception:
            context['message'] = "Check the entered reference ID"
            return render(request, 'parking_lot_app/manual_exit.html', context)
        if not parking.amount_received:
            if parking.vehicle_type == '2-WHEELER':
                slots.two_wheeler_count += 1
            elif parking.vehicle_type == '4-WHEELER':
                slots.four_wheeler_count += 1
            parking.amount_received = True
            slots.save()
            parking.save()
            # os.remove(str(
            #     BASE_DIR) + "/parking_lot_app/static/parking_lot_app/images/" + str(ref_id) + ".png")
            context['message'] = "Exit Successful"
            return render(request, 'parking_lot_app/index.html', context)
        else:
            context['message'] = "Vehicle amount already received!"
            return render(request, 'parking_lot_app/index.html', context)
    return render(request, 'parking_lot_app/manual_exit.html', context)
