from soco import SoCo
from soco import discover
import time

def get_sonos_speakers_ip_addresses():
    sonos_ip_addresses = []
    speakers = list(discover())
    for speaker in speakers:
        sonos_ip_addresses.append(speaker.ip_address)
        print(speaker.player_name + " " + speaker.ip_address + " is_coordinator " + str(speaker.is_coordinator))
    return sonos_ip_addresses

def play_song_on_sonos(sonos_ip_addresses, song_uri, volume):
    sonos = SoCo(sonos_ip_addresses[0])
    i = 1
    while i < len(sonos_ip_addresses):
        current_sonos_speaker = SoCo(sonos_ip_addresses[i])
        current_sonos_speaker.join(sonos)
        current_sonos_speaker.volume = volume
        i += 1
    sonos.volume = volume
    sonos.play_uri(song_uri)

def stop_song_on_sonos(sonos_ip_addresses):
    i = 0
    while i < len(sonos_ip_addresses):
        current_sonos_speaker = SoCo(sonos_ip_addresses[i])
        if current_sonos_speaker.is_coordinator:
            current_sonos_speaker.stop()
            break
        i += 1

def unjoin_sonos_speakers(sonos_ip_addresses):
    i = 0
    while i < len(sonos_ip_addresses):
        current_sonos_speaker = SoCo(sonos_ip_addresses[i])
        if current_sonos_speaker.is_coordinator is False:
            current_sonos_speaker.unjoin()
        i += 1

def run_sonos(volume):
    sonos_ip_addresses = get_sonos_speakers_ip_addresses()
    stop_song_on_sonos(sonos_ip_addresses=sonos_ip_addresses)
    play_song_on_sonos(sonos_ip_addresses=sonos_ip_addresses, song_uri='https://www.islamcan.com/audio/adhan/azan3.mp3', volume=volume)
    # play_song_on_sonos(sonos_ip_addresses, 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-17.mp3')
    time.sleep(300)
    print('-------------------------------------------------')
    unjoin_sonos_speakers(sonos_ip_addresses=sonos_ip_addresses)

# Example usage
if __name__ == '__main__':
    run_sonos(volume=60)
