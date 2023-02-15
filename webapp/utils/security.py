from itsdangerous import URLSafeTimedSerializer


class Ts:
    __timedser__ = None

    def settser(self,secret_key):
        self.timedser = URLSafeTimedSerializer(secret_key)

    def gettser(self):
        return self.timedser


ts = Ts()