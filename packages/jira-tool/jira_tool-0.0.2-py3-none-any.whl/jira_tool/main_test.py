import os
import unittest
from shutil import copyfile

from jira_tool.__main__ import get_labels_from_markdown, get_title_from_markdown, rename_file_to_card_number, \
    get_card_number_from_response


class MyTestCase(unittest.TestCase):

    def test_should_return_labels_in_first_line_when_get_labels_from_markdown_given_label_in_first_line(self):
        labels = get_labels_from_markdown("./", '02.md')
        self.assertEqual(["TW-AR", "MergeProject"], labels)

    def test_should_return_title_in_second_line_when_get_title_from_markdown_given_label_in_second_line(self):
        title = get_title_from_markdown("./", '02.md')
        self.assertEqual("测试转换", title)

    def test_should_rename_file_when_rename_file_to_card_number_given_card_number(self):
        copyfile("./02.md", "03.md")
        if os.path.exists("./OTRT-315.md"):
            os.remove("./OTRT-315.md")
        else:
            print('no such file:%s' % "./OTRT-315.md")
        rename_file_to_card_number("./", '03.md', "OTRT-315")
        files = os.listdir("./")
        self.assertTrue(files.__contains__("OTRT-315.md"))

    def test_should_return_OTRT_315_when_get_card_number_from_response_given_response(self):
        response = '{"issues":[{"id":"199563","key":"OTRT-315","self":"https://itsc-jira.daimler.com/jira/rest/api/2/issue/199563"}],"errors":[]}'

        card_number = get_card_number_from_response(response)
        self.assertEqual("OTRT-315", card_number)


if __name__ == '__main__':
    unittest.main()
