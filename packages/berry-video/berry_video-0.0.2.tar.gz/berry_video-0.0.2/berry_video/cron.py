import logging
import getpass


from crontab import CronTab


logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def auto_start():
    cron = CronTab(user=getpass.getuser())
    for job in cron:
        if job.comment =="start":
            logger.info("Cron de start ja criada")
            return
    
    job = cron.new(command="berry start", comment="start")
    job.every_reboot()
    job.enable()
    cron.write()
    logger.info("Cron de start criada")

def set_update(minutes):
    cron = CronTab(user=getpass.getuser())
    for job in cron:
        if job.comment =="update":
            job.minute.every(minutes)
            job.enable()
            cron.write()
            logger.info("Cron de update atualizada")
            return
    
    job = cron.new(command="berry update", comment="update")
    job.minute.every(minutes)
    job.enable()
    cron.write()
    logger.info("Cron de update criada")
