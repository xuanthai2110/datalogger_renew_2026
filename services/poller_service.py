from drivers.example_driver import ExampleDriver

class PollerService:
    def __init__(self, buffer_service):
        self.driver = ExampleDriver()
        self.buffer = buffer_service

    def poll(self):
        data = self.driver.read_data()
        self.buffer.save(data)