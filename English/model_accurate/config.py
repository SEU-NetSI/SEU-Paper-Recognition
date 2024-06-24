IAM_textrecog_data_root = 'data/IAM/words'
IAM_textrecog_test = dict(
    ann_file='test.json',
    data_root='data/IAM/words',
    pipeline=None,
    test_mode=True,
    type='OCRDataset')
IAM_textrecog_train = dict(
    ann_file='train.json',
    data_root='data/IAM/words',
    pipeline=None,
    type='OCRDataset')
TAL_textrecog_data_root = 'data/TAL'
TAL_textrecog_test = dict(
    ann_file='test.json',
    data_root='data/TAL',
    pipeline=None,
    test_mode=True,
    type='OCRDataset')
TAL_textrecog_train = dict(
    ann_file='train.json',
    data_root='data/TAL',
    pipeline=None,
    type='OCRDataset')
auto_scale_lr = dict(base_batch_size=512)
default_hooks = dict(
    checkpoint=dict(interval=1, type='CheckpointHook'),
    logger=dict(interval=100, type='LoggerHook'),
    param_scheduler=dict(type='ParamSchedulerHook'),
    sampler_seed=dict(type='DistSamplerSeedHook'),
    sync_buffer=dict(type='SyncBuffersHook'),
    timer=dict(type='IterTimerHook'),
    visualization=dict(
        draw_gt=False,
        draw_pred=False,
        enable=False,
        interval=1,
        show=False,
        type='VisualizationHook'))
default_scope = 'mmocr'
dictionary = dict(
    dict_file='mmocr/English/model_accurate/dict.txt',
    same_start_end=True,
    type='Dictionary',
    with_end=True,
    with_padding=True,
    with_start=True,
    with_unknown=True)
env_cfg = dict(
    cudnn_benchmark=False,
    dist_cfg=dict(backend='nccl'),
    mp_cfg=dict(mp_start_method='fork', opencv_num_threads=0))
launcher = 'none'
load_from = None
log_level = 'INFO'
log_processor = dict(by_epoch=True, type='LogProcessor', window_size=10)
model = dict(
    backbone=dict(hidden_dim=512, input_channels=3, type='ShallowCNN'),
    data_preprocessor=dict(
        mean=[
            123.675,
            116.28,
            103.53,
        ],
        std=[
            58.395,
            57.12,
            57.375,
        ],
        type='TextRecogDataPreprocessor'),
    decoder=dict(
        d_embedding=512,
        d_inner=2048,
        d_k=64,
        d_model=512,
        d_v=64,
        dictionary=dict(
            dict_file='mmocr/English/model_accurate/dict.txt',
            same_start_end=True,
            type='Dictionary',
            with_end=True,
            with_padding=True,
            with_start=True,
            with_unknown=True),
        max_seq_len=25,
        module_loss=dict(
            flatten=True, ignore_first_char=True, type='CEModuleLoss'),
        n_head=8,
        n_layers=6,
        postprocessor=dict(type='AttentionPostprocessor'),
        type='NRTRDecoder'),
    encoder=dict(
        d_inner=2048,
        d_k=64,
        d_model=512,
        d_v=64,
        dropout=0.1,
        n_head=8,
        n_layers=12,
        n_position=100,
        type='SATRNEncoder'),
    type='SATRN')
ocren_textrecog_data_root = 'data/ocren'
ocren_textrecog_test = dict(
    ann_file='test.json',
    data_root='data/ocren',
    pipeline=None,
    test_mode=True,
    type='OCRDataset')
ocren_textrecog_train = dict(
    ann_file='train.json',
    data_root='data/ocren',
    pipeline=None,
    type='OCRDataset')
optim_wrapper = dict(
    loss_scale='dynamic',
    optimizer=dict(lr=0.0003, type='Adam'),
    type='AmpOptimWrapper')
param_scheduler = [
    dict(end=5, milestones=[
        3,
        4,
    ], type='MultiStepLR'),
]
randomness = dict(seed=None)
resume = False
test_cfg = dict(type='TestLoop')
test_dataloader = dict(
    batch_size=1,
    dataset=dict(
        datasets=[
            dict(
                ann_file='test.json',
                data_root='data/TAL',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
            dict(
                ann_file='test.json',
                data_root='data/IAM/words',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
            dict(
                ann_file='test.json',
                data_root='data/ocren',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
        ],
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(keep_ratio=False, scale=(
                100,
                32,
            ), type='Resize'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    drop_last=False,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
test_dataset = dict(
    datasets=[
        dict(
            ann_file='test.json',
            data_root='data/TAL',
            pipeline=None,
            test_mode=True,
            type='OCRDataset'),
        dict(
            ann_file='test.json',
            data_root='data/IAM/words',
            pipeline=None,
            test_mode=True,
            type='OCRDataset'),
        dict(
            ann_file='test.json',
            data_root='data/ocren',
            pipeline=None,
            test_mode=True,
            type='OCRDataset'),
    ],
    pipeline=[
        dict(type='LoadImageFromFile'),
        dict(keep_ratio=False, scale=(
            100,
            32,
        ), type='Resize'),
        dict(type='LoadOCRAnnotations', with_text=True),
        dict(
            meta_keys=(
                'img_path',
                'ori_shape',
                'img_shape',
                'valid_ratio',
            ),
            type='PackTextRecogInputs'),
    ],
    type='ConcatDataset')
test_evaluator = dict(
    dataset_prefixes=[
        'TAL',
        'IAM',
        'ocren',
    ],
    metrics=[
        dict(
            mode=[
                'exact',
                'ignore_case',
                'ignore_case_symbol',
            ],
            type='WordMetric'),
        dict(type='CharMetric'),
    ],
    type='MultiDatasetsEvaluator')
test_list = [
    dict(
        ann_file='test.json',
        data_root='data/TAL',
        pipeline=None,
        test_mode=True,
        type='OCRDataset'),
    dict(
        ann_file='test.json',
        data_root='data/IAM/words',
        pipeline=None,
        test_mode=True,
        type='OCRDataset'),
    dict(
        ann_file='test.json',
        data_root='data/ocren',
        pipeline=None,
        test_mode=True,
        type='OCRDataset'),
]
test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(keep_ratio=False, scale=(
        100,
        32,
    ), type='Resize'),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(
        meta_keys=(
            'img_path',
            'ori_shape',
            'img_shape',
            'valid_ratio',
        ),
        type='PackTextRecogInputs'),
]
train_cfg = dict(max_epochs=20, type='EpochBasedTrainLoop', val_interval=1)
train_dataloader = dict(
    batch_size=128,
    dataset=dict(
        datasets=[
            dict(
                ann_file='train.json',
                data_root='data/TAL',
                pipeline=None,
                type='OCRDataset'),
            dict(
                ann_file='train.json',
                data_root='data/IAM/words',
                pipeline=None,
                type='OCRDataset'),
            dict(
                ann_file='train.json',
                data_root='data/ocren',
                pipeline=None,
                type='OCRDataset'),
        ],
        pipeline=[
            dict(ignore_empty=True, min_size=2, type='LoadImageFromFile'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(keep_ratio=False, scale=(
                100,
                32,
            ), type='Resize'),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    num_workers=24,
    persistent_workers=True,
    sampler=dict(shuffle=True, type='DefaultSampler'))
train_dataset = dict(
    datasets=[
        dict(
            ann_file='train.json',
            data_root='data/TAL',
            pipeline=None,
            type='OCRDataset'),
        dict(
            ann_file='train.json',
            data_root='data/IAM/words',
            pipeline=None,
            type='OCRDataset'),
        dict(
            ann_file='train.json',
            data_root='data/ocren',
            pipeline=None,
            type='OCRDataset'),
    ],
    pipeline=[
        dict(ignore_empty=True, min_size=2, type='LoadImageFromFile'),
        dict(type='LoadOCRAnnotations', with_text=True),
        dict(keep_ratio=False, scale=(
            100,
            32,
        ), type='Resize'),
        dict(
            meta_keys=(
                'img_path',
                'ori_shape',
                'img_shape',
                'valid_ratio',
            ),
            type='PackTextRecogInputs'),
    ],
    type='ConcatDataset')
train_list = [
    dict(
        ann_file='train.json',
        data_root='data/TAL',
        pipeline=None,
        type='OCRDataset'),
    dict(
        ann_file='train.json',
        data_root='data/IAM/words',
        pipeline=None,
        type='OCRDataset'),
    dict(
        ann_file='train.json',
        data_root='data/ocren',
        pipeline=None,
        type='OCRDataset'),
]
train_pipeline = [
    dict(ignore_empty=True, min_size=2, type='LoadImageFromFile'),
    dict(type='LoadOCRAnnotations', with_text=True),
    dict(keep_ratio=False, scale=(
        100,
        32,
    ), type='Resize'),
    dict(
        meta_keys=(
            'img_path',
            'ori_shape',
            'img_shape',
            'valid_ratio',
        ),
        type='PackTextRecogInputs'),
]
tta_model = dict(type='EncoderDecoderRecognizerTTAModel')
tta_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        transforms=[
            [
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=0, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=1, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
                dict(
                    condition="results['img_shape'][1]<results['img_shape'][0]",
                    true_transforms=[
                        dict(
                            args=[
                                dict(cls='Rot90', k=3, keep_size=False),
                            ],
                            type='ImgAugWrapper'),
                    ],
                    type='ConditionApply'),
            ],
            [
                dict(keep_ratio=False, scale=(
                    100,
                    32,
                ), type='Resize'),
            ],
            [
                dict(type='LoadOCRAnnotations', with_text=True),
            ],
            [
                dict(
                    meta_keys=(
                        'img_path',
                        'ori_shape',
                        'img_shape',
                        'valid_ratio',
                    ),
                    type='PackTextRecogInputs'),
            ],
        ],
        type='TestTimeAug'),
]
val_cfg = dict(type='ValLoop')
val_dataloader = dict(
    batch_size=1,
    dataset=dict(
        datasets=[
            dict(
                ann_file='test.json',
                data_root='data/TAL',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
            dict(
                ann_file='test.json',
                data_root='data/IAM/words',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
            dict(
                ann_file='test.json',
                data_root='data/ocren',
                pipeline=None,
                test_mode=True,
                type='OCRDataset'),
        ],
        pipeline=[
            dict(type='LoadImageFromFile'),
            dict(keep_ratio=False, scale=(
                100,
                32,
            ), type='Resize'),
            dict(type='LoadOCRAnnotations', with_text=True),
            dict(
                meta_keys=(
                    'img_path',
                    'ori_shape',
                    'img_shape',
                    'valid_ratio',
                ),
                type='PackTextRecogInputs'),
        ],
        type='ConcatDataset'),
    drop_last=False,
    num_workers=4,
    persistent_workers=True,
    sampler=dict(shuffle=False, type='DefaultSampler'))
val_evaluator = dict(
    dataset_prefixes=[
        'TAL',
        'IAM',
        'ocren',
    ],
    metrics=[
        dict(
            mode=[
                'exact',
                'ignore_case',
                'ignore_case_symbol',
            ],
            type='WordMetric'),
        dict(type='CharMetric'),
    ],
    type='MultiDatasetsEvaluator')
vis_backends = [
    dict(type='LocalVisBackend'),
]
visualizer = dict(
    name='visualizer',
    type='TextRecogLocalVisualizer',
    vis_backends=[
        dict(type='LocalVisBackend'),
    ])
work_dir = '/public/yuziyang/work_dirs/rec/new_dict/lines/satrn/TAL_ocren_IAM/'
