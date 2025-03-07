""" from django_cron import CronJobBase, CronJobManager

class MyCronJob(CronJobBase):
    RUN_EVERY_MINS = 10  # Ejecuta cada 10 minutos

    def do(self):
        # Aquí puedes agregar la lógica para actualizar estados y enviar notificaciones
        print("Tarea cron ejecutada") """