"Main query thread"
import datetime
import pika
from modules.stronghold import buildings
from mq import schemas

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()


def read_queued_tasks(ch, method, properties, body):
    task_model = schemas.QueuedTask.model_validate_json(body)
    print(f" [x] Received {task_model.task_type}", datetime.datetime.now())
    match task_model.task_type:
        case schemas.TaskType.BUILD_A_BUILDING:
            buildings.build(schemas.BuildingTaskDTO.model_validate_json(body))
        case _:
            msg = f'unknown task type! {task_model.task_type}'
            raise ValueError(msg)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def consume():
    channel.exchange_declare('belief_ex', 'x-delayed-message', durable=True, arguments={'x-delayed-type': 'direct'})
    channel.queue_declare(queue='belief', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='belief', on_message_callback=read_queued_tasks)
    print(' [*] Consumer waiting for messages.')
    channel.start_consuming()
