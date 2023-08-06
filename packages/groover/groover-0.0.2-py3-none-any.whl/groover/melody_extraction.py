import numpy as np


def quantize_melody(notes, tick_resol=240):
    melody_notes = []
    for note in notes:
        # cut too long notes
        if note.end - note.start > tick_resol * 8:
            note.end = note.start + tick_resol * 4

        # quantize
        note.start = int(np.round(note.start / tick_resol) * tick_resol)
        note.end = int(np.round(note.end / tick_resol) * tick_resol)

        # append
        melody_notes.append(note)
    return melody_notes


def extract_melody(notes):
    # quanrize
    melody_notes = quantize_melody(notes)

    # sort by start, pitch from high to low
    melody_notes.sort(key=lambda x: (x.start, -x.pitch))

    # exclude notes < 60
    bins = []
    prev = None
    tmp_list = []
    for nidx in range(len(melody_notes)):
        note = melody_notes[nidx]
        if note.pitch >= 60:
            if note.start != prev:
                if tmp_list:
                    bins.append(tmp_list)
                tmp_list = [note]
            else:
                tmp_list.append(note)
            prev = note.start

            # preserve only highest one at each step
    notes_out = []
    for b in bins:
        notes_out.append(b[0])

    # avoid overlapping
    notes_out.sort(key=lambda x: x.start)
    for idx in range(len(notes_out) - 1):
        if notes_out[idx].end >= notes_out[idx + 1].start:
            notes_out[idx].end = notes_out[idx + 1].start

    # delete note having no duration
    notes_clean = []
    for note in notes_out:
        if note.start != note.end:
            notes_clean.append(note)

            # filtered by interval
    notes_final = [notes_clean[0]] if notes_clean != [] else []
    for i in range(1, len(notes_clean) - 1):
        if ((notes_clean[i].pitch - notes_clean[i - 1].pitch) <= -9) and \
                ((notes_clean[i].pitch - notes_clean[i + 1].pitch) <= -9):
            continue
        else:
            notes_final.append(notes_clean[i])
    notes_final += [notes_clean[-1]] if notes_clean != [] else []
    return notes_final


def extract_accompaniment(notes):
    melody = extract_melody(notes)
    note_set = set(notes)
    melody_set = set(melody)

    return list(note_set.difference(melody_set))
