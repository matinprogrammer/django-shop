from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI("3736774F4D61735A6A65716F79586342363774575239776145327A45566A716E4D693436365452594C6E6B3D")
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'your code is {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)
