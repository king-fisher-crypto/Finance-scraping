from itemadapter import ItemAdapter
import os
from pymongo import MongoClient


mongo = MongoClient(
    host='localhost',
    port=int(os.environ.get('CRAWLAB_MONGO_PORT') or 27018),
    username=os.environ.get('CRAWLAB_MONGO_USERNAME') or 'admin',
    password=os.environ.get('CRAWLAB_MONGO_PASSWORD') or 'I7gg7887g7g67g67tyCV',
    authSource=os.environ.get('CRAWLAB_MONGO_AUTHSOURCE') or 'admin'
)
db = mongo[os.environ.get('CRAWLAB_MONGO_DB') or 'test']
col = db[os.environ.get('CRAWLAB_COLLECTION') or 'test']
task_id = os.environ.get('CRAWLAB_TASK_ID')


class JobsPipeline:
    def process_item(self, item, spider):
        item['task_id'] = task_id
        # oldItems = col.find(
        #    {'url': item['url'], 'title': item['title'], 'description': item['description']})
        # if oldItems.count() == 0:
        #     col.save(item)
        oldItems = col.count_documents(
          	{'url': item['url'], 'title': item['title'], 'description': item['description']})
        if oldItems == 0:
          	col.save(item)
        return item
