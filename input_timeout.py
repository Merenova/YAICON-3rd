import msvcrt
import threading

class InputWithTimeout:
    def __init__(self):
        self.user_input = None
        self.timeout_flag = False

    def input_thread(self, prompt, timeout):
        print(prompt, end='', flush=True)
        timer = threading.Timer(timeout, self.timeout_handler)
        timer.start()
        try:
            self.user_input = input()
        except EOFError:
            pass  # Ignore EOFError (e.g., when user presses Ctrl+D)
        finally:
            timer.cancel()  # Cancel the timer if input is received before the timeout

    def timeout_handler(self):
        self.timeout_flag = True

    def input_with_timeout(self, prompt, timeout):
        input_thread = threading.Thread(target=self.input_thread, args=(prompt, timeout))
        input_thread.start()
        input_thread.join()

        if self.timeout_flag:
            return None
        else:
            return self.user_input