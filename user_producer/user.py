class User:
    def __init__(self, id, activated, activation_token, activation_token_expiration, birth_date, email, 
                 first_name, is_veteran, last_name, password, phone, points, email_option, phone_option, dark, email_order, email_delivery):
        self.id = id
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.birth_date = birth_date
        self.password = password
        self.phone = phone
        self.is_veteran = is_veteran
        self.points = points
        self.activated = activated
        self.activation_token = activation_token
        self.activation_token_expiration = activation_token_expiration
        self.email_option = email_option
        self.phone_option = phone_option
        self.dark = dark
        self.email_order = email_order
        self.email_delivery = email_delivery

    def toDict(self):
        return {'id': self.id, 'activated': self.activated, 'activation_token': self.activation_token, 'activation_token_expiration': self.activation_token_expiration,
                'birth_date': self.birth_date, 'email': self.email, 'first_name': self.first_name, 'is_veteran': self.is_veteran, 'last_name': self.last_name, 
                'password': self.password, 'phone': self.phone, 'points': self.points, 'email_option': self.email_option, 'phone_option': self.phone_option, 'dark': self.dark, 
                'email_order': self.email_order, 'email_delivery': self.email_delivery}
