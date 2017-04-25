import csv
import os
import pickle
from io import StringIO

from sklearn.metrics import roc_auc_score as AUC

from scoring.abstract import AbstractScoring

cur_dir_path = os.path.dirname(os.path.realpath(__file__))


class AppthisAUCScoring(AbstractScoring):
    @property
    def higher_better(self):
        return True

    def validate(self, submission_text: str):
        tmp_file = StringIO(submission_text)
        reader = csv.DictReader(tmp_file)

        if set(reader.fieldnames) != set(['event_id', 'conversion_probability']):
            tmp_file.close()
            return False, (
                "The headers of your CSV file are {}. They must be 'event_id' and "
                "'conversion_probability'.".format(reader.fieldnames)
            )

        return True, None

    def score(self, submission_text: str):
        public_preds, private_preds, public_actuals, private_actuals = [1, 0], [1, 0], [1, 0], [1, 0]
        tmp_file = StringIO(submission_text)
        csv_reader = csv.DictReader(tmp_file)
        public_event_ids_pkl_name = '{}/public_validation_event_ids.pkl'.format(cur_dir_path)

        with open(public_event_ids_pkl_name, 'rb') as public_validation_event_ids_file:
            public_validation_event_ids = pickle.load(public_validation_event_ids_file)

        for row in csv_reader:
            if row['event_id'] in public_validation_event_ids:
                public_preds.append(float(row['conversion_probability']))
            else:
                private_preds.append(float(row['conversion_probability']))

        with open('{}/all_validation_labels.txt'.format(cur_dir_path), 'r') as all_validation_labels_file:
            for line in all_validation_labels_file:
                event_id, event_label = line.rstrip().split(' ')
                if event_id in public_validation_event_ids:
                    public_actuals.append(float(event_label))
                else:
                    private_actuals.append(float(event_label))

            public_score = AUC(public_actuals, public_preds)
            private_score = AUC(private_actuals, private_preds)

        return public_score, private_score, None
