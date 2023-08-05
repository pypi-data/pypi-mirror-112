from azure.storage import blob
from scrapy.extensions.feedexport import BlockingFeedStorage
from azure.storage.blob import ContainerClient

class AzureBlobFeedStorage(BlockingFeedStorage):

    def __init__(self, uri):

        '''
        Azure uses slashes '/' in their keys, which confuses the shit out of urlparse.
        So, we just handle it ourselves here.
        assuming format looks like this:

        azure://account_name:password@container/filename.jsonl

        azure://bobsaccount:1234567890abc1KUj0lK1gXHv4NHrCfKxfxHy3bwQJ+LqFHCay6r1S/Yhw2Ot4Tk6p1zF9IiMcPBo7o9poXZgA==@sites/filename.jsonl
        '''
       
        container = uri.split('@')[1].split('/')[0]
        filename = '/'.join(uri.split('@')[1].split('/')[1::])
        account_name, account_key = uri[8::].split('@')[0].split(':')
        account_url ="https://" + account_name + ".blob.core.windows.net//"
        self.account_name = account_name
        self.account_key = account_key
        self.container = container
        self.filename = filename
        self.account_url = account_url
        self.container_client = ContainerClient(container_name = self.container,account_name=self.account_name, credential=self.account_key,account_url = self.account_url)
        print(self.filename)
    def _store_in_thread(self, file):
        file.seek(0)
        self.container_client.upload_blob(name=self.filename, data=file)