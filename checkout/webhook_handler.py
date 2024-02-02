from django.http import HttpResponse


class StripeWH_Handler:
    """
    Handler for Stripe webhooks
    """

    def __init__(self, request):
        self.request = request
    
    def handle_event(self, event):
        """
        Handles a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Unhandled webhook received: {event['type']}',
            status=200
        )
    
    def handle_payment_intent_succeeded(self, event):
        """
        Handles the payment_intent.succeeded webhook
        """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Webhook received: {event['type']}',
            status=200
        )
    
    def handle_payment_intent_payment_failed(self, event):
        """
        Handles the payment_intent.payment_failed webhook
        """
        return HttpResponse(
            content=f'Webhook received: {event['type']}',
            status=200
        )