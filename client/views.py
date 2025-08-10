import os
import json
import pickle
from django.http import JsonResponse
from django.views import View

class GetTokenView(View):
    def get(self, request, email):
        file_path = os.path.join('token_files', f'{email}.pickle')

        if os.path.exists(file_path):
            with open(file_path, 'rb') as f:
                credentials = pickle.load(f)

            json_credentials = {
                "type": "authorized_user",
                "client_id": credentials.client_id,
                "client_secret": credentials.client_secret,
                "refresh_token": credentials.refresh_token,
                "token_uri": credentials.token_uri,
            }

            success_response = {
                'status': 'success',
                'token': json.dumps(json_credentials)
            }
            return JsonResponse(success_response)

        return JsonResponse({
            'status': 'failed',
            'message': f"{email} token not found"
        })
