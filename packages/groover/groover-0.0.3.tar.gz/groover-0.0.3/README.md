# groover 0.0.3

## Installation

`groover` is a beat-by-beat rhythm feature clustering and token generation tool for `.mid` files. You can download `groover` using pip:

```shell
pip install groover
```

To check if `groover` is successfully installed, type `python` in the terminal, and do the following:

```
>>> from groover import RhythmKMeans
>>> type(RhythmKMeans())
<class 'groover.classifier.RhythmKMeans'>
```

## Documentation

### data

#### `get_heat_maps(midi_obj, beat_resolution=480, rid_melody=False, min_pitch=0, max_pitch=127)`
Returns a numpy array of shape `(n, 24)`, where `n` is the number of beats in `midi_obj`. Each row is the rhythmic heat map of a beat, taking into consideration the notes' velocity and pitch.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to get heat maps from
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `rid_melody`: `bool`
     - whether to ignore melody notes when calculating rhythmic intensity
 - `min_pitch`: `int`
     - the minimum pitch of the note to be considered when calculating rhythmic intensity
 - `max_pitch`: `int`
     - the maximum pitch of the note to be considered when calculating rhythmic intensity
    
#### `get_dataset(midi_objs, beat_resolution=480, rid_melody=False, min_pitch=0, max_pitch=127)`
Returns a numpy array of shape `(n, 24)`, where `n` is the total number of beats of midi objects in `midi_objs`. Each row is the rhythmic heat map of a beat, taking into consideration the notes' velocity and pitch.
##### Parameters
 - `midi_obj`: `list`
     - the list containing midi objects to get heat maps from
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `rid_melody`: `bool`
     - whether to ignore melody notes when calculating rhythmic intensity
 - `min_pitch`: `int`
     - the minimum pitch of the note to be considered when calculating rhythmic intensity
 - `max_pitch`: `int`
     - the maximum pitch of the note to be considered when calculating rhythmic intensity
    
### RhythmKMeans
`RhythmKMeans` classifies rhythmic heat maps and use them to predict and evaluate rhythmic tokens.

#### `RhythmKMeans.__init__(self, cluster_centers=None)`
##### Parameters
 - `cluster_centers`: `numpy.ndarray`
     - the cluster centers in the shape of `(k, 24)`, where k is the number of clusters and each row is a cluster.

#### `RhythmKMeans.load_cluster_centers(self, cluster_centers)`
Loads `cluster_centers` as the classifier's cluster centers.
##### Parameters
 - `cluster_centers`: `numpy.ndarray`
     - the cluster centers in the shape of `(k, 24)`, where k is the number of clusters and each row is a cluster.

#### `RhythmKMeans.fit(self, dataset, k, max_iter=1000, epsilon=1e-6)`
Makes the classifier's cluster centers align with the dataset.
##### Parameters
 - `dataset`: `numpy.ndarray`
     - a numpy array of shape `(n, 24)`, where `n` is the total number of beats in the dataset, with each row being the rhythmic heat map of a beat
 - `k`: `int`
     - the number of clusters to be generated
 - `max_iter`: `int`
     - the maximum number of iterations to perform
 - `epsilon`: `float`
     - if the average distance of the cluster centers between iterations is lower than `epsilon`, clustering ends early

#### `RhythmKMeans.k(self)`
Returns the number of clusters of the classifier.

#### `RhythmKMeans.is_empty(self)`
Returns `True` if the classifier is not fitted to any data yet, `False` otherwise.

#### `RhythmKMeans.add_beat_clusters(self, midi_obj, beat_resolution=480, preprocessing='default', min_pitch=0, max_pitch=127)`
Adds markers with rhythm types to `midi_obj`.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to add beat-by-beat rhythm markers to
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `preprocessing`: `str`
     - can be either `'default'`, `'binary'`, or `'quantized'`, which will then change the rhythmic heat maps' values accordingly
 - `min_pitch`: `int`
     - the minimum pitch of the note to be considered when calculating rhythmic intensity
 - `max_pitch`: `int`
     - the maximum pitch of the note to be considered when calculating rhythmic intensity

#### `RhythmKMeans.get_rhythm_scores(self, midi_obj, beat_resolution=480, min_pitch=0, max_pitch=127)`
Returns a tuple of numpy arrays. The first is the rhythm types in shape `(n,)` that is specified by the markers in the midi object, and the second array is the alignment score between the notes and the rhythm type in shape `(n,)`. `n` is the number of beats in the midi object.
##### Parameters
 - `midi_obj`: `miditoolkit.midi.parser.MidiFile`
     - the midi object to be evaluated
 - `beat_resolution`: `int`
     - the number of ticks per beat
 - `preprocessing`: `str`
     - can be either `'default'`, `'binary'`, or `'quantized'`, which will then change the rhythmic heat maps' values accordingly
 - `min_pitch`: `int`
     - the minimum pitch of the note to be considered when calculating rhythmic intensity
 - `max_pitch`: `int`
     - the maximum pitch of the note to be considered when calculating rhythmic intensity
