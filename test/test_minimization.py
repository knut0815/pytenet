import unittest
import numpy as np
import sys
sys.path.append('../pytenet/')
from mps import MPS
import hamiltonian
import minimization


class TestMinimization(unittest.TestCase):

    def test_single_site(self):

        # number of lattice sites
        L = 10

        # number of left and right sweeps
        numsweeps = 4

        # construct matrix product operator representation of Heisenberg Hamiltonian
        J =  4.0/5
        D =  8.0/3
        h = -2.0/7
        mpoH = hamiltonian.heisenberg_XXZ_MPO(L, J, D, h)

        # initial wavefunction as MPS with random entries
        psi = MPS(2, [1] + (L-1) * [28] + [1], fill='random')

        en_min = minimization.calculate_ground_state_local_singlesite(mpoH, psi, numsweeps)
        # value after last iteration
        E0 = en_min[-1]

        # reference spectrum and wavefunctions
        en_ref, V_ref = np.linalg.eigh(mpoH.as_matrix())

        # compare ground state energy
        self.assertAlmostEqual(E0, en_ref[0], delta=1e-13,
            msg='ground state energy obtained by single-site optimization must match reference')

        # compare ground state wavefunction
        psi_vec = psi.as_vector()
        # multiply by phase factor to match (real-valued) reference wavefunction
        i = np.argmax(abs(psi_vec))
        z = psi_vec[i]
        psi_vec *= z.conj() / abs(z)
        if V_ref[i,0] < 0:
            psi_vec = -psi_vec
        self.assertAlmostEqual(np.linalg.norm(psi_vec - V_ref[:,0]), 0, delta=1e-7,
            msg='ground state wavefunction obtained by single-site optimization must match reference')


if __name__ == '__main__':
    unittest.main()
