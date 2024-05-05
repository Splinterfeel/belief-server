import pika
import time
import threading
from sqlalchemy import text
from orm import Session
from modules.common.config import RESOURCE_TICK_SECONDS, MAX_FOOD, MAX_GOLD, MAX_MATERIALS, MAX_POPULATION


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='belief', durable=True)


def produce_test_message():
    channel.basic_publish(
        exchange='', routing_key='belief', body='Test_message')
    print(" [x] Sent test message")


def resource_update():
    # обновить кол-во ресурсов
    while True:
        print('[ Lifecycle tick ]')
        with Session() as session:
            session.execute(text(
                '''UPDATE common.resource SET
                food = (CASE WHEN resource.food + g.food < :MAX_FOOD
                        THEN resource.food + g.food ELSE :MAX_FOOD END),
                gold = (CASE WHEN resource.gold + g.gold < :MAX_GOLD
                        THEN resource.gold + g.gold ELSE :MAX_GOLD END),
                materials = (CASE WHEN resource.materials + g.materials < :MAX_MATERIALS
                            THEN resource.materials + g.materials ELSE :MAX_MATERIALS END),
                population = (CASE WHEN resource.population + g.population < :MAX_POPULATION
                            THEN resource.population + g.population ELSE :MAX_POPULATION END)
                FROM common.resource_gain g
                WHERE common.resource.user_id = g.user_id;'''),
                {'MAX_FOOD': MAX_FOOD, 'MAX_GOLD': MAX_GOLD,
                 'MAX_MATERIALS': MAX_MATERIALS, 'MAX_POPULATION': MAX_POPULATION})
            session.commit()
        time.sleep(RESOURCE_TICK_SECONDS)  # 3600 default


def run():
    resource_update_thread = threading.Thread(target=resource_update, daemon=True)
    resource_update_thread.start()
