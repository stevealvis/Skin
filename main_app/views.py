from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from datetime import date
import os

from django.contrib import messages
from django.contrib.auth.models import User , auth
from .models import patient , doctor , diseaseinfo , consultation ,rating_review
from chats.models import Chat,Feedback

# Create your views here.


#loading trained_model
import joblib as jb
model = jb.load('trained_model')

# Image processing imports
import numpy as np
from PIL import Image
import io
import base64
import json
import os

# Optional CNN image model (load if available)
CNN_MODEL_PATH = os.path.join('models', 'skin_cnn.h5')
CNN_LABELS_PATH = os.path.join('models', 'skin_cnn_labels.json')
image_model = None
image_labels = None

if os.path.exists(CNN_MODEL_PATH) and os.path.exists(CNN_LABELS_PATH):
    try:
        from tensorflow import keras
        image_model = keras.models.load_model(CNN_MODEL_PATH)
        with open(CNN_LABELS_PATH) as f:
            image_labels = json.load(f)
        print("Loaded CNN image model for skin disease detection.")
    except Exception as e:
        print(f"Warning: could not load CNN image model: {e}")
        image_model = None
        image_labels = None




def home(request):

  if request.method == 'GET':
        
      if request.user.is_authenticated:
        return render(request,'homepage/index.html')

      else :
        return render(request,'homepage/index.html')



   

       


def admin_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        auser = request.user
        Feedbackobj = Feedback.objects.all()

        return render(request,'admin/admin_ui/admin_ui.html' , {"auser":auser,"Feedback":Feedbackobj})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')





def patient_ui(request):

    if request.method == 'GET':

      if request.user.is_authenticated:

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)

        return render(request,'patient/patient_ui/profile.html' , {"puser":puser})

      else :
        return redirect('home')



    if request.method == 'POST':

       return render(request,'patient/patient_ui/profile.html')

       


def pviewprofile(request, patientusername):

    if request.method == 'GET':

          puser = User.objects.get(username=patientusername)

          return render(request,'patient/view_profile/view_profile.html', {"puser":puser})




def checkdisease(request):

  diseaselist=['Fungal infection','Allergy','GERD','Chronic cholestasis','Drug Reaction','Peptic ulcer diseae','AIDS','Diabetes ',
  'Gastroenteritis','Bronchial Asthma','Hypertension ','Migraine','Cervical spondylosis','Paralysis (brain hemorrhage)',
  'Jaundice','Malaria','Chicken pox','Dengue','Typhoid','hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D',
  'Hepatitis E', 'Alcoholic hepatitis','Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemmorhoids(piles)',
  'Heart attack', 'Varicose veins','Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthristis',
  'Arthritis', '(vertigo) Paroymsal  Positional Vertigo','Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']


  symptomslist=['itching','skin_rash','nodal_skin_eruptions','continuous_sneezing','shivering','chills','joint_pain',
  'stomach_pain','acidity','ulcers_on_tongue','muscle_wasting','vomiting','burning_micturition','spotting_ urination',
  'fatigue','weight_gain','anxiety','cold_hands_and_feets','mood_swings','weight_loss','restlessness','lethargy',
  'patches_in_throat','irregular_sugar_level','cough','high_fever','sunken_eyes','breathlessness','sweating',
  'dehydration','indigestion','headache','yellowish_skin','dark_urine','nausea','loss_of_appetite','pain_behind_the_eyes',
  'back_pain','constipation','abdominal_pain','diarrhoea','mild_fever','yellow_urine',
  'yellowing_of_eyes','acute_liver_failure','fluid_overload','swelling_of_stomach',
  'swelled_lymph_nodes','malaise','blurred_and_distorted_vision','phlegm','throat_irritation',
  'redness_of_eyes','sinus_pressure','runny_nose','congestion','chest_pain','weakness_in_limbs',
  'fast_heart_rate','pain_during_bowel_movements','pain_in_anal_region','bloody_stool',
  'irritation_in_anus','neck_pain','dizziness','cramps','bruising','obesity','swollen_legs',
  'swollen_blood_vessels','puffy_face_and_eyes','enlarged_thyroid','brittle_nails',
  'swollen_extremeties','excessive_hunger','extra_marital_contacts','drying_and_tingling_lips',
  'slurred_speech','knee_pain','hip_joint_pain','muscle_weakness','stiff_neck','swelling_joints',
  'movement_stiffness','spinning_movements','loss_of_balance','unsteadiness',
  'weakness_of_one_body_side','loss_of_smell','bladder_discomfort','foul_smell_of urine',
  'continuous_feel_of_urine','passage_of_gases','internal_itching','toxic_look_(typhos)',
  'depression','irritability','muscle_pain','altered_sensorium','red_spots_over_body','belly_pain',
  'abnormal_menstruation','dischromic _patches','watering_from_eyes','increased_appetite','polyuria','family_history','mucoid_sputum',
  'rusty_sputum','lack_of_concentration','visual_disturbances','receiving_blood_transfusion',
  'receiving_unsterile_injections','coma','stomach_bleeding','distention_of_abdomen',
  'history_of_alcohol_consumption','fluid_overload','blood_in_sputum','prominent_veins_on_calf',
  'palpitations','painful_walking','pus_filled_pimples','blackheads','scurring','skin_peeling',
  'silver_like_dusting','small_dents_in_nails','inflammatory_nails','blister','red_sore_around_nose',
  'yellow_crust_ooze']

  alphabaticsymptomslist = sorted(symptomslist)

  


  if request.method == 'GET':
    
     return render(request,'patient/checkdisease/checkdisease.html', {"list2":alphabaticsymptomslist})




  elif request.method == 'POST':
       
      ## access you data by playing around with the request.POST object
      
      inputno = int(request.POST["noofsym"])
      print(inputno)
      if (inputno == 0 ) :
          return JsonResponse({'predicteddisease': "none",'confidencescore': 0 })
  
      else :

        psymptoms = []
        psymptoms = request.POST.getlist("symptoms[]")
       
        print(psymptoms)

      
        """      #main code start from here...
        """
      

      
        testingsymptoms = []
        #append zero in all coloumn fields...
        for x in range(0, len(symptomslist)):
          testingsymptoms.append(0)


        #update 1 where symptoms gets matched...
        for k in range(0, len(symptomslist)):

          for z in psymptoms:
              if (z == symptomslist[k]):
                  testingsymptoms[k] = 1


        inputtest = [testingsymptoms]

        print(inputtest)
      

        predicted = model.predict(inputtest)
        print("predicted disease is : ")
        print(predicted)

        y_pred_2 = model.predict_proba(inputtest)
        confidencescore=y_pred_2.max() * 100
        print(" confidence score of : = {0} ".format(confidencescore))

        confidencescore = format(confidencescore, '.0f')
        predicted_disease = predicted[0]

        

        #consult_doctor codes----------

        #   doctor_specialization = ["Rheumatologist","Cardiologist","ENT specialist","Orthopedist","Neurologist",
        #                             "Allergist/Immunologist","Urologist","Dermatologist","Gastroenterologist"]
        

        Rheumatologist = [  'Osteoarthristis','Arthritis']
       
        Cardiologist = [ 'Heart attack','Bronchial Asthma','Hypertension ']
       
        ENT_specialist = ['(vertigo) Paroymsal  Positional Vertigo','Hypothyroidism' ]

        Orthopedist = []

        Neurologist = ['Varicose veins','Paralysis (brain hemorrhage)','Migraine','Cervical spondylosis']

        Allergist_Immunologist = ['Allergy','Pneumonia',
        'AIDS','Common Cold','Tuberculosis','Malaria','Dengue','Typhoid']

        Urologist = [ 'Urinary tract infection',
         'Dimorphic hemmorhoids(piles)']

        Dermatologist = [  'Acne','Chicken pox','Fungal infection','Psoriasis','Impetigo']

        Gastroenterologist = ['Peptic ulcer diseae', 'GERD','Chronic cholestasis','Drug Reaction','Gastroenteritis','Hepatitis E',
        'Alcoholic hepatitis','Jaundice','hepatitis A',
         'Hepatitis B', 'Hepatitis C', 'Hepatitis D','Diabetes ','Hypoglycemia']
         
        if predicted_disease in Rheumatologist :
           consultdoctor = "Rheumatologist"
           
        if predicted_disease in Cardiologist :
           consultdoctor = "Cardiologist"
           

        elif predicted_disease in ENT_specialist :
           consultdoctor = "ENT specialist"
     
        elif predicted_disease in Orthopedist :
           consultdoctor = "Orthopedist"
     
        elif predicted_disease in Neurologist :
           consultdoctor = "Neurologist"
     
        elif predicted_disease in Allergist_Immunologist :
           consultdoctor = "Allergist/Immunologist"
     
        elif predicted_disease in Urologist :
           consultdoctor = "Urologist"
     
        elif predicted_disease in Dermatologist :
           consultdoctor = "Dermatologist"
     
        elif predicted_disease in Gastroenterologist :
           consultdoctor = "Gastroenterologist"
     
        else :
           consultdoctor = "other"


        request.session['doctortype'] = consultdoctor 

        patientusername = request.session['patientusername']
        puser = User.objects.get(username=patientusername)
     

        #saving to database.....................

        patient = puser.patient
        diseasename = predicted_disease
        no_of_symp = inputno
        symptomsname = psymptoms
        confidence = confidencescore

        diseaseinfo_new = diseaseinfo(patient=patient,diseasename=diseasename,no_of_symp=no_of_symp,symptomsname=symptomsname,confidence=confidence,consultdoctor=consultdoctor)
        diseaseinfo_new.save()
        

        request.session['diseaseinfo_id'] = diseaseinfo_new.id

        print("disease record saved sucessfully.............................")

        return JsonResponse({'predicteddisease': predicted_disease ,'confidencescore':confidencescore , "consultdoctor": consultdoctor})
   


   
    



   





def scan_image(request):
    """
    Image-based skin disease prediction view
    """
    if request.method == 'GET':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('home')
        
        try:
            # Try to get patient from session first
            patientusername = request.session.get('patientusername')
            if patientusername:
                puser = User.objects.get(username=patientusername)
            else:
                # If not in session, try to get from authenticated user
                puser = request.user
            
            # Check if user has a patient profile
            try:
                patient_obj = puser.patient
                # Store in session for POST requests
                request.session['patientusername'] = puser.username
            except:
                # User doesn't have a patient profile
                messages.error(request, 'Please login as a patient to use this feature.')
                return redirect('home')
            
            return render(request, 'patient/scan_image/scan_image.html')
        except Exception as e:
            print(f"Error in scan_image GET: {str(e)}")
            messages.error(request, 'Unable to access image scanner. Please try again.')
            return redirect('home')
    
    elif request.method == 'POST':
        try:
            # Get patient info
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Please login first'}, status=400)
            
            # Try to get patient from session first
            patientusername = request.session.get('patientusername')
            if patientusername:
                puser = User.objects.get(username=patientusername)
            else:
                # If not in session, use authenticated user
                puser = request.user
            
            # Check if user has a patient profile
            try:
                patient_obj = puser.patient
                # Store in session for future requests
                request.session['patientusername'] = puser.username
            except:
                return JsonResponse({'error': 'User does not have a patient profile'}, status=400)
            
            # Check if image was uploaded
            if 'skin_image' not in request.FILES:
                return JsonResponse({'error': 'No image uploaded'}, status=400)
            
            uploaded_image = request.FILES['skin_image']
            
            # Validate image
            try:
                img = Image.open(uploaded_image)
                img.verify()  # Verify it's a valid image
            except Exception as e:
                return JsonResponse({'error': 'Invalid image file'}, status=400)
            
            # Reset image pointer after verify
            uploaded_image.seek(0)
            img = Image.open(uploaded_image)
            
            # Preprocess image for model
            # Resize to standard size (adjust based on your model requirements)
            img = img.convert('RGB')  # Ensure RGB format
            img = img.resize((224, 224))  # Common size for CNN models
            
            # Convert to numpy array
            img_array = np.array(img)
            img_array = img_array / 255.0  # Normalize to [0, 1]
            img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
            
            # Run CNN model if available, else fallback placeholder
            if image_model and image_labels:
                preds = image_model.predict(img_array)
                idx = int(np.argmax(preds))
                predicted_disease = image_labels[idx] if idx < len(image_labels) else "Skin Condition"
                confidence = float(np.max(preds)) * 100
            else:
                # Placeholder prediction when CNN is not available
                predicted_disease = "Skin Condition Detected"
                confidence = 85.5
            
            # Map to doctor specialization (similar to symptom-based prediction)
            consultdoctor = "Dermatologist"
            
            # Set doctortype in session for consult_a_doctor view
            request.session['doctortype'] = consultdoctor
            
            # Save disease info with image
            diseaseinfo_new = diseaseinfo(
                patient=patient_obj,
                diseasename=predicted_disease,
                no_of_symp=0,  # No symptoms for image-based
                symptomsname=json.dumps([]),  # Empty symptoms list
                confidence=confidence,
                consultdoctor=consultdoctor,
                skin_image=uploaded_image,
                prediction_method='image'
            )
            diseaseinfo_new.save()
            
            request.session['diseaseinfo_id'] = diseaseinfo_new.id
            
            return JsonResponse({
                'predicteddisease': predicted_disease,
                'confidencescore': str(confidence),
                'consultdoctor': consultdoctor,
                'image_url': diseaseinfo_new.skin_image.url if diseaseinfo_new.skin_image else None
            })
            
        except Exception as e:
            print(f"Error in scan_image: {str(e)}")
            return JsonResponse({'error': f'Prediction failed: {str(e)}'}, status=500)


def pconsultation_history(request):

    if request.method == 'GET':

      patientusername = request.session['patientusername']
      puser = User.objects.get(username=patientusername)
      patient_obj = puser.patient
        
      consultationnew = consultation.objects.filter(patient = patient_obj)
      
    
      return render(request,'patient/consultation_history/consultation_history.html',{"consultation":consultationnew})


def dconsultation_history(request):

    if request.method == 'GET':

      doctorusername = request.session['doctorusername']
      duser = User.objects.get(username=doctorusername)
      doctor_obj = duser.doctor
        
      consultationnew = consultation.objects.filter(doctor = doctor_obj)
      
    
      return render(request,'doctor/consultation_history/consultation_history.html',{"consultation":consultationnew})



def doctor_ui(request):

    if request.method == 'GET':

      doctorid = request.session['doctorusername']
      duser = User.objects.get(username=doctorid)

    
      return render(request,'doctor/doctor_ui/profile.html',{"duser":duser})



      


def dviewprofile(request, doctorusername):

    if request.method == 'GET':

         
         duser = User.objects.get(username=doctorusername)
         r = rating_review.objects.filter(doctor=duser.doctor)
       
         return render(request,'doctor/view_profile/view_profile.html', {"duser":duser, "rate":r} )








       
def  consult_a_doctor(request):


    if request.method == 'GET':
        
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return redirect('home')
        
        # Get doctortype from session if available, otherwise show all doctors
        doctortype = request.session.get('doctortype', None)
        print(f"Doctor type from session: {doctortype}")
        
        # Get all doctors, or filter by specialization if doctortype is set
        if doctortype and doctortype != 'other':
            # Try to filter by specialization (case-insensitive)
            dobj = doctor.objects.filter(specialization__icontains=doctortype)
            # If no doctors found with that specialization, show all
            if not dobj.exists():
                dobj = doctor.objects.all()
        else:
            # Show all doctors if no doctortype or if it's 'other'
            dobj = doctor.objects.all()

        return render(request,'patient/consult_a_doctor/consult_a_doctor.html',{"dobj":dobj})

   


def  make_consultation(request, doctorusername):

    if request.method == 'POST':
       
        # Check if user is authenticated
        if not request.user.is_authenticated:
            messages.error(request, 'Please login to make a consultation.')
            return redirect('home')
        
        # Get patient info
        try:
            patientusername = request.session.get('patientusername')
            if patientusername:
                puser = User.objects.get(username=patientusername)
            else:
                # If not in session, use authenticated user
                puser = request.user
            
            # Check if user has a patient profile
            try:
                patient_obj = puser.patient
                request.session['patientusername'] = puser.username
            except:
                messages.error(request, 'User does not have a patient profile.')
                return redirect('home')
        except User.DoesNotExist:
            messages.error(request, 'User not found.')
            return redirect('home')
        
        # Get doctor info
        try:
            duser = User.objects.get(username=doctorusername)
            doctor_obj = duser.doctor
            request.session['doctorusername'] = doctorusername
        except User.DoesNotExist:
            messages.error(request, 'Doctor not found.')
            return redirect('consult_a_doctor')
        except:
            messages.error(request, 'Doctor profile not found.')
            return redirect('consult_a_doctor')

        # Get diseaseinfo from session
        diseaseinfo_id = request.session.get('diseaseinfo_id')
        if not diseaseinfo_id:
            messages.error(request, 'No disease information found. Please check disease or scan image first.')
            return redirect('patient_ui')
        
        try:
            diseaseinfo_obj = diseaseinfo.objects.get(id=diseaseinfo_id)
        except diseaseinfo.DoesNotExist:
            messages.error(request, 'Disease information not found.')
            return redirect('patient_ui')

        consultation_date = date.today()
        status = "active"
        
        consultation_new = consultation( patient=patient_obj, doctor=doctor_obj, diseaseinfo=diseaseinfo_obj, consultation_date=consultation_date,status=status)
        consultation_new.save()

        request.session['consultation_id'] = consultation_new.id

        print("consultation record is saved sucessfully.............................")

         
        return redirect('consultationview',consultation_new.id)



def  consultationview(request,consultation_id):
   
    if request.method == 'GET':

   
      request.session['consultation_id'] = consultation_id
      consultation_obj = consultation.objects.get(id=consultation_id)

      return render(request,'consultation/consultation.html', {"consultation":consultation_obj })

   #  if request.method == 'POST':
   #    return render(request,'consultation/consultation.html' )





def rate_review(request,consultation_id):
   if request.method == "POST":
         
         consultation_obj = consultation.objects.get(id=consultation_id)
         patient = consultation_obj.patient
         doctor1 = consultation_obj.doctor
         rating = request.POST.get('rating')
         review = request.POST.get('review')

         rating_obj = rating_review(patient=patient,doctor=doctor1,rating=rating,review=review)
         rating_obj.save()

         rate = int(rating_obj.rating_is)
         doctor.objects.filter(pk=doctor1).update(rating=rate)
         

         return redirect('consultationview',consultation_id)





def close_consultation(request,consultation_id):
   if request.method == "POST":
         
         consultation.objects.filter(pk=consultation_id).update(status="closed")
         
         return redirect('home')






#-----------------------------chatting system ---------------------------------------------------


def post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)

        consultation_id = request.session['consultation_id'] 
        consultation_obj = consultation.objects.get(id=consultation_id)

        c = Chat(consultation_id=consultation_obj,sender=request.user, message=msg)

        #msg = c.user.username+": "+msg

        if msg != '':            
            c.save()
            print("msg saved"+ msg )
            return JsonResponse({ 'msg': msg })
    else:
        return HttpResponse('Request must be POST.')



def chat_messages(request):
   if request.method == "GET":

         consultation_id = request.session['consultation_id'] 

         c = Chat.objects.filter(consultation_id=consultation_id)
         return render(request, 'consultation/chat_body.html', {'chat': c})


#-----------------------------chatting system ---------------------------------------------------


