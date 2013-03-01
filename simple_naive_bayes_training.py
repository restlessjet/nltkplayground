from nltk.probability import ELEProbDist, FreqDist
from nltk import NaiveBayesClassifier
from collections import defaultdict

train_samples = {
    'Aku benci kamu dan kamu adalah orang yang buruk': 'neg',
    'Aku mencintaimu dan Anda adalah orang yang baik': 'pos',
    'Saya gagal dalam segala sesuatu dan saya ingin membunuh orang': 'neg',
    'Saya menang di segala sesuatu dan saya ingin mengasihi orang-orang': 'pos',
    'menyedihkan adalah hal-hal yang heppening. fml': 'neg',
    'baik adalah hal-hal yang heppening. gbu ':'pos',
    'Saya sangat miskin':'neg',
    'Saya sangat kaya':'pos',
    'Aku benci kamu mommy! Anda adalah orang yang saya mengerikan':'neg',
    'I love you mommy! Anda adalah orang yang mengagumkan saya': 'pos',
    'Saya ingin membunuh kupu-kupu karena mereka membuat saya sedih ':'neg',
    'Saya ingin mengejar kupu-kupu karena mereka membuat saya bahagia ':'pos',
    'Saya ingin menyakiti kelinci ':'neg',
    'Saya ingin memeluk kelinci ':'pos',
    'Anda membuat saya mengerutkan kening ':'neg',
    'Anda membuat saya tersenyum ':'pos',
}

test_samples = [
   'Anda adalah orang yang mengerikan dan semua yang Anda lakukan adalah buruk',
   'Aku mencintai kalian semua dan Anda membuat saya bahagia',
   'Saya mengerutkan kening setiap kali saya melihat Anda dalam keadaan miskin pikiran',
   'Akhirnya menjadi kaya dari ide-ide saya. Mereka membuat saya tersenyum.',
   'Ibu saya adalah miskin',
   'Saya suka kupu-kupu. Yay untuk bahagia',
   'Semuanya gagal hari ini dan aku benci hal-hal',
]


def gen_bow(text):
    words = text.split()
    bow = {}
    for word in words:
        bow[word.lower()] = True
    return bow


def get_labeled_features(samples):
    word_freqs = {}
    for text, label in train_samples.items():
        tokens = text.split()
        for token in tokens:
            if token not in word_freqs:
                word_freqs[token] = {'pos': 0, 'neg': 0}
            word_freqs[token][label] += 1
    return word_freqs


def get_label_probdist(labeled_features):
    label_fd = FreqDist()
    for item,counts in labeled_features.items():
        for label in ['neg','pos']:
            if counts[label] > 0:
                label_fd.inc(label)
    label_probdist = ELEProbDist(label_fd)
    return label_probdist


def get_feature_probdist(labeled_features):
    feature_freqdist = defaultdict(FreqDist)
    feature_values = defaultdict(set)
    num_samples = len(train_samples) / 2
    for token, counts in labeled_features.items():
        for label in ['neg','pos']:
            feature_freqdist[label, token].inc(True, count=counts[label])
            feature_freqdist[label, token].inc(None, num_samples - counts[label])
            feature_values[token].add(None)
            feature_values[token].add(True)
    for item in feature_freqdist.items():
        print item[0],item[1]
    feature_probdist = {}
    for ((label, fname), freqdist) in feature_freqdist.items():
        probdist = ELEProbDist(freqdist, bins=len(feature_values[fname]))
        feature_probdist[label,fname] = probdist
    return feature_probdist


labeled_features = get_labeled_features(train_samples)

label_probdist = get_label_probdist(labeled_features)

feature_probdist = get_feature_probdist(labeled_features)

classifier = NaiveBayesClassifier(label_probdist, feature_probdist)

for sample in test_samples:
    print "%s | %s" % (sample, classifier.classify(gen_bow(sample)))

classifier.show_most_informative_features()
