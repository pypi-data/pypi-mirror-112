
class VentureCodeSuffix:
    def __init__(self, venture_code) -> None:
        self.venture_code = venture_code

    def __call__(self, *args, **kwds) -> str:
        return f'__{self.venture_code}'


class DailyActionLogSuffix:
    def __init__(self, venture_code) -> None:
        self.venture_code = venture_code

    def __call__(self, re_replace=None, *args, **kwds) -> str:
        if re_replace is None or (date := re_replace.get(R'\$\(date\)')) is None:
            return f'__{self.venture_code}'
        return f'__{date}__{self.venture_code}'
