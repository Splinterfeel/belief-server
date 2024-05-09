import pika
import time
from sqlalchemy import bindparam, text
import datetime
from mq import schemas
from orm import Session
from modules.common.config import QUEUE_SEND_MINSECONDS, QUEUE_TICK_SECONDS

MILLISECONDS = 1000


connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.exchange_declare('belief_ex', 'x-delayed-message', durable=True, arguments={'x-delayed-type': 'direct'})
channel.queue_declare(queue='belief', durable=True)


def apply_delay_to_tasks(tasks: list[schemas.QueuedTask]) -> list[schemas.QueuedTask]:
    for task in tasks:
        now = datetime.datetime.now()
        if task.scheduled_at <= now:
            task.delay = 0
        else:
            task.delay = task.scheduled_at - now
    return tasks


def send_tasks_to_mq(tasks: list[schemas.QueuedTask]) -> None:
    "Отправить задачи в очередь для исполнения"
    for task in tasks:
        channel.basic_publish(
            'belief_ex', routing_key='belief', body=task.model_dump_json(),
            properties=pika.BasicProperties(headers={"x-delay":  task.delay * MILLISECONDS}))
    print(f'[*] Producer sent {len(tasks)} tasks into queue for executing')


def produce_queued_tasks() -> None:
    "Главный метод вычитывания разных задач для отправки в очередь"
    print(' [*] Producer waiting for tasks.')
    while True:
        all_tasks = []
        with Session() as session:
            all_tasks.extend(get_building_tasks(session))
            if all_tasks:
                all_tasks = apply_delay_to_tasks(all_tasks)
                send_tasks_to_mq(all_tasks)
            session.commit()
        time.sleep(QUEUE_TICK_SECONDS)


def get_building_tasks(session) -> list[schemas.QueuedTask]:
    "Метод вычитывания задач по зданиям для отправки в очередь"
    tasks_raw = session.execute(text(
        '''SELECT * FROM queued.building
        WHERE not done and not queued
        and current_timestamp AT TIME ZONE '-03:00' >= scheduled_at - interval ':MINSECONDS sec'
        ORDER BY scheduled_at '''
    ), {'MINSECONDS': QUEUE_SEND_MINSECONDS}).mappings().all()
    if not tasks_raw:
        return []
    tasks = [schemas.BuildingTaskDTO.model_validate(
        dict(task) | {'table': schemas.TaskTable.BUILDING, 'task_type': schemas.TaskType.BUILD_A_BUILDING},
        from_attributes=True,
        ) for task in tasks_raw]
    for task in tasks:
        task.task_type = schemas.TaskType.BUILD_A_BUILDING
    # отметить id-шники задач как отправленные в очередь
    params = {'ids': [t['id'] for t in tasks_raw]}
    t = text('UPDATE queued.building SET queued = true WHERE id IN :ids')
    t = t.bindparams(bindparam('ids', expanding=True))
    session.execute(t, params)
    return tasks
