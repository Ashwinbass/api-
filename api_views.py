import requests
from django.shortcuts import render, redirect
import logging

# Configure logger
logger = logging.getLogger(__name__)
from .forms import *
from api_gateway_frontend.settings import BASE_URL
from .api_call import *
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import json


def client_dashboard(request):
    try:
        session= request.session.get('username') 
        access_token = request.session['access_token']
        process_endpoint = "getProcessTableList"
        unprocess_endpoint = "getUnProcessTableList"
        backend_endpoint = "getAllBackend"
        service_endpoint = "getAllService"
        process__endpoint = "getAllProcess"
        service_process_endpoint = "getAllServiceProcess"
        service_orchestration_endpoint = "getAllServiceOrchestration"

        #backend to orchestration

        backend = call_get_method(BASE_URL, backend_endpoint, access_token)
        if backend.status_code == 404:
            return render(request, '404page.html', {'error': backend.json()})    
        elif backend.status_code == 403:
            return render(request, '403page.html', {'error': backend.json()})
        elif backend.status_code == 200:
            backend_data = backend.json()
            backend_count = len(backend_data)
            print("backend_count:", backend_count)
        else:
            return render(request, '500page.html', {'error': backend.json()})


        service = call_get_method(BASE_URL, service_endpoint, access_token)
        if service.status_code == 404:
            return render(request, '404page.html', {'error': service.json()})    
        elif service.status_code == 403:
            return render(request, '403page.html', {'error': service.json()})
        elif service.status_code == 200:
            service_data = service.json()
            service_count = len(service_data)
            print("service_count:", service_count)
        else:
            return render(request, '500page.html', {'error': service.json()})
        process_get = call_get_method(BASE_URL, process__endpoint, access_token)
        if process_get.status_code != 200:
            return render(request, '500page.html', {'error': process_get.json()})
        process_data = process_get.json()
        process_count = len(process_data)
        print("process_count:", process_count)

        service_process = call_get_method(BASE_URL, service_process_endpoint, access_token)
        if service_process.status_code != 200:
            return render(request, '500page.html', {'error': service_process.json()})
        service_process_sec = service_process.json()
        service_process_count = len(service_process_sec)
        print("service_process_count:", service_process_count)


        service_orchestration = call_get_method(BASE_URL, service_orchestration_endpoint, access_token)
        if service_orchestration.status_code != 200:
            return render(request, '500page.html', {'error': service_orchestration.json()})
        service_orchestration_sec = service_orchestration.json()
        service_orchestration_count = len(service_orchestration_sec)
        print("service_orchestration_count:", service_orchestration_count)

        total1= backend_count + service_count + process_count + service_process_count + service_orchestration_count
        if total1 > 0:
            backend_percentage= (backend_count/total1)*100
            service_percentage= (service_count/total1)*100
            process_percentage= (process_count/total1)*100
            service_process_percentage= (service_process_count/total1)*100
            service_orchestration_percentage= (service_orchestration_count/total1)*100
            backend=round(float(backend_percentage))
            service=round(float(service_percentage))
            process_get=round(float(process_percentage))
            service_process=round(float(service_process_percentage))
            service_orchestration=round(float(service_orchestration_percentage))
        else:
            # Default values when total1 is 0
            backend = 0
            service = 0
            process_get = 0
            service_process = 0
            service_orchestration = 0
        print("backend:", backend)
        print("service:", service)
        print("service_process:", service_process)
        print("service_orchestration:", service_orchestration)
        return render(request, 'client_dashboard.html', {'backend': backend if backend else 0,'service_orchestration': service_orchestration if service_orchestration else 0,'service_process': service_process if service_process else 0,'service': service if service else 0,'process_section': process_get if process_get else 0})    
    except Exception as error:  
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

def user_dashboard(request):
    try:
        session= request.session.get('username') 
        access_token = request.session['access_token']
        process_endpoint = "getProcessTableList"
        unprocess_endpoint = "getUnProcessTableList"
        backend_endpoint = "getAllBackend"
        service_endpoint = "getAllService"
        process__endpoint = "getAllProcess"
        service_process_endpoint = "getAllServiceProcess"
        service_orchestration_endpoint = "getAllServiceOrchestration"

        #backend to orchestration

        backend = call_get_method(BASE_URL, backend_endpoint, access_token)
        if backend.status_code != 200:
            return render(request, '500page.html', {'error': backend.json()})
        backend_data = backend.json()
        backend_count = len(backend_data)
        print("backend_count:", backend_count)

        service = call_get_method(BASE_URL, service_endpoint, access_token)
        if service.status_code != 200:
            return render(request, '500page.html', {'error': service.json()})
        service_data = service.json()
        service_count = len(service_data)
        print("service_count:", service_count)

        process_get = call_get_method(BASE_URL, process__endpoint, access_token)
        if process_get.status_code != 200:
            return render(request, '500page.html', {'error': process_get.json()})
        process_data = process_get.json()
        process_count = len(process_data)
        print("process_count:", process_count)

        service_process = call_get_method(BASE_URL, service_process_endpoint, access_token)
        if service_process.status_code != 200:
            return render(request, '500page.html', {'error': service_process.json()})
        service_process_sec = service_process.json()
        service_process_count = len(service_process_sec)
        print("service_process_count:", service_process_count)


        service_orchestration = call_get_method(BASE_URL, service_orchestration_endpoint, access_token)
        if service_orchestration.status_code != 200:
            return render(request, '500page.html', {'error': service_orchestration.json()})
        service_orchestration_sec = service_orchestration.json()
        service_orchestration_count = len(service_orchestration_sec)
        print("service_orchestration_count:", service_orchestration_count)

        total1= backend_count + service_count + process_count + service_process_count + service_orchestration_count
        if total1 > 0:
            backend_percentage= (backend_count/total1)*100
            service_percentage= (service_count/total1)*100
            process_percentage= (process_count/total1)*100
            service_process_percentage= (service_process_count/total1)*100
            service_orchestration_percentage= (service_orchestration_count/total1)*100
            backend=round(float(backend_percentage))
            service=round(float(service_percentage))
            process_get=round(float(process_percentage))
            service_process=round(float(service_process_percentage))
            service_orchestration=round(float(service_orchestration_percentage))
        else:
            # Default values when total1 is 0
            backend = 0
            service = 0
            process_get = 0
            service_process = 0
            service_orchestration = 0
        print("backend:", backend)
        print("service:", service)
        print("service_process:", service_process)
        print("service_orchestration:", service_orchestration)

        return render(request,'user_dashboard.html',{'backend':backend,'service_orchestration':service_orchestration,'service_process':service_process,'service':service,'process_section':process_get})
    except Exception as error:  
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})
def dashboard(request):
    try:
        session= request.session.get('username') 
        access_token = request.session['access_token']
        process_endpoint = "getProcessTableList"
        unprocess_endpoint = "getUnProcessTableList"
        backend_endpoint = "getAllBackend"
        service_endpoint = "getAllService"
        process__endpoint = "getAllProcess"
        service_process_endpoint = "getAllServiceProcess"
        service_orchestration_endpoint = "getAllServiceOrchestration"

        #backend to orchestration

        backend = call_get_method(BASE_URL, backend_endpoint, access_token)
        if backend.status_code != 200:
            return render(request, '500page.html', {'error': backend.json()})
        backend_data = backend.json()
        backend_count = len(backend_data)
        print("backend_count:", backend_count)

        service = call_get_method(BASE_URL, service_endpoint, access_token)
        if service.status_code != 200:
            return render(request, '500page.html', {'error': service.json()})
        service_data = service.json()
        service_count = len(service_data)
        print("service_count:", service_count)

        process_get = call_get_method(BASE_URL, process__endpoint, access_token)
        if process_get.status_code != 200:
            return render(request, '500page.html', {'error': process_get.json()})
        process_data = process_get.json()
        process_count = len(process_data)
        print("process_count:", process_count)

        service_process = call_get_method(BASE_URL, service_process_endpoint, access_token)
        if service_process.status_code != 200:
            return render(request, '500page.html', {'error': service_process.json()})
        service_process_sec = service_process.json()
        service_process_count = len(service_process_sec)
        print("service_process_count:", service_process_count)


        service_orchestration = call_get_method(BASE_URL, service_orchestration_endpoint, access_token)
        if service_orchestration.status_code != 200:
            return render(request, '500page.html', {'error': service_orchestration.json()})
        service_orchestration_sec = service_orchestration.json()
        service_orchestration_count = len(service_orchestration_sec)
        print("service_orchestration_count:", service_orchestration_count)

        total1= backend_count + service_count + process_count + service_process_count + service_orchestration_count
        if total1 > 0:
            backend_percentage= (backend_count/total1)*100
            service_percentage= (service_count/total1)*100
            process_percentage= (process_count/total1)*100
            service_process_percentage= (service_process_count/total1)*100
            service_orchestration_percentage= (service_orchestration_count/total1)*100
            backend=round(float(backend_percentage))
            service=round(float(service_percentage))
            process_get=round(float(process_percentage))
            service_process=round(float(service_process_percentage))
            service_orchestration=round(float(service_orchestration_percentage))
        else:
            # Default values when total1 is 0
            backend = 0
            service = 0
            process_get = 0
            service_process = 0
            service_orchestration = 0
        print("backend:", backend)
        print("service:", service)
        print("service_process:", service_process)
        print("service_orchestration:", service_orchestration)
        #process and unprocess
        process_list = call_get_method(BASE_URL, process_endpoint, access_token)
        if process_list.status_code != 200:
            return render(request, '500page.html', {'error': process_list.json()})
        process_data = process_list.json()
        count = len(process_data)
        print("process_count:", count)


        unprocess_list = call_get_method(BASE_URL, unprocess_endpoint, access_token)
        unprocess_data = unprocess_list.json()
        unprocess_count = len(unprocess_data)
        print("unprocess_count:", unprocess_count)


        total= count + unprocess_count
        if total > 0:
            process_percentage= (count/total)*100
            unprocess_percentage= (unprocess_count/total)*100
            process=round(float(process_percentage))
            unprocess=round(float(unprocess_percentage))
            process_percentage= (count/total)*100
            unprocess_percentage= (unprocess_count/total)*100
            process=round(float(process_percentage))
            unprocess=round(float(unprocess_percentage))
            print("process_percentage", round(float(process_percentage)))
            print("unprocess_percentage", round(float(unprocess_percentage)))
            print("Total count:", total)
        else:
            # Default values when total is 0
            process = 0
            unprocess = 0



        return render(request, 'dashboard.html',{'session':session,'process':process,'unprocess':unprocess,'backend':backend,'service_orchestration':service_orchestration,'service_process':service_process,'service':service,'process_section':process_get})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

# ----------------------------------register backend------------------------------------------------------------------

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required

def register_be(request):
        try:
            access_token = request.session['access_token']
            endpoint = "Backend"
            
            # Fetch both public and private backends
            public_backends = call_get_method(BASE_URL, "getAllBackend", access_token)
            private_backends = call_get_method(BASE_URL, "getAllPrivateBackend", access_token)
            
            # Combine both lists
            backend_data = []
            if public_backends.status_code == 200:
                backend_data.extend(public_backends.json())
            if private_backends.status_code == 200:
                backend_data.extend(private_backends.json())
            
            if not backend_data:
                return render(request, '500page.html', {'error': "Could not fetch backend data"})
                
            form_data = None
            
            if request.method == "POST":
                # Extract form data
                form_data = {
                    'field_name': request.POST.get('field_name', ''),
                    'api_url': request.POST.get('api_url', ''),
                    'url_type': request.POST.get('url_type', ''),
                    'authRequire': 'authRequire' in request.POST,
                    'username': request.POST.get('username', ''),
                    'password': request.POST.get('password', ''),
                    'authUrl': request.POST.get('authUrl', ''),
                    'depend_api': 'depend_api' in request.POST,
                    'depend_serviceflow_id': request.POST.get('depend_serviceflow_id', ''),
                    'depend_url': request.POST.get('depend_url', ''),
                    'status': request.POST.get('status', ''),
                    'depend_api_parameter_required': 'depend_api_parameter_required' in request.POST,
                    'parameter_required': 'parameter_required' in request.POST,
                    'visibility': request.POST.get('visibility', 'public'),
                    'depend_params': [],
                    'methods_params': []
                }
                
                # Process depend parameters
                depend_param_count = int(request.POST.get('depend_param_count', 0))
                for i in range(1, depend_param_count + 1):
                    form_data['depend_params'].append({
                        'name': request.POST.get(f'depend_name_{i}', ''),
                        'dataType': request.POST.get(f'depend_dataType_{i}', ''),
                        'mandatory': request.POST.get(f'depend_mandatory_{i}', 'off') == 'on',
                        'minLength': request.POST.get(f'depend_minLength_{i}', ''),
                        'maxLength': request.POST.get(f'depend_maxLength_{i}', ''),
                        'dependParam': request.POST.get(f'depend_dependParam_{i}', 'off') == 'on',
                        'dependParameterName': request.POST.get(f'depend_dependParameterName_{i}', '')
                    })
                
                # Process main parameters
                param_count = int(request.POST.get('parameter_count', 0))
                for i in range(1, param_count + 1):
                    form_data['methods_params'].append({
                        'name': request.POST.get(f'param_name_{i}', ''),
                        'dataType': request.POST.get(f'param_dataType_{i}', ''),
                        'mandatory': request.POST.get(f'param_mandatory_{i}', 'off') == 'on',
                        'minLength': request.POST.get(f'param_minLength_{i}', ''),
                        'maxLength': request.POST.get(f'param_maxLength_{i}', ''),
                        'dependParam': request.POST.get(f'param_dependParam_{i}', 'off') == 'on',
                        'dependParameterName': request.POST.get(f'param_dependParameterName_{i}', '')
                    })
                
                # Prepare API payload
                api_payload = {
                    "name": form_data['field_name'],
                    "authRequire": form_data['authRequire'],
                    "authUrl": form_data['authUrl'] or None,
                    "username": form_data['username'] or None,
                    "password": form_data['password'] or None,
                    "apiURL": form_data['api_url'],
                    "urlType": form_data['url_type'].upper(),
                    "dependApis": form_data['depend_api'],
                    "dependServiceFlowID": form_data['depend_serviceflow_id'] or None,
                    "dependUrl": form_data['depend_url'] or None,
                    "dependurlType": form_data['status'].upper(),
                    "dependParamRequire": form_data['depend_api_parameter_required'],
                    "dependParam": form_data['depend_params'],
                    "paramRequire": form_data['parameter_required'],
                    "methodsParam": form_data['methods_params'],
                    "visibility": form_data['visibility']
                }
                
                try:
                    response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
                    
                    if response.status_code == 200:
                        messages.success(request, "Backend registered successfully!")
                        return redirect("backendurl")
                    else:
                        messages.error(request, f"Error: {response.text}")
                        return render(request, 'regbackend.html', {
                            'form_data': form_data,
                            'backend_data': backend_data
                        })
                        
                except requests.exceptions.RequestException as e:
                    messages.error(request, f"Request Error: {str(e)}")
                    return render(request, 'regbackend.html', {
                        'form_data': form_data,
                        'backend_data': backend_data
                    })
                    
            return render(request, 'regbackend.html', {
                'form_data': form_data,
                'backend_data': backend_data
            })
            
        except Exception as error:
            print(f'Error: {error}')
            return render(request, '500page.html', {'error': str(error)})



# final working code 
# def register_be(request):
#     try:
#         access_token = request.session['access_token']
#         print("0000000",access_token)
#         endpoint = "Backend"
#         endpoint1 = "getAllBackend"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             print("000000",backend_url_list.text)
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         backend_data = backend_url_list.json()
#         if request.method == "POST":
#             print("Form data received:", request.POST)  
#             # Extract form data from the request
#             name = request.POST.get("field_name")
#             authRequire = request.POST.get("authRequire")
#             api_url = request.POST.get("api_url")
#             url_type = request.POST.get("url_type")
#             auth_url = request.POST.get("authUrl", "")
#             username = request.POST.get("username", "")
#             password = request.POST.get("password", "")
#             depend_api = "depend_api" in request.POST  # This will check if the checkbox is checked
#             depend_service_flow_id = request.POST.get("depend_serviceflow_id")
#             depend_url = request.POST.get("depend_url", "")
#             depend_url_type = request.POST.get("status", "")
#             print("maniiiiiiiiiii",depend_url_type)
#             depend_param_required = "depend_api_parameter_required" in request.POST
#             parameter_required = "parameter_required" in request.POST
#               # Handle visibility
#                # Correct visibility handling - checks both checkbox and hidden field
#             visibility = request.POST.get('visibility', 'public')
#             print(f"Final visibility: {visibility}")
#             depend_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))  # Get the number of depend parameters
#             if depend_param_required and depend_param_count > 0:
#                 for i in range(1, depend_param_count + 1):
#                     param_name = request.POST.get(f"depend_name_{i}")
#                     param_data_type = request.POST.get(f"depend_dataType_{i}")
#                     param_is_mandatory = request.POST.get(f"depend_mandatory_{i}") == "on"
#                     param_min_length = request.POST.get(f"depend_minLength_{i}")
#                     param_max_length = request.POST.get(f"depend_maxLength_{i}")
#                     depend_param = request.POST.get(f"depend_dependParam_{i}") == "on"
#                     depend_parameter_name = request.POST.get(f"depend_dependParameterName_{i}")

#                     # Add to depend_params if param_name or param_data_type is provided
#                     if param_name or param_data_type:
#                         depend_params.append({
#                             "name": param_name,
#                             "dataType": param_data_type,
#                             "isMandatory": param_is_mandatory,
#                             "minLength": param_min_length,
#                             "maxLength": param_max_length,
#                             "dependParam": depend_param,
#                             "dependParameterName": depend_parameter_name,
#                         })
#             print("depend_params:", depend_params)
#             # Handle methodsParam fields
#             methods_params = []
#             print("methods_params:", methods_params)
#             param_count = int(request.POST.get('parameter_count', 0))
#             if parameter_required and param_count > 0:
#                 for i in range(1, param_count + 1):
#                     param_name = request.POST.get(f"name1_{i}")
#                     param_data_type = request.POST.get(f"dataType1_{i}")
#                     param_is_mandatory = request.POST.get(f"mandatory1_{i}") == 'on'
#                     param_min_length = request.POST.get(f"minLength1_{i}")
#                     param_max_length = request.POST.get(f"maxLength1_{i}")
#                     depend_param = request.POST.get(f"dependParam1_{i}") == 'on'
#                     depend_parameter_name = request.POST.get(f"dependParameterName1_{i}")

#                     # Add to methods_params if param_name or param_data_type is provided
#                     if param_name or param_data_type:
#                         methods_params.append({
#                             "name": param_name,
#                             "dataType": param_data_type,
#                             "isMandatory": param_is_mandatory,
#                             "minLength": param_min_length,
#                             "maxLength": param_max_length,
#                             "dependParam": depend_param,
#                             "dependParameterName": depend_parameter_name,
#                         })
#             print("methods_params:", methods_params)
                    
#             # Construct API Payload
#             api_payload = {
#                 "name": name,
#                 "authRequire": "authRequire" in request.POST,
#                 "authUrl": auth_url or None,
#                 "username": username or None,
#                 "password": password or None,
#                 "apiURL": api_url,
#                 "urlType": url_type.upper(),
#                 "dependApis": depend_api,
#                 "dependServiceFlowID": depend_service_flow_id or None,
#                 "dependUrl": depend_url or None,
#                 "dependurlType":depend_url_type.upper(),
#                 "dependParamRequire": depend_param_required,
#                 "dependParam": depend_params,
#                 "paramRequire": parameter_required,
#                 "methodsParam": methods_params,
#                 "visibility": visibility,    
#                 }
#             print("Received Visibility:", visibility)       
#             print("api_payload:", api_payload)
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
#                 print("Raw response:", response.text)  # Log the raw response for debugging
#                 print("Response status code:", response.status_code)

#                 # Check if the response contains valid JSON
#                 if response.status_code != 200:
#                     print(f"API Error: {response.status_code}, {response.text}")
#                     messages.error(request, f"API Error: {response.text}")
#                     return redirect(f"{reverse('backendurl')}?source={visibility}")
#                 elif response.status_code == 200:
#                     print(f"API Sucess: {response.status_code}, {response.text}")
#                     messages.success(request, f"{response.text}")
#                     return redirect("backendurl")
#                 # Parse JSON response
#                 try:
#                     response_data = response.json()
#                     print("Response from backend:", response_data)
#                 except ValueError:
#                     print("Error: Response is not valid JSON.")
#                     messages.error(request, "Backend did not return valid JSON.")
#                     return redirect("backendurl")
#                 # Success
#                 messages.success(request, "Backend Registration saved successfully.")
#                 return redirect("backendurl")
#             except requests.exceptions.RequestException as e:
#                 print(f"Request Error: {e}")
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect("regbackend")
#         else:
#             form = RegisterForm()
#             return render(request, 'regbackend.html', {'form': form, 'backend_data': backend_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})


# param datasalso savced 
# def register_be(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "Backend"
#         endpoint1 = "getAllBackend"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
        
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
            
#         backend_data = backend_url_list.json()
#         form_data = None
        
#         if request.method == "POST":
#             # Extract form data
#             form_data = {
#                 'field_name': request.POST.get('field_name', ''),
#                 'api_url': request.POST.get('api_url', ''),
#                 'url_type': request.POST.get('url_type', ''),
#                 'authRequire': 'authRequire' in request.POST,
#                 'username': request.POST.get('username', ''),
#                 'password': request.POST.get('password', ''),
#                 'authUrl': request.POST.get('authUrl', ''),
#                 'depend_api': 'depend_api' in request.POST,
#                 'depend_serviceflow_id': request.POST.get('depend_serviceflow_id', ''),
#                 'depend_url': request.POST.get('depend_url', ''),
#                 'status': request.POST.get('status', ''),
#                 'depend_api_parameter_required': 'depend_api_parameter_required' in request.POST,
#                 'parameter_required': 'parameter_required' in request.POST,
#                 'visibility': request.POST.get('visibility', 'public'),
#                 'depend_params': [],
#                 'methods_params': []
#             }
            
#             # Process depend parameters
#             depend_param_count = int(request.POST.get('depend_param_count', 0))
#             for i in range(1, depend_param_count + 1):
#                 form_data['depend_params'].append({
#                     'name': request.POST.get(f'depend_name_{i}', ''),
#                     'dataType': request.POST.get(f'depend_dataType_{i}', ''),
#                     'mandatory': request.POST.get(f'depend_mandatory_{i}', 'off') == 'on',
#                     'minLength': request.POST.get(f'depend_minLength_{i}', ''),
#                     'maxLength': request.POST.get(f'depend_maxLength_{i}', ''),
#                     'dependParam': request.POST.get(f'depend_dependParam_{i}', 'off') == 'on',
#                     'dependParameterName': request.POST.get(f'depend_dependParameterName_{i}', '')
#                 })
            
#             # Process main parameters
#             param_count = int(request.POST.get('parameter_count', 0))
#             for i in range(1, param_count + 1):
#                 form_data['methods_params'].append({
#                     'name': request.POST.get(f'param_name_{i}', ''),
#                     'dataType': request.POST.get(f'param_dataType_{i}', ''),
#                     'mandatory': request.POST.get(f'param_mandatory_{i}', 'off') == 'on',
#                     'minLength': request.POST.get(f'param_minLength_{i}', ''),
#                     'maxLength': request.POST.get(f'param_maxLength_{i}', ''),
#                     'dependParam': request.POST.get(f'param_dependParam_{i}', 'off') == 'on',
#                     'dependParameterName': request.POST.get(f'param_dependParameterName_{i}', '')
#                 })
            
#             # Prepare API payload
#             api_payload = {
#                 "name": form_data['field_name'],
#                 "authRequire": form_data['authRequire'],
#                 "authUrl": form_data['authUrl'] or None,
#                 "username": form_data['username'] or None,
#                 "password": form_data['password'] or None,
#                 "apiURL": form_data['api_url'],
#                 "urlType": form_data['url_type'].upper(),
#                 "dependApis": form_data['depend_api'],
#                 "dependServiceFlowID": form_data['depend_serviceflow_id'] or None,
#                 "dependUrl": form_data['depend_url'] or None,
#                 "dependurlType": form_data['status'].upper(),
#                 "dependParamRequire": form_data['depend_api_parameter_required'],
#                 "dependParam": form_data['depend_params'],
#                 "paramRequire": form_data['parameter_required'],
#                 "methodsParam": form_data['methods_params'],
#                 "visibility": form_data['visibility']
#             }
            
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
                
#                 if response.status_code == 200:
#                     messages.success(request, "Backend registered successfully!")
#                     return redirect("backendurl")
#                 else:
#                     messages.error(request, f"Error: {response.text}")
#                     return render(request, 'regbackend.html', {
#                         'form_data': form_data,
#                         'backend_data': backend_data
#                     })
                    
#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return render(request, 'regbackend.html', {
#                     'form_data': form_data,
#                     'backend_data': backend_data
#                 })
                
#         return render(request, 'regbackend.html', {
#             'form_data': form_data,
#             'backend_data': backend_data
#         })
        
#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})











# def register_be(request,backend_type):
#     try:
    
#         access_token = request.session['access_token']
#         print("000000",access_token)
#         if backend_type == "public":
#             endpoint = "Backend"
#             endpoint1 = "getAllBackend"  
#         elif backend_type == "private":
#             endpoint = "getAllPrivateBackend"
#             endpoint1 = "getAllPrivateBackend"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             print("000000",backend_url_list.text)
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         backend_data = backend_url_list.json()
#         if request.method == "POST":
#             # Extract form data from the request
#             name = request.POST.get("field_name")
#             authRequire = request.POST.get("authRequire")
#             api_url = request.POST.get("api_url")
#             url_type = request.POST.get("url_type")
#             auth_url = request.POST.get("authUrl", "")
#             username = request.POST.get("username", "")
#             password = request.POST.get("password", "")
#             depend_api = "depend_api" in request.POST  # This will check if the checkbox is checked
#             depend_service_flow_id = request.POST.get("depend_serviceflow_id")
#             depend_url = request.POST.get("depend_url", "")
#             depend_url_type = request.POST.get("status", "")
#             print("maniiiiiiiiiii",depend_url_type)
#             depend_param_required = "depend_api_parameter_required" in request.POST
#             parameter_required = "parameter_required" in request.POST
#             # Handle dependParam fields
#             depend_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))  # Get the number of depend parameters
#             if depend_param_required and depend_param_count > 0:
#                 for i in range(1, depend_param_count + 1):
#                     param_name = request.POST.get(f"depend_name_{i}")
#                     param_data_type = request.POST.get(f"depend_dataType_{i}")
#                     param_is_mandatory = request.POST.get(f"depend_mandatory_{i}") == "on"
#                     param_min_length = request.POST.get(f"depend_minLength_{i}")
#                     param_max_length = request.POST.get(f"depend_maxLength_{i}")
#                     depend_param = request.POST.get(f"depend_dependParam_{i}") == "on"
#                     depend_parameter_name = request.POST.get(f"depend_dependParameterName_{i}")

#                     # Add to depend_params if param_name or param_data_type is provided
#                     if param_name or param_data_type:
#                         depend_params.append({
#                             "name": param_name,
#                             "dataType": param_data_type,
#                             "isMandatory": param_is_mandatory,
#                             "minLength": param_min_length,
#                             "maxLength": param_max_length,
#                             "dependParam": depend_param,
#                             "dependParameterName": depend_parameter_name,
#                         })
#             print("depend_params:", depend_params)
#             # Handle methodsParam fields
#             methods_params = []
#             print("methods_params:", methods_params)
#             param_count = int(request.POST.get('parameter_count', 0))
#             if parameter_required and param_count > 0:
#                 for i in range(1, param_count + 1):
#                     param_name = request.POST.get(f"name1_{i}")
#                     param_data_type = request.POST.get(f"dataType1_{i}")
#                     param_is_mandatory = request.POST.get(f"mandatory1_{i}") == 'on'
#                     param_min_length = request.POST.get(f"minLength1_{i}")
#                     param_max_length = request.POST.get(f"maxLength1_{i}")
#                     depend_param = request.POST.get(f"dependParam1_{i}") == 'on'
#                     depend_parameter_name = request.POST.get(f"dependParameterName1_{i}")

#                     # Add to methods_params if param_name or param_data_type is provided
#                     if param_name or param_data_type:
#                         methods_params.append({
#                             "name": param_name,
#                             "dataType": param_data_type,
#                             "isMandatory": param_is_mandatory,
#                             "minLength": param_min_length,
#                             "maxLength": param_max_length,
#                             "dependParam": depend_param,
#                             "dependParameterName": depend_parameter_name,
#                         })
#             print("methods_params:", methods_params)
                    
#             # Construct API Payload
#             api_payload = {
#                 "name": name,
#                 "authRequire": "authRequire" in request.POST,
#                 "authUrl": auth_url or None,
#                 "username": username or None,
#                 "password": password or None,
#                 "apiURL": api_url,
#                 "urlType": url_type.upper(),
#                 "dependApis": depend_api,
#                 "dependServiceFlowID": depend_service_flow_id or None,
#                 "dependUrl": depend_url or None,
#                 "dependurlType":depend_url_type.upper(),
#                 "dependParamRequire": depend_param_required,
#                 "dependParam": depend_params,
#                 "paramRequire": parameter_required,
#                 "methodsParam": methods_params,
                
#             }
#             print("api_payload:", api_payload)
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
#                 print("Raw response:", response.text)  # Log the raw response for debugging
#                 print("Response status code:", response.status_code)

#                 # Check if the response contains valid JSON
#                 if response.status_code != 200:
#                     print(f"API Error: {response.status_code}, {response.text}")
#                     messages.error(request, f"API Error: {response.text}")
#                     return redirect("backendurl")
#                 elif response.status_code == 200:
#                     print(f"API Sucess: {response.status_code}, {response.text}")
#                     messages.success(request, f"{response.text}")
#                     return redirect("backendurl")
#                 # Parse JSON response
#                 try:
#                     response_data = response.json()
#                     print("Response from backend:", response_data)
#                 except ValueError:
#                     print("Error: Response is not valid JSON.")
#                     messages.error(request, "Backend did not return valid JSON.")
#                     return redirect("backendurl")
#                 # Success
#                 messages.success(request, "Backend Registration saved successfully.")
#                 return redirect("backendurl")
#             except requests.exceptions.RequestException as e:
#                 print(f"Request Error: {e}")
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect("regbackend")
#         else:
#             form = RegisterForm()
#             return render(request, 'regbackend.html', {'form': form, 'backend_data': backend_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

################################################################################
#Frontend URL 
# POST

# from django.contrib import messages
# @role_required(allowed_roles=['ADMIN','USER','CLIENT'])
# @custom_login_required
# def registerfrontend(request):
#     try:
#         access_token = request.session['access_token']
#         if request.method == 'POST':
#             form = RegisterFrontendForm(request.POST)
#             if form.is_valid():
#                 name = form.cleaned_data['name']
#                 user_name = form.cleaned_data['user_name']
#                 password = request.POST.get('password')
#                 user = form.cleaned_data['user']
#                 role = form.cleaned_data['role']
#                 emp_code = form.cleaned_data['emp_code']
#                 email = form.cleaned_data['email_id']
#                 data = {
#                     'name':name,
#                     'userName': user_name,
#                     'password':password,
#                     "user": user,
#                     "role": role.upper() if role.upper() else "CLIENT",
#                     'empCode': emp_code,
#                     "email": email
#                 }
#                 print("data0",data)
#                 endpoint = "Frontend"
#                 json_data = json.dumps(data)
#                 frontend_url_list = call_post_with_method(BASE_URL, endpoint, json_data, access_token)
#                 if frontend_url_list.status_code != 200:
#                     messages.error(request, 'An error occurred while processing your request.')
#                     return render(request, 'registerfrontend.html', {'form': form})
#                 frontend_data = None 
#                 try:
#                     frontend_data = frontend_url_list.json()
#                     messages.success(request, 'Frontend registration was successful!')
#                     return redirect('frontendurl')
#                 except requests.exceptions.JSONDecodeError:
#                     messages.success(request, frontend_url_list.text)  # Plain success message
#                     print("frontend_data",frontend_data)

#                 return render(request, 'registerfrontend.html', {'form': form, 'frontend_data': frontend_data})

#             else:
#                 print("vvvvvvvvvvvvvvvvv",form.errors)

#         form = RegisterFrontendForm()
#         return render(request, 'registerfrontend.html', {'form': form})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

# GET
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_frontendurl(request):
    try:
        access_token = request.session['access_token']
        endpoint = "listOfFrontend"
        frontend_url_list = call_get_method(BASE_URL, endpoint, access_token)
        print("frontend_url_list",frontend_url_list.text)
        if frontend_url_list.status_code != 200:
            return render(request, '500page.html', {'error': frontend_url_list.json()})
        frontend_data = frontend_url_list.json()
        return render(request, 'frontendurl.html', {'form': frontend_data})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_frontendurl_single(request,pk):
    try:
        access_token = request.session['access_token']
        endpoint = f'getFrontend/{pk}'
        frontend_url_list = call_get_method(BASE_URL, endpoint, access_token)
        print("frontend_url_list",frontend_url_list.text)
        if frontend_url_list.status_code != 200:
            return render(request, '500page.html', {'error': frontend_url_list.json()})
        frontend_data = frontend_url_list.json()
        return render(request, 'frontendurl_single.html', {'form': frontend_data})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})


@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def frontendurl_edit(request, pk):
    try:
        """
        Handle GET and POST requests for updating frontend data.
        """
        access_token = request.session.get('access_token')

        # Fetch existing data for the form
        if request.method == 'GET':
            endpoint = f"getFrontend/{pk}"  # API call to get existing data
            response = call_get_method(BASE_URL, endpoint, access_token)

            if response.status_code == 200:
                frontend_data = response.json()
                return render(request, 'frontend_edit.html', {'frontend': frontend_data, 'pk': pk})
            else:
                messages.error(request, "Error fetching data")
                return redirect("frontendurl")

        # Handle form submission and update the data
        elif request.method == 'POST':
            data = json.loads(request.body)  # Get updated data from request
            endpoint = f"updateFrontend/{pk}"  # API endpoint for updating
            response = call_put_method(BASE_URL, endpoint, json.dumps(data), access_token)

            if response.status_code == 200:
                messages.success(request, "Frontend data updated successfully.")
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Failed to update data'}, status=400)

        return JsonResponse({'error': 'Invalid request method'}, status=400)

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': str(error)})


###############################################################################################


@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required 
def get_backendurl(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get source parameter with validation
        data_source = request.GET.get('source', 'public').lower()
        if data_source not in ['public', 'private']:
            data_source = 'public'
            
        print(f"Fetching {data_source} backend URLs")
        
        # Choose endpoint based on visibility
        endpoint = "getAllPrivateBackend" if data_source == 'private' else "getAllBackend"
        
        # Make API call
        backend_url_list = call_get_method(BASE_URL, endpoint, access_token)
        
        if backend_url_list.status_code != 200:
            return render(request, '500page.html', {'error': f"API Error: {backend_url_list.status_code}"})

        try:
            backend_data = backend_url_list.json()
            print(f"Received {len(backend_data)} {data_source} items")
        except Exception as e:
            return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

        return render(request, 'backendurl.html', {
            'form': backend_data, 
            'source': data_source
        })

    except Exception as error:
        print(f'Error in get_backendurl view: {error}')
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def get_backendurl(request):
#     try:
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         # Get the source parameter (default to public)
#         data_source = request.GET.get('source', 'public').lower()
#         print(f"Fetching {data_source} backend URLs")  # Debug

        
#         # Choose endpoint based on user role and requested source
#         if request.session.get('user_role') in ['ADMIN', 'USER']:
#             if data_source == 'public':
#                 endpoint = "getAllBackend"
#             elif data_source == 'private':
#                 endpoint = "getAllPrivateBackend"
#             else:
#                 return render(request, '500page.html', {'error': 'Invalid data source'})
#         else:
#             # For non-admin/users, only show public data
#             endpoint = "getAllBackend"
#             data_source = 'public'

#         backend_url_list = call_get_method(BASE_URL, endpoint, access_token)

#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': f"API Error: {backend_url_list.status_code}"})

#         try:
#             backend_data = backend_url_list.json()
#             print(f"Fetching {data_source} data from endpoint: {endpoint}")

#             print(f"Received {len(backend_data)} items")
#         except Exception as e:
#             return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

#         return render(request, 'backendurl.html', {
#             'form': backend_data, 
#             'source': data_source
#         })

#     except Exception as error:
#         print(f'Error in get_backendurl view: {error}')
#         return render(request, '500page.html', {'error': f'An error occurred: {error}'})
# final working code
# def get_backendurl(request):
#     try:
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         # Get the source parameter from the request (default to "public")
#         data_source = request.GET.get('source', 'public').lower()
#         print(f"Received source: {data_source}")  # Debugging

#         # Choose the appropriate API endpoint
#         if data_source == "public":
#             endpoint = "getAllBackend"
#         elif data_source == "private":
#             endpoint = "getAllPrivateBackend"
#         else:
#             print("Invalid data source requested")
#             return render(request, '500page.html', {'error': 'Invalid data source'})

#         print(f"Calling API Endpoint: {endpoint}")

#         backend_url_list = call_get_method(BASE_URL, endpoint, access_token)

#         # **🔹 Step 1: Print the raw response**
#         print(f"Raw Response Status: {backend_url_list.status_code}")
#         print(f"Raw Response Content: {backend_url_list.text}")  # Debugging

#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': f"API Error: {backend_url_list.status_code}"})

#         try:
#             backend_data = backend_url_list.json()
#         except Exception as e:
#             print(f"JSON Parse Error: {e}")  # Debugging
#             return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

#         print(f"Fetched {len(backend_data)} records from {endpoint}")

#         return render(request, 'backendurl.html', {'form': backend_data, 'source': data_source})

#     except Exception as error:
#         print(f'Error in get_backendurl view: {error}')
#         return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def get_backendurl(request):
#     # try:
#         access_token = request.session['access_token']
#         endpoint = "getAllBackend"
#         backend_url_list = call_get_method(BASE_URL, endpoint, access_token)

#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         backend_data = backend_url_list.json()
#         return render(request, 'backendurl.html', {'form': backend_data})    
#     # except Exception as error:
#     #     # print(f'Error: {error}')  
#     #     # return render(request, '500page.html', {'error': str(error)})


@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
def get_backendurl_single(request,pk,accessType):
    try:
        access_token = request.session.get('access_token', '')
        endpoint = f'getBackend/{pk}/{accessType}'
        print('////////////endpointtttttttttttttttttt/////////////')

        print('endpointtttttttttttttttttt',endpoint)
        backend_url_list = call_get_method(BASE_URL, endpoint, access_token)
        if backend_url_list.status_code != 200:
            return render(request, '500page.html', {'error': backend_url_list.json()})
        backend_data = backend_url_list.json() 
        print("backend_data",backend_data) 
        return render(request, 'get_backent_single.html', {'form': backend_data})    

    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})




@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required 
def backend_edit(request, pk, accessType):
    try:
        if not request.session.get('access_token'):
            messages.error(request, "Authentication required")
            return redirect('login')

        access_token = request.session['access_token']

        # Handle GET request - show edit form
        if request.method == 'GET':
            endpoint = f"getBackend/{pk}/{accessType}"
            response = call_get_method(BASE_URL, endpoint, access_token)
            
            if response.status_code == 200:
                backend_data = response.json()
                return render(request, 'backend_edit.html', {
                    'backend': backend_data,
                    'pk': pk,
                    'accessType': accessType
                })
            else:
                messages.error(request, f"Failed to fetch backend data: {response.text}")
                return redirect("backendurl")

        # Handle POST request - process form submission
        elif request.method == 'POST':
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({
                    'success': False,
                    'error': 'Invalid JSON data'
                }, status=400)

            # Validate required fields
            required_fields = ['name', 'apiURL']
            for field in required_fields:
                if not data.get(field):
                    return JsonResponse({
                        'success': False,
                        'error': f'{field} is required'
                    }, status=400)

            # Determine which endpoint to use based on accessType
            endpoint = f"modify{'Private' if accessType == 'private' else ''}Backend/{pk}"
            response = call_put_method(BASE_URL, endpoint, json.dumps(data), access_token)

            if response.status_code == 200:
                return JsonResponse({
                    'success': True,
                    'message': f'{accessType.capitalize()} backend updated successfully'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'error': f'Failed to update {accessType} backend',
                    'details': response.text
                }, status=400)

        return JsonResponse({
            'error': 'Invalid request method'
        }, status=405)

    except Exception as error:
        logger.error(f'Backend edit error: {error}')
        return JsonResponse({
            'success': False,
            'error': 'An unexpected error occurred'
        }, status=500)
# final code:
# def backend_edit(request, pk, accessType):
#     try:
#         access_token = request.session.get('access_token')

#         # Fetch existing backend data
#         if request.method == 'GET':
#             endpoint = f"getBackend/{pk}/{accessType}"  # API call to get existing backend data
#             response = call_get_method(BASE_URL, endpoint, access_token)
#             if response.status_code == 200:
#                 backend_data = response.json()
#                 return render(request, 'backend_edit.html', {'backend': backend_data, 'pk': pk , 'accessType': accessType})
                
#             else:
#                 messages.error(request, "Error fetching backend data")
#                 return redirect("backendurl")

       
#         elif request.method == 'POST':
#             data = json.loads(request.body)  
            
#             public_endpoint = f"modifyBackend/{pk}"  
#             private_endpoint = f"modifyPrivateBackend/{pk}" 

            
#             public_response = call_put_method(BASE_URL, public_endpoint, json.dumps(data), access_token)
#             private_response = call_put_method(BASE_URL, private_endpoint, json.dumps(data), access_token)
#             print("endddddddddddddddddd",public_endpoint)
           
#             if public_response.status_code == 200 and private_response.status_code == 200:
#                 messages.success(request, "Backend data updated successfully in both public and private endpoints.")
#                 return JsonResponse({'success': True, 'message': 'Backend data updated successfully in both endpoints'})
#             else:
#                 return JsonResponse({'success': False, 'error': 'Failed to update backend data'}, status=400)

#         return JsonResponse({'error': 'Invalid request method'}, status=400)

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})

# def backend_edit(request, pk, accessType):
#     try:
#         access_token = request.session.get('access_token')
#         # Fetch existing backend data
#         if request.method == 'GET':
#             endpoint = f"getBackend/{pk}/{accessType}"  # API call to get existing backend data
#             response = call_get_method(BASE_URL, endpoint, access_token)
#             if response.status_code == 200:
#                 backend_data = response.json()
#                 return render(request, 'backend_edit.html', {'backend': backend_data, 'pk': pk})
#             else:
#                 messages.error(request, "Error fetching backend data")
#                 return redirect("backendurl")

#         # Handle update request
#         elif request.method == 'POST':
#             data = json.loads(request.body)  # Get updated data from request
#             endpoint = f"modifyBackend/{pk}"  # API endpoint for updating
#             response = call_put_method(BASE_URL, endpoint, json.dumps(data), access_token)

#             if response.status_code == 200:
#                 messages.success(request, "Backend data updated successfully.")
#                 return JsonResponse({'success': True, 'message': 'Backend data updated successfully'})
#             else:
#                 return JsonResponse({'success': False, 'error': 'Failed to update backend data'}, status=400)

#         return JsonResponse({'error': 'Invalid request method'}, status=400)

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})


@role_required(allowed_roles=['ADMIN'])
@custom_login_required
@csrf_exempt
def register_backend_delete(request, pk, accessType):
    """
    Handle DELETE requests to remove a backend URL entry.
    """
    try:
        print(f"Received request method: {request.method}")  # Debugging log
        access_token = request.session.get('access_token')  # Get access token

        if request.method == 'POST':  # Change from DELETE to POST for template compatibility
            endpoint = f"{BASE_URL}deleteBackend/{pk}/{accessType}"  # Construct API endpoint
            print("endpoint check....................................")
            print("endpoint name ",endpoint)
            headers = {"Authorization": access_token}

            response = requests.delete(endpoint, headers=headers)  # Call the API
            print("resssssssssssssssss",response)
            if response.status_code == 200:
                messages.success(request, "Backend entry deleted successfully!")
            else:
                messages.error(request, f"Error deleting entry: {response.text}")

            return redirect("backendurl")  # Redirect back to the list page

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': str(error)})

    return redirect("backendurl")
# def register_backend_delete(request, pk,accessType):
#     try:
#         """
#         Handle DELETE requests for backend deletion.
#         """
#         print(f"Received request method: {request.method}")  # Debugging: Log received method
#         access_token = request.session['access_token']
#         if request.method == 'DELETE':  # Only process DELETE requests
#             endpoint = f"/deleteBackend/{pk}/{accessType}"  # Construct API endpoint
#             response = call_delete_method(BASE_URL, endpoint, access_token)
#             if response.status_code == 200:
#                 try:
#                     response_data = response.json() 
#                     messages.success(request,response.text)
#                     print("respoooooq",response.text)
#                     return redirect("backendurl")
#                 except ValueError:
#                     print("respooooo3",response.text)
#                     response.text 
#                     return redirect("backendurl")
#             else:
#                 return redirect("backendurl")
#         return redirect("backendurl")
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})


#
@role_required(allowed_roles=['ADMIN'])
@custom_login_required
@csrf_exempt
def register_frontend_delete(request, pk):
    try:
        access_token = request.session['access_token']
        
        if request.method == 'POST':  # Accept POST instead of DELETE
            endpoint = f"deleteFrontend/{pk}"
            response = call_delete_method(BASE_URL, endpoint, access_token)

            if response.status_code == 200:
                messages.success(request, "Deleted successfully")
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'error': 'Error deleting data'}, status=response.status_code)
        
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
    except Exception as error:
        print(f'Error: {error}')
        return JsonResponse({'error': str(error)}, status=500)
    
# def register_frontend_delete(request, pk):
#     try:
#         """
#         Handle DELETE requests for backend deletion.
#         """
#         access_token = request.session['access_token']
#         if request.method == 'DELETE':  # Only process DELETE requests
#             endpoint = f"deleteFrontend/{pk}"  # Construct API endpoint
#             response = call_delete_method(BASE_URL, endpoint, access_token)

#             if response.status_code == 200:
#                 try:
#                     messages.success(request, response.text)  # Optionally display message
#                     return JsonResponse({'success': True})
#                 except ValueError:
#                     return JsonResponse({'success': True})
#             else:
#                 return JsonResponse({'error': 'Error deleting data'}, status=response.status_code)
        
#         return JsonResponse({'error': 'Invalid request method'}, status=405)
    
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})


@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def processtable(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get data source
        data_source = request.GET.get('source', 'public')
        given_by = request.GET.get('givenBy', '').strip()

        print(f"Received source: {data_source}")  # Debugging

        if data_source == "public":
            endpoint = "getProcessTableList"
        elif data_source == "private":
            endpoint = "getPrivateProcessTableList"
        elif data_source == "givenBy":  
            if not given_by:
                return render(request, 'processtable.html', {'error': 'Please enter a GivenBy ID.'})
            endpoint = f"getOtherPrivateProcessTableList?userName={given_by}"
        else:
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")  # Debugging

        process_list = call_get_method(BASE_URL, endpoint, access_token)

        if process_list.status_code != 200:
            print(f"API Error: {process_list.status_code} - {process_list.text}")  # Debugging
            return render(request, '500page.html', {'error': process_list.text})

        process_data = process_list.json()
        print(f"Fetched {len(process_data)} records from {endpoint}")  # Debugging

        reversed_data = process_data[::-1]  # Reverse the list

        return render(request, 'processtable.html', {
            'form': reversed_data,
            'source': data_source,
            'givenBy': given_by
        })

    except Exception as error:
        print(f'Error in processtable view: {error}')  # Debugging
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def processtable(request):
#     try:
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         # Determine data source based on query parameter
#         data_source = request.GET.get('source', 'public')

#         if data_source == "public":
#             endpoint = "getProcessTableList"
#         elif data_source == "private":
#             endpoint = "getPrivateProcessTableList"
#         elif data_source == "givenBy":
#             endpoint = "getOtherPrivateProcessTableList"
#         else:
#             return render(request, '500page.html', {'error': 'Invalid data source'})

#         process_list = call_get_method(BASE_URL, endpoint, access_token)

#         if process_list.status_code != 200:
#             return render(request, '500page.html', {'error': process_list.json()})

#         process_data = process_list.json()
#         count = len(process_data)
#         print("Total count:", count)
#         print("Process data:", process_data)

#         reversed_data = process_data[::-1]  # Reverse the list

#         return render(request, 'processtable.html', {'form': reversed_data, 'source': data_source})

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': 'An error occurred while fetching process table data.'})

# def processtable(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getProcessTableList"
#         process_list = call_get_method(BASE_URL, endpoint, access_token)
        
#         if process_list.status_code != 200:
#             return render(request, '500page.html', {'error': process_list.json()})

#         process_data = process_list.json()
#         count = len(process_data)
#         print("Total count:", count)
#         print("process_data",process_data)
#         reversed_data = process_data[::-1]  # Reverse the list
#         return render(request, 'processtable.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def unprocesstable(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get data source
        data_source = request.GET.get('source', 'public')
        given_by = request.GET.get('givenBy', '').strip()

        print(f"Received source: {data_source}")  # Debugging

        if data_source == "public":
            endpoint = "getUnProcessTableList"
        elif data_source == "private":
            endpoint = "getPrivateUnProcessTableList"
        elif data_source == "givenBy":
            if not given_by:
                return render(request, 'unprocesstable.html', {'error': 'Please enter a GivenBy ID.'})
            endpoint = f"getOtherPrivateUnProcessTableList?userName={given_by}"
        else:
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")  # Debugging

        unprocess_list = call_get_method(BASE_URL, endpoint, access_token)

        if unprocess_list.status_code != 200:
            print(f"API Error: {unprocess_list.status_code} - {unprocess_list.text}")  # Debugging
            return render(request, '500page.html', {'error': unprocess_list.text})

        unprocess_data = unprocess_list.json()
        print(f"Fetched {len(unprocess_data)} records from {endpoint}")  # Debugging

        reversed_data = unprocess_data[::-1]  # Reverse the list

        return render(request, 'unprocesstable.html', {
            'form': reversed_data,
            'source': data_source,
            'givenBy': given_by
        })

    except Exception as error:
        print(f'Error in unprocesstable view: {error}')  # Debugging
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def unprocesstable(request):
#     try:
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         # Get the data source from URL parameters
#         data_source = request.GET.get('source', 'public')
#         print(f"Received source: {data_source}")  # Debugging

#         if data_source == "public":
#             endpoint = "getUnProcessTableList"
#         elif data_source == "private":
#             endpoint = "getPrivateUnProcessTableList"
#         elif data_source == "givenBy":
#             endpoint = "getOtherPrivateUnProcessTableList"
#         else:
#             print("Invalid data source requested")  # Debugging
#             return render(request, '500page.html', {'error': 'Invalid data source'})

#         print(f"Calling API Endpoint: {endpoint}")  # Debugging

#         unprocess_list = call_get_method(BASE_URL, endpoint, access_token)

#         if unprocess_list.status_code != 200:
#             print(f"API Error: {unprocess_list.status_code} - {unprocess_list.json()}")  # Debugging
#             return render(request, '500page.html', {'error': unprocess_list.json()})

#         unprocess_data = unprocess_list.json()
#         print(f"Fetched {len(unprocess_data)} records from {endpoint}")  # Debugging

#         reversed_data = unprocess_data[::-1]  # Reverse the list

#         return render(request, 'unprocesstable.html', {'form': reversed_data, 'source': data_source})

#     except Exception as error:
#         print(f'Error in unprocesstable view: {error}')  # Debugging
#         return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def unprocesstable(request):
#     try:
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         # Determine data source based on query parameter
#         data_source = request.GET.get('source', 'public')

#         if data_source == "public":
#             endpoint = "getUnProcessTableList"
#         elif data_source == "private":
#             endpoint = "getPrivateUnProcessTableList"
#         elif data_source == "givenBy":
#             endpoint = "getOtherPrivateUnProcessTableList"
#         else:
#             return render(request, '500page.html', {'error': 'Invalid data source'})

#         unprocess_list = call_get_method(BASE_URL, endpoint, access_token)

#         if unprocess_list.status_code != 200:
#             return render(request, '500page.html', {'error': unprocess_list.json()})

#         unprocess_data = unprocess_list.json()
#         unprocess_count = len(unprocess_data)
#         print("Total Unprocessed Count:", unprocess_count)
#         print("Unprocessed Data:", unprocess_data)

#         reversed_data = unprocess_data[::-1]  # Reverse the list

#         return render(request, 'unprocesstable.html', {'form': reversed_data, 'source': data_source})

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': 'An error occurred while fetching unprocessed table data.'})

# def unprocesstable(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getUnProcessTableList"
#         unprocess_list = call_get_method(BASE_URL, endpoint, access_token)
#         if unprocess_list.status_code != 200:
#             return render(request, '500page.html', {'error': unprocess_list.json()})
#         unprocess_data = unprocess_list.json()
#         unprocess_count = len(unprocess_data)
#         reversed_data = unprocess_data[::-1]  # Reverse the list

#         return render(request, 'unprocesstable.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    

#ajaxxx
from django.http import JsonResponse

def get_process_data(request):
    # Check if it's an AJAX request by verifying the 'X-Requested-With' header
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

    access_token = request.session.get('access_token')
    endpoint = "getProcessTableList"
    process_list = call_get_method(BASE_URL, endpoint, access_token)

    if process_list.status_code != 200:
        return JsonResponse({'success': False, 'message': 'Error fetching data'})

    process_data = process_list.json()
    return JsonResponse({'success': True, 'items': process_data})

def get_unprocess_data(request):
    # Check if it's an AJAX request by verifying the 'X-Requested-With' header
    if request.headers.get('X-Requested-With') != 'XMLHttpRequest':
        return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)

    access_token = request.session.get('access_token')
    endpoint = "getUnProcessTableList"
    unprocess_list = call_get_method(BASE_URL, endpoint, access_token)

    if unprocess_list.status_code != 200:
        return JsonResponse({'success': False, 'message': 'Error fetching data'})

    unprocess_data = unprocess_list.json()
    return JsonResponse({'success': True, 'items': unprocess_data})


###############################################################################################
#                                         SERVICE

import requests
import json
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def servicesection_be(request):
    try:
        access_token = request.session['access_token']
        endpoint = "ServiceRegister"
        endpoint1 = "getAllService"
        endpoint2 = "getAllBackend"  # Public backend
        endpoint4 = "getAllPrivateBackend"  # Private backend

        # Fetch Public Service Data
        backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
        if backend_url_list.status_code != 200:
            return render(request, '500page.html', {'error': backend_url_list.json()})
        backend_data = backend_url_list.json()

        # Fetch Public and Private Backend Data
        backend_url_list1 = call_get_method(BASE_URL, endpoint2, access_token)
        backend_url_list2 = call_get_method(BASE_URL, endpoint4, access_token)

        if backend_url_list1.status_code != 200 or backend_url_list2.status_code != 200:
            return render(request, '500page.html', {'error': 'Failed to fetch backend data'})

        # Merge Public and Private backend data
        backend_data1 = backend_url_list1.json() + backend_url_list2.json()

        if request.method == "POST":
            # Extract form data
            service_name = request.POST.get("field_name")
            backend_ids = request.POST.getlist("backend_id[]")
            depend_api_required = "depend_api_required" in request.POST
            depend_service_id = request.POST.getlist("depend_service_id[]")
            depend_api_url = request.POST.get("depend_api_url", "")
            url_type = request.POST.get("url_type", "")
            depend_api_param_required = "depend_api_parameter_required" in request.POST
            visibility = "private" if request.POST.get('visibility') == 'on' else "public"
            print(f"Final visibility: {visibility}")

            # Dynamic Depend API Params
            depend_api_params = []
            depend_param_count = int(request.POST.get("depend_param_count", 0))

            for i in range(1, depend_param_count + 1):
                param_name = request.POST.get(f"param_name_{i}")
                data_type = request.POST.get(f"data_type_{i}")
                mandatory = request.POST.get(f"is_mandatory_{i}") == "on"
                min_length = request.POST.get(f"min_length_{i}")
                max_length = request.POST.get(f"max_length_{i}")
                depend_param = request.POST.get(f"depend_param_{i}") == "on"
                depend_param_name = request.POST.get(f"depend_param_name_{i}")

                if param_name:
                    depend_api_params.append({
                        "name": param_name,
                        "dataType": data_type,
                        "isMandatory": mandatory,
                        "minLength": int(min_length) if min_length else None,
                        "maxLength": int(max_length) if max_length else None,
                        "dependParam": depend_param,
                        "dependParameterName": depend_param_name if depend_param_name else None,
                    })

            # Payload Construction
            api_payload = {
                "serviceName": service_name,
                "backendID": [int(bid) for bid in backend_ids if bid],
                "dependAPIRequired": depend_api_required,
                "dependBackendID": [int(did) for did in depend_service_id if did],
                "dependAPIURL": depend_api_url or None,
                "dependUrlType": url_type,
                "dependAPIParamRequired": depend_api_param_required,
                "dependAPIParam": depend_api_params,
                "visibility": visibility,
            }
            print("API Payload:", api_payload)

            # API call to Register Service
            try:
                response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
                if response.status_code != 200:
                    messages.error(request, f"API Error: {response.text}")
                    return redirect("servicesection")
                else:
                    messages.success(request, f"{response.text}")
                    return redirect("get_all_services")
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request Error: {str(e)}")
                return redirect("get_all_services")

        else:
            form = ServiceSectionForm()
            return render(request, 'servicesection.html', {
                'form': form,
                'backend_data': backend_data,
                'backend_data1': backend_data1
            })

    except Exception as error:
        print(f"Error: {error}")
        return render(request, '500page.html', {'error': str(error)})

# def servicesection_be(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "ServiceRegister"
#         endpoint1 = "getAllService" 
#         endpoint2 = "getAllBackend"
#         endpoint4 ="getAllPrivateBackend"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         elif backend_url_list.status_code == 200:
#             print("backend_url_list",backend_url_list.text)
#         backend_data = backend_url_list.json()
#         backend_url_list1 = call_get_method(BASE_URL, endpoint2, access_token)
#         if backend_url_list1.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list1.json()})
#         backend_data1 = backend_url_list1.json()
#         if request.method == "POST":
#             # Extract form data
#             service_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_service_id = request.POST.getlist("depend_service_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_param_required = "depend_api_parameter_required" in request.POST
#             visibility = request.POST.get('visibility', 'public')
#             print(f"Final visibility: {visibility}")
#             # Dynamic fields processing
#             depend_api_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))

#             for i in range(1, depend_param_count + 1):
#                 param_name = request.POST.get(f"param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 mandatory = request.POST.get(f"is_mandatory_{i}", "") == "on"
#                 min_length = request.POST.get(f"min_length_{i}", "")
#                 max_length = request.POST.get(f"max_length_{i}", "")
#                 depend_param = request.POST.get(f"depend_param_{i}", "") == "on"
#                 depend_param_name = request.POST.get(f"depend_param_name_{i}")
#                 print("mandatory",mandatory)

#                 if param_name:  # Ensure field is not empty
#                     depend_api_params.append({
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": mandatory,
#                         "minLength": int(min_length) if min_length else None,
#                         "maxLength": int(max_length) if max_length else None,
#                         "dependParam": depend_param,
#                         "dependParameterName": depend_param_name if depend_param_name else None ,
#                     })

#             # Construct payload
#             api_payload = {
#                 "serviceName": service_name,
#                 "backendID": [int(bid) for bid in backend_ids if bid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependBackendID": [int(did) for did in depend_service_id if did],
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType":url_type,
#                 "dependAPIParamRequired": depend_api_param_required,
#                 "dependAPIParam": depend_api_params,
#                  "visibility": visibility, 
#             }
#             print("api_payload",api_payload)
#             # API call logic
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
#                 if response.status_code != 200:
#                     messages.error(request, f"API Error: {response.text}")
#                     return redirect("servicesection")
#                 elif response.status_code == 200:
#                     messages.success(request, f"{response.text}")
#                     return redirect("get_all_services")
#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect("get_all_services")
#         else:
#             form = ServiceSectionForm()
#             return render(request, 'servicesection.html', {'form': form,'backend_data':backend_data,'backend_data1':backend_data1
#             })
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
####################################################################################################
#                                   PROCESS SECTION 
# POST
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def process_section(request):
    try:
        access_token = request.session['access_token']
        endpoint = "ProcessRegister"
        service_public_endpoint = "getAllService"
        service_private_endpoint = "getAllPrivateService"
        process_public_endpoint = "getAllProcess"
        process_private_endpoint = "getAllPrivateProcess"

        # Fetch Public and Private Services
        service_public = call_get_method(BASE_URL, service_public_endpoint, access_token)
        service_private = call_get_method(BASE_URL, service_private_endpoint, access_token)

        if service_public.status_code != 200 or service_private.status_code != 200:
            return render(request, '500page.html', {'error': 'Failed to fetch service data'})

        backend_data = service_public.json() + service_private.json()

        # Fetch Public and Private Processes (for listing if needed)
        process_public = call_get_method(BASE_URL, process_public_endpoint, access_token)
        process_private = call_get_method(BASE_URL, process_private_endpoint, access_token)

        if process_public.status_code != 200 or process_private.status_code != 200:
            return render(request, '500page.html', {'error': 'Failed to fetch process data'})

        backend_data1 = process_public.json() + process_private.json()

        if request.method == "POST":
            # Extract form data
            name = request.POST.get("field_name")
            backend_ids = request.POST.getlist("backend_id[]")
            depend_api_required = "depend_api_required" in request.POST
            depend_service_id = request.POST.getlist("depend_service_id[]")
            depend_api_url = request.POST.get("depend_api_url", "")
            url_type = request.POST.get("url_type", "")
            depend_api_param_required = "depend_api_parameter_required" in request.POST
            visibility = "private" if request.POST.get('visibility') == 'on' else "public"
            print(f"Final visibility: {visibility}")

            # Handle dynamic parameter fields
            depend_api_params = []
            depend_param_count = int(request.POST.get("depend_param_count", 0))
            for i in range(1, depend_param_count + 1):
                param_name = request.POST.get(f"depend_param_name_{i}")
                data_type = request.POST.get(f"data_type_{i}")
                is_mandatory = request.POST.get(f"is_mandatory_{i}") == "on"
                min_length = request.POST.get(f"min_length_{i}")
                max_length = request.POST.get(f"max_length_{i}")
                depend_param = request.POST.get(f"depend_param_{i}") == "on"
                dependParameterName = request.POST.get(f"depend_parameter_name_{i}")

                if param_name:
                    param_data = {
                        "name": param_name,
                        "dataType": data_type,
                        "isMandatory": is_mandatory,
                        "minLength": int(min_length) if min_length else None,
                        "maxLength": int(max_length) if max_length else None,
                        "dependParam": depend_param,
                        "dependParameterName": dependParameterName if dependParameterName else None,
                    }
                    depend_api_params.append(param_data)

            # Construct API payload
            api_payload = {
                "processName": name,
                "serviceID": [int(sid) for sid in backend_ids if sid],
                "dependAPIRequired": depend_api_required,
                "dependingServiceID": [int(did) for did in depend_service_id if did],
                "dependAPIURL": depend_api_url or None,
                "dependUrlType": url_type or None,
                "dependAPIParamRequired": depend_api_param_required,
                "dependAPIParam": depend_api_params,
                "visibility": visibility,
            }
            print("API Payload:", api_payload)

            # API call
            try:
                response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
                if response.status_code != 200:
                    messages.error(request, f"API Error: {response.text}")
                    return redirect('processsection')
                else:
                    messages.success(request, f"{response.text}")
                    return redirect('get_all_processes')
            except requests.exceptions.RequestException as e:
                messages.error(request, f"Request Error: {str(e)}")
                return redirect('processsection')

        else:
            form = ProcessSectionForm()
            return render(request, 'process_section.html', {
                'form': form,
                'backend_data': backend_data,
                'backend_data1': backend_data1
            })

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': str(error)})

# def process_section(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "ProcessRegister"
#         endpoint1 = "getAllService"
#         endpoint2="getAllProcess"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         backend_data = backend_url_list.json()

#         backend_url_list1 = call_get_method(BASE_URL, endpoint2, access_token)
#         if backend_url_list1.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list1.json()})
#         backend_data1 = backend_url_list1.json()
#         if request.method == "POST":
#             # Extract form data
#             name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_service_id = request.POST.getlist("depend_service_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_param_required = "depend_api_parameter_required" in request.POST
#             visibility = request.POST.get('visibility', 'public')
#             print(f"Final visibility: {visibility}")


#             # Handle dynamic parameter fields
#             depend_api_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))
#             for i in range(1, depend_param_count + 1):
#                 param_name = request.POST.get(f"depend_param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}") == "on"
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}") == "on"
#                 dependParameterName = request.POST.get(f"depend_parameter_name_{i}")


#                 # Append param data if param_name is present
#                 if param_name:
#                     param_data = {
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": is_mandatory == 'on',  # Check if box is checked
#                         "minLength": min_length,
#                         "maxLength": max_length,
#                         "dependParam": depend_param == 'on',  # Check if box is checked
#                         "dependParameterName":dependParameterName if dependParameterName else None,
#                     }
#                     depend_api_params.append(param_data)

#             print("depend_api_params:", depend_api_params)  # Debug output for verification

#             # Construct API payload
#             api_payload = {
#                 "processName": name,
#                 "serviceID": [int(sid) for sid in backend_ids if sid],  # Renamed `backendID` to `serviceID` to match the JSON structure
#                 "dependAPIRequired": depend_api_required,
#                 "dependingServiceID": [int(did) for did in depend_service_id if did],  # Renamed `dependBackendID` to `dependingServiceID`
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType":url_type or None,
#                 "dependAPIParamRequired": depend_api_param_required,
#                 "dependAPIParam": depend_api_params,  # Kept `dependAPIParam` as it matches the JSON structure
#                 "visibility": visibility,
#             }


#             print("api_payload:", api_payload)  # Debugging output to verify payload

#             # API call with payload
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)

#                 if response.status_code != 200:
#                     # Log the error details
#                     print(f"API Error: {response.status_code}, {response.text}")
#                     messages.error(request, f"API returned an error: {response.text}")
#                     return redirect('processsection')  # Redirect to the processsection URL

#                 # Parse JSON response safely
#                 try:
#                     response_data = response.text
#                     print("Response from backend:", response_data)
#                 except ValueError:
#                     # Handle case where response is not valid JSON
#                     print("Error: Response is not valid JSON.")
#                     messages.error(request, "Backend returned invalid JSON.")
#                     return redirect('get_all_processes')  # Redirect to the processsection URL

#                 # Redirect with success message
#                 messages.success(request, "Backend processed successfully!")
#                 return redirect('get_all_processes')  # Redirect to the processsection URL

#             except requests.exceptions.RequestException as e:
#                 # Log the request exception and redirect with error message
#                 print(f"Request Error: {e}")
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect('processsection')  # Redirect to the processsection URL
#         else:
#             # Handle GET request by returning an empty form
#             form = ProcessSectionForm()
#             return render(request, 'process_section.html', {'form': form,'backend_data':backend_data,'backend_data1':backend_data1})

#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

# ------------------------------------------service process---------------------------------

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
@csrf_exempt

def service_process(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            messages.error(request, "Access token missing.")
            return redirect('login')  # Redirect to login or appropriate page

        endpoint = "ServiceProcessRegister"

        # === FETCH BOTH PUBLIC AND PRIVATE PROCESSES ===
        public_process = call_get_method(BASE_URL, "getAllProcess", access_token)
        private_process = call_get_method(BASE_URL, "getAllPrivateProcess", access_token)

        if public_process.status_code != 200 or private_process.status_code != 200:
            return render(request, '500page.html', {'error': 'Error fetching process data'})

        backend_data = public_process.json() + private_process.json()

        # === FETCH BOTH PUBLIC AND PRIVATE SERVICE PROCESSES ===
        public_service = call_get_method(BASE_URL, "getAllServiceProcess", access_token)
        private_service = call_get_method(BASE_URL, "getAllPrivateServiceProcess", access_token)

        if public_service.status_code != 200 or private_service.status_code != 200:
            return render(request, '500page.html', {'error': 'Error fetching service-process data'})

        backend_data1 = public_service.json() + private_service.json()

        # === POST: Create a New Service Process ===
        if request.method == "POST":
            try:
                service_name = request.POST.get("field_name")
                backend_ids = request.POST.getlist("backend_id[]")
                depend_api_required = "depend_api_required" in request.POST
                depend_process_id = request.POST.getlist("depend_process_id[]")
                depend_api_url = request.POST.get("depend_api_url", "")
                url_type = request.POST.get("url_type", "")
                depend_api_parameter_required = "depend_api_parameter_required" in request.POST
                visibility = "private" if request.POST.get("visibility") == "on" else "public"

                # Build API Parameters
                param_count = int(request.POST.get("depend_param_count", 0))
                api_params = []

                for i in range(1, param_count + 1):
                    param_name = request.POST.get(f"depend_param_name_{i}")
                    data_type = request.POST.get(f"data_type_{i}")
                    is_mandatory = request.POST.get(f"is_mandatory_{i}") == 'on'
                    min_length = request.POST.get(f"min_length_{i}")
                    max_length = request.POST.get(f"max_length_{i}")
                    depend_param = request.POST.get(f"depend_param_{i}") == 'on'

                    if param_name and data_type:
                        api_params.append({
                            "name": param_name,
                            "dataType": data_type,
                            "isMandatory": is_mandatory,
                            "minLength": int(min_length) if min_length else None,
                            "maxLength": int(max_length) if max_length else None,
                            "dependParam": depend_param,
                        })

                # Final Payload
                api_payload = {
                    "serviceProcessName": service_name,
                    "processID": [int(pid) for pid in backend_ids if pid],
                    "dependAPIRequired": depend_api_required,
                    "dependingProcessID": [int(did) for did in depend_process_id if did],
                    "dependAPIURL": depend_api_url or None,
                    "dependUrlType": url_type or None,
                    "dependAPIParamRequired": depend_api_parameter_required,
                    "dependAPIParam": api_params,
                    "visiblility": visibility,
                }

                # API Call to Save
                response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)

                if response.status_code != 200:
                    content_type = response.headers.get('Content-Type', '')
                    error_message = response.json() if 'application/json' in content_type else response.text
                    messages.error(request, f"API Error: {error_message}")
                    return redirect('get_all_serviceprocess')

                messages.success(request, f"Service Process '{service_name}' created successfully.")
                return redirect('get_all_serviceprocess')

            except Exception as post_error:
                print("POST Error:", str(post_error))
                messages.error(request, f"Error during form submission: {str(post_error)}")
                return redirect('get_all_serviceprocess')

        # === GET: Render Form with Data ===
        else:
            form = ServiceProcessForm()
            return render(request, 'service_process.html', {
                'form': form,
                'backend_data': backend_data,     # All processes (public + private)
                'backend_data1': backend_data1,   # All service-processes (public + private)
            })

    except Exception as error:
        print("Top-level Exception:", str(error))
        return render(request, '500page.html', {'error': str(error)})


# def service_process(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "ServiceProcessRegister"
#         print("request.post",request.POST)
#         # Process Fetch APIs
#         public_process_endpoint = "getAllProcess"
#         private_process_endpoint = "getAllPrivateProcess"

#         # ServiceProcess Fetch APIs
#         public_serviceprocess_endpoint = "getAllServiceProcess"
#         private_serviceprocess_endpoint = "getAllPrivateServiceProcess"

#         # Fetch Public and Private Processes
#         process_public = call_get_method(BASE_URL, public_process_endpoint, access_token)
#         process_private = call_get_method(BASE_URL, private_process_endpoint, access_token)
#         print("process_private",process_private.text)
#         print("process_public",process_public.text)

#         if process_public.status_code != 200 or process_private.status_code != 200:
#             return render(request, '500page.html', {'error': 'Error fetching process data'})

#         backend_data = process_public.json() + process_private.json()

#         # Fetch Public and Private Service Processes
#         serviceproc_public = call_get_method(BASE_URL, public_serviceprocess_endpoint, access_token)
#         serviceproc_private = call_get_method(BASE_URL, private_serviceprocess_endpoint, access_token)

#         if serviceproc_public.status_code != 200 or serviceproc_private.status_code != 200:
#             return render(request, '500page.html', {'error': 'Error fetching service-process data'})

#         backend_data1 = serviceproc_public.json() + serviceproc_private.json()

#         if request.method == "POST":
#             # Retrieve form fields
#             service_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_process_id = request.POST.getlist("depend_process_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_parameter_required = "depend_api_parameter_required" in request.POST
#             visibility = "private" if request.POST.get('visibility') == 'on' else "public"
#             print(f"Final visibility: {visibility}")

#             # Parameters
#             api_params = []
#             param_count = int(request.POST.get("depend_param_count", 0))

#             for i in range(1, param_count + 1):
#                 param_name = request.POST.get(f"depend_param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}") == 'on'
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}") == 'on'

#                 if param_name and data_type:
#                     api_params.append({
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": is_mandatory,
#                         "minLength": int(min_length) if min_length else None,
#                         "maxLength": int(max_length) if max_length else None,
#                         "dependParam": depend_param,
#                     })

#             # Build Payload
#             api_payload = {
#                 "serviceProcessName": service_name,
#                 "processID": [int(pid) for pid in backend_ids if pid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependingProcessID": [int(did) for did in depend_process_id if did],
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType": url_type or None,
#                 "dependAPIParamRequired": depend_api_parameter_required,
#                 "dependAPIParam": api_params,
#                 "visibility": visibility,
#             }
#             print("payload", api_payload)

#             # Call POST API
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)

#                 if response.status_code != 200:
#                     error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
#                     messages.error(request, f"API Error: {error_message}")
#                     return redirect('get_all_serviceprocess')

#                 response_data = response.text
#                 messages.success(request, f"API Success: {response_data}")
#                 return redirect('get_all_serviceprocess')

#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect('get_all_serviceprocess')

#         else:
#             form = ServiceProcessForm()
#             return render(request, 'service_process.html', {
#                 'form': form,
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1
#             })

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})


#  def service_process(request):
#     try:
#         print("\n=== START OF service_process VIEW ===")
#         print("1. Checking session authentication...")

#         # Authentication check
#         if 'access_token' not in request.session:
#             print("! ERROR: No access_token in session")
#             messages.error(request, "Session expired. Please login again.")
#             return redirect('login')

#         access_token = request.session['access_token']
#         print(f"2. Access token found: {access_token[:5]}...{access_token[-5:]}")

#         # Check for JSESSIONID cookie
#         jsessionid = request.COOKIES.get('JSESSIONID')
#         if jsessionid:
#             request.session['jsessionid'] = jsessionid
#             print(f"2a. JSESSIONID found: {jsessionid}")

#         # Fetch required data from APIs
#         print("3. Starting to fetch data from APIs...")
#         try:
#             print("4. Fetching public processes...")
#             process_public = requests.get(
#                 f"{BASE_URL}getAllProcess",
#                 headers={'Authorization': access_token},
#                 timeout=30
#             )
#             print(f"5. Public processes status: {process_public.status_code}")

#             print("6. Fetching private processes...")
#             process_private = requests.get(
#                 f"{BASE_URL}getAllPrivateProcess",
#                 headers={'Authorization': access_token},
#                 timeout=30
#             )
#             print(f"7. Private processes status: {process_private.status_code}")

#             if process_public.status_code != 200 or process_private.status_code != 200:
#                 print(f"! ERROR: Failed to fetch processes - Public: {process_public.status_code}, Private: {process_private.status_code}")
#                 return render(request, '500page.html', {'error': 'Error fetching process data'})

#             backend_data = process_public.json() + process_private.json()
#             print(f"8. Combined processes count: {len(backend_data)}")

#             print("9. Fetching public service processes...")
#             serviceproc_public = requests.get(
#                 f"{BASE_URL}getAllServiceProcess",
#                 headers={'Authorization': access_token},
#                 timeout=30
#             )
#             print(f"10. Public service processes status: {serviceproc_public.status_code}")

#             print("11. Fetching private service processes...")
#             serviceproc_private = requests.get(
#                 f"{BASE_URL}getAllPrivateServiceProcess",
#                 headers={'Authorization': access_token},
#                 timeout=30
#             )
#             print(f"12. Private service processes status: {serviceproc_private.status_code}")

#             if serviceproc_public.status_code != 200 or serviceproc_private.status_code != 200:
#                 print(f"! ERROR: Failed to fetch service processes - Public: {serviceproc_public.status_code}, Private: {serviceproc_private.status_code}")
#                 return render(request, '500page.html', {'error': 'Error fetching service-process data'})

#             backend_data1 = serviceproc_public.json() + serviceproc_private.json()
#             print(f"13. Combined service processes count: {len(backend_data1)}")

#         except requests.exceptions.RequestException as e:
#             print(f"! EXCEPTION: API connection failed - {str(e)}")
#             return render(request, '500page.html', {'error': 'Failed to connect to API services'})

#         if request.method == "POST":
#             print("\n14. Handling POST request...")
#             print(f"15. Raw POST data: {request.POST}")

#             try:
#                 # Prepare API payload
#                 service_name = request.POST.get("field_name", "").strip()
#                 print(f"16. Service name from form: '{service_name}'")

#                 if not service_name:
#                     print("! ERROR: Service name is empty")
#                     messages.error(request, "Service name is required")
#                     raise ValueError("Service name is required")

#                 backend_ids = request.POST.getlist("backend_id[]")
#                 print(f"17. Backend IDs: {backend_ids}")

#                 visibility = "private" if request.POST.get('visibility') == 'on' else "public"
#                 print(f"18. Visibility: {visibility}")

#                 api_payload = {
#                     "serviceProcessName": service_name,
#                     "processID": [int(pid) for pid in backend_ids if pid],
#                     "visibility": visibility,
#                     "dependAPIRequired": "depend_api_required" in request.POST,
#                     "dependingProcessID": [int(did) for did in request.POST.getlist("depend_process_id[]") if did],
#                     "dependAPIURL": request.POST.get("depend_api_url", "").strip() or None,
#                     "dependUrlType": request.POST.get("url_type", "").strip() or None,
#                     "dependAPIParamRequired": "depend_api_parameter_required" in request.POST,
#                     "dependAPIParam": []
#                 }

#                 print("19. Base payload constructed:")
#                 print(json.dumps(api_payload, indent=2))

#                 # Handle parameters if needed
#                 if api_payload["dependAPIParamRequired"]:
#                     print("20. Processing dependent parameters...")
#                     param_count = int(request.POST.get("depend_param_count", 0))
#                     print(f"21. Parameter count: {param_count}")

#                     for i in range(1, param_count + 1):
#                         param_name = request.POST.get(f"depend_param_name_{i}", "").strip()
#                         data_type = request.POST.get(f"data_type_{i}", "").strip()

#                         if param_name and data_type:
#                             print(f"22. Adding parameter {i}: {param_name} ({data_type})")
#                             api_payload["dependAPIParam"].append({
#                                 "name": param_name,
#                                 "dataType": data_type,
#                                 "isMandatory": request.POST.get(f"is_mandatory_{i}") == 'on',
#                                 "minLength": int(request.POST.get(f"min_length_{i}", 0)) or None,
#                                 "maxLength": int(request.POST.get(f"max_length_{i}", 0)) or None,
#                                 "dependParam": request.POST.get(f"depend_param_{i}") == 'on'
#                             })

#                 print("23. Final payload before API call:")
#                 print(json.dumps(api_payload, indent=2))

#                 # Make API call with enhanced headers
#                 print("24. Making API call to ServiceProcessRegister...")
#                 headers = {
#                     'Authorization': access_token,
#                     'Content-Type': 'application/json',
#                 }
#                 if 'jsessionid' in request.session:
#                     headers['Cookie'] = f'JSESSIONID={request.session["jsessionid"]}'
#                     print("24a. Added JSESSIONID to headers")

#                 response = requests.post(
#                     f"{BASE_URL}ServiceProcessRegister",
#                     headers=headers,
#                     data=json.dumps(api_payload),
#                     timeout=30
#                 )
#                 print(f"25. API response status: {response.status_code}")
#                 print(f"25a. Response headers: {response.headers}")
#                 print(f"25b. Response text (first 200 chars): {response.text[:200]}")

#                 if response.status_code == 200:
#                     print("26. API call successful!")
#                     messages.success(request, "Service Process created successfully!")
#                     return redirect('get_all_serviceprocess')

#                 elif response.status_code == 403:
#                     print("27. Handling 403 Forbidden response")
#                     print("27a. Full 403 response content:")
#                     print(response.text)

#                     try:
#                         error_data = response.json()
#                         error_msg = error_data.get('message', response.text)
#                         print(f"27b. Extracted JSON message: {error_msg}")
#                     except ValueError:
#                         error_msg = response.text
#                         print(f"27c. Non-JSON response body: {error_msg}")

#                     if "expired" in error_msg.lower():
#                         messages.error(request, "Your session has expired. Please login again.")
#                         return redirect('login')
#                     elif "permission" in error_msg.lower():
#                         messages.error(request, "You don't have permission to create this type of service process")
#                     else:
#                         messages.error(request, f"403 Forbidden: {error_msg}")

#                 else:
#                     try:
#                         error_data = response.json()
#                         error_msg = error_data.get('message', response.text)
#                         print(f"28. API error message: {error_msg}")
#                     except ValueError:
#                         error_msg = response.text
#                         print(f"29. API returned non-JSON error: {error_msg}")
#                     messages.error(request, f"API Error: {error_msg}")

#             except ValueError as ve:
#                 print(f"30. ValueError: {str(ve)}")
#                 pass  # Already handled by messages
#             except Exception as e:
#                 print(f"31. Unexpected error: {str(e)}")
#                 messages.error(request, "An unexpected error occurred")

#             # Return form with errors
#             print("32. Rendering form with errors...")
#             form = ServiceProcessForm(request.POST)
#             return render(request, 'service_process.html', {
#                 'form': form,
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1
#             })

#         else:
#             # GET request - show form
#             print("33. Handling GET request - showing form")
#             form = ServiceProcessForm()
#             return render(request, 'service_process.html', {
#                 'form': form,
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1
#             })

#     except Exception as error:
#         print(f"! TOP-LEVEL EXCEPTION: {str(error)}")
#         print("=== END OF service_process VIEW ===")

#         return render(request, '500page.html', {'error': str(error)})
        
# def service_process(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "ServiceProcessRegister"
        
#         # Determine if we should use private or public endpoints
#         is_private = request.method == "POST" and request.POST.get("visibility") == "on"
        
#         # Get appropriate endpoints based on visibility
#         process_endpoint = "getAllPrivateProcess" if is_private else "getAllProcess"
#         service_endpoint = "getAllPrivateServiceProcess" if is_private else "getAllServiceProcess"

#         # Fetch processes
#         backend_url_list = call_get_method(BASE_URL, process_endpoint, access_token)
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
#         backend_data = backend_url_list.json()
        
#         # Fetch service processes
#         backend_url_list1 = call_get_method(BASE_URL, service_endpoint, access_token)
#         if backend_url_list1.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list1.json()})
#         backend_data1 = backend_url_list1.json()

#         if request.method == "POST":
#             # Retrieve form data
#             service_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_process_id = request.POST.getlist("depend_process_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_parameter_required = "depend_api_parameter_required" in request.POST
#             visibility = "private" if "visibility" in request.POST else "public"

#             # Process dynamic parameters
#             api_params = []
#             param_count = int(request.POST.get("depend_param_count", 0))
            
#             for i in range(1, param_count + 1):
#                 param_name = request.POST.get(f"depend_param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}", 'off') == 'on'
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}", 'off') == 'on'

#                 if param_name and data_type:
#                     api_params.append({
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": is_mandatory,
#                         "minLength": int(min_length) if min_length else None,
#                         "maxLength": int(max_length) if max_length else None,
#                         "dependParam": depend_param,
#                     })

#             # Prepare API payload
#             api_payload = {
#                 "serviceProcessName": service_name,
#                 "processID": [int(pid) for pid in backend_ids if pid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependingProcessID": [int(did) for did in depend_process_id if did],
#                 "dependAPIURL": depend_api_url if depend_api_url else None,
#                 "dependUrlType": url_type if url_type else None,
#                 "dependAPIParamRequired": depend_api_parameter_required,
#                 "dependAPIParam": api_params,
#                 "visibility": visibility,
#             }

#             # Make API call
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
                
#                 if response.status_code == 200:
#                     messages.success(request, "Service process created successfully!")
#                     return redirect('get_all_serviceprocess')
#                 else:
#                     error_msg = response.json().get('message', 'Unknown error occurred')
#                     messages.error(request, f"Failed to create service process: {error_msg}")
#             except Exception as e:
#                 messages.error(request, f"API Error: {str(e)}")
            
#             return render(request, 'service_process.html', {
#                 'form': ServiceProcessForm(request.POST),
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1
#             })

#         # GET request - show empty form
#         return render(request, 'service_process.html', {
#             'form': ServiceProcessForm(),
#             'backend_data': backend_data,
#             'backend_data1': backend_data1
#         })

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})

# ---------------------------service processs final working codse--------------------------

# def service_process(request):
#     try:
#         access_token = request.session['access_token']
#         print("Access Token:", access_token)

#         endpoint = "ServiceProcessRegister"
#         public_process_endpoint = "getAllProcess"
#         private_process_endpoint = "getAllPrivateProcess"
#         public_serviceproc_endpoint = "getAllServiceProcess"
#         private_serviceproc_endpoint = "getAllPrivateServiceProcess"

#         # Determine source (public/private)
#         source = request.GET.get("source", "public").lower()
#         print("Source:", source)

#         # Use appropriate endpoints based on source
#         process_endpoint = private_process_endpoint if source == "private" else public_process_endpoint
#         serviceproc_endpoint = private_serviceproc_endpoint if source == "private" else public_serviceproc_endpoint

#         # Fetch processes
#         process_response = call_get_method(BASE_URL, process_endpoint, access_token)
#         if process_response.status_code != 200:
#             return render(request, '500page.html', {'error': process_response.json()})
#         backend_data = process_response.json()

#         # Fetch service processes
#         serviceproc_response = call_get_method(BASE_URL, serviceproc_endpoint, access_token)
#         if serviceproc_response.status_code != 200:
#             return render(request, '500page.html', {'error': serviceproc_response.json()})
#         backend_data1 = serviceproc_response.json()

#         if request.method == "POST":
#             service_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_process_id = request.POST.getlist("depend_process_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_parameter_required = "depend_api_parameter_required" in request.POST
#             visibility = "private" if request.POST.get("visibility") == "on" else "public"
#             print("Final visibility:", visibility)

#             # Build depend parameters
#             api_params = []
#             param_count = int(request.POST.get("depend_param_count", 0))
#             for i in range(1, param_count + 1):
#                 param_name = request.POST.get(f"depend_param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}") == "on"
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}") == "on"

#                 if param_name and data_type:
#                     api_params.append({
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": is_mandatory,
#                         "minLength": int(min_length) if min_length else None,
#                         "maxLength": int(max_length) if max_length else None,
#                         "dependParam": depend_param,
#                     })

#             # Final payloadserviceProcessName
#             api_payload = {
#                 "serviceProcessName": service_name,
#                 "processID": [int(pid) for pid in backend_ids if pid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependingProcessID": [int(did) for did in depend_process_id if did],
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType": url_type or None,
#                 "dependAPIParamRequired": depend_api_parameter_required,
#                 "dependAPIParam": api_params,
#                 "visiblility": visibility,  # ✅ Corrected key
#             }
#             print("Payload:", api_payload)

#             # API POST call
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
#                 print("Response Status:", response.status_code)

#                 if response.status_code != 200:
#                     error_message = response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text
#                     messages.error(request, f"API Error: {error_message}")
#                     return redirect('get_all_serviceprocess')

#                 messages.success(request, "Service Process Registered Successfully")
#                 return redirect('get_all_serviceprocess')

#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect('get_all_serviceprocess')

#         else:
#             form = ServiceProcessForm()
#             return render(request, 'service_process.html', {
#                 'form': form,
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1,
#                 'source': source
#             })

#     except Exception as error:
#         print(f"Error: {error}")
#         return render(request, '500page.html', {'error': str(error)})



# MANI CODE 
# def service_process(request):
#     try:
#         access_token = request.session['access_token']
#         print("acessssssssssss",access_token)
#         endpoint = "ServiceProcessRegister"
#         endpoint1 = "getAllProcess"
#         private_endpoint = "getAllPrivateProcess"
#         all_service_process_endpoint1 = "getAllPrivateServiceProcess"

#         all_service_process_endpoint1_list = call_get_method(BASE_URL,all_service_process_endpoint1, access_token)
#         if all_service_process_endpoint1_list.status_code != 200:
#             return render(request, '500page.html', {'error': all_service_process_endpoint1_list.json()})


#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
        
#         private_endpoint = call_get_method(BASE_URL, endpoint1, access_token)
#         if private_endpoint.status_code != 200:
#             return render(request, '500page.html', {'error': private_endpoint.json()})
#         backend_data = private_endpoint.json()


#         endpoint2 = "getAllServiceProcess"
#         backend_url_list1 = call_get_method(BASE_URL, endpoint2, access_token)
#         if backend_url_list1.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list1.json()})
#         backend_data1 = backend_url_list1.json()

#         if request.method == "POST":
#             # Retrieve general form fields
#             service_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_process_id = request.POST.getlist("depend_process_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_parameter_required = "depend_api_parameter_required" in request.POST
#             visibility = request.POST.get('visibility', 'public')
#             print(f"Final visibility: {visibility}")


#             # Initialize list for API parameters
#             api_params = []
#             param_count = int(request.POST.get("depend_param_count", 0))

#             # Loop through the dynamic parameter fields
#             for i in range(1, param_count + 1):
#                 param_name = request.POST.get(f"depend_param_name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}", 'off') == 'on'
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}", 'off') == 'on'

#                 # Validate and append parameters
#                 if param_name and data_type:
#                     api_params.append({
#                         "name": param_name,
#                         "dataType": data_type,
#                         "isMandatory": is_mandatory,
#                         "minLength": int(min_length) if min_length else None,
#                         "maxLength": int(max_length) if max_length else None,
#                         "dependParam": depend_param,
#                     })

#             # Construct API payload
#             api_payload = {
#     "serviceProcessName": service_name,
#     "processID": [int(pid) for pid in backend_ids if pid],
#     "dependAPIRequired": depend_api_required,
#     "dependingProcessID": [int(did) for did in depend_process_id if did],
#     "dependAPIURL": depend_api_url or None,
#     "dependUrlType": url_type or None,
#     "dependAPIParamRequired": depend_api_parameter_required,
#     "dependAPIParam": api_params,
#     "visiblility": visibility,
# }
#             print("payload",api_payload)
#             print("access_token",access_token)

            
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)
#                 print("resssssssss",response)
#                 if response.status_code != 200:
#                     # Add the API error response to messages
#                     error_message = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
#                     messages.error(request, f"API Error: {error_message}")
#                     return redirect('get_all_serviceprocess')  # Redirect to the desired page

#                 # Parse the successful API response
#                 try:
#                     response_data = response.text
#                     messages.success(request, f"API Success: {response_data}")
#                 except ValueError:
#                     # Handle invalid JSON response
#                     messages.error(request, "Backend returned invalid JSON.")
#                     return redirect('get_all_serviceprocess')

#                 return redirect('get_all_serviceprocess')  # Redirect after handling response

#             except requests.exceptions.RequestException as e:
#                 # Add the request exception to messages
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect('get_all_serviceprocess')

#         else:
#             form = ServiceProcessForm()
#             return render(request, 'service_process.html', {'form': form, 'backend_data': backend_data,'backend_data1':backend_data1})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
####################################################################################################
#                                  SERVICE ORCHESTRATION SECTION 
# POST
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
@csrf_exempt
# def service_orchestration(request):
#     try:
#         access_token = request.session['access_token']
#         print("Access token:", access_token)

#         endpoint = "ServiceOrchestrationRegister"

#         # Toggle-based endpoints
#         source = request.GET.get("source", "public").lower()
#         print("Source:", source)

#         process_endpoint = "getAllPrivateServiceProcess" if source == "private" else "getAllServiceProcess"
#         orchestration_endpoint = "getAllPrivateServiceOrchestration" if source == "private" else "getAllServiceOrchestration"

#         # Fetch service processes
#         process_response = call_get_method(BASE_URL, process_endpoint, access_token)
#         if process_response.status_code != 200:
#             return render(request, '500page.html', {'error': process_response.json()})
#         backend_data = process_response.json()

#         # Fetch service orchestrations
#         orchestration_response = call_get_method(BASE_URL, orchestration_endpoint, access_token)
#         if orchestration_response.status_code != 200:
#             return render(request, '500page.html', {'error': orchestration_response.json()})
#         backend_data1 = orchestration_response.json()

#         if request.method == "POST":
#             service_orchestration_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_service_id = request.POST.getlist("depend_service_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")
#             depend_api_param_required = "depend_api_parameter_required" in request.POST
#             visibility = "private" if request.POST.get("visibility") == "on" else "public"
#             print(f"Final visibility: {visibility}")

#             # Extract parameters
#             depend_api_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))
#             for i in range(1, depend_param_count + 1):
#                 param_name = request.POST.get(f"name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}") == "on"
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}") == "on"

#                 if param_name:
#                     depend_api_params.append({
#                         "param_name": param_name,
#                         "data_type": data_type,
#                         "is_mandatory": is_mandatory,
#                         "min_length": int(min_length) if min_length else None,
#                         "max_length": int(max_length) if max_length else None,
#                         "depend_param": depend_param,
#                     })

#             # Payload
#             api_payload = {
#                 "serviceOrchestrationName": service_orchestration_name,
#                 "serviceProcessID": [int(sid) for sid in backend_ids if sid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependingServiceProcessID": [int(did) for did in depend_service_id if did],
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType": url_type or None,
#                 "dependAPIParamRequired": depend_api_param_required,
#                 "dependAPIParam": depend_api_params,
#                 "visibility": visibility,
#             }

#             print("Payload:", api_payload)

#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)

#                 if response.status_code != 200:
#                     error_message = response.json().get('message', response.text) if 'application/json' in response.headers.get('Content-Type', '') else response.text
#                     messages.error(request, f"API Error: {error_message}")
#                     return redirect("get_all_serviceorchestration")

#                 success_message = response.json().get('message', "Service Orchestration registered successfully.") if 'application/json' in response.headers.get('Content-Type', '') else "Service Orchestration registered successfully."
#                 messages.success(request, success_message)
#                 return redirect("get_all_serviceorchestration")

#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect("get_all_serviceorchestration")

#         else:
#             form = ServiceOrchestrationForm()
#             return render(request, 'service_orchestration.html', {
#                 'form': form,
#                 'backend_data': backend_data,
#                 'backend_data1': backend_data1,
#                 'source': source
#             })

#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})


def service_orchestration(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            messages.error(request, "Access token not found. Please log in.")
            return redirect('login')

        # === ENDPOINTS ===
        register_endpoint = "ServiceOrchestrationRegister"
        public_process_endpoint = "getAllServiceProcess"
        private_process_endpoint = "getAllPrivateServiceProcess"
        public_orch_endpoint = "getAllServiceOrchestration"
        private_orch_endpoint = "getAllPrivateServiceOrchestration"

        # === GET: Public + Private Service Processes ===
        public_proc_resp = call_get_method(BASE_URL, public_process_endpoint, access_token)
        private_proc_resp = call_get_method(BASE_URL, private_process_endpoint, access_token)
        if public_proc_resp.status_code != 200 or private_proc_resp.status_code != 200:
            return render(request, '500page.html', {'error': 'Error fetching service process data'})

        backend_data = public_proc_resp.json() + private_proc_resp.json()

        # === GET: Public + Private Service Orchestrations ===
        public_orch_resp = call_get_method(BASE_URL, public_orch_endpoint, access_token)
        private_orch_resp = call_get_method(BASE_URL, private_orch_endpoint, access_token)
        if public_orch_resp.status_code != 200 or private_orch_resp.status_code != 200:
            return render(request, '500page.html', {'error': 'Error fetching orchestration data'})

        backend_data1 = public_orch_resp.json() + private_orch_resp.json()

        # === POST: Handle Form Submission ===
        if request.method == "POST":
            try:
                service_orchestration_name = request.POST.get("field_name")
                backend_ids = request.POST.getlist("backend_id[]")
                depend_api_required = "depend_api_required" in request.POST
                depend_service_id = request.POST.getlist("depend_service_id[]")
                depend_api_url = request.POST.get("depend_api_url", "")
                url_type = request.POST.get("url_type", "")
                depend_api_param_required = "depend_api_parameter_required" in request.POST
                visibility = "private" if request.POST.get("visibility") == "on" else "public"

                # === Dynamic API Parameters ===
                depend_api_params = []
                depend_param_count = int(request.POST.get("depend_param_count", 0))

                for i in range(1, depend_param_count + 1):
                    param_name = request.POST.get(f"name_{i}")
                    data_type = request.POST.get(f"data_type_{i}")
                    is_mandatory = request.POST.get(f"is_mandatory_{i}", "off") == "on"
                    min_length = request.POST.get(f"min_length_{i}")
                    max_length = request.POST.get(f"max_length_{i}")
                    depend_param = request.POST.get(f"depend_param_{i}", "off") == "on"

                    if param_name:
                        depend_api_params.append({
                            "param_name": param_name,
                            "data_type": data_type,
                            "is_mandatory": is_mandatory,
                            "min_length": int(min_length) if min_length else None,
                            "max_length": int(max_length) if max_length else None,
                            "depend_param": depend_param,
                        })

                # === Final Payload ===
                api_payload = {
                    "serviceOrchestrationName": service_orchestration_name,
                    "serviceProcessID": [int(pid) for pid in backend_ids if pid],
                    "dependAPIRequired": depend_api_required,
                    "dependingServiceProcessID": [int(did) for did in depend_service_id if did],
                    "dependAPIURL": depend_api_url or None,
                    "dependUrlType": url_type,
                    "dependAPIParamRequired": depend_api_param_required,
                    "dependAPIParam": depend_api_params,
                    "visibility": visibility,
                }

                # === API Call ===
                response = call_post_with_method(BASE_URL, register_endpoint, json.dumps(api_payload), access_token)

                if response.status_code != 200:
                    error_msg = response.json().get('message', response.text) if 'application/json' in response.headers.get('Content-Type', '') else response.text
                    messages.error(request, f"API Error: {error_msg}")
                    return redirect("get_all_serviceorchestration")

                success_msg = response.json().get('message', "Service orchestration registered.")
                messages.success(request, success_msg)
                return redirect("get_all_serviceorchestration")

            except Exception as post_error:
                print("POST Error:", str(post_error))
                messages.error(request, f"Error during submission: {post_error}")
                return redirect("get_all_serviceorchestration")

        # === GET: Initial Page Load ===
        else:
            form = ServiceOrchestrationForm()
            return render(request, 'service_orchestration.html', {
                'form': form,
                'backend_data': backend_data,
                'backend_data1': backend_data1
            })

    except Exception as e:
        print("Top-level Exception:", str(e))
        return render(request, '500page.html', {'error': str(e)})

# mani code
# def service_orchestration(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "ServiceOrchestrationRegister"
#         endpoint1 = "getAllServiceProcess"
#         backend_url_list = call_get_method(BASE_URL, endpoint1, access_token)
#         if backend_url_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list.json()})
        
#         backend_data = backend_url_list.json()
#         endpoint2 = "getAllServiceOrchestration"
#         backend_url_list1 = call_get_method(BASE_URL, endpoint2, access_token)
#         if backend_url_list1.status_code != 200:
#             return render(request, '500page.html', {'error': backend_url_list1.json()})
        
#         backend_data1 = backend_url_list1.json()

#         if request.method == "POST":
#             # Extract form data
#             service_orchestration_name = request.POST.get("field_name")
#             backend_ids = request.POST.getlist("backend_id[]")
#             depend_api_required = "depend_api_required" in request.POST
#             depend_service_id = request.POST.getlist("depend_service_id[]")
#             depend_api_url = request.POST.get("depend_api_url", "")
#             url_type = request.POST.get("url_type", "")

#             depend_api_param_required = "depend_api_parameter_required" in request.POST
#             visibility = request.POST.get('visibility', 'public')
#             print(f"Final visibility: {visibility}")
#             # Extract dynamic parameters
#             depend_api_params = []
#             depend_param_count = int(request.POST.get("depend_param_count", 0))

#             for i in range(1, depend_param_count + 1):
#                 param_name = request.POST.get(f"name_{i}")
#                 data_type = request.POST.get(f"data_type_{i}")
#                 is_mandatory = request.POST.get(f"is_mandatory_{i}", "off") == "on"
#                 min_length = request.POST.get(f"min_length_{i}")
#                 max_length = request.POST.get(f"max_length_{i}")
#                 depend_param = request.POST.get(f"depend_param_{i}", "off") == "on"

#                 if param_name:
#                     depend_api_params.append({
#                         "param_name": param_name,
#                         "data_type": data_type,
#                         "is_mandatory": is_mandatory,
#                         "min_length": int(min_length) if min_length else None,
#                         "max_length": int(max_length) if max_length else None,
#                         "depend_param": depend_param,
#                     })

#             # Construct API payload
#             api_payload = {
#                 "serviceOrchestrationName": service_orchestration_name,
#                 "serviceProcessID": [int(sid) for sid in backend_ids if sid],
#                 "dependAPIRequired": depend_api_required,
#                 "dependingServiceProcessID": [int(did) for did in depend_service_id if did],
#                 "dependAPIURL": depend_api_url or None,
#                 "dependUrlType":url_type,
#                 "dependAPIParamRequired": depend_api_param_required,
#                 "dependAPIParam": depend_api_params,
#                 "visibility": visibility,  

#             }

#             # Debugging outputs
#             print("depend_api_params:", depend_api_params)
#             print("api_payload:", api_payload)

#             # API call with payload
#             try:
#                 response = call_post_with_method(BASE_URL, endpoint, json.dumps(api_payload), access_token)

#                 if response.status_code != 200:
#                     # Add error message from API response
#                     error_message = response.json().get('message', response.text) if response.headers.get('Content-Type') == 'application/json' else response.text
#                     messages.error(request, f"API Error: {error_message}")
#                     return redirect("get_all_serviceorchestration")

#                 # Add success message
#                 success_message = response.json().get('message', "Operation completed successfully.") if response.headers.get('Content-Type') == 'application/json' else "Operation completed successfully."
#                 messages.success(request, success_message)
#                 return redirect("get_all_serviceorchestration")

#             except requests.exceptions.RequestException as e:
#                 # Add request exception message
#                 messages.error(request, f"Request Error: {str(e)}")
#                 return redirect("get_all_serviceorchestration")
#         else:
#             form = ServiceOrchestrationForm()
#             return render(request, 'service_orchestration.html', {'form': form, 'backend_data': backend_data,'backend_data1':backend_data1})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

####################################################################################################
#                                  FRONTEND  
# GET 
from django.shortcuts import render
import requests
@custom_login_required
@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
def get_frontend(request):
    try:
        access_token = request.session['access_token']
        if request.method == 'POST':
            pk1 = request.POST.get("id")
            endpoint = "getFrontend/" + pk1
            endpoint_modify = "/updateFrontend/" + pk1
            endpoint_delete = "/deleteFrontend/" + pk1

            # Call the external service or API to get the frontend data
            get_frontend = call_get_method(BASE_URL, endpoint, access_token)
            if get_frontend.status_code != 200:
                return render(request, '500page.html', {'error': get_frontend.json()})

            frontend_data = get_frontend.json()
            print("uuuuuuuuuuu",frontend_data)
            
            # If the call is successful, return the data to the template
            return render(request, 'datamanipulation.html', {'get_frontend': frontend_data})
        
        return render(request, 'datamanipulation.html')  # Default when accessed via GET

    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

#########################################################################################################
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def deleted_frontendurl(request):
    try:
        access_token = request.session['access_token']
        endpoint = "listOfDeletedFrontend"
        frontend_deleted_list = call_get_method(BASE_URL, endpoint, access_token)

        if frontend_deleted_list.status_code != 200:
            return render(request, '500page.html', {'error': frontend_deleted_list.json()})

        frontend_deleted_data = frontend_deleted_list.json()
        reversed_data = frontend_deleted_data[::-1]  # Reverse the list
        return render(request, 'deletedfrontend.html', {'form': reversed_data})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

@custom_login_required
def deleted_backendurl(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine the data source (Public or Private)
        data_source = request.GET.get('source', 'public')
        endpoint = "listOfDeletedBackend" if data_source == "public" else "listOfDeletedPrivateBackend"

        backend_deleted_list = call_get_method(BASE_URL, endpoint, access_token)

        if backend_deleted_list.status_code != 200:
            return render(request, '500page.html', {'error': backend_deleted_list.json()})

        backend_deleted_data = backend_deleted_list.json()
        reversed_data = backend_deleted_data[::-1]  # Reverse the list to show latest first

        return render(request, 'deletedbackend.html', {'form': reversed_data, 'source': data_source})

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def deleted_backendurl(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "listOfDeletedBackend"
#         backend_deleted_list = call_get_method(BASE_URL, endpoint, access_token)
#         if backend_deleted_list.status_code != 200:
#             return render(request, '500page.html', {'error': backend_deleted_list.json()})

#         backend_deleted_data = backend_deleted_list.json()
#         reversed_data = backend_deleted_data[::-1]  # Reverse the list
#         return render(request, 'deletedbackend.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    

@custom_login_required
def pipe_activity(request):
    try:
        access_token = request.session['access_token']
        endpoint = "getPipeActivity"
        endpoint1="getPrivatePipeActivity"
        pipe_activity_list = call_get_method(BASE_URL, endpoint, access_token)
       

        if pipe_activity_list.status_code != 200:
            return render(request, '500page.html', {'error': pipe_activity_list.json()})
        pipeactivity_data = pipe_activity_list.json()
        reversed_data = pipeactivity_data[::-1]  # Reverse the list
        return render(request, 'pipeactivity.html', {'form': reversed_data})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})
    
@custom_login_required
def process_error(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine the data source (Public or Private)
        data_source = request.GET.get('source', 'public')
        endpoint = "processError" if data_source == "public" else "getPrivateProcessError"

        processtable_error = call_get_method(BASE_URL, endpoint, access_token)
        
        if processtable_error.status_code != 200:
            return render(request, '500page.html', {'error': processtable_error.json()})
        
        process_error_data = processtable_error.json()
        reversed_data = process_error_data[::-1]  # Reverse the list to show latest first

        return render(request, 'processtableerror.html', {'form': reversed_data, 'source': data_source})

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def process_error(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "processError"
#         processtable_error = call_get_method(BASE_URL, endpoint, access_token)
#         if processtable_error.status_code != 200:
#             return render(request, '500page.html', {'error': processtable_error.json()})
#         process_error_data = processtable_error.json()
#         reversed_data = process_error_data[::-1]  # Reverse the list
#         return render(request, 'processtableerror.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    

@custom_login_required
def inbound(request):
    try:
        access_token = request.session['access_token']
        endpoint="inbound"
        inbound_table=call_get_method(BASE_URL,endpoint,access_token)
        if inbound_table.status_code == 200:
            return render(request,'messageinbound.html' , {'form':inbound_table.json()})
        else:
            return render(request,'error.html', {'error':inbound_table.json()})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})
    
def login_view(request):
    try:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            endpoint = "Login"
            data = {
                'userName': username,
                'password': password
            }
            print("data==", data)
            json_data = json.dumps(data)
            response = call_post_method_for_without_token(BASE_URL, endpoint, json_data)
            print("response---",response)
            if response.status_code != 200:
                error_message = response
                print("error_message++++",error_message)
                messages.error(request, f"Login Failed Please provide correct Username and Password")
                return redirect('login')
            elif response.status_code == 500:
                c=response.text
                messages.error(request, f"Login Failed Please provide correct Username and Password")
                return render(request,"500page.html",{"error":c})
            elif response.status_code == 200:
                try:
                    response_json_success = response.json()
                    username_txt=response.text
                    print("============username_txt",username_txt)
                    print("============username_txt",username_txt)
                    request.session['username'] = username_txt
                    endd="generateToken"
                    print("============endd",endd)
                    session= request.session.get('username')
                    print("=========session",session)
                    endpoint1=username + endd
                    print("=========username",username)
                    print("=========end",endd)
                    print("=========endpoint",endpoint1)
                    user_token = call_get_method_without_token(BASE_URL, endpoint1)
                    print("000000000token",user_token)
                    print("000000000token",user_token.text)
                    request.session['access_token'] = user_token
                    print("0accessss000",user_token)
                    if user_token.status_code != 200:
                        return render(request,"500page.html",{"error":user_token.text})
                    else:
                        user_token_data = user_token.json()
                        print("frontend_data els",user_token_data)
                        request.session['username'] = username
                        endd="/generateToken"
                        print("============ elseend",endd)
                        session= request.session.get('username')
                        print("=========session else",session)
                        endpoint1=username + endd
                        print("=========username else",username)
                        print("=========end else",endd)
                        print("=========endpoint else",endpoint1)
                        user_token = call_get_method_without_token(BASE_URL, endpoint1)
                        print("000000000token else",user_token)
                        request.session['access_token'] = user_token
                        print("0accessss000",user_token)
                        if user_token.status_code != 200:
                            messages.error(request, 'error')
                        messages.success(request, 'user_token successs')

                except ValueError:
                    username_txt=response.text
                    print("============username_txt",username_txt)
                    request.session['username'] = username_txt
                    session = request.session.get('username')
                    endd= "/generateToken"
                    print("=========endd exce", endd)
                    print("=========session excep", session)
                    # Correctly construct the endpoint
                    endpoint1 = f"{session}{endd}"  # Concatenate BASE_URL with endd directly
                    print("=========end excep", endd)
                    print("=========endpoint excep", endpoint1)
                    # Call the function to get the token
                    user_token = call_get_method_without_token(BASE_URL,endpoint1,)
                    print("000000000token excep", user_token)
                    # Save token in session
                    if user_token.status_code == 200:
                        print("user_token", user_token.text)
                        # Assuming the response contains a JSON with 'token' and 'userRole'
                        token_data = user_token.json()  # Convert response text to JSON
                        request.session['access_token'] = token_data.get('token', '')  # Save token
                        request.session['user_role'] = token_data.get('userRole', '')  # Save userRole
                        print("0accessss000", request.session['access_token'])
                        print("0user_role000", request.session['user_role'])
                        request.session['username'] = username
                        session = request.session.get('user_role')
                        if session == "ADMIN":
                            return redirect('dashboard')
                        elif session == "USER":
                            return redirect('user_dashboard')
                        else:
                            return redirect('client_dashboard')
                    else:
                        return render(request,"500page.html",{"error":c})
                        
                messages.error(request, f"Successfully logged in. Welcome! {username}")
                    # Save the username in the session even in case of error
        return render(request, 'login.html')
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})

##############################################################################
@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
def get_all_services(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get the source parameter from the request (default to "public")
        data_source = request.GET.get('source', 'public').lower()
        print(f"Received source: {data_source}")  # Debugging

        # Choose the appropriate API endpoint
        if data_source == "public":
            endpoint = "getAllService"
        elif data_source == "private":
            endpoint = "getAllPrivateService"
        else:
            print("Invalid data source requested")
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")

        service_data_response = call_get_method(BASE_URL, endpoint, access_token)

        # **🔹 Step 1: Print the raw response**
        print(f"Raw Response Status: {service_data_response.status_code}")
        print(f"Raw Response Content: {service_data_response.text}")  # Debugging

        if service_data_response.status_code != 200:
            return render(request, '500page.html', {'error': f"API Error: {service_data_response.status_code}"})

        try:
            service_data = service_data_response.json()
        except Exception as e:
            print(f"JSON Parse Error: {e}")  # Debugging
            return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

        print(f"Fetched {len(service_data)} records from {endpoint}")

        return render(request, 'allservices.html', {'services': service_data, 'source': data_source})

    except Exception as error:
        print(f'Error in get_all_services view: {error}')
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def get_all_services(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getAllService"
#         service_data_response = call_get_method(BASE_URL, endpoint, access_token)
#         if service_data_response.status_code != 200:
#             return render(request, '500page.html', {'error': service_data_response.json()})
#         service_data = service_data_response.json()
#         return render(request, 'allservices.html', {'services': service_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
def get_all_processes(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get the source parameter from the request (default to "public")
        data_source = request.GET.get('source', 'public').lower()
        print(f"Received source: {data_source}")  # Debugging

        # Choose the appropriate API endpoint
        if data_source == "public":
            endpoint = "getAllProcess"
        elif data_source == "private":
            endpoint = "getAllPrivateProcess"
        else:
            print("Invalid data source requested")
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")

        process_data_response = call_get_method(BASE_URL, endpoint, access_token)

        # **🔹 Debugging: Print the raw response**
        print(f"Raw Response Status: {process_data_response.status_code}")
        print(f"Raw Response Content: {process_data_response.text}")

        if process_data_response.status_code != 200:
            return render(request, '500page.html', {'error': f"API Error: {process_data_response.status_code}"})

        try:
            process_data = process_data_response.json()
        except Exception as e:
            print(f"JSON Parse Error: {e}")  # Debugging
            return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

        print(f"Fetched {len(process_data)} records from {endpoint}")

        return render(request, 'getallprocessesection.html', {'processes': process_data, 'source': data_source})

    except Exception as error:
        print(f'Error in get_all_processes view: {error}')
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def get_all_processes(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getAllProcess"
#         process_data_response = call_get_method(BASE_URL, endpoint, access_token)
#         if process_data_response.status_code != 200:
#             return render(request, '500page.html', {'error': process_data_response.json()})
#         process_data = process_data_response.json()
#         return render(request, 'getallprocessesection.html', {'processes': process_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
# def get_all_serviceprocess(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getAllServiceProcess"
#         response = call_get_method(BASE_URL, endpoint, access_token)

#         if response.status_code != 200:
#             return render(request, '500page.html', {'error': response.json()})

#         service_process_data = response.json()

#         return render(request, 'getall_serviceprocess.html', {'service_processes': service_process_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
def get_all_serviceprocess(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get the source parameter from the request (default to "public")
        data_source = request.GET.get('source', 'public').lower()
        print(f"Received source: {data_source}")  # Debugging

        # Choose the appropriate API endpoint
        if data_source == "public":
            endpoint = "getAllServiceProcess"
        elif data_source == "private":
            endpoint = "getAllPrivateServiceProcess"
        else:
            print("Invalid data source requested")
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")

        response = call_get_method(BASE_URL, endpoint, access_token)

        # **🔹 Debugging: Print the raw response**
        print(f"Raw Response Status: {response.status_code}")
        print(f"Raw Response Content: {response.text}")

        if response.status_code != 200:
            return render(request, '500page.html', {'error': f"API Error: {response.status_code}"})

        try:
            service_process_data = response.json()
        except Exception as e:
            print(f"JSON Parse Error: {e}")  # Debugging
            return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

        print(f"Fetched {len(service_process_data)} records from {endpoint}")

        return render(request, 'getall_serviceprocess.html', {'service_processes': service_process_data, 'source': data_source})

    except Exception as error:
        print(f'Error in get_all_serviceprocess view: {error}')
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})


@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
def get_all_serviceorchestration(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Get the source parameter from the request (default to "public")
        data_source = request.GET.get('source', 'public').lower()
        print(f"Received source: {data_source}")  # Debugging

        # Choose the appropriate API endpoint
        if data_source == "public":
            endpoint = "getAllServiceOrchestration"
        elif data_source == "private":
            endpoint = "getAllPrivateServiceOrchestration"
        else:
            print("Invalid data source requested")
            return render(request, '500page.html', {'error': 'Invalid data source'})

        print(f"Calling API Endpoint: {endpoint}")

        response = call_get_method(BASE_URL, endpoint, access_token)

        # **🔹 Debugging: Print the raw response**
        print(f"Raw Response Status: {response.status_code}")
        print(f"Raw Response Content: {response.text}")

        if response.status_code != 200:
            return render(request, '500page.html', {'error': f"API Error: {response.status_code}"})

        try:
            service_orchestration_data = response.json()
        except Exception as e:
            print(f"JSON Parse Error: {e}")  # Debugging
            return render(request, '500page.html', {'error': 'Invalid JSON response from API'})

        print(f"Fetched {len(service_orchestration_data)} records from {endpoint}")

        return render(request, 'getall_serviceorchestration.html', {'service_orchestrations': service_orchestration_data, 'source': data_source})

    except Exception as error:
        print(f'Error in get_all_serviceorchestration view: {error}')
        return render(request, '500page.html', {'error': f'An error occurred: {error}'})

# def get_all_serviceorchestration(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getAllServiceOrchestration"
#         response = call_get_method(BASE_URL, endpoint, access_token)
#         if response.status_code != 200:
#             return render(request, '500page.html', {'error': response.json()})

#         service_orchestration_data = response.json()

#         return render(request, 'getall_serviceorchestration.html', {'service_orchestrations': service_orchestration_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    
#29-1
# @custom_login_required
# def callserviceflow(request):
#     # try:
#         access_token = request.session['access_token']
#         endpoint1 = "callServiceParam"
#         endpoint2 = "callService" 
#         form = CallServiceFlowForm(request.POST or None)
#         api_response = None
#         matches = []  

#         if request.method == "POST":
#             if 'get_parameter' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")
#                 client_token = request.session['access_token']
#                 data = {
#                     "serviceFlowID": service_flow_id,
#                     "serviceFlowName": service_flow_name
#                 }
                
#                 response1 = call_post_with_method(BASE_URL, endpoint1, json.dumps(data), access_token)
#                 if response1.status_code == 200:
#                     response_data = response1.json()
#                     matches = []
#                     # Split parameter names and datatypes and store as tuples
#                     for match in response_data:
#                         param_name, datatype = match.split(',')
#                         matches.append((param_name, datatype))  # Store as a tuple (name, datatype)
                
#                 return render(request, 'callserviceflow.html', {'form': form, 'api_response': api_response, "matches": matches})

#             elif 'submit' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")
#                 client_token = request.session['access_token']
                
#                 # Retrieve stored matches from hidden fields
#                 matches = request.POST.getlist("matches[]")
#                 datatypes = request.POST.getlist("datatypes[]")  # Get the datatypes as well
#                 fields = []
#                 for index, match in enumerate(matches):
#                     value = request.POST.get(f"para_{index+1}")
#                     datatype = datatypes[index]  # Get the corresponding datatype
#                     if match and value:
#                         fields.append({
#                             "paramName": match,
#                             "value": value,
#                             "dataType": datatype  # Send the datatype along with the value
#                         })

#                 data1 = {
#                     "serviceFlowName": service_flow_name,
#                     "serviceFlowID": service_flow_id,
#                     "fields": fields
#                 }
#                 print("========data1", data1)

#                 response2 = call_post_with_method(BASE_URL, endpoint2, json.dumps(data1), access_token)
#                 print("========response2", response2)
#                 if response2.status_code == 200:
#                     print("response2", response2.text)
#                     print("response2", response2.json())
#                     print("response2", response2.status_code)
#                     api_response = response2.json()
#                     print("api_response", api_response)
#                     messages.success(request, api_response)
#                     redirect("callserviceflow")
#                 else:
#                     api_response = {"error": f"API call failed with status {response2.status_code}"}

#         return render(request, 'callserviceflow.html', {'form': form, 'api_response': api_response, "matches": matches})

#     # except Exception as error:
#     #     print(f'Error: {error}')  
#     #     return render(request, '500page.html', {'error': str(error)})


import re
@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
def callserviceflow(request):
        try:
            access_token = request.session.get('access_token')  # Use .get() to avoid KeyError
            endpoint1 = "callServiceParam"
            endpoint2 = "callService"
            form = CallServiceFlowForm(request.POST or None)
            api_response = None
            matches = []  

            # Initialize variables
            service_flow_id = None
            service_flow_name = None
            access_type = None

            if request.method == "POST":
                if 'get_parameter' in request.POST:  
                    service_flow_id = request.POST.get("service_flow_id")
                    service_flow_name = request.POST.get("service_flow_name")
                    access_type = request.POST.get("access_type")

                    # Validate access type and flow name consistency
                    if service_flow_name.startswith('private') and access_type != 'Private':
                        messages.error(request, "Please select 'Private' access type for private flows.")
                    elif not service_flow_name.startswith('private') and access_type == 'Private':
                        messages.error(request, "Please select a private flow type for private access.")
                    elif not service_flow_id or not service_flow_name or not access_type:
                        messages.error(request, "Please select a valid Service Flow Name, ID, and Access Type.")
                    else:
                        data = {
                            "serviceFlowID": service_flow_id,
                            "serviceFlowName": service_flow_name,
                            "accessType": access_type
                        }
                        
                        print("daytaaaaaaaaaaaaa",data)
                        # Make API call to get parameters
                        response1 = call_post_with_method(BASE_URL, endpoint1, json.dumps(data), access_token)
                        print("resssssssssssssssssss",response1.text)
                        
                        if response1.status_code == 200:
                            try:
                                response_data = response1.json()
                                matches = []
                                for match in response_data:
                                    parts = match.split(',')
                                    if len(parts) == 2:  # Ensure proper unpacking
                                        param_name, datatype = parts
                                        matches.append((param_name.strip(), datatype.strip()))
                            except ValueError:
                                messages.error(request, "Error: Unexpected response format.")
                            except Exception as e:
                                messages.error(request, f"Error processing parameters: {str(e)}")
                        else:
                            error_msg = f"Failed to fetch parameters. Status: {response1.status_code}"
                            try:
                                error_detail = response1.json().get('error', 'No additional error details')
                                error_msg += f" - {error_detail}"
                            except:
                                pass
                            messages.error(request, error_msg)

                    return render(request, 'callserviceflow.html', {
                        'form': form,
                        'api_response': api_response,
                        "matches": matches,
                        "selected_service_flow_id": service_flow_id,
                        "selected_service_flow_name": service_flow_name,
                        "selected_access_type": access_type
                    })

                elif 'submit' in request.POST:  
                    service_flow_id = request.POST.get("service_flow_id")
                    service_flow_name = request.POST.get("service_flow_name")            
                    access_type = request.POST.get("access_type")   
                    matches = request.POST.getlist("matches[]")
                    datatypes = request.POST.getlist("datatypes[]")

                    # Validate before processing
                    if not service_flow_id or not service_flow_name or not access_type:
                        messages.error(request, "Missing required fields")
                        return redirect("callserviceflow")

                    # Build fields array from parameters
                    fields = []
                    for index, match in enumerate(matches):
                        value = request.POST.get(f"para_{index+1}")
                        datatype = datatypes[index]
                        if match and value:
                            fields.append({
                                "paramName": match,
                                "value": value,
                                "dataType": datatype
                            })

                    if not fields:
                        messages.error(request, "No valid parameters provided.")
                        return redirect("callserviceflow")

                    try:
                        data1 = {
                            "serviceFlowName": service_flow_name,
                            "serviceFlowID": service_flow_id,
                            "accessType": access_type,
                            "fields": fields
                        }
                        
                        # Make the service call
                        response2 = call_post_with_method(BASE_URL, endpoint2, json.dumps(data1), access_token)
                        print("resssssssspooooocallservice",response2.text)
                        if response2.status_code == 200:
                            response_text = response2.text
                            # Extract success message
                            match = re.search(r"(Calling Backend Service ID: \d+.*)", response_text, re.DOTALL)
                            if match:
                                result_message = match.group(1).strip()
                            else:
                                result_message = response_text[:500] + "..." if len(response_text) > 500 else response_text
                            
                            messages.success(request, result_message)
                        else:
                            error_msg = f"API call failed with status: {response2.status_code}"
                            try:
                                error_detail = response2.json().get('error', response2.text[:500])
                                error_msg += f" - {error_detail}"
                            except:
                                error_msg += f" - {response2.text[:500]}"
                            messages.error(request, error_msg)

                    except Exception as e:
                        messages.error(request, f"Error making service call: {str(e)}")

                    return redirect("callserviceflow")

            # GET request or initial load
            return render(request, 'callserviceflow.html', {
                'form': form,
                'api_response': api_response,
                "matches": matches,
                "selected_service_flow_id": service_flow_id,
                "selected_service_flow_name": service_flow_name,
                "selected_access_type": access_type
            })

        except Exception as error:
            print(f'Error: {error}')
            messages.error(request, f"An unexpected error occurred: {str(error)}")
            return render(request, '500page.html', {'error': str(error)})



# mani code 
# def callserviceflow(request):
#     try:
#         access_token = request.session.get('access_token')  # Use .get() to avoid KeyError
#         endpoint1 = "callServiceParam"
#         endpoint2 = "callService"
#         form = CallServiceFlowForm(request.POST or None)
#         api_response = None
#         matches = []  

#         service_flow_id = None  # Initialize variables
#         service_flow_name = None
#         access_type = None

#         if request.method == "POST":
#             if 'get_parameter' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")
#                 access_type = request.POST.get("access_type")  # Get access type

#                 if not service_flow_id or not service_flow_name or not access_type:
#                     messages.error(request, "Please select a valid Service Flow Name, ID, and Access Type.")
#                 else:
#                     data = {
#                         "serviceFlowID": service_flow_id,
#                         "serviceFlowName": service_flow_name,
#                         "accessType": access_type  # Pass access type
#                     }
#                     response1 = call_post_with_method(BASE_URL, endpoint1, json.dumps(data), access_token)
                    
#                     if response1.status_code == 200:
#                         try:
#                             response_data = response1.json()
#                             matches = []
#                             for match in response_data:
#                                 parts = match.split(',')
#                                 if len(parts) == 2:  # Ensure proper unpacking
#                                     param_name, datatype = parts
#                                     matches.append((param_name.strip(), datatype.strip()))
#                         except ValueError:
#                             messages.error(request, "Error: Unexpected response format.")
#                     else:
#                         messages.error(request, f"Failed to fetch parameters. Status: {response1.status_code}")
                
#                 return render(request, 'callserviceflow.html', {
#                     'form': form,
#                     'api_response': api_response,
#                     "matches": matches,
#                     "selected_service_flow_id": service_flow_id,
#                     "selected_service_flow_name": service_flow_name,
#                     "selected_access_type": access_type  # Pass selected access type
#                 })

#             elif 'submit' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")            
#                 access_type = request.POST.get("access_type")  # Get access type
#                 matches = request.POST.getlist("matches[]")
#                 datatypes = request.POST.getlist("datatypes[]")

#                 fields = []
#                 for index, match in enumerate(matches):
#                     value = request.POST.get(f"para_{index+1}")
#                     datatype = datatypes[index]
#                     if match and value:
#                         fields.append({
#                             "paramName": match,
#                             "value": value,
#                             "dataType": datatype
#                         })

#                 if not fields:
#                     messages.error(request, "No valid parameters provided.")
#                 else:
#                     data1 = {
#                         "serviceFlowName": service_flow_name,
#                         "serviceFlowID": service_flow_id,
#                         "accessType": access_type,  # Include access type
#                         "fields": fields
#                     }
#                     print("data1", data1)
#                     response2 = call_post_with_method(BASE_URL, endpoint2, json.dumps(data1), access_token)
#                     print("response2", response2)
#                     print("response2-", response2.text)
#                     print("response2", response2.status_code)
#                     if response2.status_code == 200:
#                         response_text = response2.text

#                         # Match "Calling Backend Service ID" and capture everything after it
#                         match = re.search(r"(Calling Backend Service ID: \d+.*)", response_text, re.DOTALL)
#                         if match:
#                             result_message = match.group(1).strip()  # Extract and clean up the matched text
#                         else:
#                             result_message = "No relevant response found."
#                         print("Extracted Response:", result_message)
#                         messages.success(request, result_message)
#                         return redirect("callserviceflow")
#                     else:
#                         messages.error(request, f"API call failed with status: {response2.status_code}, Response: {response2.text}")

#         return render(request, 'callserviceflow.html', {
#             'form': form,
#             'api_response': api_response,
#             "matches": matches,
#             "selected_service_flow_id": service_flow_id,
#             "selected_service_flow_name": service_flow_name,
#             "selected_access_type": access_type  # Pass selected access type
#         })
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})


# def callserviceflow(request):
#     try:
#         access_token = request.session.get('access_token')  # Use .get() to avoid KeyError
#         endpoint1 = "callServiceParam"
#         endpoint2 = "callService"
#         form = CallServiceFlowForm(request.POST or None)
#         api_response = None
#         matches = []  

#         service_flow_id = None  # Initialize variables
#         service_flow_name = None

#         if request.method == "POST":
#             if 'get_parameter' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")

#                 if not service_flow_id or not service_flow_name:
#                     messages.error(request, "Please select a valid Service Flow Name and ID.")
#                 else:
#                     data = {
#                         "serviceFlowID": service_flow_id,
#                         "serviceFlowName": service_flow_name
#                     }
#                     response1 = call_post_with_method(BASE_URL, endpoint1, json.dumps(data), access_token)
                    
#                     if response1.status_code == 200:
#                         try:
#                             response_data = response1.json()
#                             matches = []
#                             for match in response_data:
#                                 parts = match.split(',')
#                                 if len(parts) == 2:  # Ensure proper unpacking
#                                     param_name, datatype = parts
#                                     matches.append((param_name.strip(), datatype.strip()))
#                         except ValueError:
#                             messages.error(request, "Error: Unexpected response format.")
#                     else:
#                         messages.error(request, f"Failed to fetch parameters. Status: {response1.status_code}")
                
#                 return render(request, 'callserviceflow.html', {
#                     'form': form,
#                     'api_response': api_response,
#                     "matches": matches,
#                     "selected_service_flow_id": service_flow_id,
#                     "selected_service_flow_name": service_flow_name
#                 })

#             elif 'submit' in request.POST:  
#                 service_flow_id = request.POST.get("service_flow_id")
#                 service_flow_name = request.POST.get("service_flow_name")            
#                 matches = request.POST.getlist("matches[]")
#                 datatypes = request.POST.getlist("datatypes[]")

#                 fields = []
#                 for index, match in enumerate(matches):
#                     value = request.POST.get(f"para_{index+1}")
#                     datatype = datatypes[index]
#                     if match and value:
#                         fields.append({
#                             "paramName": match,
#                             "value": value,
#                             "dataType": datatype
#                         })

#                 if not fields:
#                     messages.error(request, "No valid parameters provided.")
#                 else:
#                     data1 = {
#                         "serviceFlowName": service_flow_name,
#                         "serviceFlowID": service_flow_id,
#                         "fields": fields
#                     }
#                     print("data1", data1)
#                     response2 = call_post_with_method(BASE_URL, endpoint2, json.dumps(data1), access_token)
#                     print("response2", response2)
#                     print("response2-", response2.text)
#                     print("response2", response2.status_code)
#                     if response2.status_code == 200:
#                         response_text = response2.text

#                         # Match "Calling Backend Service ID" and capture everything after it
#                         match = re.search(r"(Calling Backend Service ID: \d+.*)", response_text, re.DOTALL)
#                         if match:
#                             result_message = match.group(1).strip()  # Extract and clean up the matched text
#                         else:
#                             result_message = "No relevant response found."
#                         print("Extracted Response:", result_message)
#                         messages.success(request, result_message)
#                         return redirect("callserviceflow")
#                     else:
#                         messages.error(request, f"API call failed with status: {response2.status_code}, Response: {response2.text}")

#         return render(request, 'callserviceflow.html', {
#             'form': form,
#             'api_response': api_response,
#             "matches": matches,
#             "selected_service_flow_id": service_flow_id,
#             "selected_service_flow_name": service_flow_name
#         })
#     except Exception as error :
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})


@role_required(allowed_roles=['ADMIN','USER','CLIENT'])
@custom_login_required
@require_GET
# def get_service_data(request):
#     try:
#         # Check for access token
#         access_token = request.session.get('access_token')
#         if not access_token:
#             return JsonResponse({'error': 'Authentication required'}, status=401)

#         # Get the 'flow' parameter from the request
#         flow_type = request.GET.get('flow', '')
        
#         # Define all available endpoints (public and private)
#         flow_endpoints = {
#             # Public endpoints
#             'backend': "getAllBackend",
#             'serviceorchestration': "getAllServiceOrchestration",
#             'serviceprocess': "getAllServiceProcess",
#             'service': "getAllService",
#             'process': "getAllProcess",
            
#             # Private endpoints
#             'privatebackend': "getAllPrivateBackend",
#             'privateserviceorchestration': "getAllPrivateServiceOrchestration",
#             'privateserviceprocess': "getAllPrivateServiceProcess",
#             'privateservice': "getAllPrivateService",
#             'privateprocess': "getAllPrivateProcess"
#         }

#         # Validate flow type
#         if not flow_type or flow_type not in flow_endpoints:
#             return JsonResponse({
#                 'error': 'Invalid flow type',
#                 'available_flows': list(flow_endpoints.keys())
#             }, status=400)

#         # Make the API call
#         endpoint = flow_endpoints[flow_type]
#         response = call_get_method(BASE_URL, endpoint, access_token)
        
#         # Log response details for debugging
#         logger.debug(f"API Response - Status: {response.status_code}")
#         logger.debug(f"API Response - Headers: {response.headers}")
        
#         if response.status_code != 200:
#             error_detail = f"Endpoint: {endpoint} returned {response.status_code}"
#             try:
#                 error_detail += f" - {response.json().get('error', 'No error details')}"
#             except:
#                 error_detail += f" - {response.text[:200]}"
            
#             logger.error(f"API call failed: {error_detail}")
#             return JsonResponse({
#                 'error': 'Failed to fetch data',
#                 'detail': error_detail
#             }, status=500)

#         # Process successful response
#         try:
#             data = response.json()
#             logger.info(f"Successfully fetched data for flow: {flow_type}")
#             return JsonResponse(data, safe=False)
            
#         except ValueError as e:
#             logger.error(f"JSON parsing error: {str(e)} - Response: {response.text[:200]}")
#             return JsonResponse({
#                 'error': 'Invalid response format',
#                 'detail': str(e)
#             }, status=500)

#     except KeyError as e:
#         logger.error(f"Session key error: {str(e)}")
#         return JsonResponse({'error': 'Session error'}, status=401)
        
#     except Exception as error:
#         logger.exception(f"Unexpected error in get_service_data: {str(error)}")
#         return JsonResponse({
#             'error': 'Internal server error',
#             'detail': str(error)
#         }, status=500)

# single name for both private and public endpoint
def get_service_data(request):
    try:
        access_token = request.session['access_token']
        
        # Get parameters from the request
        flow_type = request.GET.get('flow', '')
        is_private = request.GET.get('private', 'false').lower() == 'true'

        # Define endpoint mapping for both public and private
        flow_endpoints = {
            'backend': {
                'public': "getAllBackend",
                'private': "getAllPrivateBackend"
            },
            'serviceorchestration': {
                'public': "getAllServiceOrchestration",
                'private': "getAllPrivateServiceOrchestration"
            },
            'serviceprocess': {
                'public': "getAllServiceProcess",
                'private': "getAllPrivateServiceProcess"
            },
            'service': {
                'public': "getAllService",
                'private': "getAllPrivateService"
            },
            'process': {
                'public': "getAllProcess",
                'private': "getAllPrivateProcess"
            }
        }

        # Validate flow type
        if flow_type not in flow_endpoints:
            return JsonResponse({'error': 'Invalid flow type'}, status=400)

        # Choose the correct endpoint based on `private` flag
        visibility = 'private' if is_private else 'public'
        endpoint = flow_endpoints[flow_type][visibility]

        # Call API
        response = call_get_method(BASE_URL, endpoint, access_token)

        print("Response status:", response.status_code)
        print("Response text:", response.text)

        if response.status_code != 200:
            return JsonResponse({'error': 'Failed to fetch data'}, status=500)

        data = response.json()
        print("Data received:", data)
        return JsonResponse(data, safe=False)

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': str(error)})

# MANI CODE  
# def get_service_data(request):
#     try:
#         access_token = request.session['access_token']
#         # Get the 'flow' parameter from the request
#         flow_type = request.GET.get('flow', '')
#         flow_endpoints = {
#             'backend': "getAllBackend",               # Backend URL
#             'serviceorchestration': "getAllServiceOrchestration",   # Service Orchestration
#             'serviceprocess': "getAllServiceProcess",         # Service Process
#             'service': "getAllService",               # Services
#             'process': "getAllProcess"                 # Processes
#         }
#         if flow_type not in flow_endpoints:
#             return JsonResponse({'error': 'Invalid flow type'}, status=400)
#         endpoint = flow_endpoints[flow_type]
#         response = call_get_method(BASE_URL, endpoint, access_token)
#         print("respppp",response)
#         print("respppptt",response.text)

#         if response.status_code != 200:
#             return JsonResponse({'error': 'Failed to fetch data'}, status=500)
#         data = response.json()
#         print("data----===",data)
#         return JsonResponse(data, safe=False)
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

# GET
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_messageinbound(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine which endpoint to use based on query parameter
        data_source = request.GET.get('source', 'public')
        endpoint = "messageInbound" if data_source == "public" else "getPrivateMessageInbound"

        messageinbound = call_get_method(BASE_URL, endpoint, access_token)
        
        if messageinbound.status_code != 200:
            return render(request, '500page.html', {'error': messageinbound.json()})
        
        messageinbound_data = messageinbound.json()
        reversed_data = messageinbound_data[::-1]  # Reverse the list for latest data first

        return render(request, 'messageinbound.html', {'form': reversed_data, 'source': data_source})
    
    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def get_messageinbound(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "messageInbound"
#         messageinbound = call_get_method(BASE_URL, endpoint, access_token)
#         if messageinbound.status_code != 200:
#             return render(request, '500page.html', {'error': messageinbound.json()})
#         messageinbound_data = messageinbound.json()
#         print("============",messageinbound_data)
#         reversed_data = messageinbound_data[::-1]  # Reverse the list
#         return render(request, 'messageinbound.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_messageOutbound(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine which endpoint to use based on query parameter
        data_source = request.GET.get('source', 'public')
        endpoint = "messageOutbound" if data_source == "public" else "getPrivateMessageOutbound"

        messageoutbound = call_get_method(BASE_URL, endpoint, access_token)
        
        if messageoutbound.status_code != 200:
            return render(request, '500page.html', {'error': messageoutbound.json()})
        
        messageoutbound_data = messageoutbound.json()
        reversed_data = messageoutbound_data[::-1]  # Reverse the list for latest data first

        return render(request, 'messageoutbound.html', {'form': reversed_data, 'source': data_source})
    
    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def get_messageOutbound(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "messageOutbound"
#         messageoutound = call_get_method(BASE_URL, endpoint, access_token)
#         if messageoutound.status_code != 200:
#             return render(request, '500page.html', {'error': messageoutound.json()})
#         messageoutound_data = messageoutound.json()
#         reversed_data = messageoutound_data[::-1]  # Reverse the list
#         return render(request, 'messageoutbound.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    
@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_messagemapping(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine which endpoint to use based on a query parameter
        data_source = request.GET.get('source', 'public')
        endpoint = "getMessageMappingList" if data_source == "public" else "getPrivateMessageMappingList"

        messagemapping = call_get_method(BASE_URL, endpoint, access_token)
        
        if messagemapping.status_code != 200:
            return render(request, '500page.html', {'error': messagemapping.json()})
        
        messagemapping_data = messagemapping.json()
        reversed_data = messagemapping_data[::-1]  # Reverse the list for latest data first

        return render(request, 'messagemapping.html', {'form': reversed_data, 'source': data_source})
    
    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})


# def get_messagemapping(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getMessageMappingList"
#         messagemapping = call_get_method(BASE_URL, endpoint, access_token)
#         if messagemapping.status_code != 200:
#             return render(request, '500page.html', {'error': messagemapping.json()})
#         messagemapping_data = messagemapping.json()
#         reversed_data = messagemapping_data[::-1]  # Reverse the list
#         return render(request, 'messagemapping.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER']) 
@custom_login_required
def get_monitorData(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine the data source (Public or Private)
        data_source = request.GET.get('source', 'public')
        endpoint = "MonitorData" if data_source == "public" else "getPrivateMonitorData"

        monitorData_list = call_get_method(BASE_URL, endpoint, access_token)
        
        if monitorData_list.status_code != 200:
            return render(request, '500page.html', {'error': monitorData_list.json()})
        
        monitorData_data = monitorData_list.json()
        reversed_data = monitorData_data[::-1]  # Reverse the list to show latest first

        return render(request, 'get_monitordata.html', {'form': reversed_data, 'source': data_source})

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def get_monitorData(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "MonitorData"
#         monitorData_list = call_get_method(BASE_URL, endpoint, access_token)
#         if monitorData_list.status_code != 200:
#             return render(request, '500page.html', {'error': monitorData_list.json()})

#         monitorData_data = monitorData_list.json()
#         reversed_data = monitorData_data[::-1]  # Reverse the list


#         return render(request, 'get_monitordata.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

from django.shortcuts import render
from django.http import JsonResponse
from .forms import CallServiceFlowForm  # Import your form here
import json

@role_required(allowed_roles=['ADMIN'])
@csrf_exempt
@custom_login_required
def deleteserviceflow(request):
    try:
        if request.method == "POST":
            access_token = request.session.get('access_token')
            username = request.session.get('username')

            # Retrieve form data
            service_flow_id = request.POST.get("service_flow_id")
            service_flow_name = request.POST.get("service_flow_name")
            access_type = request.POST.get("accessType")
            delete_type = request.POST.get("delete_type")  # Determines which delete endpoint to use

            # Check for missing inputs
            if not service_flow_id or not service_flow_name:
                messages.error(request, "Service Flow ID and Name are required.")
                return render(request, "deleteserviceflow.html", {
                    "form": CallServiceFlowForm()
                })

            # Select API endpoint based on button clicked
            if delete_type == "flow":
                endpoint = BASE_URL + "deleteServiceFlow"
            else:
                endpoint = BASE_URL + "deleteService"

            # Data to send in the API request
            data = {
                "serviceID": service_flow_id,
                "serviceName": service_flow_name,
                "accessType": access_type,
            }

            # Headers for the API request
            headers = {
                "Authorization": access_token,
                "Content-Type": "application/json"
            }

            try:
                # Make the API request
                response = requests.delete(endpoint, json=data, headers=headers)

                # Check the API response
                if response.status_code == 200:
                    messages.success(request, response.text)
                else:
                    error_msg = f"Failed to delete. Status: {response.status_code}"
                    try:
                        error_detail = response.json().get('message', response.text[:500])
                        error_msg += f" - {error_detail}"
                    except:
                        error_msg += f" - {response.text[:500]}"
                    messages.error(request, error_msg)

                return redirect("delete_serviceflow")

            except requests.exceptions.RequestException as e:
                messages.error(request, f"An error occurred: {str(e)}")
                return redirect("delete_serviceflow")

        return render(request, "deleteserviceflow.html", {
            "form": CallServiceFlowForm()
        })
    except Exception as error:
        print(f'Error: {error}')
        messages.error(request, f"An unexpected error occurred: {str(error)}")
        return render(request, '500page.html', {'error': str(error)})

# final code 
# def deleteserviceflow(request):
#     try:
#         if request.method == "POST":
#             access_token = request.session.get('access_token')
#             username = request.session.get('username')

#             # Retrieve form data
#             service_flow_id = request.POST.get("service_flow_id")
#             service_flow_name = request.POST.get("service_flow_name")
#             access_type = request.POST.get("accessType")  # New field
#             delete_type = request.POST.get("delete_type")  # Determines which delete endpoint to use

#             # Check for missing inputs
#             if not service_flow_id or not service_flow_name:
#                 return render(request, "deleteserviceflow.html", {
#                     "form": CallServiceFlowForm(),
#                     "error": "Service Flow ID and Name are required."
#                 })

#             # Select API endpoint based on button clicked
#             if delete_type == "flow":
#                 endpoint = BASE_URL + "getPrivateServiceFlowDetailList"
#             else:
#                 endpoint = BASE_URL + "deleteServiceFlow"

#             # Data to send in the API request
#             data = {
#                 "serviceID": service_flow_id,
#                 "serviceName": service_flow_name,
#                 "accessType": access_type,
#                 }

#             # Headers for the API request
#             headers = {
#                 "Authorization": access_token,
#                 "Content-Type": "application/json"
#             }

#             try:
#                 # Make the API request
#                 response = requests.delete(endpoint, json=data, headers=headers)

#                 # Check the API response
#                 if response.status_code == 200:
#                     messages.success(request, response.text)
#                     return redirect("delete_serviceflow")
#                 else:
#                     return render(request, "deleteserviceflow.html", {
#                         "form": CallServiceFlowForm(),
#                         "error": f"Failed to delete service flow. Error: {response.json().get('message', 'Unknown error')}"
#                     })

#             except requests.exceptions.RequestException as e:
#                 return render(request, "deleteserviceflow.html", {
#                     "form": CallServiceFlowForm(),
#                     "error": f"An error occurred: {str(e)}"
#                 })

#         return render(request, "deleteserviceflow.html", {
#             "form": CallServiceFlowForm()
#         })
#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})

# def deleteserviceflow(request):
#     try:
#         if request.method == "POST":
#             access_token = request.session.get('access_token')
#             username = request.session.get('username')

#             # Retrieve form data
#             service_flow_id = request.POST.get("service_flow_id")
#             service_flow_name = request.POST.get("service_flow_name")

#             # Check for missing inputs
#             if not service_flow_id or not service_flow_name:
#                 return render(request, "deleteserviceflow.html", {
#                     "form": CallServiceFlowForm(),
#                     "error": "Service Flow ID and Name are required."
#                 })

#             # API endpoint for deleting service flow
#             endpoint = BASE_URL+"deleteServiceFlow"  # Replace with actual endpoint
            
#             # Data to send in the API request
#             data = {
#                 "serviceID": service_flow_id,
#                 # "userName": username,
#                 "serviceName": service_flow_name,
#             }

#             # Headers for the API request
#             headers = {
#                 "Authorization":access_token,
#                 "Content-Type": "application/json"
#             }

#             try:
#                 # Make the API request
#                 response = requests.delete(endpoint, json=data, headers=headers)

#                 # Check the API response
#                 if response.status_code == 200:
#                     # Redirect or return success message
#                     messages.success(request,response.text)
#                     return redirect("delete_serviceflow")  # Replace with actual success URL
#                 else:
#                     # Handle API error
#                     return render(request, "deleteserviceflow.html", {
#                         "form": CallServiceFlowForm(),
#                         "error": f"Failed to delete service flow. Error: {response.json().get('message', 'Unknown error')}"
#                     })

#             except requests.exceptions.RequestException as e:
#                 # Handle network or connection error
#                 return render(request, "deleteserviceflow.html", {
#                     "form": CallServiceFlowForm(),
#                     "error": f"An error occurred: {str(e)}"
#                 })

#         # Render form for GET requests
#         return render(request, "deleteserviceflow.html", {
#             "form": CallServiceFlowForm()
#         })
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

@role_required(allowed_roles=['ADMIN','USER'])
@custom_login_required
def get_validationResult(request):
    try:
        access_token = request.session.get('access_token')
        if not access_token:
            return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

        # Determine the data source (Public or Private)
        data_source = request.GET.get('source', 'public')
        endpoint = "getParameterValidationList" if data_source == "public" else "getPrivateValidationResult"

        validationResult_list = call_get_method(BASE_URL, endpoint, access_token)
        
        if validationResult_list.status_code != 200:
            return render(request, '500page.html', {'error': validationResult_list.json()})
        
        validationResult_data = validationResult_list.json()
        reversed_data = validationResult_data[::-1]  # Reverse the list to show latest first

        return render(request, 'get_validationResult.html', {'form': reversed_data, 'source': data_source})

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': 'An error occurred while fetching data.'})

# def get_validationResult(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getParameterValidationList"
#         validationResult_list = call_get_method(BASE_URL, endpoint, access_token)
#         if validationResult_list.status_code != 200:
#             return render(request, '500page.html', {'error': validationResult_list.json()})
#         validationResult_data = validationResult_list.json()
#         reversed_data = validationResult_data[::-1]  # Reverse the list
#         return render(request, 'get_validationResult.html', {'form': reversed_data})
#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})
    
# @custom_login_required
# def get_getServiceFlowDetailList(request):
#     try:
#         access_token = request.session['access_token']
#         endpoint = "getServiceFlowDetailList"
#         getServiceFlowDetail_list = call_get_method(BASE_URL, endpoint, access_token)
#         if getServiceFlowDetail_list.status_code != 200:
#             return render(request, '500page.html', {'error': getServiceFlowDetail_list.json()})
#         getServiceFlowDetail_data = getServiceFlowDetail_list.json()

#         return render(request, 'get_getServiceFlowDetail.html', {'form': getServiceFlowDetail_data})

#     except Exception as error:
#         print(f'Error: {error}')  
#         return render(request, '500page.html', {'error': str(error)})

def clientregister(request):
    try:
        if request.method == 'POST':
            form = RegisterFrontendForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                user_name = form.cleaned_data['user_name']
                password = request.POST.get('password')
                user = form.cleaned_data['user']
                role = form.cleaned_data['role']
                emp_code = form.cleaned_data['emp_code']
                email = form.cleaned_data['email_id']
                companyCode=form.cleaned_data['companyCode']



                data = {
                    'name':name,
                    'userName': user_name,
                    'password':password,
                    "user": user,
                    "role": role.upper() if role.upper() else "CLIENT",
                    'empCode': emp_code,
                    "email": email,
                    "companyCode":companyCode
                }
                print("data0",data)
                endpoint = "Frontend"
                json_data = json.dumps(data)
                frontend_url_list = call_post_with_method(BASE_URL, endpoint, json_data, access_token=None)
                if frontend_url_list.status_code != 200:
                    messages.error(request, 'An error occurred while processing your request.')
                    return render(request, 'clientregister.html', {'form': form})
                frontend_data = None 
                try:
                    frontend_data = frontend_url_list.json()
                    messages.success(request, 'Frontend registration was successful!')
                    print("frontend_data",frontend_data)
                    return redirect("login")
                except requests.exceptions.JSONDecodeError:
                    messages.success(request, frontend_url_list.text)  # Plain success message
                    print("frontend_data",frontend_data)

                return redirect("login") 
            else:
                print("vvvvvvvvvvvvvvvvv",form.errors)
        form = RegisterFrontendForm()
        return render(request, 'clientregister.html', {'form': form})
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})



# def serviceflowdetails(request):
#     try:
#         if request.method == "POST":
#             # Fetch table name and tableId from the POST data
#             tablename = request.POST.get("tablename")
#             tableId = request.POST.get("tableId")
#             access_token = request.session.get('access_token')

#             if not access_token:
#                 return render(request, '500page.html', {'error': 'Access token is missing.'})
#             # Prepare the body data
#             body_data = {
#                 'tableName': tablename,
#                 'tableId': tableId}
#             # Adding access_token to the headers for Authorization
#             headers = {
#                 'Authorization': access_token,
#                 'X-Requested-With': 'XMLHttpRequest',  # Optional, ensures it's an AJAX request
# }
#             # Prepare the API endpoint (use POST to send body data)
#             endpoint = "getServiceFlowDetailList"
#             serviceflowdetails = call_get_method(BASE_URL, endpoint, access_token=access_token)
#             if serviceflowdetails.status_code != 200:
#                 return render(request, '500page.html', {'error': serviceflowdetails.json()})
#             data = serviceflowdetails.json()
#             return render(request, 'serviceflowdetails.html',)
#         else:
#             return render(request, 'serviceflowdetails.html')
#     except Exception as error:
#         print(f'Error: {error}')
#         return render(request, '500page.html', {'error': str(error)})

   

# def serviceflowdetails(request):
#     # try:
#         if request.method == "POST":
#             # Fetch table name and tableId from the POST data
#             table_name = request.POST.get("tablename")
#             print("table_name",table_name)
#             table_id = request.POST.get("pipeId")
#             print("table_id",table_id)
#             access_token = request.session.get("access_token")
#             # Ensure both table_name and table_id are provided
#             if not table_name or not table_id:
#                 return render(request, "500page.html", {"error": "Both tableName and tableId are required."})
#             if not access_token:
#                 return render(request, "500page.html", {"error": "Access token is missing."})
#             # Prepare the body data for the GET request
#             params = {
#                 "tableName": table_name,
#                 "tableId": table_id
#             }
#             # Adding access_token to the headers for Authorization
#             headers = {
#                 "Authorization": access_token,
#                 "X-Requested-With": "XMLHttpRequest"  # Optional, ensures it's an AJAX request
#             }
#             # Prepare the API endpoint
#             endpoint = f"{BASE_URL}getServiceFlowDetailList"
#             # Call the API
#             response = requests.get(endpoint, headers=headers, params=params)
#             # Check if the response is successful
#             if response.status_code == 200:
#                 data = response.text
#                 print("dataaaaaaaaaaaaa",data)
#                 print("dtextttttttttttt",response.text)
#                 return render(request, "serviceflowdetails.html", {"data": data})
#             else:
#                 error_message = response.text
#                 print("error_message",error_message)
#                 return render(request, "500page.html", {"error": error_message})
#         # For GET requests, render the empty form
#         return render(request, "serviceflowdetails.html")
#     # except Exception as error:
#     #     print(f"Error: {error}")
#     #     return render(request, "500page.html", {"error": str(error)})



import requests

# def serviceflowdetails(request):
#     # try:
#         if request.method == "POST":
#             # Fetch table name and tableId from the POST data
#             table_name = request.POST.get("tablename")
#             table_id = request.POST.get("tableId")
#             access_token = request.session.get("access_token")

#             # Ensure both table_name and table_id are provided
#             if not table_name or not table_id:
#                 return render(request, "500page.html", {"error": "Both tableName and tableId are required."})

#             if not access_token:
#                 return render(request, "500page.html", {"error": "Access token is missing."})

#             # Prepare the body data
#             body = {
#                 "tableName": table_name,
#                 "tableId": table_id
#             }

#             # Adding access_token to the headers for Authorization
#             headers = {
#                 "Authorization": access_token,
#                 "X-Requested-With": "XMLHttpRequest"
#             }

#             # Prepare the API endpoint
#             endpoint = f"{BASE_URL}/getServiceFlowDetailList"

#             # Call the API with body in GET request (if supported)
#             session = requests.Session()
#             response = session.request("GET", endpoint, headers=headers, json=body)

#             # Check if the response is successful
#             if response.status_code == 200:
#                 data = response.json()
#                 print("data", data)
#                 print("response", response.text)
#                 print("STATUS", response.status_code)
#                 return render(request, "serviceflowdetails.html", {"data": data})
#             else:
#                 error_message = response.json().get("message", "An error occurred while fetching data.")
#                 print("response", response.text)
#                 print("STATUS", response.status_code)
#                 return render(request, "500page.html", {"error": error_message})

#         # For GET requests, render the empty form
#         return render(request, "serviceflowdetails.html")

#     # except Exception as error:
#     #     print(f"Error: {error}")
#     #     return render(request, "500page.html", {"error": str(error)})


@role_required(allowed_roles=['ADMIN','USER'])
def serviceflowdetails(request):
    try:
        if request.method == "POST":
            # Get data from the form
            table_name = request.POST.get("tablename")
            table_id = request.POST.get("pipeId")
            access_token = request.session.get("access_token")
            print("Table Name:", table_name)
            print("Table ID:", table_id)
            print("Access Token:", access_token)
            
            # Debugging: Print received data
            print("Table Name:", table_name)
            print("Table ID:", table_id)
            
            # Prepare API request
            url=f'{BASE_URL}getServiceFlowDetailList'
            headers = {"Authorization": access_token}
            body = {
                "tableName": table_name,
                "tableId": table_id
            }
            try:
                # Make the API request
                response = requests.get(url, headers=headers, json=body)
                response_data = response.json()
                
                # Check API response status
                if response.status_code == 200:
                    print("Response Data:", response_data)
                    print("Response Data:1", response.text)

                    return render(request, "serviceflowdetails.html", {"response_data": response_data})
                else:
                    # Handle API errors
                    error_message = response_data.get("message", "Failed to fetch data")
                    return render(request, "serviceflowdetails.html", {"error": error_message})
            except Exception as e:
                # Handle exceptions
                print("Error:", e)
                return render(request, "serviceflowdetails.html", {"error": "An error occurred while fetching data."})
        
        # For GET requests, render the empty form
        return render(request, "serviceflowdetails.html")
    except Exception as error:
        print(f'Error: {error}')  
        return render(request, '500page.html', {'error': str(error)})



############### 3/11/25 ############################## New code ############################################



# import requests
# from django.shortcuts import render, redirect

# from django.contrib.auth.decorators import login_required
# from .forms import APIAccessRequestForm  # Make sure to create this form


# def private_api_request(request):
#     """Handles API Access Request Submission"""
#     form = APIAccessRequestForm()

#     if request.method == "POST":
#         form = APIAccessRequestForm(request.POST)
#         if form.is_valid():
#             data = {
#                 "AccessName": form.cleaned_data["access_name"],
#                 "ApiName": form.cleaned_data["api_name"],
#                 "AccessType": form.cleaned_data["access_type"],
#             }
#             response = requests.post(f"{BASE_URL}/userAccessRequest", json=data)

#             if response.status_code == 200:
#                 return redirect("private_api_approval")  # Redirect to approval page

#     return render(request, "private_api_request.html", {"form": form})



import requests
from django.shortcuts import render, redirect
from .forms import APIAccessRequestForm


def private_api_request(request):
    form = APIAccessRequestForm()

    if request.method == "POST":
        form = APIAccessRequestForm(request.POST)
        if form.is_valid():
            data = {
                "AccessName": form.cleaned_data["access_name"],
                "ApiName": form.cleaned_data["api_name"],
                "AccessType": form.cleaned_data["access_type"],
            }

            try:
                response = requests.post(f"{BASE_URL}/userAccessRequest", json=data)
                if response.status_code == 200:
                    return redirect("private_api_approval")
                else:
                    form.add_error(None, f"Request failed. Status code: {response.status_code}")
            except requests.exceptions.RequestException as e:
                form.add_error(None, f"API request error: {str(e)}")

    return render(request, "private_api_request.html", {"form": form})

# /////////////////////////////private response /////////////////

import json
import requests
from django.http import JsonResponse
from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.decorators import login_required


def private_api_approval(request):
    """Handles both displaying API requests and processing approvals/rejections"""
    token = request.session.get('access_token', '')
    headers = {"Authorization":token, "Content-Type": "application/json"}

    # If POST request → Process Approve/Reject action
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            request_id = data.get("request_id")
            action = data.get("action")

            if not request_id or action not in ["approved", "rejected"]:
                return JsonResponse({"success": False, "message": "Invalid request data."}, status=400)

            approval_url = f"{BASE_URL}/requestApproval/{token}"
            payload = {"requestId": request_id, "action": action}
            response = requests.post(approval_url, json=payload, headers=headers)

            if response.status_code == 200:
                return JsonResponse({"success": True, "message": f"Request {action} successfully!"})
            return JsonResponse({"success": False, "message": "Failed to process request."}, status=500)

        except json.JSONDecodeError:
            return JsonResponse({"success": False, "message": "Invalid JSON data."}, status=400)

    # If GET request → Fetch API requests for approval
    all_requests_url = f"{BASE_URL}/getAllRequest/{token}"
    my_requests_url = f"{BASE_URL}/getAllMyRequest/{token}"

    try:
        all_requests_response = requests.get(all_requests_url, headers=headers)
        my_requests_response = requests.get(my_requests_url, headers=headers)

        all_requests = all_requests_response.json() if all_requests_response.status_code == 200 else []
        my_requests = my_requests_response.json() if my_requests_response.status_code == 200 else []
    
    except requests.exceptions.RequestException:
        all_requests, my_requests = [], []  # Handle any API request failures gracefully

    return render(request, "private_api_approval.html", {
        "all_requests": all_requests,
        "my_requests": my_requests
    })

# /////////////////////////////////////////user appproval ///////////////////////

@role_required(allowed_roles=['ADMIN'])
@custom_login_required


def admin_approval(request):
    access_token = request.session.get('access_token')
    
    if not access_token:
        return redirect('login')

    headers = {
        "Authorization": access_token,
        "Content-Type": "application/json"
    }

    company_approval_api = f"{BASE_URL}getAllCompanyRegister"
    client_approval_api = f"{BASE_URL}getAllClientRegister"
    approval_api = f"{BASE_URL}statusConfirmation"

    if request.method == "POST":
        email = request.POST.get("email")
        status = request.POST.get("status")

        if not email or not status:
            return JsonResponse({"success": False, "error": "Email and status are required."})

        api_url = f"{approval_api}?email={email}&status={status}"

        try:
            response = requests.post(api_url, headers=headers)
            if response.status_code == 200:
                return JsonResponse({"success": True})
            else:
                return JsonResponse({"success": False, "error": response.text})
        except requests.exceptions.RequestException as e:
            return JsonResponse({"success": False, "error": str(e)})

    # GET request (load data)
    companies = []
    clients = []

    try:
        company_response = requests.get(company_approval_api, headers=headers)
        client_response = requests.get(client_approval_api, headers=headers)

        if company_response.status_code == 200:
            companies = [c for c in company_response.json() if c.get('status', '').upper() in ['PENDING', 'REJECTED']]

        if client_response.status_code == 200:
            clients = [c for c in client_response.json() if c.get('status', '').upper() in ['PENDING', 'REJECTED']]

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Error fetching approvals: {str(e)}")

    return render(request, "approval_page.html", {
        "clients": clients,
        "companies": companies,
    })# def admin_approval(request):


#     access_token = request.session.get('access_token')
    
#     if not access_token:
#         return redirect('login')  # Redirect to login if session expired

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     company_approval_api = f"{BASE_URL}getAllCompanyRegister"
#     client_approval_api = f"{BASE_URL}getAllClientRegister"
#     approval_api = f"{BASE_URL}statusConfirmation"

#     if request.method == "POST":
#         email = request.POST.get("email")
#         status = request.POST.get("status")

#         if not email or not status:
#             return JsonResponse({"success": False, "error": "Email and status are required."})

#         api_url = f"{approval_api}?email={email}&status={status}"

#         try:
#             response = requests.post(api_url, headers=headers)
#             if response.status_code == 200:
#                 return JsonResponse({"success": True})
#             else:
#                 return JsonResponse({"success": False, "error": response.text})
#         except requests.exceptions.RequestException as e:
#             return JsonResponse({"success": False, "error": str(e)})

#     # GET request (load page with data)
#     companies = []
#     clients = []

#     try:
#         company_response = requests.get(company_approval_api, headers=headers)
#         client_response = requests.get(client_approval_api, headers=headers)

#         if company_response.status_code == 200:
#             companies = [c for c in company_response.json() if c.get('status', '').upper() == 'PENDING']

#         if client_response.status_code == 200:
#             clients = [c for c in client_response.json() if c.get('status', '').upper() == 'PENDING']

#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error fetching approvals: {str(e)}")

#     return render(request, "approval_page.html", {
#         "clients": clients,
#         "companies": companies,
#     })


# def admin_approval(request):
#     access_token = request.session.get('access_token')
    
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     # API Endpoints
#     company_approval_api = f"{BASE_URL}getAllCompanyRegister"
#     client_approval_api = f"{BASE_URL}getAllClientRegister"
#     approval_api = f"{BASE_URL}statusConfirmation"

#     # Initialize empty lists
#     companies, clients = [], []
    
#     try:
#         # Fetch fresh data
#         company_response = requests.get(company_approval_api, headers=headers)
#         client_response = requests.get(client_approval_api, headers=headers)

#         if company_response.status_code == 200:
#             companies = [c for c in company_response.json() if c.get('status', '').upper() == 'PENDING']
        
#         if client_response.status_code == 200:
#             clients = [c for c in client_response.json() if c.get('status', '').upper() == 'PENDING']

#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error fetching approvals: {str(e)}")

#     if request.method == "POST":
#         email = request.POST.get("email")
#         status = request.POST.get("status")  # Only 'APPROVED' is needed now

#         if not email or not status:
#             messages.error(request, "Email and status are required.")
#         else:
#             api_url = f"{approval_api}?email={email}&status={status}"

#             try:
#                 response = requests.post(api_url, headers=headers)
#                 if response.status_code == 200:
#                     return redirect("frontendurl")  # Immediately redirect for approved users
#                 else:
#                     messages.error(request, f"Failed to update status: {response.text}")
#                     return redirect("admin_approval")

#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"API Error: {str(e)}")
#                 return redirect("admin_approval")

#     return render(request, "approval_page.html", {
#         "clients": clients,
#         "companies": companies
#     })
# def admin_approval(request):
#     access_token = request.session.get('access_token')
    
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     # Required API Endpoints
#     company_approval_api = f"{BASE_URL}getAllCompanyRegister"
#     client_approval_api = f"{BASE_URL}getAllClientRegister"
#     approval_api = f"{BASE_URL}statusConfirmation"

#     # Fetch Companies & Clients for Approval
#     companies, clients = [], []
    
#     try:
#         company_response = requests.get(company_approval_api, headers=headers)
#         client_response = requests.get(client_approval_api, headers=headers)

#         if company_response.status_code == 200:
#             companies = company_response.json()
#             print(companies)
#         if client_response.status_code == 200:
#             clients = client_response.json()

#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error fetching approvals: {str(e)}")

#     if request.method == "POST":
#         email = request.POST.get("email")
#         status = request.POST.get("status")  # 'APPROVED' or 'REJECTED'

#         if not email or not status:
#             messages.error(request, "Email and status are required.")
#         else:
#             api_url = f"{approval_api}?email={email}&status={status}"

#             try:
#                 response = requests.post(api_url, headers=headers)
#                 if response.status_code == 200:
#                     if status == "APPROVED":
#                         return redirect("frontendurl")  # Redirect approved users
#                     else:
#                         messages.error(request, "User approval rejected.")
#                 else:
#                     messages.error(request, f"Failed to update status: {response.text}")

#             except requests.exceptions.RequestException as e:
#                 messages.error(request, f"API Error: {str(e)}")

#     return render(request, "approval_page.html", {"clients": clients, "companies": companies})
# def admin_approval(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     company_approval_api = f"{BASE_URL}getAllCompanyRegister"
#     client_approval_api = f"{BASE_URL}getAllClientRegister"
#     status_confirmation_api = f"{BASE_URL}statusConfirmation"

#     headers = {
#     "Authorization": access_token,
#     "Content-Type": "application/json",
#     "Accept": "application/json"
# }


#     try:
#         company_response = requests.get(company_approval_api, headers=headers)
#         client_response = requests.get(client_approval_api, headers=headers)

#         companies = company_response.json() if company_response.status_code == 200 else []
#         clients = client_response.json() if client_response.status_code == 200 else []

#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Error fetching approvals: {str(e)}")
#         companies, clients = [], []

#     if request.method == "POST":
#         user_id = request.POST.get("user_id")
#         action = request.POST.get("action")

#         payload = {"user_id": user_id, "action": action}

#         try:
#             response = requests.post(status_confirmation_api, json=payload, headers=headers)
#             print("API Response Status Code:", response.status_code)
#             print("API Response Text:", response.text)  # Print the API response for debugging

#             if response.status_code == 200:
#                 if action == "approve":
#                     messages.success(request, "User approved successfully.")
#                     return redirect("frontendurl")
#                 elif action == "reject":
#                     messages.success(request, "User rejected successfully.")
#                     return redirect("approval_page")
#             else:
#                 messages.error(request, f"Failed to update status. API Response: {response.text}")
#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"API Error: {str(e)}")

#     return render(request, "approval_page.html", {"clients": clients, "companies": companies})




# import requests
# from django.shortcuts import render, redirect


# TOKEN_API = f"{BASE_URL}/token"

# def get_auth_token(request):
#     """Fetches the auth token and stores it in session."""
#     token = request.session.get("auth_token")  # Check if token is already in session

#     if not token:  # If no token, fetch a new one
#         try:
#             response = requests.get(TOKEN_API)  # Fetch token from API
#             if response.status_code == 200:
#                 token = response.json().get("token")  # Extract token from response
#                 request.session["auth_token"] = token  # Store in session
#         except requests.exceptions.RequestException:
#             return None  # Return None if token retrieval fails

#     return token  # Return token from session

# def admin_approval(request):
#     """Single view for both company and client approvals."""
#     token = get_auth_token(request)  # Fetch token from session or API

#     if not token:
#         return render(request, "approval_page.html", {"error": "Failed to authenticate."})

#     approval_type = request.GET.get("type", "all")  # Get type from query params (default: all)

#     # Define API endpoints
#     company_approval_api = f"{BASE_URL}/getAllCompanyRegister/{token}"
#     client_approval_api = f"{BASE_URL}/getAllClientRegister/{token}"

#     clients, companies = [], []

#     try:
#         # Fetch company approvals if type is 'company' or 'all'
#         if approval_type in ["company", "all"]:
#             company_response = requests.get(company_approval_api)
#             if company_response.status_code == 200:
#                 companies = company_response.json().get("companies", [])

#         # Fetch client approvals if type is 'client' or 'all'
#         if approval_type in ["client", "all"]:
#             client_response = requests.get(client_approval_api)
#             if client_response.status_code == 200:
#                 clients = client_response.json().get("clients", [])

#     except requests.exceptions.RequestException:
#         return render(request, "approval_page.html", {"error": "Failed to fetch data."})
#     return render(request, "approval_page.html", {"clients": clients, "companies": companies})





# import requests
# from django.shortcuts import render

# # Base API URL

# TOKEN_API = f"{BASE_URL}/token"
# STATUS_CONFIRMATION_API = f"{BASE_URL}/statusConfirmation/token"

# # Function to fetch the authentication token
# def get_auth_token():
#     try:
#         response = requests.get(TOKEN_API)  # Fetch token
#         if response.status_code == 200:
#             return response.json().get("token")  # Extract token from response
#     except requests.exceptions.RequestException:
#         return None  # Handle token retrieval failure
#     return None

# def admin_approval(request):
#     token = get_auth_token()  # Fetch new token dynamically

#     if not token:
#         return render(request, "approval_page.html", {"error": "Failed to authenticate."})

#     headers = {"Authorization": f"Bearer {token}"}
#     clients, companies = [], []

#     try:
#         response = requests.get(STATUS_CONFIRMATION_API, headers=headers)  # Fetch data
#         if response.status_code == 200:
#             data = response.json()
#             clients = data.get("clients", [])  # Extract clients
#             companies = data.get("companies", [])  # Extract companies
#     except requests.exceptions.RequestException:
#         return render(request, "approval_page.html", {"error": "Failed to fetch data."})

#     return render(request, "approval_page.html", {"clients": clients, "companies": companies})


# ////////////////////////upload files //////////////////////////////


# import pandas as pd
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages

# import pandas as pd
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages



# import pandas as pd
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import logging

# logger = logging.getLogger(__name__)



# import pandas as pd
# import requests
# import logging
# from django.shortcuts import render, redirect
# from django.contrib import messages

# logger = logging.getLogger(__name__)


import pandas as pd
import requests
import logging
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages

logger = logging.getLogger(__name__)


# def upload_csv(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     if request.method == "GET":
#         # Clear session data on page load
#         request.session.pop("company_data", None)
#         request.session.pop("employee_data", None)

#     # Fetch backend company codes
#     try:
#         res = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         backend_codes = {c.get("companyCode") for c in res.json()} if res.status_code == 200 else set()
#     except Exception as e:
#         messages.error(request, f"Error fetching company list: {e}")
#         logger.error("Company list fetch error: %s", e)
#         backend_codes = set()

#     # Uploaded data
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     uploaded_codes = {c.get("companyCode") for c in company_data}
#     valid_company_codes = backend_codes.union(uploaded_codes)

#     if request.method == "POST":
#         # Handle company upload
#         if "upload_company" in request.POST:
#             file = request.FILES.get("company_file")
#             if file:
#                 try:
#                     df = pd.read_csv(file)
#                     df.rename(columns={
#                         "CompanyName": "companyName",
#                         "companyName": "companyName",
#                         "CompanyCode": "companyCode",
#                         "companyCode": "companyCode"
#                     }, inplace=True)
#                     df = df[["companyName", "companyCode"]].drop_duplicates()
#                     company_data = df.to_dict(orient="records")
#                     request.session["company_data"] = company_data
#                     messages.success(request, "Company CSV uploaded successfully!")
#                     logger.info("Uploaded Company Data: %s", company_data)
#                 except Exception as e:
#                     logger.error("Company CSV error: %s", e)
#                     messages.error(request, f"Failed to read Company CSV: {e}")

#         # Handle employee upload
#         elif "upload_employee" in request.POST:
#             file = request.FILES.get("employee_file")
#             if file:
#                 try:
#                     df = pd.read_csv(file)
#                     df.rename(columns={
#                         "Name": "Name",
#                         "Email": "Email",
#                         "Usertype": "Usertype",
#                         "CompanyCode": "companyCode",
#                         "companyCode": "companyCode",
#                         "EmpCode": "EmpCode"
#                     }, inplace=True)
#                     df = df[["Name", "Email", "Usertype", "companyCode", "EmpCode"]].drop_duplicates()
#                     records = df.to_dict(orient="records")

#                     invalid = [emp for emp in records if emp["companyCode"] not in valid_company_codes]
#                     if invalid:
#                         messages.error(request, "Some employees have invalid company codes.")
#                         logger.warning("Invalid employee codes: %s", invalid)
#                     else:
#                         employee_data = records
#                         request.session["employee_data"] = employee_data
#                         messages.success(request, "Employee CSV uploaded successfully!")
#                         logger.info("Uploaded Employee Data: %s", employee_data)
#                 except Exception as e:
#                     logger.error("Employee CSV error: %s", e)
#                     messages.error(request, f"Failed to read Employee CSV: {e}")

#         # Save company
#         elif "save_company" in request.POST:
#             payload = {
#                 "companies": company_data,
#                 "metadata": {"source": "web-upload", "user": request.user.username if request.user.is_authenticated else "anonymous"}
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Company data saved successfully!")
#                     request.session.pop("company_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Company save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Company save error: %s", e)
#                 messages.error(request, f"Error saving company data: {e}")

#         # Save employee
#         elif "save_employee" in request.POST:
#             payload = {
#                 "employees": employee_data,
#                 "metadata": {"source": "web-upload", "user": request.user.username if request.user.is_authenticated else "anonymous"}
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Employee data saved successfully!")
#                     request.session.pop("employee_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Employee save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Employee save error: %s", e)
#                 messages.error(request, f"Error saving employee data: {e}")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": bool(company_data),
#         "show_save_employee": bool(employee_data),
#     })










# ///////////final///////////////////////////////////
# ////////////working ////////////////////////////////
# ///////////code////////////////////////////////////






# def upload_csv(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})



#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     # Session-stored data
   
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Get backend company codes
#     try:
#         res = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         backend_codes = {c.get("companyCode") for c in res.json()} if res.status_code == 200 else set()
#     except Exception as e:
#         messages.error(request, f"Error fetching company list: {e}")
#         logger.error("Company list fetch error: %s", e)
#         backend_codes = set()

#     # Combine uploaded and backend codes for validation
#     uploaded_codes = {c.get("companyCode") for c in company_data}
#     valid_company_codes = backend_codes.union(uploaded_codes)

#     if request.method == "POST":
#         # Upload Company CSV
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["company_file"])
#                 df.rename(columns={
#                     "CompanyName": "companyName",
#                     "companyName": "companyName",
#                     "CompanyCode": "companyCode",
#                     "companyCode": "companyCode"
#                 }, inplace=True)
#                 df = df[["companyName", "companyCode"]].drop_duplicates()
#                 company_data = df.to_dict(orient="records")
#                 request.session["company_data"] = company_data
#                 messages.success(request, "Company CSV uploaded successfully!")
#                 logger.info("Uploaded Company Data: %s", company_data)
#             except Exception as e:
#                 logger.error("Company CSV error: %s", e)
#                 messages.error(request, f"Failed to read Company CSV: {e}")

#         # Upload Employee CSV
#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 df.rename(columns={
#                     "Name": "Name",
#                     "Email": "Email",
#                     "Usertype": "Usertype",
#                     "CompanyCode": "companyCode",
#                     "companyCode": "companyCode",
#                     "EmpCode": "EmpCode"
#                 }, inplace=True)
#                 df = df[["Name", "Email", "Usertype", "companyCode", "EmpCode"]].drop_duplicates()
#                 records = df.to_dict(orient="records")

#                 # Validate against combined codes
#                 invalid = [emp for emp in records if emp["companyCode"] not in valid_company_codes]
#                 if invalid:
#                     logger.warning("Invalid employee company codes: %s", invalid)
#                     messages.error(request, "Some employees have invalid company codes.")
#                 else:
#                     employee_data = records
#                     request.session["employee_data"] = employee_data
#                     messages.success(request, "Employee CSV uploaded successfully!")
#                     logger.info("Uploaded Employee Data: %s", employee_data)
#             except Exception as e:
#                 logger.error("Employee CSV error: %s", e)
#                 messages.error(request, f"Failed to read Employee CSV: {e}")

#         # Save Company
#         elif "save_company" in request.POST and company_data:
        
#             payload = {
#                 "companies": company_data,
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Company data saved successfully!")
#                     request.session.pop("company_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Company save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Company save error: %s", e)
#                 messages.error(request, f"Error saving company data: {e}")

#         # Save Employee
#         elif "save_employee" in request.POST and employee_data:
#             payload = {
#                 "employees": employee_data,
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Employee data saved successfully!")
#                     request.session.pop("employee_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Employee save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Employee save error: %s", e)
#                 messages.error(request, f"Error saving employee data: {e}")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": bool(company_data),
#         "show_save_employee": bool(employee_data),
#     })


# def upload_csv(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Fetch company list for validating employee CompanyCode
#     try:
#         company_response = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         if company_response.status_code == 200:
#             company_list = company_response.json()
#         else:
#             company_list = []
#     except Exception as e:
#         messages.error(request, f"Error fetching company list: {str(e)}")
#         company_list = []

#     valid_company_codes = {c.get("companyCode") for c in company_list if "companyCode" in c}

#     if request.method == "POST":
#         # Upload company CSV
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             df.rename(columns={
#             #    "CompanyCode": "companyCode",
#                "companyCode": "companyCode",
#                "CompanyName": "companyName",
#             "companyName": "companyName"
                
#             }, inplace=True)
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             request.session["company_data"] = company_data
#             messages.success(request, "Company CSV uploaded successfully!")

#         # Upload employee CSV
#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             df.rename(columns={
#     "Name": "Name",
#     "Email": "Email",
#     "Usertype": "Usertype",
#     "CompanyCode": "companyCode",  # Always convert to lowercase
#     "companyCode": "companyCode",
#     "EmpCode": "EmpCode"
# }, inplace=True)

#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             invalid = [emp for emp in employee_data if emp["companyCode"] not in valid_company_codes]
#             if invalid:
#                 messages.error(request, "Some employees have invalid Company Codes.")
#                 employee_data = []
#             else:
#                 request.session["employee_data"] = employee_data
#                 messages.success(request, "Employee CSV uploaded successfully!")

#         # Save company data
#         elif "save_company" in request.POST and "company_data" in request.session:
#             payload = {
#                 "companies": request.session["company_data"],
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#             if response.status_code == 200:
#                 del request.session["company_data"]
#                 messages.success(request, "Company data saved successfully!")
#                 return redirect("company_list")
#             else:
#                 messages.error(request, "Company data save failed.")

#         # Save employee data
#         elif "save_employee" in request.POST and "employee_data" in request.session:
#             payload = {
#                 "employees": request.session["employee_data"],
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#             if response.status_code == 200:
#                 del request.session["employee_data"]
#                 messages.success(request, "Employee data saved successfully!")
#                 return redirect("employee_list")
#             else:
#                 messages.error(request, "Employee data save failed.")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": "company_data" in request.session,
#         "show_save_employee": "employee_data" in request.session
#     })



# def upload_csv(request):
#     access_token = request.session.get('access_token')

#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Fetch company list for validation
#     try:
#         company_response = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         if company_response.status_code == 200:
#             company_data = company_response.json()
#     except Exception as e:
#         messages.error(request, f"Error fetching company list: {str(e)}")

#     valid_company_codes = {company.get("CompanyCode") for company in company_data if "CompanyCode" in company}


#     # Fetch employee list (optional display)
#     try:
#         employee_response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers)
#         if employee_response.status_code == 200:
#             employee_data = employee_response.json()
#     except Exception as e:
#         messages.error(request, f"Error fetching employee list: {str(e)}")

#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             request.session["company_data"] = company_data
#             messages.success(request, "Company CSV uploaded successfully!")

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             invalid = [emp for emp in employee_data if emp["CompanyCode"] not in valid_company_codes]
#             if invalid:
#                 messages.error(request, "Some employees have invalid Company Codes.")
#                 employee_data = []
#             else:
#                 request.session["employee_data"] = employee_data
#                 messages.success(request, "Employee CSV uploaded successfully!")

#         elif "save_company" in request.POST and "company_data" in request.session:
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadCompany", json=request.session["company_data"], headers=headers)
#                 if response.status_code == 200:
#                     del request.session["company_data"]
#                     messages.success(request, "Company data saved successfully!")
#                     return redirect("company_list")
#                 else:
#                     messages.error(request, f"Failed to save company data: {response.status_code}")
#             except Exception as e:
#                 messages.error(request, f"Error saving company data: {str(e)}")

#         elif "save_employee" in request.POST and "employee_data" in request.session:
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadEmployee", json=request.session["employee_data"], headers=headers)
#                 if response.status_code == 200:
#                     del request.session["employee_data"]
#                     messages.success(request, "Employee data saved successfully!")
#                     return redirect("employee_list")
#                 else:
#                     messages.error(request, f"Failed to save employee data: {response.status_code}")
#             except Exception as e:
#                 messages.error(request, f"Error saving employee data: {str(e)}")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": "company_data" in request.session,
#         "show_save_employee": "employee_data" in request.session
#     })



# def debug_api_call(request, url, method='POST', payload=None):
#     """Helper function to debug API calls"""
#  headers = {"Authorization": access_token}
    
#     print(f"Making {method} request to: {url}")
#     print("Headers:", json.dumps(headers, indent=2))
    
    
#     try:
#         if method == 'POST':
#             response = requests.post(url, headers=headers, json=payload, timeout=10)
#         else:
#             response = requests.get(url, headers=headers, timeout=10)
        
#         print(f"Response Status: {response.status_code}")
#         print("Response Headers:", dict(response.headers))
#         print("Response Body:", response.text)
        
#         return response
        
#     except requests.exceptions.RequestException as e:
#         print(f"Request failed: {str(e)}")
#         if hasattr(e, 'response') and e.response:
#             print(f"Error response: {e.response.text}")
#         raise

# @require_http_methods(["GET", "POST"])
# def upload_csv(request):
#     # Debug session and authentication
#     print("\n===== SESSION DATA =====")
#     print("Session keys:", request.session.keys())
#     print("Access token exists:", 'access_token' in request.session)
    
#     if not request.session.get('access_token'):
#         messages.error(request, 'Session expired. Please login again.')
#         return redirect('login')

#     # Initialize session data
#     request.session.setdefault("company_data", [])
#     request.session.setdefault("employee_data", [])
    
#     if request.method == "POST":
#         # Handle Company Save
#         if "save_company" in request.POST:
#             print("\n===== ATTEMPTING COMPANY SAVE =====")
#             try:
#                 payload = {
#                     "companies": request.session.get("company_data", []),
#                     "metadata": {
#                         "source": "web-upload",
#                         "user": request.user.username if request.user.is_authenticated else "anonymous"
#                     }
#                 }
                
#                 # Make the API call with debugging
#                 response = debug_api_call(
#                     request,
#                     f"{BASE_URL}fileUploadCompany",
#                     payload=payload
#                 )
                
#                 if response.status_code == 200:
#                     del request.session["company_data"]
#                     messages.success(request, "Company data saved successfully!")
#                 elif response.status_code == 403:
#                     error_msg = response.json().get('message', "Permission denied")
#                     messages.error(request, f"Authorization failed: {error_msg}")
#                     print("Potential causes:")
#                     print("- Invalid/expired access token")
#                     print("- Missing required permissions")
#                     print("- CSRF token missing (if required)")
#                 else:
#                     messages.error(request, f"Save failed with status {response.status_code}")
                
#             except Exception as e:
#                 messages.error(request, f"Save failed: {str(e)}")
#                 print("Full error traceback:", repr(e))
#                 return redirect('upload_csv')
        
#         # Similar handling for employee save...
#         elif "save_employee" in request.POST:
#             print("\n===== ATTEMPTING EMPLOYEE SAVE =====")
#             try:
#                 payload = {
#                     "employees": request.session.get("employee_data", []),
#                     "metadata": {
#                         "source": "web-upload",
#                         "user": request.user.username if request.user.is_authenticated else "anonymous"
#                     }
#                 }
                
#                 response = debug_api_call(
#                     request,
#                     f"{BASE_URL}fileUploadEmployee",
#                     payload=payload
#                 )
                
#                 if response.status_code == 200:
#                     del request.session["employee_data"]
#                     messages.success(request, "Employee data saved successfully!")
#                 elif response.status_code == 403:
#                     error_detail = response.json().get('detail', "Check your permissions")
#                     messages.error(request, f"Authorization error: {error_detail}")
#                 else:
#                     messages.error(request, f"Save failed with status {response.status_code}")
                
#             except Exception as e:
#                 messages.error(request, f"Save failed: {str(e)}")
#                 print("Employee save error:", repr(e))
    
#     return render(request, "upload_csv.html", {
#         "company_data": request.session.get("company_data"),
#         "employee_data": request.session.get("employee_data"),
#         "show_save_company": bool(request.session.get("company_data")),
#         "show_save_employee": bool(request.session.get("employee_data")),
#     })



# def upload_csv(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     try:
#         company_response = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         if company_response.status_code == 200:
#             company_data = company_response.json()
#             request.session["company_data"] = company_data
#     except Exception as e:
#         print("Company fetch failed:", e)

#     valid_company_codes = {c.get("CompanyCode") for c in company_data}

#     try:
#         employee_response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers)
#         if employee_response.status_code == 200:
#             employee_data = employee_response.json()
#             request.session["employee_data"] = employee_data
#     except Exception as e:
#         print("Employee fetch failed:", e)

#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["company_file"])
#                 company_data = df.drop_duplicates().to_dict(orient="records")
#                 request.session["company_data"] = company_data
#                 messages.success(request, "Company CSV uploaded successfully!")
#             except Exception as e:
#                 print("Error reading company CSV:", e)
#                 messages.error(request, "Invalid company CSV file.")

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 employee_data = df.drop_duplicates().to_dict(orient="records")
#                 invalid_employees = [emp for emp in employee_data if emp.get("CompanyCode") not in valid_company_codes]
#                 if invalid_employees:
#                     messages.error(request, "Some employees have invalid Company Codes.")
#                 else:
#                     request.session["employee_data"] = employee_data
#                     messages.success(request, "Employee CSV uploaded successfully!")
#             except Exception as e:
#                 print("Error reading employee CSV:", e)
#                 messages.error(request, "Invalid employee CSV file.")

#         elif "save_company" in request.POST:
#             post_data = request.session.get("company_data", [])
#             try:
#                 res = requests.post(f"{BASE_URL}fileUploadCompany", json=post_data, headers=headers)
#                 if res.status_code == 200:
#                     del request.session["company_data"]
#                     messages.success(request, "Company data saved to database.")
#                 else:
#                     messages.error(request, "Failed to save company data.")
#             except Exception as e:
#                 print("Company save error:", e)

#         elif "save_employee" in request.POST:
#             post_data = request.session.get("employee_data", [])
#             try:
#                 res = requests.post(f"{BASE_URL}fileUploadEmployee", json=post_data, headers=headers)
#                 if res.status_code == 200:
#                     del request.session["employee_data"]
#                     messages.success(request, "Employee data saved to database.")
#                 else:
#                     messages.error(request, "Failed to save employee data.")
#             except Exception as e:
#                 print("Employee save error:", e)

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": request.session.get("company_data", []),
#         "employee_data": request.session.get("employee_data", []),
#         "show_save_company": "company_data" in request.session,
#         "show_save_employee": "employee_data" in request.session,
#     })

# final working code 4/16/25

# def upload_csv(request):
#     session_token = request.session.get("token", "your_generated_token")
#     request.session["token"] = session_token

#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     company_response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#     if company_response.status_code == 200:
#         company_data = company_response.json()
    
#     valid_company_codes = {company["CompanyCode"] for company in company_data}

#     employee_response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#     if employee_response.status_code == 200:
#         employee_data = employee_response.json()

#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             request.session["company_data"] = company_data
#             messages.success(request, "Company CSV uploaded successfully!")

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

            
#             invalid_employees = [emp for emp in employee_data if emp["CompanyCode"] not in valid_company_codes]
#             if invalid_employees:
#                 messages.error(request, "Error: Some employees have an invalid Company Code. Upload cancelled.")
#                 employee_data = []
#             else:
#                 request.session["employee_data"] = employee_data
#                 messages.success(request, "Employee CSV uploaded successfully!")

        
#         elif "save_company" in request.POST:
#             if "company_data" in request.session:
#                 requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=request.session["company_data"])
#                 del request.session["company_data"]
#                 messages.success(request, "Company data saved to Database!")
#                 return redirect("company_list")  

#         elif "save_employee" in request.POST:
#             if "employee_data" in request.session:
#                 requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=request.session["employee_data"])
#                 del request.session["employee_data"]
#                 messages.success(request, "Employee data saved to Database!")
#                 return redirect("employee_list")  

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": "company_data" in request.session,
#         "show_save_employee": "employee_data" in request.session,
#         "token": session_token
#     })



import csv
from django.http import HttpResponse
from django.shortcuts import render

# Export Empty Company CSV
# def export_company(request):
#     # Create the response object and specify it's a CSV file
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="empty_company.csv"'

#     # Create a CSV writer
#     writer = csv.writer(response)
#     # Write the header for company data
#     writer.writerow(['company Name', 'Company Code'])

#     # Return the response with empty content
#     return response

# # Export Empty Employee CSV
# def export_employee(request):
#     # Create the response object and specify it's a CSV file
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="empty_employee.csv"'

#     # Create a CSV writer
#     writer = csv.writer(response)
#     # Write the header for employee data
#     writer.writerow(['Name', 'Email', 'Usertype', 'Company Code', 'Emp Code'])

#     # Return the response with empty content
#     return response

# ?????????????????????????????final working code for showing company and employee data in table?????????????????????????????????????
# def upload_csv(request):
#     session_token = request.session.get("token", "your_generated_token")
#     request.session["token"] = session_token

#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Fetch existing company data
#     company_response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#     if company_response.status_code == 200:
#         company_data = company_response.json()
    
#     valid_company_codes = {company["CompanyCode"] for company in company_data}

#     # Fetch existing employee data
#     employee_response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#     if employee_response.status_code == 200:
#         employee_data = employee_response.json()

#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             request.session["company_data"] = company_data  # Store temporarily
#             messages.success(request, "Company CSV uploaded successfully!")

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             # Validate Employee Company Codes
#             invalid_employees = [emp for emp in employee_data if emp["CompanyCode"] not in valid_company_codes]
#             if invalid_employees:
#                 messages.error(request, "Error: Some employees have an invalid Company Code. Upload cancelled.")
#                 employee_data = []
#             else:
#                 request.session["employee_data"] = employee_data  # Store temporarily
#                 messages.success(request, "Employee CSV uploaded successfully!")

#         elif "save_company" in request.POST:
#             if "company_data" in request.session:
#                 requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=request.session["company_data"])
#                 del request.session["company_data"]  # Remove after saving
#                 messages.success(request, "Company data saved to Database!")

#         elif "save_employee" in request.POST:
#             if "employee_data" in request.session:
#                 requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=request.session["employee_data"])
#                 del request.session["employee_data"]  # Remove after saving
#                 messages.success(request, "Employee data saved to Database!")

#         return redirect("upload_csv")  # Reload page to refresh UI

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": "company_data" in request.session,
#         "show_save_employee": "employee_data" in request.session,
#         "token": session_token
#     })

# import pandas as pd
# import requests
# from django.shortcuts import render
# from django.http import JsonResponse

# def upload_csv(request):
#     """Handles company and employee CSV uploads, validates, and displays data."""
    
#     session_token = request.session.get("token")
#     if not session_token:
#         session_token = "your_generated_token"  # Replace with actual logic
#         request.session["token"] = session_token

#     company_data = []
#     employee_data = []

#     # 🔹 Always Fetch Company Data First (Ensures Company Table is Always Visible)
#     company_response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#     if company_response.status_code == 200:
#         company_data = company_response.json()

#     # 🔹 Always Fetch Employee Data (Ensures Employee Table is Always Visible)
#     employee_response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#     if employee_response.status_code == 200:
#         employee_data = employee_response.json()

#     # Handle CSV uploads
#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=company_data)

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             # 🔹 Validate Employee Company Codes
#             company_codes = {company["CompanyCode"] for company in company_data}
#             invalid_employees = [emp for emp in employee_data if emp["CompanyCode"] not in company_codes]

#             if invalid_employees:
#                 return render(request, "upload_csv.html", {
#                     "company_data": company_data,  # ✅ Ensure Company Table is Shown
#                     "employee_data": employee_data,  # ✅ Ensure Employee Table is Shown
#                     "error": "Some employees have an invalid Company Code.",
#                     "token": session_token
#                 })

#             requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=employee_data)

#         # 🔹 Re-fetch Company & Employee Data After Upload
#         company_response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#         if company_response.status_code == 200:
#             company_data = company_response.json()

#         employee_response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#         if employee_response.status_code == 200:
#             employee_data = employee_response.json()

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,  # ✅ Always Show Company Table
#         "employee_data": employee_data,  # ✅ Always Show Employee Table
#         "token": session_token
#     })


# import pandas as pd
# import requests
# from django.shortcuts import render
# from django.http import JsonResponse

# def upload_csv(request):
#     """Handles company and employee CSV uploads, validates, and displays data."""
    
#     session_token = request.session.get("token")
#     if not session_token:
#         session_token = "your_generated_token"  # Replace with actual logic
#         request.session["token"] = session_token

#     company_data = []
#     employee_data = []

#     # Always fetch the latest company list
#     response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#     if response.status_code == 200:
#         company_data = response.json()

#     # Fetch employees if requested
#     if request.GET.get("action") == "getEmployeeList":
#         response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#         if response.status_code == 200:
#             employee_data = response.json()

#     # Handle CSV uploads
#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=company_data)

#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             # Validate Employee Company Codes against existing Company Codes
#             company_codes = {company["CompanyCode"] for company in company_data}
#             invalid_employees = [emp for emp in employee_data if emp["CompanyCode"] not in company_codes]

#             if invalid_employees:
#                 return render(request, "upload_csv.html", {
#                     "company_data": company_data,
#                     "employee_data": employee_data,
#                     "error": "Some employees have an invalid Company Code.",
#                     "token": session_token
#                 })

#             requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=employee_data)

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "token": session_token
#     })

# def upload_csv(request):
#     """Handles company and employee CSV uploads, validates, and displays data."""
    
#     session_token = request.session.get("token")
#     if not session_token:
#         session_token = "your_generated_token"  # Replace with actual logic
#         request.session["token"] = session_token

#     company_data = []
#     employee_data = []

#     # Fetch existing data
#     action = request.GET.get("action")
#     if action == "getCompanyList":
#         response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#         if response.status_code == 200:
#             company_data = response.json()
#     elif action == "getEmployeeList":
#         response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#         if response.status_code == 200:
#             employee_data = response.json()
#     elif action == "token":
#         return JsonResponse({"token": session_token})

#     # Handle CSV uploads
#     if request.method == "POST":
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.drop_duplicates().to_dict(orient="records")
#             requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=company_data)
        
#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.drop_duplicates().to_dict(orient="records")

#             # Validate Company Codes
#             company_codes = {company["CompanyCode"] for company in company_data}
#             invalid_employees = [emp for emp in employee_data if emp["CompanyCode"] not in company_codes]

#             if invalid_employees:
#                 return render(request, "upload_csv.html", {
#                     "company_data": company_data,
#                     "employee_data": employee_data,
#                     "error": "Some employees have an invalid Company Code.",
#                     "token": session_token
#                 })

#             requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=employee_data)

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "token": session_token
#     })



# def upload_csv(request):
#     """Handles company and employee CSV uploads, validates, and displays data."""

#     session_token = request.session.get("token")
#     if not session_token:
#         session_token = "your_generated_token"  # Replace with actual logic
#         request.session["token"] = session_token

#     company_data = []
#     employee_data = []

#     # Handle GET requests
#     action = request.GET.get("action")
#     if action == "getCompanyList":
#         response = requests.get(f"{BASE_URL}getCompanyList/{session_token}")
#         if response.status_code == 200:
#             company_data = response.json()
#     elif action == "getEmployeeList":
#         response = requests.get(f"{BASE_URL}getEmployeeList/{session_token}")
#         if response.status_code == 200:
#             employee_data = response.json()
#     elif action == "token":
#         return JsonResponse({"token": session_token})

#     # Handle POST file uploads
#     if request.method == "POST":
#         if "company_file" in request.FILES:
#             df = pd.read_csv(request.FILES["company_file"])
#             company_data = df.to_dict(orient="records")
#             requests.post(f"{BASE_URL}fileUploadCompany/{session_token}", json=company_data)
        
#         elif "employee_file" in request.FILES:
#             df = pd.read_csv(request.FILES["employee_file"])
#             employee_data = df.to_dict(orient="records")
#             requests.post(f"{BASE_URL}fileUploadEmployee/{session_token}", json=employee_data)

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "token": session_token
#     })

# import csv
# from django.shortcuts import render
# from .forms import CompanyCSVUploadForm, EmployeeCSVUploadForm

# import csv
# from django.shortcuts import render
# from django.contrib import messages
# from .forms import CompanyCSVUploadForm, EmployeeCSVUploadForm  # Ensure these forms exist

# def upload_csv(request):
#     """Handles company and employee CSV uploads, validates, and displays data."""
    
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])
#     alerts = []

#     if request.method == "POST":
#         # Check which form was submitted
#         if "company_file" in request.FILES:
#             company_form = CompanyCSVUploadForm(request.POST, request.FILES)
#             employee_form = EmployeeCSVUploadForm()

#             if company_form.is_valid():
#                 uploaded_file = request.FILES["company_file"]
#                 data = list(csv.DictReader(uploaded_file.read().decode("utf-8").splitlines()))

#                 # Save Company Data to session
#                 request.session["company_data"] = data
#                 request.session["company_codes"] = list({row["CompanyCode"] for row in data})  # ✅ Convert set to list
#                 company_data = data  

#         elif "employee_file" in request.FILES:
#             employee_form = EmployeeCSVUploadForm(request.POST, request.FILES)
#             company_form = CompanyCSVUploadForm()

#             if employee_form.is_valid():
#                 uploaded_file = request.FILES["employee_file"]
#                 data = list(csv.DictReader(uploaded_file.read().decode("utf-8").splitlines()))

#                 # Validate Employee's CompanyCode with stored CompanyCode
#                 company_codes = set(request.session.get("company_codes", []))  # ✅ Convert list back to set
#                 valid_employees = []

#                 for row in data:
#                     if row["CompanyCode"] in company_codes:
#                         valid_employees.append(row)
#                     else:
#                         alerts.append(f"❌ Company Code {row['CompanyCode']} not found in Company Data.")

#                 request.session["employee_data"] = valid_employees
#                 employee_data = valid_employees  

#     else:
#         company_form = CompanyCSVUploadForm()
#         employee_form = EmployeeCSVUploadForm()

#     return render(request, "upload_csv.html", {
#         "company_form": company_form,
#         "employee_form": employee_form,
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "alerts": alerts
#     })


# already workin for showing the data in the table
# import requests
# import pandas as pd
# from django.shortcuts import render
# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# from .forms import CompanyUploadForm, EmployeeUploadForm

# BASE_URL = "http://195.35.45.101:9002/spring-API/"

# @csrf_exempt
# def upload_csv(request):
#     if "company_data" not in request.session:
#         request.session["company_data"] = []

#     company_data = request.session.get("company_data", [])
#     employee_data = []

#     if request.method == "POST":
#         if "company_file" in request.FILES:
#             form = CompanyUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 df = pd.read_csv(request.FILES["company_file"])
#                 company_data = df.to_dict(orient="records")
#                 request.session["company_data"] = company_data

#                 # Send to backend
#                 requests.post(BASE_URL + "fileUploadCompany", json=company_data)

#         elif "employee_file" in request.FILES:
#             form = EmployeeUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 employee_data = df.to_dict(orient="records")

#                 # Validate Employee CompanyCode
#                 company_codes = {c["CompanyCode"] for c in company_data}
#                 for emp in employee_data:
#                     if emp["CompanyCode"] not in company_codes:
#                         return JsonResponse({"error": "Employee CompanyCode not matched"}, status=400)

#                 # Send to backend
#                 requests.post(BASE_URL + "fileUploadEmployee", json=employee_data)

#     return render(request, "upload_csv.html", {"company_data": company_data, "employee_data": employee_data})



@role_required(allowed_roles=['ADMIN', 'USER', 'CLIENT'])
@custom_login_required
def registerfrontend(request):
    try:
        access_token = request.session['access_token']
        
        if request.method == 'POST':
            form = RegisterFrontendForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                user_name = form.cleaned_data['user_name']
                password = request.POST.get('password')
                user = form.cleaned_data['user']
                role = form.cleaned_data['role']
                emp_code = form.cleaned_data['emp_code']
                companyCode = form.cleaned_data['companyCode']
                email = form.cleaned_data['email_id']

                # Prepare data for backend API
                data = {
           
                    'name': name,
                    'userName': user_name,
                    'password': password,
                    "user": user,
                    "role": role.upper() if role.upper() else "CLIENT",
                    "companyCode": companyCode,
                    'empCode': emp_code,
                    "email": email
                }
                print("data0", data)

                # Call backend API to register user
                endpoint = "Frontend"
                json_data = json.dumps(data)
                frontend_url_list = call_post_with_method(BASE_URL, endpoint, json_data, access_token)

                if frontend_url_list.status_code != 200:
                    messages.error(request, 'An error occurred while processing your request.')
                    return render(request, 'registerfrontend.html', {'form': form})

                # Send registration email
                send_registration_email(name, email)

                messages.success(request, 'Registration successful! A confirmation email has been sent.')
                return redirect('frontendurl')

            else:
                print("Form errors:", form.errors)

        form = RegisterFrontendForm()
        return render(request, 'registerfrontend.html', {'form': form})

    except Exception as error:
        print(f'Error: {error}')
        return render(request, '500page.html', {'error': str(error)})


def send_registration_email(name, email):
    """
    Sends a welcome email with a registration confirmation link.
    """
    subject = "Welcome to Our Platform!"
    message = f"""
    Hi {name},

    Thank you for registering with us. Your account has been successfully created.

    Click the link below to confirm your email and log in:
    https://API Gateway/login

    If you did not register, please ignore this email.

    Best regards,
    Your Website Team
    """
    from_email = "syedmydeen140897@gmail.com"  
    recipient_list = [email]

    send_mail(subject, message, from_email, recipient_list)




    # //////////////////////////////company list//////////////////////////////////




# def company_list(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     companies = []
#     try:
#         response = requests.get(f"{BASE_URL}getCompanyList", headers=headers, timeout=10)
#         response.raise_for_status()
#         companies = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch companies: {str(e)}")

#     return render(request, "company_list.html", {"companies": companies})


# def employee_list(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     employees = []
#     try:
#         response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers, timeout=10)
#         response.raise_for_status()
#         employees = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch employees: {str(e)}")

#     return render(request, "employee_list.html", {"employees": employees})


# def update(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     if request.method == 'POST':
#         headers = {
#             "Authorization": access_token,
#             "Content-Type": "application/json"
#         }

#         update_type = request.POST.get('updateType')
#         status = request.POST.get('status')

#         try:
#             if update_type == 'company':
#                 data = {
#                     "companyCode": request.POST.get('companyCode'),
#                     "status": status
#                 }
#                 response = requests.post(f"{BASE_URL}updateCompanyStatus", headers=headers, json=data)
#             else:
#                 data = {
#                     "empCode": request.POST.get('empCode'),
#                     "companyCode": request.POST.get('companyCode'),
#                     "status": status
#                 }
#                 response = requests.post(f"{BASE_URL}updateEmployeeStatus", headers=headers, json=data)

#             response.raise_for_status()
#             messages.success(request, "Status updated successfully")
#             return redirect('update')

#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Update failed: {str(e)}")

#     return render(request, "update_page.html")



# ////////////////////////final version of upload company employe list update 



# def upload_csv(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     # Session-stored data
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Get backend company codes
#     try:
#         res = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         backend_codes = {c.get("companyCode") for c in res.json()} if res.status_code == 200 else set()
#     except Exception as e:
#         messages.error(request, f"Error fetching company list: {e}")
#         logger.error("Company list fetch error: %s", e)
#         backend_codes = set()

#     # Combine uploaded and backend codes for validation
#     uploaded_codes = {c.get("companyCode") for c in company_data}
#     valid_company_codes = backend_codes.union(uploaded_codes)

#     if request.method == "POST":
#         # Upload Company CSV
#         if "upload_company" in request.POST and "company_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["company_file"])
#                 df.rename(columns={
#                     "CompanyName": "companyName",
#                     "companyName": "companyName",
#                     "CompanyCode": "companyCode",
#                     "companyCode": "companyCode"
#                 }, inplace=True)
#                 df = df[["companyName", "companyCode"]].drop_duplicates()
#                 company_data = df.to_dict(orient="records")
#                 request.session["company_data"] = company_data
#                 messages.success(request, "Company CSV uploaded successfully!")
#                 logger.info("Uploaded Company Data: %s", company_data)
#             except Exception as e:
#                 logger.error("Company CSV error: %s", e)
#                 messages.error(request, f"Failed to read Company CSV: {e}")

#         # Upload Employee CSV
#         elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#             try:
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 df.rename(columns={
#                     "Name": "Name",
#                     "Email": "Email",
#                     "Usertype": "Usertype",
#                     "CompanyCode": "companyCode",
#                     "companyCode": "companyCode",
#                     "EmpCode": "EmpCode"
#                 }, inplace=True)
#                 df = df[["Name", "Email", "Usertype", "companyCode", "EmpCode"]].drop_duplicates()
#                 records = df.to_dict(orient="records")

#                 # Validate against combined codes
#                 invalid = [emp for emp in records if emp["companyCode"] not in valid_company_codes]
#                 if invalid:
#                     logger.warning("Invalid employee company codes: %s", invalid)
#                     messages.error(request, "Some employees have invalid company codes.")
#                 else:
#                     employee_data = records
#                     request.session["employee_data"] = employee_data
#                     messages.success(request, "Employee CSV uploaded successfully!")
#                     logger.info("Uploaded Employee Data: %s", employee_data)
#             except Exception as e:
#                 logger.error("Employee CSV error: %s", e)
#                 messages.error(request, f"Failed to read Employee CSV: {e}")

#         # Save Company
#         elif "save_company" in request.POST and company_data:
#             payload = {
#                 "companies": company_data,
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Company data saved successfully!")
#                     request.session.pop("company_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Company save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Company save error: %s", e)
#                 messages.error(request, f"Error saving company data: {e}")

#         # Save Employee
#         elif "save_employee" in request.POST and employee_data:
#             payload = {
#                 "employees": employee_data,
#                 "metadata": {
#                     "source": "web-upload",
#                     "user": request.user.username if request.user.is_authenticated else "anonymous"
#                 }
#             }
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#                 if response.status_code == 200:
#                     messages.success(request, "Employee data saved successfully!")
#                     request.session.pop("employee_data", None)
#                     return redirect("upload_csv")
#                 else:
#                     messages.error(request, f"Employee save failed: {response.text}")
#             except Exception as e:
#                 logger.error("Employee save error: %s", e)
#                 messages.error(request, f"Error saving employee data: {e}")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": bool(company_data),
#         "show_save_employee": bool(employee_data),
#     })










import pandas as pd
import requests
from django.shortcuts import render, redirect
from django.contrib import messages
import logging

logger = logging.getLogger(__name__)

# def upload_csv(request):
#         print(">> upload_csv view called")
#         access_token = request.session.get('access_token')
#         print("Access Token:", access_token)

#         if not access_token:
#             print("Session expired")
#             return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#         headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json',
#             }


#         company_data = request.session.get("company_data", [])
#         employee_data = request.session.get("employee_data", [])
#         print("Session - company_data:", company_data)
#         print("Session - employee_data:", employee_data)

#         # Get backend company codes
#         try:
#             print("Fetching company list from backend...")
#             res = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#             if res.status_code == 200:
#                 backend_codes = {c.get("companyCode") for c in res.json()}
#             else:
#                 backend_codes = set()
#             print("Backend company codes:", backend_codes)
#         except Exception as e:
#             messages.error(request, f"Error fetching company list: {e}")
#             logger.error("Company list fetch error: %s", e)
#             backend_codes = set()

#         uploaded_codes = {c.get("companyCode") for c in company_data}
#         valid_company_codes = backend_codes.union(uploaded_codes)
#         print("Valid company codes for validation:", valid_company_codes)

#         if request.method == "POST":
#             print("Handling POST request")

#             if "upload_company" in request.POST and "company_file" in request.FILES:
#                 print("Uploading Company CSV")
#                 try:
#                     df = pd.read_csv(request.FILES["company_file"])
#                     print("Raw Company CSV data:\n", df.head())
#                     df.rename(columns={
#                         "CompanyName": "companyName",
#                         "companyName": "companyName",
#                         "CompanyCode": "companyCode",
#                         "companyCode": "companyCode"
#                     }, inplace=True)
#                     df = df[["companyName", "companyCode"]].drop_duplicates()
#                     company_data = df.to_dict(orient="records")
#                     print("Processed company data:", company_data)
#                     request.session["company_data"] = company_data
#                     messages.success(request, "Company CSV uploaded successfully!")
#                 except Exception as e:
#                     logger.error("Company CSV error: %s", e)
#                     messages.error(request, f"Failed to read Company CSV: {e}")

#             elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#                 print("Uploading Employee CSV")
#                 try:
#                     df = pd.read_csv(request.FILES["employee_file"])
#                     print("Raw Employee CSV data:\n", df.head())
#                     df.rename(columns={
#                         "Name": "Name",
#                         "Email": "Email",
#                         "Usertype": "Usertype",
#                         "CompanyCode": "companyCode",
#                         "companyCode": "companyCode",
#                         "EmpCode": "EmpCode"
#                     }, inplace=True)
#                     df = df[["Name", "Email", "Usertype", "companyCode", "EmpCode"]].drop_duplicates()
#                     records = df.to_dict(orient="records")
#                     print("Processed employee records:", records)

#                     invalid = [emp for emp in records if emp["companyCode"] not in valid_company_codes]
#                     if invalid:
#                         print("Invalid employee company codes found:", invalid)
#                         messages.error(request, "Some employees have invalid company codes.")
#                     else:
#                         employee_data = records
#                         request.session["employee_data"] = employee_data
#                         messages.success(request, "Employee CSV uploaded successfully!")
#                 except Exception as e:
#                     logger.error("Employee CSV error: %s", e)
#                     messages.error(request, f"Failed to read Employee CSV: {e}")

#             elif "save_company" in request.POST and company_data:
#                 print("Saving Company Data")
#                 payload = {
#                     "companies": company_data,
                    
#                 }
#                 print("Company payload:", payload)
#                 try:
#                     response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#                     print("Company save response:", response.status_code, response.text)
#                     if response.status_code == 200:
#                         messages.success(request, "Company data saved successfully!")
#                         request.session.pop("company_data", None)
#                         return redirect("upload_csv")
#                     else:
#                         print("Response headers:", response.headers)
#                         print("Response body:", response.text)
#                         messages.error(request, f"Save failed: {response.text}")

#                 except Exception as e:
#                     logger.error("Company save error: %s", e)
#                     messages.error(request, f"Error saving company data: {e}")

#             elif "save_employee" in request.POST and employee_data:
#                 print("Saving Employee Data")
#                 payload = {
#                     "employees": employee_data,
                
#                 }
#                 print("Employee payload:", payload)
#                 try:
#                     response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#                     print("Employee save response:", response.status_code, response.text)
#                     if response.status_code == 200:
#                         messages.success(request, "Employee data saved successfully!")
#                         request.session.pop("employee_data", None)
#                         return redirect("upload_csv")
#                     else:
#                         messages.error(request, f"Employee save failed: {response.text}")
#                 except Exception as e:
#                     logger.error("Employee save error: %s", e)
#                     messages.error(request, f"Error saving employee data: {e}")

#             return redirect("upload_csv")

#         return render(request, "upload_csv.html", {
#             "company_data": company_data,
#             "employee_data": employee_data,
#             "show_save_company": bool(company_data),
#             "show_save_employee": bool(employee_data),
#         })





# import pandas as pd
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages


# import requests
# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages

# def upload_csv(request):
#     print(">> upload_csv view called")

#     # Access token validation
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         'Authorization': access_token,
#         'Content-Type': 'application/json'
#     }

#     # Session-stored data
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Get current backend company codes
#     try:
#         res = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         backend_codes = {c.get("companyCode") for c in res.json()} if res.status_code == 200 else set()
#     except Exception as e:
#         backend_codes = set()
#         messages.error(request, f"Failed to fetch company list: {e}")

#     uploaded_codes = {c.get("companyCode") for c in company_data}
#     valid_company_codes = backend_codes.union(uploaded_codes)

#     if request.method == "POST":
#         if "upload_company" in request.POST:
#             try:
#                 df = pd.read_csv(request.FILES["company_file"])
#                 df.rename(columns=lambda x: x.strip(), inplace=True)
#                 df.rename(columns={"CompanyName": "companyName", "CompanyCode": "companyCode"}, inplace=True)
#                 df = df[["companyName", "companyCode"]].drop_duplicates()
#                 request.session["company_data"] = df.to_dict(orient="records")
#                 messages.success(request, "Company CSV uploaded successfully!")
#             except Exception as e:
#                 messages.error(request, f"Company CSV upload failed: {e}")

#         elif "upload_employee" in request.POST:
#             try:
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 df.rename(columns=lambda x: x.strip(), inplace=True)
#                 df = df[["Name", "Email", "Usertype", "CompanyCode", "EmpCode"]].drop_duplicates()
#                 df.rename(columns={"CompanyCode": "companyCode"}, inplace=True)
#                 employee_records = df.to_dict(orient="records")
#                 invalid = [emp for emp in employee_records if emp["companyCode"] not in valid_company_codes]
#                 if invalid:
#                     messages.error(request, "Invalid company codes in employee data.")
#                 else:
#                     request.session["employee_data"] = employee_records
#                     messages.success(request, "Employee CSV uploaded successfully!")
#             except Exception as e:
#                 messages.error(request, f"Employee CSV upload failed: {e}")

#         elif "save_company" in request.POST and company_data:
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadCompany", json=company_data, headers=headers)
#                 if response.status_code == 200:
#                     request.session.pop("company_data", None)
#                     messages.success(request, "Company data saved successfully!")
#                     return redirect("company_list")
#                 else:
#                     messages.error(request, f"Company save failed: {response.text}")
#             except Exception as e:
#                 messages.error(request, f"Company save error: {e}")

#         elif "save_employee" in request.POST and employee_data:
#             try:
#                 response = requests.post(f"{BASE_URL}fileUploadEmployee", json=employee_data, headers=headers)
#                 if response.status_code == 200:
#                     request.session.pop("employee_data", None)
#                     messages.success(request, "Employee data saved successfully!")
#                     return redirect("employee_list")
#                 else:
#                     messages.error(request, f"Employee save failed: {response.text}")
#             except Exception as e:
#                 messages.error(request, f"Employee save error: {e}")

#         return redirect("upload_csv")

#     return render(request, "upload_csv.html", {
#         "company_data": company_data,
#         "employee_data": employee_data,
#         "show_save_company": bool(company_data),
#         "show_save_employee": bool(employee_data),
#     })
    
# from django.shortcuts import render,redirect 
# import pandas as pd
# import requests
# from django.contrib import messages

# import pandas as pd
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import requests

import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
import requests

# def upload_csv(request):
#     print(">> upload_csv view called")

#     # Get access token from session
#     access_token = request.session.get('access_token')
#     if not access_token:
#         return render(request, 'login.html', {'error': 'Session expired. Please log in again.'})

#     headers = {
#         'Authorization': f'Bearer {access_token}',
#         'Content-Type': 'application/json'
#     }
#     print("Response Headers:", save_response.headers)
#     print("Response Body:", save_response.text)  
#     # Load existing session data
#     company_data = request.session.get("company_data", [])
#     employee_data = request.session.get("employee_data", [])

#     # Fetch backend company codes
#     try:
#         response = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
#         backend_codes = {item.get("companyCode") for item in response.json()} if response.status_code == 200 else set()
#     except Exception as e:
#         backend_codes = set()
#         messages.error(request, f"Failed to fetch company codes from backend: {str(e)}")

#     uploaded_codes = {c.get("companyCode") for c in company_data}
#     valid_company_codes = backend_codes.union(uploaded_codes)

#     if request.method == "POST":
#         try:
#             # --- Upload Company File ---
#             if "upload_company" in request.POST and "company_file" in request.FILES:
#                 df = pd.read_csv(request.FILES["company_file"])
#                 df.rename(columns=lambda x: x.strip(), inplace=True)
#                 df.rename(columns={"CompanyName": "companyName", "CompanyCode": "companyCode"}, inplace=True)
#                 df = df[["companyName", "companyCode"]].dropna().drop_duplicates()

#                 company_records = df.to_dict(orient="records")
#                 request.session["company_data"] = company_records
#                 request.session.pop("employee_data", None)

#                 messages.success(request, f"{len(company_records)} company record(s) uploaded successfully.")

#             # --- Upload Employee File ---
#             elif "upload_employee" in request.POST and "employee_file" in request.FILES:
#                 df = pd.read_csv(request.FILES["employee_file"])
#                 df.rename(columns=lambda x: x.strip(), inplace=True)
#                 df = df[["Name", "Email", "Usertype", "CompanyCode", "EmpCode"]].dropna().drop_duplicates()
#                 df.rename(columns={"CompanyCode": "companyCode"}, inplace=True)

#                 employee_records = df.to_dict(orient="records")

#                 invalid_records = [emp for emp in employee_records if emp["companyCode"] not in valid_company_codes]
#                 if invalid_records:
#                     invalid_codes = sorted({emp["companyCode"] for emp in invalid_records})
#                     messages.error(request, f"Invalid company codes in employee data: {', '.join(invalid_codes)}")
#                 else:
#                     request.session["employee_data"] = employee_records
#                     messages.success(request, f"{len(employee_records)} employee record(s) uploaded successfully.")

#             # --- Save Company Records ---
#             elif "save_company" in request.POST and company_data:
#                 payload = {"companies": company_data}
#                 print("Company Payload:", payload)  # Debugging
#                 try:
#                     save_response = requests.post(f"{BASE_URL}fileUploadCompany", json=payload, headers=headers)
#                     print("Response Status Code:", save_response.status_code)
#                     print("Response Text:", save_response.text)
#                     if save_response.status_code == 200:
#                         request.session.pop("company_data", None)
#                         messages.success(request, "Company records saved successfully.")
#                         return redirect('upload_csv')  # Redirect after success
#                     else:
#                         error_message = save_response.json().get('message', save_response.text)
#                         messages.error(request, f"Failed to save company data: {error_message}")
#                 except Exception as e:
#                     messages.error(request, f"Error saving company data: {str(e)}")

#             # --- Save Employee Records ---
#             elif "save_employee" in request.POST and employee_data:
#                 payload = {"employees": employee_data}
#                 print("Employee Payload:", payload)  # Debugging
#                 try:
#                     save_response = requests.post(f"{BASE_URL}fileUploadEmployee", json=payload, headers=headers)
#                     print("Response Status Code:", save_response.status_code)
#                     print("Response Text:", save_response.text)
#                     if save_response.status_code == 200:
#                         request.session.pop("employee_data", None)
#                         messages.success(request, "Employee records saved successfully.")
#                         return redirect('upload_csv')  # Redirect after success
#                     else:
#                         error_message = save_response.json().get('message', save_response.text)
#                         messages.error(request, f"Failed to save employee data: {error_message}")
#                 except Exception as e:
#                     messages.error(request, f"Error saving employee data: {str(e)}")

#         except Exception as e:
#             messages.error(request, f"Error processing file: {str(e)}")

#     return render(request, 'upload_csv.html', {
#         'company_data': request.session.get("company_data", []),
#         'employee_data': request.session.get("employee_data", []),
#         'show_save_company': bool(company_data),
#         'show_save_employee': bool(employee_data)
#     })
# def company_list(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     companies = []
#     try:
#         response = requests.get(f"{BASE_URL}getCompanyList", headers=headers, timeout=10)
#         response.raise_for_status()
#         companies = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch companies: {str(e)}")

#     return render(request, "company_list.html", {"companies": companies})

# def employee_list(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     employees = []
#     try:
#         response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers, timeout=10)
#         response.raise_for_status()
#         employees = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch employees: {str(e)}")

#     return render(request, "employee_list.html", {"employees": employees})

# def update(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     if request.method == 'POST':
#         headers = {
#             "Authorization": access_token,
#             "Content-Type": "application/json"
#         }

#         update_type = request.POST.get('updateType')
#         status = request.POST.get('status')

#         try:
#             if update_type == 'company':
#                 data = {
#                     "companyCode": request.POST.get('companyCode'),
#                     "status": status
#                 }
#                 response = requests.post(f"{BASE_URL}updateCompanyStatus", headers=headers, json=data)
#             else:
#                 data = {
#                     "empCode": request.POST.get('empCode'),
#                     "companyCode": request.POST.get('companyCode'),
#                     "status": status
#                 }
#                 response = requests.post(f"{BASE_URL}updateEmployeeStatus", headers=headers, json=data)

#             response.raise_for_status()
#             messages.success(request, "Status updated successfully")
#             return redirect('update')

#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Update failed: {str(e)}")

#     return render(request, "update_page.html")



# import pandas as pd
# import requests
# from django.shortcuts import render, redirect
# from django.contrib import messages
# import requests
# import pandas as pd
# from io import StringIO
# from django.shortcuts import render, redirect
# from django.contrib import messages
import requests
import pandas as pd
from io import StringIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse



def upload_csv(request):
    # Authentication check
    access_token = request.session.get('access_token')
    if not access_token:
        return redirect('login')

    # Initialize session data
    company_data = request.session.get("company_data", [])
    employee_data = request.session.get("employee_data", [])

    # Get valid company codes
    valid_company_codes = set(c['companyCode'] for c in company_data)
    
    # Try to fetch existing company codes from backend
    try:
        headers = {'Authorization': access_token}
        response = requests.get(f"{BASE_URL}getCompanyList", headers=headers)
        if response.status_code == 200:
            backend_codes = {item['companyCode'] for item in response.json()}
            valid_company_codes.update(backend_codes)
    except Exception as e:
        print(f"Error fetching company list: {str(e)}")

    if request.method == "POST":
        try:
            # --- Upload Company File ---
            if "upload_company" in request.POST and "company_file" in request.FILES:
                df = pd.read_csv(request.FILES["company_file"])
                df.columns = df.columns.str.strip().str.lower()
                
                # Column mapping
                column_map = {
                    'companyname': 'companyName',
                    'companycode': 'companyCode'
                }
                df.rename(columns=column_map, inplace=True)
                
                # Validation
                if not all(col in df.columns for col in ['companyName', 'companyCode']):
                    messages.error(request, "CSV must contain companyName and companyCode columns")
                    return redirect('upload_csv')
                
                df = df[['companyName', 'companyCode']].dropna().drop_duplicates()
                company_records = df.to_dict(orient="records")
                
                request.session["company_data"] = company_records
                request.session.pop("employee_data", None)  # Clear employee data
                messages.success(request, f"{len(company_records)} company records validated")
                return redirect('upload_csv')

            # --- Upload Employee File ---
            elif "upload_employee" in request.POST and "employee_file" in request.FILES:
                if not valid_company_codes:
                    messages.error(request, "Please upload company data first")
                    return redirect('upload_csv')
                
                df = pd.read_csv(request.FILES["employee_file"])
                df.columns = df.columns.str.strip().str.lower()
                
                # Column mapping
                column_map = {
                    'name': 'Name',
                    'email': 'Email',
                    'usertype': 'Usertype',
                    'companycode': 'companyCode',
                    'empcode': 'EmpCode'
                }
                df.rename(columns=column_map, inplace=True)
                
                # Validation
                required_cols = ['Name', 'Email', 'Usertype', 'companyCode', 'EmpCode']
                if not all(col in df.columns for col in required_cols):
                    messages.error(request, f"CSV must contain: {', '.join(required_cols)}")
                    return redirect('upload_csv')
                
                df = df[required_cols].dropna().drop_duplicates()
                employee_records = df.to_dict(orient="records")
                
                # Company code validation
                invalid_employees = []
                valid_employees = []
                for emp in employee_records:
                    if emp['companyCode'] in valid_company_codes:
                        valid_employees.append(emp)
                    else:
                        invalid_employees.append(emp)
                
                if invalid_employees:
                    invalid_codes = {emp['companyCode'] for emp in invalid_employees}
                    messages.error(request, 
                        f"{len(invalid_employees)} records with invalid company codes: {', '.join(invalid_codes)}"
                    )
                    if valid_employees:
                        request.session["employee_data"] = valid_employees
                        messages.info(request, f"{len(valid_employees)} valid records retained")
                    return redirect('upload_csv')
                
                request.session["employee_data"] = employee_records
                messages.success(request, f"{len(employee_records)} employee records validated")
                return redirect('upload_csv')

            # --- Save Data ---
            elif "save_company" in request.POST and company_data:
                headers = {'Authorization': access_token}
                csv_buffer = StringIO()
                pd.DataFrame(company_data).to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                files = {'file': ('companies.csv', csv_buffer, 'text/csv')}
                response = requests.post(
                    f"{BASE_URL}fileUploadCompany",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    request.session.pop("company_data", None)
                    messages.success(request, "Company data saved successfully!")
                else:
                    messages.error(request, f"Error saving company data: {response.text}")
                return redirect('upload_csv')

            elif "save_employee" in request.POST and employee_data:
                headers = {'Authorization': access_token}
                csv_buffer = StringIO()
                pd.DataFrame(employee_data).to_csv(csv_buffer, index=False)
                csv_buffer.seek(0)
                
                files = {'file': ('employees.csv', csv_buffer, 'text/csv')}
                response = requests.post(
                    f"{BASE_URL}fileUploadEmployee",
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    request.session.pop("employee_data", None)
                    messages.success(request, "Employee data saved successfully!")
                else:
                    messages.error(request, f"Error saving employee data: {response.text}")
                return redirect('upload_csv')

        except Exception as e:
            messages.error(request, f"Processing error: {str(e)}")
            return redirect('upload_csv')

    return render(request, 'upload_csv.html', {
        'company_data': company_data,
        'employee_data': employee_data,
        'show_save_company': bool(company_data),
        'show_save_employee': bool(employee_data),
        'valid_company_codes': valid_company_codes
    })

def export_company(request):
    data = pd.DataFrame(columns=['companyName', 'companyCode'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="company_template.csv"'
    data.to_csv(response, index=False)
    return response

def export_employee(request):
    data = pd.DataFrame(columns=['Name', 'Email', 'Usertype', 'companyCode', 'EmpCode'])
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="employee_template.csv"'
    data.to_csv(response, index=False)
    return response


from urllib.parse import urlencode


def company_list(request):
    # Authentication check
    if 'access_token' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')

    headers = {
        "Authorization": request.session['access_token'],
        "Cookie": f"JSESSIONID={request.session.get('jsessionid', '')}"
    }

    try:
        response = requests.get(f"{BASE_URL}getCompanyList", headers=headers, timeout=10)
        response.raise_for_status()
        companies = response.json() if response.content else []
        
        for company in companies:
            status = company.get('companyStatus')
            company['status'] = 'DEACTIVE' if status is None else str(status).upper()
        
        return render(request, "company_list.html", {
            "companies": companies,
            "messages": messages.get_messages(request)
        })

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to fetch companies: {str(e)}")
        return render(request, "company_list.html", {"companies": []})

def employee_list(request):
    # Authentication check
    if 'access_token' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')

    headers = {
        "Authorization": request.session['access_token'],
        "Cookie": f"JSESSIONID={request.session.get('jsessionid', '')}"
    }

    try:
        response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers, timeout=10)
        response.raise_for_status()
        employees = response.json() if response.content else []
        
        for employee in employees:
            status = employee.get('empStatus')
            employee['status'] = 'DEACTIVE' if status is None else str(status).upper()
        
        return render(request, "employee_list.html", {
            "employees": employees,
            "messages": messages.get_messages(request)
        })

    except requests.exceptions.RequestException as e:
        messages.error(request, f"Failed to fetch employees: {str(e)}")
        return render(request, "employee_list.html", {"employees": []})

def update(request):
    # Authentication check
    if 'access_token' not in request.session:
        messages.error(request, 'Please login first')
        return redirect('login')

    # Prepare headers - exactly matching your Postman examples
    headers = {
        "Authorization": request.session['access_token'],
        "Content-Type": "application/json"
    }

    # Handle form display
    if request.method == 'GET' and not request.GET.get('is_submitted'):
        update_type = request.GET.get('type')
        if not update_type:
            messages.error(request, "Invalid request type")
            return redirect('dashboard')
        
        return render(request, "update_page.html", {
            'update_type': update_type,
            'code': request.GET.get('code'),
            'company_code': request.GET.get('company_code'),
            'status': request.GET.get('status', 'ACTIVE')
        })

    # Handle form submission - using PUT for both as per your Postman
    elif request.method == 'GET' and request.GET.get('is_submitted'):
        update_type = request.GET.get('update_type')
        status = request.GET.get('status', 'ACTIVE').upper()

        try:
            if update_type == 'company':
                # Company update (PUT with empty data as per Postman)
                params = {
                    'companyCode': request.GET.get('code'),
                    'status': status
                }
                url = f"{BASE_URL}updateCompanyStatus?{urlencode(params)}"
                response = requests.put(url, headers=headers, data='')
                redirect_page = 'company_list'
            else:
                # Employee update (PUT as per Postman)
                params = {
                    'empCode': request.GET.get('code'),
                    'companyCode': request.GET.get('company_code'),
                    'status': status
                }
                url = f"{BASE_URL}updateEmployeeStatus?{urlencode(params)}"
                response = requests.put(url, headers=headers)
                redirect_page = 'employee_list'

            # Debugging outputs
            print(f"Making PUT request to: {url}")
            print(f"Request headers: {headers}")
            print(f"Request params: {params}")
            print(f"Response status: {response.status_code}")
            print(f"Response content: {response.text}")

            response.raise_for_status()
            messages.success(request, f"Status updated to {status} successfully")
            return redirect(redirect_page)

        except requests.exceptions.RequestException as e:
            error_msg = f"Update failed: {str(e)}"
            if hasattr(e, 'response'):
                error_msg += f" (Status: {e.response.status_code})"
                print(f"Error response: {e.response.text}")
            messages.error(request, error_msg)
            return redirect(request.META.get('HTTP_REFERER', redirect_page))
        except Exception as e:
            messages.error(request, f"System error: {str(e)}")
            return redirect('dashboard')

        # def company_list(request):

#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     companies = []
#     try:
#         response = requests.get(f"{BASE_URL}getCompanyList", headers=headers, timeout=10)
#         response.raise_for_status()
#         companies = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch companies: {str(e)}")

#     return render(request, "company_list.html", {"companies": companies})


# def employee_list(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     employees = []
#     try:
#         response = requests.get(f"{BASE_URL}getEmployeeList", headers=headers, timeout=10)
#         response.raise_for_status()
#         employees = response.json()
#     except requests.exceptions.RequestException as e:
#         messages.error(request, f"Failed to fetch employees: {str(e)}")

#     return render(request, "employee_list.html", {"employees": employees})

# def update(request):
#     access_token = request.session.get('access_token')
#     if not access_token:
#         messages.error(request, 'Please login first')
#         return redirect('login')

#     headers = {
#         "Authorization": access_token,
#         "Content-Type": "application/json"
#     }

#     if request.method == 'GET':
#         # For GET requests, render the update page with prefilled data
#         update_type = request.GET.get('type')
#         context = {'update_type': update_type}
        
#         if update_type == 'company':
#             context.update({
#                 'companyCode': request.GET.get('companyCode'),
#                 'status': request.GET.get('status')
#             })
#         elif update_type == 'employee':
#             context.update({
#                 'empCode': request.GET.get('empCode'),
#                 'companyCode': request.GET.get('companyCode'),
#                 'status': request.GET.get('status')
#             })
        
#         return render(request, "update_page.html", context)

#     elif request.method == 'POST':
#         # Handle the update submission
#         update_type = request.POST.get('updateType')
#         status = request.POST.get('status')

#         try:
#             if update_type == 'company':
#                 company_code = request.POST.get('companyCode')
#                 response = requests.post(
#                     f"{BASE_URL}updateCompanyStatus?companyCode={company_code}&status={status}",
#                     headers=headers,
#                     data=''
#                 )
#                 redirect_page = 'company_list'
#             else:
#                 data = {
#                     "empCode": request.POST.get('empCode'),
#                     "companyCode": request.POST.get('companyCode'),
#                     "status": status
#                 }
#                 response = requests.post(
#                     f"{BASE_URL}updateEmployeeStatus",
#                     headers=headers,
#                     json=data
#                 )
#                 redirect_page = 'employee_list'

#             response.raise_for_status()
#             messages.success(request, "Status updated successfully")
#             return redirect(redirect_page)

#         except requests.exceptions.RequestException as e:
#             messages.error(request, f"Update failed: {str(e)}")
#             return redirect(request.META.get('HTTP_REFERER', redirect_page))


