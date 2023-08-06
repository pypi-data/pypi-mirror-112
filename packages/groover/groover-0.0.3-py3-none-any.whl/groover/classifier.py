import numpy as np
from miditoolkit.midi import containers
from .data import get_heat_maps
from .metrics import rhythm_similarity
from .timepoints import get_rhythm_markers_by_beat


class RhythmKMeans:
    def __init__(self, cluster_centers=None):
        if cluster_centers is None:
            self.cluster_centers_ = np.zeros((0, 24))
        else:
            if type(cluster_centers) != np.ndarray:
                raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
            elif len(cluster_centers.shape) != 2:
                raise AssertionError("K-means cluster centers has to be a 2D array")
            elif cluster_centers.shape[1] != 24:
                raise AssertionError("K-means cluster centers has to have 24 columns")
            self.cluster_centers_ = cluster_centers.copy()

    def fit(self, dataset, k, max_iter=1000, epsilon=1e-6):
        N, n_features = dataset.shape
        if n_features != 24:
            raise AssertionError("dataset has to have 24 columns")
        elif N < k:
            raise AssertionError("")
        init_indices = np.random.choice(N, size=k, replace=False)
        cluster_centers = dataset[init_indices]
        for i in range(max_iter):
            new_centers = cluster_centers.copy()
            n_points = np.ones((k, 1))

            for data in dataset:
                cluster = np.argmax(rhythm_similarity(data, cluster_centers))
                new_centers[cluster] += data
                n_points[cluster, 0] += 1

            new_centers = new_centers / n_points

            if np.mean(rhythm_similarity(new_centers, cluster_centers)) > 1 - epsilon:
                self.cluster_centers_ = new_centers
                return
            else:
                cluster_centers = new_centers

        self.cluster_centers_ = cluster_centers
        return

    def load_cluster_centers(self, cluster_centers):
        if type(cluster_centers) != np.ndarray:
            raise TypeError("K-means cluster centers has to be in the form of numpy.ndarray")
        elif len(cluster_centers.shape) != 2:
            raise AssertionError("K-means cluster centers has to be a 2D array")
        elif cluster_centers.shape[1] != 24:
            raise AssertionError("K-means cluster centers has to have 24 columns")
        self.cluster_centers_ = cluster_centers.copy()

    def k(self):
        return self.cluster_centers_.shape[0]

    def is_empty(self):
        return self.k() == 0

    def add_beat_clusters(self, midi_obj, beat_resolution=480, preprocessing='default', min_pitch=0, max_pitch=127):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, min_pitch=min_pitch, max_pitch=max_pitch)
        if preprocessing == 'binary':
            heat_maps = np.clip(np.ceil(heat_maps), 0., 1.)
        elif preprocessing == 'quantized':
            bins = [0, 0.5, 1.5, 2.5, 4, 5.5, 6.5, 8.5, 11]
            for i, l, r in zip(range(len(bins)), bins[:-1], bins[1:]):
                heat_maps[(heat_maps >= l) & (heat_maps < r)] = i

        for beat, heat_map in enumerate(heat_maps):
            rhythm_type = np.argmax(rhythm_similarity(heat_map, self.cluster_centers_))
            marker = containers.Marker(text=f'{preprocessing} rhythm {int(rhythm_type)}',
                                       time=beat * beat_resolution)
            midi_obj.markers.append(marker)

    def get_rhythm_scores(self, midi_obj, beat_resolution=480, min_pitch=0, max_pitch=127):
        if self.is_empty():
            raise AssertionError('K-means classifier is empty. Use fit() to generate cluster centers')

        heat_maps = get_heat_maps(midi_obj, beat_resolution=beat_resolution, min_pitch=min_pitch, max_pitch=max_pitch)
        types = np.zeros(heat_maps.shape[0])
        centers_by_beats = np.zeros((heat_maps.shape[0], 24))

        rhythm_markers_by_beat = get_rhythm_markers_by_beat(midi_obj, heat_maps.shape[0], resolution=beat_resolution)
        for i, marker in enumerate(rhythm_markers_by_beat):
            if marker is None:
                continue
            rhythm_type = int(marker.text.split(' ')[1])
            types[i] = rhythm_type
            try:
                centers_by_beats[i] = self.cluster_centers_[rhythm_type]
            except IndexError:
                pass

        return types.astype(int), rhythm_similarity(heat_maps, centers_by_beats)
