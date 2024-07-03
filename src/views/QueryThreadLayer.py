import asyncio
from PyQt5.QtCore import QThread, pyqtSignal


class QueryLayerThread(QThread):
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str, str, str)

    def __init__(self, controller, **kwargs):
        super().__init__()
        self.controller = controller
        self.kwargs = kwargs

    def run(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.execute_query())

    async def execute_query(self):
        try:
            self.progress_signal.emit(10)
            json_path, excel_path = await self.controller.query_layer(self.kwargs)
            if not json_path and not excel_path:
                self.progress_signal.emit(100)
                self.result_signal.emit(None, None, "No updates")
            else:

                self.progress_signal.emit(100)
                self.result_signal.emit(json_path, excel_path, None)
        except Exception as e:
            self.progress_signal.emit(100)
            self.result_signal.emit(None, None, str(e))