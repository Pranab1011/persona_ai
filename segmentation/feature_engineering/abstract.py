from abc import ABC, abstractmethod
import pandas as pd


class BaseFeatureEngineer(ABC):
    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def transform(self) -> pd.DataFrame:
        pass

    @abstractmethod
    def get_feature_names(self) -> list:
        pass

    def fit_transform(self):
        pass
