_base_ = [
    'detr_base.py', '../../_base_/datasets/mot_challenge.py', '../../_base_/default_runtime.py']
dataset_type = 'CocoVideoDataset'
classes = ('drone',)
...
data = dict(
    samples_per_gpu=2,
    workers_per_gpu=2,
    train=dict(
        type=dataset_type,
        classes=classes,
        ann_file='../mmtracking/data/multirotor-aerial-vehicle-vid-mavvid-dataset/mav_vid_dataset/train/annotations.json',
        img_prefix='../mmtracking/data/multirotor-aerial-vehicle-vid-mavvid-dataset/mav_vid_dataset/train/img/'
        # ann_file='data/strig-drones/datasets/mav-vid/train_annotations.json',
        ),
    test=dict(
        type=dataset_type,
        classes=classes,
        ann_file='../mmtracking/data/multirotor-aerial-vehicle-vid-mavvid-dataset/mav_vid_dataset/val/annotations.json',
        # ann_file='data/strig-drones/datasets/mav-vid/val_annotations.json',
        img_prefix='../mmtracking/data/multirotor-aerial-vehicle-vid-mavvid-dataset/mav_vid_dataset/val/img/'
        ))
model = dict(
    type='Tracktor',
    pretrains=dict(
        detector=  # noqa: E251
        # 'C:\\Users\\Matt\\Documents\\PhD\\drone\\mmtracking\\configs\\mot\\deepsort\\faster.pth', # noqa: E501
        "/home2/lgfm95/drone/Strig-UAV-Project/MAV-VID/DETR/full/latest.pth",
        reid=  # noqa: E251
        'https://download.openmmlab.com/mmtracking/mot/reid/tracktor_reid_r50_iter25245-a452f51f.pth'  # noqa: E501
    ),
    detector=dict(
    type='DETR',
    pretrained='torchvision://resnet50',
    backbone=dict(
        type='ResNet',
        depth=50,
        num_stages=4,
        out_indices=(3, ),
        frozen_stages=1,
        norm_cfg=dict(type='BN', requires_grad=False),
        norm_eval=True,
        style='pytorch'),
    bbox_head=dict(
        type='TransformerHead',
        num_classes=1,
        in_channels=2048,
        num_fcs=2,
        transformer=dict(
            type='Transformer',
            embed_dims=256,
            num_heads=8,
            num_encoder_layers=6,
            num_decoder_layers=6,
            feedforward_channels=2048,
            dropout=0.1,
            act_cfg=dict(type='ReLU', inplace=True),
            norm_cfg=dict(type='LN'),
            num_fcs=2,
            pre_norm=False,
            return_intermediate_dec=True),
        positional_encoding=dict(
            type='SinePositionalEncoding', num_feats=128, normalize=True),
        loss_cls=dict(
            type='CrossEntropyLoss',
            bg_cls_weight=0.1,
            use_sigmoid=False,
            loss_weight=1.0,
            class_weight=1.0),
        loss_bbox=dict(type='L1Loss', loss_weight=5.0),
        loss_iou=dict(type='GIoULoss', loss_weight=2.0))),
    reid=dict(
        type='BaseReID',
        backbone=dict(
            type='ResNet',
            depth=50,
            num_stages=4,
            out_indices=(3, ),
            style='pytorch'),
        neck=dict(type='GlobalAveragePooling', kernel_size=(8, 4), stride=1),
        head=dict(
            type='LinearReIDHead',
            num_fcs=1,
            in_channels=2048,
            fc_channels=1024,
            out_channels=128,
            norm_cfg=dict(type='BN1d'),
            act_cfg=dict(type='ReLU'))),
    motion=dict(
        type='CameraMotionCompensation',
        warp_mode='cv2.MOTION_EUCLIDEAN',
        num_iters=100,
        stop_eps=0.00001),
    tracker=dict(
        type='TracktorTracker',
        obj_score_thr=0.5,
        regression=dict(
            obj_score_thr=0.5,
            nms=dict(type='nms', iou_threshold=0.6),
            match_iou_thr=0.3),
        reid=dict(
            num_samples=10,
            img_scale=(256, 128),
            img_norm_cfg=None,
            match_score_thr=2.0,
            match_iou_thr=0.2),
        momentums=None,
        num_frames_retain=10))
# data_root = 'data/MOT17/'
# test_set = 'train'
# data = dict(
#     train=dict(ann_file=data_root + 'annotations/train_cocoformat.json'),
#     val=dict(ann_file=data_root + 'annotations/train_cocoformat.json'),
#     test=dict(
#         ann_file=data_root + f'annotations/{test_set}_cocoformat.json',
#         img_prefix=data_root + test_set))
