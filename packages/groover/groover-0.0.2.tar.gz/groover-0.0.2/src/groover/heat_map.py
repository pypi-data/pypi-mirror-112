import numpy as np


def pitch_weight(pitch):
    return -pitch / 128 + 1


def velocity_weight(velocity):
    return velocity / 128


def notes_weight(notes):
    pitches = np.array([note.pitch for note in notes])
    velocities = np.array([note.velocity for note in notes])

    return pitch_weight(pitches) + velocity_weight(velocities)


def get_heat_map(notes, beat_resolution=480, min_pitch=0, max_pitch=127):
    bin_resolution = np.ceil(beat_resolution / 24).astype(int)
    notes = [note for note in notes if min_pitch <= note.pitch <= max_pitch]
    heat_map = np.zeros(24)
    weights = notes_weight(notes)
    for note, weight in zip(notes, weights):
        heat_map[(note.start % beat_resolution) // bin_resolution] += weight

    return heat_map
