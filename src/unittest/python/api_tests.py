from unittest import TestCase, mock

from resco import api


class ContextVerifier(object):

    def __enter__(self, *args, **kwargs):
        self.calls = []
        self.active = True

    def __exit__(self, *args):
        self.active = False

    def add_call(self, *args, **kwargs):
        if self.active:
            self.calls.append((args, kwargs))

    def attach(self, context, target):
        context.return_value = self
        target.side_effect = self.add_call


class TestRunCommand(TestCase):

    def setUp(self):
        self.patches = mock.patch.multiple('resco.api',
                                           local=mock.DEFAULT,
                                           put=mock.DEFAULT,
                                           run=mock.DEFAULT,
                                           cd=mock.DEFAULT,
                                           )
        self.mocks = self.patches.start()
        self.mock_venv = mock.MagicMock()

    def tearDown(self):
        mock.patch.stopall()

    def test_copies_files(self):
        api.run_command('{cmd}:{module}',
                        'ANY_SCRIPT',
                        self.mock_venv,
                        'ANY_MODULE',
                        'ANY_DIR')
        self.mocks['put'].assert_any_call('ANY_MODULE', 'ANY_DIR')

    def test_copies_scripts(self):
        api.run_command('{cmd}:{module}',
                        'ANY_SCRIPT',
                        self.mock_venv,
                        'ANY_MODULE',
                        'ANY_DIR')
        self.mocks['put'].assert_any_call('scripts', 'ANY_DIR')

    def test_runs_remotely(self):
        cv = ContextVerifier()
        cv.attach(self.mocks['cd'], self.mocks['run'])
        api.run_command('{cmd}:{module}',
                        'scripts/ANY_SCRIPT',
                        self.mock_venv,
                        'ANY_MODULE',
                        'ANY_DIR')
        self.mocks['run'].assert_called_once_with(
            'scripts/ANY_SCRIPT:ANY_MODULE')
        self.assertEqual(len(cv.calls), 1)

    @mock.patch('resco.api.run_unit_tests')
    def test_runs_unit_tests_first(self, mock_run_unit_tests):
        api.run_command('{cmd}:{module}',
                        'ANY_SCRIPT',
                        self.mock_venv,
                        'ANY_MODULE',
                        'ANY_DIR')
        mock_run_unit_tests.assert_called_once_with()

    def test_runs_in_venv(self):
        cv = ContextVerifier()
        cv.attach(self.mock_venv.activate, self.mocks['run'])
        api.run_command('{cmd}:{module}',
                        'ANY_SCRIPT',
                        self.mock_venv,
                        'ANY_MODULE',
                        'ANY_DIR')
        self.assertEqual(len(cv.calls), 1)


class TestRunScriptStartScript(TestCase):

    def setUp(self):
        self.mock_run_command = mock.patch('resco.api.run_command').start()
        self.mock_venv = mock.MagicMock()

        class MockEnv(object):
            venv = self.mock_venv
            module_name = 'ANY_MODULE'
            working_dir = 'ANY_DIR'

        self.mock_env = mock.patch('resco.api.env', MockEnv()).start()

    def tearDown(self):
        mock.patch.stopall()

    def test_run_script_calls_correctly(self):
        api.run_script('ANY_SCRIPT')
        self.mock_run_command.assert_called_once_with(
            '{cmd}',
            'PYTHONPATH=. python scripts/ANY_SCRIPT',
            self.mock_venv,
            'ANY_MODULE',
            'ANY_DIR',
        )

    def test_start_script_calls_correctly(self):
        api.start_script('ANY_SCRIPT')
        self.mock_run_command.assert_called_once_with(
            'tmux new-session -d -s ANY_MODULE "{cmd}"',
            'PYTHONPATH=. python scripts/ANY_SCRIPT',
            self.mock_venv,
            'ANY_MODULE',
            'ANY_DIR',
        )

    def test_start_script_accepts_jobname(self):
        api.start_script('ANY_SCRIPT', 'ANY_JOBNAME')
        self.mock_run_command.assert_called_once_with(
            'tmux new-session -d -s ANY_JOBNAME "{cmd}"',
            'PYTHONPATH=. python scripts/ANY_SCRIPT',
            self.mock_venv,
            'ANY_MODULE',
            'ANY_DIR',
        )


class TestCreateCommand(TestCase):

    def test_with_prefix(self):
        cmd = api.create_command('scripts/ANY_SCRIPT')
        self.assertEqual(cmd, 'PYTHONPATH=. python scripts/ANY_SCRIPT')

    def test_without_prefix(self):
        cmd = api.create_command('ANY_SCRIPT')
        self.assertEqual(cmd, 'PYTHONPATH=. python scripts/ANY_SCRIPT')


class TestFetchLs(TestCase):

    def setUp(self):
        self.mock_venv = mock.MagicMock()

        class MockEnv(object):
            venv = self.mock_venv
            module_name = 'ANY_MODULE'
            working_dir = 'ANY_DIR'

        self.mock_env = mock.patch('resco.api.env', MockEnv()).start()

    @mock.patch('resco.api.get')
    def test_fetch_fetches_to_same_location(self, mock_get):
        api.fetch('*.py')
        mock_get.assert_called_once_with(remote_path='target/*.py',
                                         local_path='%(path)s')
