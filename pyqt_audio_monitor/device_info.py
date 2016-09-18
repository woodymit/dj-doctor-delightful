import pyaudio


def main():
    p = pyaudio.PyAudio()

    for device in range(p.get_device_count()):
        info = p.get_device_info_by_index(device)
        print info


main()
