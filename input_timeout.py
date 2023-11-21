import signal

def input_with_timeout(prompt, timeout):
    print(prompt, end='', flush=True)

    # 시그널 핸들러 설정
    def timeout_handler(signum, frame):
        raise TimeoutError

    signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(timeout)  # 타임아웃 시간 설정

    try:
        user_input = input()
        signal.alarm(0)  # 타임아웃 시간 해제
        return user_input
    except TimeoutError:
        return None