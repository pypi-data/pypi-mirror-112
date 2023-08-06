import unittest 
import anatools

class Tests(unittest.TestCase):

    def a_test_invite_user_to_workspace(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.invite_user_to_workspace(email="samkulkarni.d@gmail.com", workspaceId="52ad7a96-bc33-4852-8702-ed45fbbade6b")

    def a_test_add_workspace_channel(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.get_channels()
        self.ana.add_workspace_channel(channel_name='satrgb', workspaceId='ca905d49-248f-44f5-bca1-0e3e485d756c')

    def a_test_remove_workspace_channel(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.get_channels()
        self.ana.remove_workspace_channel(channel_name='satrgb', workspaceId='ca905d49-248f-44f5-bca1-0e3e485d756c')

    def a_test_create_pkg(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.create_package(name='test_create', location='s3://renderedai-dev-data/packages/testcreate')

    def a_test_generate_annotation(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.generate_annotation(datasetId='3aade6a4-a0ec-4a24-83ff-7131e4fdeaa9', annotation_format='COCO', annotation_map='afv', workspaceId='52ad7a96-bc33-4852-8702-ed45fbbade6b')

    def a_test_download_annotation(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.download_annotation(datasetId='3aade6a4-a0ec-4a24-83ff-7131e4fdeaa9', annotationId='6e927250-84f9-49a4-96b3-96d8dea4180a', workspaceId='52ad7a96-bc33-4852-8702-ed45fbbade6b')

    def a_test_remove_channel_owner(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.remove_channel_owner(email='ethan@rendered.ai', channel_name='example')
        self.ana.register_channel_owner(email='ethan@rendered.ai', channel='example')

    def a_test_register_data(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.register_package_data(package='example', location='/Users/samruddhi/ana/ana/data/packages')

    def a_test_stop(self):
        self.ana = anatools.AnaClient(None, 'dev', 'debug')
        self.ana.stop_execution(datasetId='e37a181b-dd84-43fb-8d3f-5eead509601d', workspaceId='52ad7a96-bc33-4852-8702-ed45fbbade6b')

if __name__ == '__main__':
    unittest.main()