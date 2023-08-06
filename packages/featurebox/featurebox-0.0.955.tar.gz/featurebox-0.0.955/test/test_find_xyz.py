import unittest

import pandas as pd

from featurebox.data.check_data import CheckElements
from featurebox.featurizers.envir.environment import BaseNNGet


class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        ce = CheckElements.from_pymatgen_structures()
        self.data = pd.read_pickle("data_structure.pkl_pd")
        self.data2 = pd.read_pickle("data_structure2.pkl_pd")
        self.data0 = self.data[0]
        self.data0_3 = ce.check(self.data)[:10]
        self.data0_checked = ce.check(self.data)[:10]

    def test_size_xyz(self):
        bag = BaseNNGet(cutoff=5.0, nn_strategy="find_xyz_in_spheres")
        for i in self.data0_3:
            center_indices, atom_nbr_idx, bond_states, bonds, center_prop = bag.convert(i)
            print(center_indices.shape)
            print(atom_nbr_idx.shape)
            print(bond_states.shape)
            print(bonds.shape)
            print(center_prop.shape)
            print("next")

    def test_size_radius(self):
        bag = BaseNNGet(cutoff=5.0, nn_strategy="find_points_in_spheres")
        for i in self.data0_3:
            center_indices, atom_nbr_idx, bond_states, bonds, center_prop = bag.convert(i)
            print(center_indices.shape)
            print(atom_nbr_idx.shape)
            print(bond_states.shape)
            print(bonds.shape)
            print(center_prop.shape)
            print("next")

    def test_size_strategy(self):
        bag = BaseNNGet(cutoff=5.0, nn_strategy="MinimumDistanceNNAll")
        for i in self.data0_3:
            center_indices, atom_nbr_idx, bond_states, bonds, center_prop = bag.convert(i)
            print(center_indices.shape)
            print(atom_nbr_idx.shape)
            print(bond_states.shape)
            print(bonds.shape)
            print(center_prop.shape)
            print("next")
