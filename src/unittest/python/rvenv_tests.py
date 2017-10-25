from unittest import TestCase, mock

from resco import rvenv


class TestRemoteVirtualEnv(TestCase):

    def setUp(self):
        # Patch all fabric imports
        self.patches = mock.patch.multiple('resco.rvenv',
                                           prefix=mock.DEFAULT,
                                           exists=mock.DEFAULT,
                                           run=mock.DEFAULT,
                                           put=mock.DEFAULT)
        self.mocks = self.patches.start()

    def tearDown(self):
        mock.patch.stopall()

    def test_runner_is_fabric_run(self):
        venv = rvenv.RemoteVirtualEnv('ANY_VENV')
        self.assertEqual(venv.runner, self.mocks['run'])

    def test_init_creates_if_not_exists(self):
        self.mocks['exists'].return_value = False
        venv = rvenv.RemoteVirtualEnv('ANY_VENV')
        venv.init()
        self.mocks['run'].assert_called_once_with('python3 -m venv ANY_VENV')

    def test_init_does_not_create_exists(self):
        self.mocks['exists'].return_value = True
        venv = rvenv.RemoteVirtualEnv('ANY_VENV')
        venv.init()
        self.mocks['run'].assert_not_called()
