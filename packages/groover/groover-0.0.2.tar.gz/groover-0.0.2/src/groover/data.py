from .heat_map import get_heat_map
from .melody_extraction import extract_accompaniment
from .timepoints import get_notes_by_period
import numpy as np


def get_heat_maps(midi_obj, beat_resolution=480, rid_melody=False, min_pitch=0, max_pitch=127):
    notes = []
    for instrument in midi_obj.instruments:
        if not instrument.is_drum:
            notes += instrument.notes
    if rid_melody:
        notes = extract_accompaniment(notes)
    notes_by_beats = get_notes_by_period(notes, resolution=beat_resolution)

    return np.stack([get_heat_map(note_set, beat_resolution=beat_resolution, min_pitch=min_pitch, max_pitch=max_pitch)
                     for note_set in notes_by_beats])


def get_dataset(midi_objs, beat_resolution=480, rid_melody=False, min_pitch=0, max_pitch=127):
    dataset = np.zeros((0, 24))
    for midi_obj in midi_objs:
        heat_maps = get_heat_maps(
            midi_obj=midi_obj,
            beat_resolution=beat_resolution,
            rid_melody=rid_melody,
            min_pitch=min_pitch,
            max_pitch=max_pitch)
        dataset = np.concatenate((dataset, heat_maps))

    return dataset
