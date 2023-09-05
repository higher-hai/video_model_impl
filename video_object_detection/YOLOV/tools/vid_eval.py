#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Copyright (c) Megvii, Inc. and its affiliates.

import argparse
import random
import warnings
from loguru import logger
import os

import torch
import torch.backends.cudnn as cudnn

from yolox.core import launch
from yolox.core.vid_trainer import Trainer

from yolox.exp import get_exp
from yolox.utils import configure_nccl, configure_omp, get_num_devices
from yolox.data.data_augment import Vid_Val_Transform
from yolox.data.datasets import vid

def make_parser():
    parser = argparse.ArgumentParser("YOLOX train parser")
    parser.add_argument("-expn", "--experiment-name", type=str, default=None)
    parser.add_argument("-n", "--name", type=str, default=None, help="model name")
    parser.add_argument("--tsize", default=576, type=int, help="test img size")
    # distributed
    parser.add_argument(
        "--dist-backend", default="nccl", type=str, help="distributed backend"
    )
    parser.add_argument(
        "--dist-urlT",
        default=None,
        type=str,
        help="url used to set up distributed training",
    )
    parser.add_argument("-b", "--batch-size", type=int, default=32, help="batch size")
    parser.add_argument(
        "-d", "--devices", default=1, type=int, help="device for training"
    )
    parser.add_argument(
        "-f",
        "--exp_file",
        default='',
        type=str,
        help="plz input your expriment description file",
    )
    parser.add_argument(
        "--resume", default=False, action="store_true", help="resume training"
    )
    parser.add_argument("-c", "--ckpt", default='', type=str, help="checkpoint file")
    parser.add_argument(
        '-data_dir',
        default='',
        type=str,
        help="path to your dataset",

    )
    parser.add_argument(
        "-e",
        "--start_epoch",
        default=None,
        type=int,
        help="resume training start epoch",
    )
    parser.add_argument(
        "--num_machines", default=1, type=int, help="num of node for training"
    )
    parser.add_argument(
        "--machine_rank", default=0, type=int, help="node rank for multi-node training"
    )
    parser.add_argument(
        "--fp16",
        dest="fp16",
        default=False,
        action="store_true",
        help="Adopting mix precision training.",
    )
    parser.add_argument(
        "--cache",
        dest="cache",
        default=False,
        action="store_true",
        help="Caching imgs to RAM for fast training.",
    )
    parser.add_argument(
        "-o",
        "--occupy",
        dest="occupy",
        default=False,
        action="store_true",
        help="occupy GPU memory first for training.",
    )
    parser.add_argument(
        "opts",
        help="Modify config options using the command-line",
        default=None,
        nargs=argparse.REMAINDER,
    )

    parser.add_argument('--lframe', default=0, help='local frame num')
    parser.add_argument('--gframe', default=32, help='global frame num')
    parser.add_argument('--mode', default='random', help='frame sample mode')
    parser.add_argument('--tnum', default=-1, help='vid test sequences')
    return parser


@logger.catch
def main(exp, args):
    if exp.seed is not None:
        random.seed(exp.seed)
        torch.manual_seed(exp.seed)
        cudnn.deterministic = True
        warnings.warn(
            "You have chosen to seed training. This will turn on the CUDNN deterministic setting, "
            "which can slow down your training considerably! You may see unexpected behavior "
            "when restarting from checkpoints."
        )

    # set environment variables for distributed training
    configure_nccl()
    configure_omp()
    cudnn.benchmark = True
    lframe = int(args.lframe)
    gframe = int(args.gframe)

    dataset_val = vid.VIDDataset(file_path='./yolox/data/datasets/val_seq.npy',
                                 img_size=(args.tsize, args.tsize), preproc=Vid_Val_Transform(), lframe=lframe,
                                 gframe=gframe, val=True,mode=args.mode,dataset_pth=exp.data_dir,tnum=int(args.tnum))
    val_loader = vid.get_vid_loader(batch_size=lframe + gframe, data_num_workers=4, dataset=dataset_val,)

    trainer = Trainer(exp, args,val_loader,val=True)


if __name__ == "__main__":
    args = make_parser().parse_args()

    exp = get_exp(args.exp_file, args.name)
    exp.test_size = (args.tsize, args.tsize)
    exp.merge(args.opts)
    if not args.experiment_name:
        args.experiment_name = exp.exp_name

    num_gpu = get_num_devices() if args.devices is None else args.devices
    assert num_gpu <= get_num_devices()
    args.machine_rank = 1
    dist_url = "auto" #if args.dist_url is None else args.dist_url
    launch(
        main,
        num_gpu,
        args.num_machines,
        args.machine_rank,
        backend=args.dist_backend,
        dist_url=dist_url,
        args=(exp, args),
    )
