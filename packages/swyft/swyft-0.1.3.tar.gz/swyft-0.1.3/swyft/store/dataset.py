import logging

import numpy as np
import torch
from torch.utils.data import Dataset as torch_Dataset

import swyft

log = logging.getLogger(__name__)


class Dataset(torch_Dataset):
    """Dataset for access to swyft.Store."""

    def __init__(self, N, prior, store, bound=None, simhook=None, simkeys = None):
        """Initialize Dataset.

        Args:
            N (int): Number of samples.
            prior (swyft.Prior): Parameter prior.
            store (swyft.Store): Store reference.
            simhook (Callable): Posthook for simulations. Applied on-the-fly to each point.
            simkeys (list of strings): List of simulation keys that should be exposed 
                                        (None means that all store sims are exposed).

        Notes:
            Due to the statistical nature of the Store, the returned number of
            samples is effectively drawn from a Poisson distribution with mean
            N.
        """
        super().__init__()

        # Initialization
        self._trunc_prior = swyft.TruncatedPrior(prior, bound)
        self._indices = store.sample(N, prior, bound=bound)

        self._store = store
        self._simhook = simhook
        self._simkeys = simkeys if simkeys else list(self._store.sims)

    def __len__(self):
        return len(self._indices)

    @property
    def prior(self):
        return self._trunc_prior.prior

    @property
    def bound(self):
        return self._trunc_prior.bound

    def _tensorfy(self, x):
        return {k: torch.tensor(v).float() for k, v in x.items()}

    @property
    def indices(self):
        return self._indices

    def _no_store(self):
        if self._store is None:
            print("WARNING: No store defined.")
            return True
        else:
            return False

    def simulate(self, batch_size=None, wait_for_results=True):
        """Trigger simulations for points in the dataset."""
        if self._no_store():
            return
        self._store.simulate(
            self.indices, batch_size=batch_size, wait_for_results=wait_for_results
        )

    def set_store(self, store):
        self._store = store

    @property
    def requires_sim(self):
        """Check if simulations are required for points in the dataset."""
        if self._no_store():
            return
        return self._store.requires_sim(self.indices)

    @property
    def pars(self):
        """Return all parameters as npoints x zdim array."""
        if self._no_store():
            return
        return np.array([self._store.pars[i] for i in self._indices])

    def __getitem__(self, idx):
        if self._no_store():
            return
        i = self._indices[idx]
        x_keys = self._simkeys
        x = {k: self._store.sims[k][i] for k in x_keys}
        z = self._store.pars[i]
        u = self._trunc_prior.prior.u(z.reshape(1, -1)).flatten()

        if self._simhook is not None:
            x = self._simhook(x, z)

        return (self._tensorfy(x), torch.tensor(u).float())

    def state_dict(self):
        return dict(
            indices=self._indices,
            trunc_prior=self._trunc_prior.state_dict(),
            simhook=bool(self._simhook),
            simkeys=self._simkeys
        )

    @classmethod
    def from_state_dict(cls, state_dict, store, simhook=None):
        obj = Dataset.__new__(Dataset)
        obj._trunc_prior = swyft.TruncatedPrior.from_state_dict(
            state_dict["trunc_prior"]
        )
        obj._indices = state_dict["indices"]

        obj._store = store
        obj._simhook = simhook
        obj._simkeys = state_dict['simkeys']
        if state_dict["simhook"] and not simhook:
            log.warning(
                "A simhook was specified when the dataset was saved, but is missing now."
            )
        if not state_dict["simhook"] and simhook:
            log.warning(
                "A simhook was specified, but no simhook was specified when the Dataset was saved."
            )
        return obj

    def save(self, filename):
        torch.save(self.state_dict(), filename)

    @classmethod
    def load(cls, filename, store, simhook=None):
        sd = torch.load(filename)
        return cls.from_state_dict(sd, store, simhook=simhook)


# TODO: Needs to be updated
class ExactDataset(Dataset):
    """Dataset with exactly a certain number of simulations."""

    def __init__(self, N, prior, store, simhook=None, oversample_factor: float = 1.2):
        """Initialize Dataset.

        Args:
            N (int): Number of samples.
            prior (swyft.Prior): Parameter prior.
            store (swyft.Store): Store reference.
            simhook (Callable): Posthook for simulations. Applied on-the-fly to each point.
            oversample_factor (float): how many extra samples to draw (to make sure we can subsample to get an exact length)
        """
        super().__init__(int(oversample_factor * N), prior, store, simhook=simhook)
        while len(self) < N:
            indices = store.sample(int(oversample_factor * N), prior)
            self._indices = indices
        self._indices = self._indices[:N]

    @classmethod
    def from_parent_dataset(
        cls, N, parent_dataset: Dataset, oversample_factor: float = 1.2
    ):
        """Initialize Dataset from a parent. Story is copied and simulations are help in in oversampled memory store.

        Args:
            N (int): number of samples.
            parent_dataset (Dataset): where to draw the prior and copy the store from.
            oversample_factor (float): how many extra samples to draw (to make sure we can subsample to get an exact length)
        """
        prior = parent_dataset.prior
        store = parent_dataset._store.copy()
        simhook = parent_dataset._simhook
        dataset = cls(int(oversample_factor * N), prior, store, simhook)

        counter = 0
        while len(dataset) < N:
            dataset._indices = dataset._store.sample(int(oversample_factor * N), prior)
            counter += 1

            if counter > 10:
                raise RuntimeError()
        dataset._indices = dataset._indices[:N]
        return dataset
