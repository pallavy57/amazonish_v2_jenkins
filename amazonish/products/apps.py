from django.apps import AppConfig
from django.views.decorators.csrf import csrf_exempt
from apscheduler.schedulers.background import BackgroundScheduler







class ProductsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'products'

    def ready(self):
        from tasks.views import ProductsCron
        from tasks.publisher import RetryingEmailSentsPublisher
        from tasks.subscriber import RetryingEmailSentsConsumer
        
        scheduler = BackgroundScheduler()
        scheduler.add_job(lambda: csrf_exempt(
            ProductsCron(None).runCron(0)), 'interval', minutes=0.2)
        scheduler.add_job(lambda: csrf_exempt(
            RetryingEmailSentsPublisher().publishMessage()), 'interval', minutes=0.3)
        scheduler.add_job(lambda: csrf_exempt(
            RetryingEmailSentsConsumer().consumer_e()), 'interval', minutes=0.5)
        
        scheduler.start()
       
