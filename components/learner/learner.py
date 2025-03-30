# Written by: Christopher Gholmieh
# Imports:

# Collections:
from collections import Counter

# SKLearn:
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score

# Typing:
from typing import Tuple, List

# Joblib:
from joblib import dump, load

# Loguru:
from loguru import logger

# Pandas:
from pandas import DataFrame, read_csv

# Numpy:
from numpy import ndarray, array


# Learner:
class Learner:
    """
    * Predicts whether a person is moving forwards, moving backwards, or idle.
        * Used to decide whether the writer should send a signal.
    """

    # Initialization:
    def __init__(self, learner_path: str, estimators: int = 100) -> None:
        # Constants:
        # Learner:
        self.learner_path: str = learner_path

        # Window:
        self.window_size: int = 3

        # Stride:
        self.stride: int = 1

        # State:
        self.state: int = 42

        # Variables (Assignment):
        # Learner:
        self.learner: RandomForestClassifier = RandomForestClassifier(
            # Estimators:
            n_estimators=estimators,

            # State:
            random_state=self.state,
        )

        # Encoder:
        self.encoder: LabelEncoder = LabelEncoder()

    # Methods:
    def create_sliding_windows(self, data: List[List[str]]) -> Tuple[ndarray, ndarray]:
        # Variables (Assignment):
        # Windows:
        windows: List[List[float]] = []

        # Labels:
        labels: List[str] = []

        # Logic:
        for iteration in range(0, len(data) - self.window_size + 1, self.stride):
            # Variables (Assignment):
            # Window:
            window: List[float] = list(map(float, data[iteration][:-1]))

            # Logic:
            for second_iteration in range(1, self.window_size):
                window.extend(map(float, data[iteration + second_iteration][:-1]))

            # Variables (Assignment):
            # Labels:
            window_labels: List[str] = [data[iteration + second_iteration][-1] for second_iteration in range(self.window_size)]

            # Majority:
            majority: str = Counter(window_labels).most_common(1)[0][0]

            # Logic:
            # Windows:
            windows.append(window)

            # Labels:
            labels.append(majority)

        # Logic:
        return array(windows), array(labels)

    # Predict:
    def predict(self, data: List[List[float]]) -> str:
        try:
            # Validation:
            if len(data) != self.window_size:
                raise ValueError("Inputted data must have exactly {} acceleration vectors!".format(
                    self.window_size
                ))

            # Variables (Assignment):
            # Window:
            window: ndarray = array(data).flatten().reshape(1, -1)

            # Prediction:
            prediction: ndarray = self.learner.predict(window)

            # Logic:
            return self.encoder.inverse_transform(prediction)[0]
        except Exception as exception:
            logger.error(f"[Error]: {exception}")

    # Train:
    def train(self, file: str) -> None:
        # Logic:
        try:
            # Variables (Assignment):
            # Data:
            data: DataFrame = read_csv(file)

            # List:
            data_list: List[List[str]] = data.values.tolist()

            # Arrays:
            window_array, label_array = self.create_sliding_windows(data_list)

            # Labels:
            encoded_labels: ndarray = self.encoder.fit_transform(label_array)

            # Variables (Declaration):
            # Window:
            window_train: ndarray
            window_test: ndarray

            # Labels:
            label_train: ndarray
            label_test: ndarray

            # Variables (Definition):
            # Windows & Labels:
            window_train, window_test, label_train, label_test = train_test_split(
                window_array, encoded_labels, random_state=self.state, test_size=0.2
            )

            # Logic:
            self.learner.fit(window_train, label_train)

            # Variables (Assignment):
            # Prediction:
            label_prediction: ndarray = self.learner.predict(window_test)

            # Accuracy:
            accuracy: float = accuracy_score(label_test, label_prediction)

            # Logging:
            logger.info("Learner accuracy: {:3f}".format(accuracy))

            # Logic:
            if input("[?] Would you like to save this potential learner? [y/N]: ").strip().lower() in "yes":
                # Logic:
                self.save()
            else:
                # Logging:
                logger.info("[*] Learner not saved..")

        # Exceptions:
        except FileNotFoundError as exception:
            logger.error("[!] Data file {} not found. Please recheck file path.".format(file))
        except Exception as exception:
            logger.error("[!] An error occured during training: {}".format(exception))
    
    # Load:
    def load(self) -> None:
        # Logic:
        try:
            # Variables (Assignment):
            # Learner:
            self.learner: RandomForestClassifier = load(
                self.learner_path
            )

            # Encoder:
            self.encoder: LabelEncoder = load(
                self.learner_path.replace(".pkl", "-encoder.pkl")
            )

            # Logging:
            logger.info("[*] Learner loaded successfully from {}".format(self.learner_path))
        except FileNotFoundError:
            # Logging:
            logger.error("[!] Learner file {} was not found.".format(
                self.learner_path
            ))

    # Save:
    def save(self) -> None:
        # Logic:
        try:
            # Learner:
            dump(self.learner, self.learner_path)
            
            # Encoder:
            dump(self.encoder, self.learner_path.replace(".pkl", "-encoder.pkl"))

            # Logging:
            logger.info("[*] Learner saved successfully to {}".format(self.learner_path))
        except Exception as exception:
            # Logging:
            logger.error("[!] Unable to save learner to {} | {}".format(
                self.learner_path, exception
            ))
