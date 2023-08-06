import numpy as np


def get_notes_by_period(notes, resolution):
    n_period = max([note.start for note in notes]) // resolution
    notes_by_period = [[] for _ in np.arange(n_period + 1)]
    for note in notes:
        notes_by_period[note.start // resolution].append(note)

    return notes_by_period


def get_rhythm_markers_by_beat(midi_obj, n_beats, resolution):
    markers_by_beat = [None for _ in range(n_beats)]
    for marker in midi_obj.markers:
        if marker.text.split(' ')[0] == 'rhythm':
            try:
                markers_by_beat[np.around(marker.time / resolution).astype(int)] = marker
            except IndexError:
                pass

    return markers_by_beat
