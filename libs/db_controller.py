import ast
import os

import pymongo

from libs.logger import Logger


class DBController:
    def __init__(
        self,
        host_ip: str,
        host_port: int,
        user: str,
        passwd: str,
        db_name: str,
    ) -> None:
        super().__init__()
        self.logger = Logger(
            class_name=os.path.basename(__file__).split(".")[0],
            lvl="INFO",
            file_path="logs",
        ).logger
        self.logger.info(pymongo.__version__)

        self._connect(
            host_ip=host_ip,
            host_port=host_port,
            user=user,
            passwd=passwd,
            db_name=db_name,
        )

    def _connect(
        self,
        host_ip: str,
        host_port: int,
        user: str,
        passwd: str,
        db_name: str,
    ):
        client = pymongo.MongoClient(
            host=host_ip,
            port=host_port,
            username=user,
            password=passwd,
        )
        self.database = client.get_database(db_name)

    def _added_db(
        self,
        ce_name: str,
        data: dict,
    ):
        if ce_name in self.database.list_collection_names():
            pass
        else:
            self.database.drop_collection(ce_name)

        collection = self.database.get_collection(ce_name)
        collection.insert_one(data)

    def registration(
        self,
        collection: str,
        name: str,
        embs: list,
    ):
        self._added_db(
            ce_name=collection,
            data={
                "name": name,
                "face_emb": embs,
            },
        )

    def finder(self, ce_name):
        collection = self.database.get_collection(ce_name)
        embs = []
        names = []
        for i in collection.find({}):
            embs.append(ast.literal_eval(i["face_emb"]))
            names.append(i["name"])
        return names, embs
