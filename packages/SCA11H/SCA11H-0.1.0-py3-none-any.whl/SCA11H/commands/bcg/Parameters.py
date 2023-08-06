from SCA11H import get_argument_name


class Parameters:
    def __init__(self, signal_high: int, signal_low: int, min_amplitude: int, tentative_stroke_vol: int,
                 typ_amplitude: int, scale: int):
        def check(val, low, high):
            if val < low or val > high:
                raise Exception('%s=%s is out of range [%s, %s]' % (get_argument_name(val), val, low, high))

        check(signal_high, 1000, 30000)
        check(signal_low, 100, 10000)
        check(min_amplitude, 500, 20000)
        check(tentative_stroke_vol, 0, 20000)
        check(typ_amplitude, 100, 10000)
        check(scale, 2, 15)

        self.signal_high = signal_high
        self.signal_low = signal_low
        self.min_amplitude = min_amplitude
        self.tentative_stroke_vol = tentative_stroke_vol
        self.typ_amplitude = typ_amplitude
        self.scale = scale

    @staticmethod
    def from_string(text: str):
        pars = [int(x.strip()) for x in text.split(',')]
        if len(pars) != 6:
            raise Exception('Unexpected parameters string: "%s"' % text)

        return Parameters(*pars)

    def to_payload(self):
        return ','.join(str(x) for x in
                        [self.signal_high, self.signal_low, self.min_amplitude, self.tentative_stroke_vol,
                         self.typ_amplitude, self.scale])

    def as_list(self):
        return [
            'Signal high:          %d' % self.signal_high,
            'Signal low:           %d' % self.signal_low,
            'Min amplitude:        %d' % self.min_amplitude,
            'Tentative stroke vol: %d' % self.tentative_stroke_vol,
            'Typ amplitude:        %d' % self.typ_amplitude,
            'Scale:                %d' % self.scale,
        ]

    def __str__(self):
        return '\n'.join(self.as_list())
