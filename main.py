import json
import os
from glob import glob

from libs import utils as ut
from libs.db_controller import DBController
from libs.face_recognition.face_recognition import FaceRecognition
from libs.logger import Logger
from libs.slacksender import SlackSender

logger = None


def file_getter(paths: str):
    _path = glob(
        os.path.join(
            paths,
            "**",
            "*",
        ),
        recursive=True,
    )
    files = []
    for i in _path:
        if os.path.isdir(i):
            pass
        else:
            files.append(i)
    return files


def main(cfg):
    global logger
    slack = cfg["slack"]
    test = cfg["test"]
    mongo = cfg["mongo"]
    logger.info(f"\n slack\n{json.dumps(slack, indent=4, sort_keys=True)}")
    logger.info(f"\n test\n{json.dumps(test, indent=4, sort_keys=True)}")
    logger.info(f"\n mongo\n{json.dumps(mongo, indent=4, sort_keys=True)}")

    db = DBController(
        host_ip=mongo["host_ip"],
        host_port=mongo["host_port"],
        user=mongo["user"],
        passwd=mongo["passwd"],
        db_name=mongo["database"],
    )
    collection_name = mongo["collection"]

    fr = FaceRecognition(databases=db)
    sender = SlackSender(
        token=slack["token"],
    )
    #
    files = file_getter(paths=test["path"])
    REG = False
    if REG:
        for fname in files:
            fr.registration(
                collection=collection_name,
                name=f"{fname.split('/')[-1].split('_')[0]}",
                frame=fname,
            )
    idx, emb, score, name = fr.compare(
        collection=collection_name,
        target=test["file"],
    )
    # print(f"{idx}\n{emb}\n{score}\n{name}")

    response = sender.message_sender(
        channel=slack["channel"],
        message=f"{name}[{round(score, 2)}] 찾았다.",
    )
    logger.info(response)


if __name__ == "__main__":
    cfg = ut.read_config("config.json")
    log_cfg = cfg["log"]

    logger = Logger(
        class_name=os.path.basename(__file__).split(".")[0],
        lvl=log_cfg["level"],
        file_path=log_cfg["dst"],
        save=log_cfg["save"],
    ).logger

    main(cfg)
