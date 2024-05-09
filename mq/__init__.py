import threading
import time
from sqlalchemy import text
from mq import belief_producer, belief_consumer
from modules.common.config import RESOURCE_TICK_SECONDS, MAX_FOOD, MAX_GOLD, MAX_MATERIALS, MAX_POPULATION
from orm import Session


def resource_update():
    "Обновить кол-во ресурсов"
    while True:
        print('[ Resource tick ]')
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


def run_daemons():
    consumer_thread = threading.Thread(target=belief_consumer.consume, daemon=True)
    producer_thread = threading.Thread(target=belief_producer.produce_queued_tasks, daemon=True)
    resource_update_thread = threading.Thread(target=resource_update, daemon=True)
    # TODO worker для очищения таблиц queue, где done=true

    consumer_thread.start()
    producer_thread.start()
    resource_update_thread.start()
