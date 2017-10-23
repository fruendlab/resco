from unittest import TestCase, mock

from resco import utils


class TestCreateTree(TestCase):

    def setUp(self):
        self.patches = {
            'touch': mock.patch('resco.utils.touch'),
            'makedirs': mock.patch('os.makedirs'),
        }
        self.mocks = {name: patch.start()
                      for name, patch in self.patches.items()}

    def tearDown(self):
        mock.patch.stopall()

    def test_string_creates_file(self):
        utils.create_tree('ANY_FILE')
        self.mocks['touch'].assert_called_once_with('ANY_FILE')

    def test_creates_dictionary_key_as_a_path(self):
        utils.create_tree({'ANY_DIRECTORY': {}})
        self.mocks['makedirs'].assert_called_once_with('ANY_DIRECTORY',
                                                       exist_ok=True)

    def test_creates_all_elements_in_lists(self):
        utils.create_tree({'ANY_DIRECTORY': ['ANY_FILE',
                                             {'ANY_SUBDIRECTORY': {}}]})
        self.mocks['touch'].assert_called_once_with('ANY_DIRECTORY/ANY_FILE')
        self.mocks['makedirs'].assert_has_calls([
            mock.call('ANY_DIRECTORY', exist_ok=True),
            mock.call('ANY_DIRECTORY/ANY_SUBDIRECTORY', exist_ok=True),
        ])


class TestTouch(TestCase):

    @mock.patch('builtins.open')
    def test_touch(self, mock_open):
        utils.touch('ANY_FILE')
        mock_open.assert_called_once_with('ANY_FILE', 'a')
        mock_open.return_value.close.assert_called_once_with()
