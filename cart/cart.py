from item.models import Item
from authentication.models import Profile


class Cart:
    def __init__(self, request):
        self.request = request
        self.session = request.session

        # Load existing cart or initialize
        cart = self.session.get('session_key')
        if not cart:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, quantity):
        product_id = str(product.id)  # ✅ FIXED
        try:
            quantity = int(quantity)
        except ValueError:
            raise ValueError(f"Invalid quantity: {quantity}")

        if product_id in self.cart:
            self.cart[product_id] += quantity
        else:
            self.cart[product_id] = quantity

        self.session.modified = True
        self._sync_profile()

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
            self._sync_profile()

    def update(self, product, quantity):
        product_id = str(product.id)
        quantity = int(quantity)

        if product_id in self.cart:
            self.cart[product_id] = quantity
            self.session.modified = True
            self._sync_profile()

        return self.cart

    def delete(self, product_id):
        product_id = str(product_id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.session.modified = True
            self._sync_profile()

        return self.cart

    def clear(self):
        self.cart.clear()
        self.session.modified = True
        self._sync_profile(clear=True)

    def __len__(self):
        return len(self.cart)

    def get_products(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)

        for product in products:
            product.quantity = self.cart.get(str(product.id), 0)

        return products

    def get_total_price(self):
        product_ids = self.cart.keys()
        products = Item.objects.filter(id__in=product_ids)

        total = 0
        for product in products:
            qty = self.cart.get(str(product.id), 0)
            price = product.sale_price if product.is_sale else product.price
            total += price * qty  # ✅ FIXED: was prematurely returned

        return total

    def _sync_profile(self, clear=False):
        """Sync cart with user profile if authenticated."""
        if self.request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=self.request.user)
                profile.cart = {} if clear else self.cart
                profile.save()
            except Profile.DoesNotExist:
                pass
