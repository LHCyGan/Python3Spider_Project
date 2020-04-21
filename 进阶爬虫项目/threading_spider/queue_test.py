from queue import Queue
import queue

if __name__ == "__main__":
    message_queue = Queue(maxsize=2)

    message_queue.put("bobby")
    message_queue.put("bobby2")
    message = message_queue.get()
    print(message)

    message = message_queue.get()
    print(message)
