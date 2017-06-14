class Channel:
    def __init__(self, channel):
        self.__channel = channel

    def data(self):
        import spidev
        spi = spidev.SpiDev()
        spi.open(0, 0)
        adc = spi.xfer2([1, (8 + self.__channel) << 4, 0])
        data = ((adc[1] & 3) << 8) | adc[2]
        spi.close()
        return data