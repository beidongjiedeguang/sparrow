import pendulum


class Beijing:
    def __init__(self):
        self.timezones = pendulum.timezones

    @property
    def now(self):
        return pendulum.now("Asia/Shanghai").strftime('%m-%d %H:%M:%S')

