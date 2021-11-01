class Order:
    def __init__(self, id, active, address, delivery, driver_note, delivery_slot, driver_accept, driver_complete, order_complete,
                 placed, restaurant_accept, restaurant_complete, restaurant_start, delivery_price, food_price,
                 tip, refunded, restaurant_note, driver_user_id, user_id, confirmation_code, payment_confirmed):
        self.id = id
        self.active = active
        self.address = address
        self.delivery = delivery
        self.driver_note = driver_note
        self.delivery_slot = delivery_slot
        self.driver_accept = driver_accept
        self.driver_complete = driver_complete
        self.order_complete = order_complete
        self.placed = placed
        self.restaurant_accept = restaurant_accept
        self.restaurant_complete = restaurant_complete
        self.restaurant_start = restaurant_start
        self.delivery_price = delivery_price
        self.food_price = food_price
        self.tip = tip
        self.refunded = refunded
        self.restaurant_note = restaurant_note
        self.driver_user_id = driver_user_id
        self.user_id = user_id
        self.confirmation_code = confirmation_code
        self.payment_confirmed = payment_confirmed

    def toDict(self):
        return {
            'id': self.id,
            'active': self.active,
            'address': self.address,
            'delivery': self.delivery,
            'driver_note': self.driver_note,
            'delivery_slot': self.delivery_slot,
            'driver_accept': self.driver_accept,
            'driver_complete': self.driver_complete,
            'order_complete': self.order_complete,
            'placed': self.placed,
            'restaurant_accept': self.restaurant_accept,
            'restaurant_complete': self.restaurant_complete,
            'restaurant_start': self.restaurant_start,
            'delivery_price': self.delivery_price,
            'food_price': self.food_price,
            'tip': self.tip,
            'refunded': self.refunded,
            'restaurant_note': self.restaurant_note,
            'driver_user_id': self.driver_user_id,
            'user_id': self.user_id,
            'confirmation_code': self.confirmation_code,
            'payment_confirmed': self.payment_confirmed,
        }
