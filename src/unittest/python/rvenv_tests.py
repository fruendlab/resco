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

    def test_init_does_not_create_existing(self):
        self.mocks['exists'].return_value = True
        venv = rvenv.RemoteVirtualEnv('ANY_VENV')
        venv.init()
        self.mocks['run'].assert_not_called()

    def test_activate_manages_context(self):
        venv = rvenv.RemoteVirtualEnv('ANY_VENV')

        mock_context = self.mocks['prefix'].return_value

        with venv.activate():
            self.mocks['prefix'].assert_called_once_with(
                '. ANY_VENV/bin/activate')
            mock_context.__enter__.assert_called_once_with()
            mock_context.__exit__.assert_not_called()
        mock_context.__exit__.assert_called_once_with(
            None, None, None
        )

    def test_install_with_command(self):
        venv = rvenv.RemoteVirtualEnv('ANY_VENV', ['!ANY_COMMAND'])
        venv.install()
        self.assertIn(mock.call('ANY_COMMAND'), self.mocks['run'].mock_calls)

    def test_install_updates_pip(self):
        venv = rvenv.RemoteVirtualEnv('ANY_VENV', ['!ANY_COMMAND'])
        venv.install()
        self.assertIn(mock.call('pip install -U pip', pty=False),
                      self.mocks['run'].mock_calls)
