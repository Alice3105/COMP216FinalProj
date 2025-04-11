import threading
import queue
import json
import time
import paho.mqtt.client as mqtt

class MQTTWorkerThread:
    """A worker thread that processes MQTT publishing tasks from a queue"""
    def __init__(self, thread_id, task_queue, client, topic):
        self.thread_id = thread_id
        self.task_queue = task_queue
        self.client = client
        self.topic = topic
        self.running = True
        
        # Create and start the worker thread
        self.thread = threading.Thread(
            target=self._worker_function,
            daemon=True
        )
        self.thread.start()
        print(f"Worker thread {thread_id} initialized")
    
    def _worker_function(self):
        """Internal worker function that processes tasks from the queue"""
        while self.running:
            try:
                # Get task from queue, with a timeout to periodically check if should exit
                task = self.task_queue.get(timeout=1.0)
                
                if task is None:  # None is a signal to exit
                    break
                    
                # Unpack task data
                data_point, payload_id = task
                
                # Create payload
                payload = {
                    'id': payload_id,
                    'location': data_point['location'],
                    'timestamp': time.asctime(),
                    'temperature_c': int(round(data_point['temperature_c'], 0)),
                    'thread': f"Thread-{self.thread_id}"
                }
                
                # Publish
                json_payload = json.dumps(payload)
                self.client.publish(self.topic, json_payload)
                print(f"Thread-{self.thread_id} published to {self.topic}: {json_payload}")
                time.sleep(5)  # Simulate processing time
                
                # Mark task as done
                self.task_queue.task_done()
                
            except queue.Empty:
                # Queue timeout - just continue the loop
                continue
            except Exception as e:
                print(f"Error in worker Thread-{self.thread_id}: {str(e)}")
    
    def stop(self):
        """Stop the worker thread"""
        self.running = False
        self.task_queue.put(None)  # Signal to exit
        if self.thread.is_alive():
            self.thread.join(timeout=0.5)

class MQTTThreadManager:
    """Manages a pool of MQTT worker threads"""
    def __init__(self, client, topic, num_workers=3):
        self.client = client
        self.topic = topic
        self.num_workers = num_workers
        self.workers = []
        self.task_queues = []
        
        # Initialize worker threads
        self._initialize_workers()
    
    def _initialize_workers(self):
        """Create worker threads and their task queues"""
        for i in range(self.num_workers):
            task_queue = queue.Queue()
            self.task_queues.append(task_queue)
            
            worker = MQTTWorkerThread(i, task_queue, self.client, self.topic)
            self.workers.append(worker)
    
    def publish_data(self, data_point, start_id):
        """Add a publishing task to each worker's queue"""
        for i in range(self.num_workers):
            # Send the data point and a unique ID to the worker
            self.task_queues[i].put((data_point, start_id + i))
    
    def stop_all(self):
        """Stop all worker threads"""
        for worker in self.workers:
            worker.stop() 