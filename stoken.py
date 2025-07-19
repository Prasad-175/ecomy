from itsdangerous import URLSafeSerializer
secret_key='code@2018'
salt='otpverify'
def entoken(data):
    serializer=URLSafeSerializer(secret_key)
    return serializer.dumps(data,salt)
def dtoken(data):
    serializer=URLSafeSerializer(secret_key)
    return serializer.loads(data,salt=salt)