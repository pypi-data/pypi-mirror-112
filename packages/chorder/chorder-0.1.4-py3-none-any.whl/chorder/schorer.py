from .timepoints import get_notes_by_beat, get_chords_by_beat
from .dechorder import Dechorder
import numpy as np


class Schorer:
    @staticmethod
    def get_regional_chord_score(notes, chord, start=0, end=1e7):
        if not chord.is_complete():
            return 10.
        root = chord.root_pc
        quality = chord.quality
        weights = Dechorder.chord_weights[quality]
        weights = weights[-root:] + weights[:-root]
        chord_map = Dechorder.get_chord_map(notes, start, end)

        return (np.nan_to_num(np.sum(np.array(weights) * np.array(chord_map)) / np.sum(chord_map)) + 5) / 15

    @staticmethod
    def get_chord_scores(midi_obj, split_char='_'):
        notes_by_beat = get_notes_by_beat(midi_obj)
        chord_by_beat = get_chords_by_beat(midi_obj, split_char)
        scores = []
        chords = []
        for i, (notes, chord) in enumerate(zip(notes_by_beat, chord_by_beat)):
            chords.append(chord)
            scores.append(
                Schorer.get_regional_chord_score(notes, chord, start=i * 480, end=(i + 1) * 480))

        return chords, np.array(scores)
