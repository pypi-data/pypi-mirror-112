from mmdet.datasets import DATASETS, CustomDataset
import mmcv
import numpy as np
from mmcv.utils import print_log
from collections import OrderedDict
from mmdet.core import eval_map, eval_recalls
from .mean_ap import eval_precious


@DATASETS.register_module()
class MyDataset(CustomDataset):
    def load_annotations(self, ann_file):
        ann_list = mmcv.list_from_file(ann_file)

        data_infos = []
        for i, data_line in enumerate(ann_list):
            image_path = data_line.strip().split(' ')[0]
            image = mmcv.imread(image_path)
            image_shape = image.shape
            height, width = image_shape[0:2]

            annos = data_line.strip().split(' ')[1:]
            bboxes = []
            labels = []
            for anno in annos:
                anno = anno.strip().split(',')
                bboxes.append(anno[0:4])
                labels.append(anno[-1])

            data_infos.append(
                dict(
                    filename=image_path,
                    width=width,
                    height=height,
                    ann=dict(
                        bboxes=np.array(bboxes, dtype=np.float32),
                        labels=np.array(labels, dtype=np.int64)
                    )
                )
            )
        return data_infos

    def get_ann_info(self, idx):
        return self.data_infos[idx]['ann']

    def evaluate(self,
                 results,
                 metric='mAP',
                 logger=None,
                 proposal_nums=(100, 300, 1000),
                 iou_thr=0.5,
                 scale_ranges=None):
        """Evaluate the dataset.

        Args:
            results (list): Testing results of the dataset.
            metric (str | list[str]): Metrics to be evaluated.
            logger (logging.Logger | None | str): Logger used for printing
                related information during evaluation. Default: None.
            proposal_nums (Sequence[int]): Proposal number used for evaluating
                recalls, such as recall@100, recall@1000.
                Default: (100, 300, 1000).
            iou_thr (float | list[float]): IoU threshold. Default: 0.5.
            scale_ranges (list[tuple] | None): Scale ranges for evaluating mAP.
                Default: None.
        """

        if not isinstance(metric, str):
            assert len(metric) == 1
            metric = metric[0]
        allowed_metrics = ['mAP', 'recall', 'precious']
        print(metric)
        if metric not in allowed_metrics:
            raise KeyError(f'metric {metric} is not supported')
        annotations = [self.get_ann_info(i) for i in range(len(self))]
        eval_results = OrderedDict()
        iou_thrs = [iou_thr] if isinstance(iou_thr, float) else iou_thr
        if metric == 'mAP':
            assert isinstance(iou_thrs, list)
            mean_aps = []
            for iou_thr in iou_thrs:
                print_log(f'\n{"-" * 15}iou_thr: {iou_thr}{"-" * 15}')
                mean_ap, _ = eval_map(
                    results,
                    annotations,
                    scale_ranges=scale_ranges,
                    iou_thr=iou_thr,
                    dataset=self.CLASSES,
                    logger=logger)
                mean_aps.append(mean_ap)
                eval_results[f'AP{int(iou_thr * 100):02d}'] = round(mean_ap, 3)
            eval_results['mAP'] = sum(mean_aps) / len(mean_aps)
        elif metric == 'precious':
            assert isinstance(iou_thrs, list)
            for iou_thr in iou_thrs:
                print_log(f'\n{"-" * 15}iou_thr: {iou_thr}{"-" * 15}')
                results = eval_precious(
                    results,
                    annotations,
                    scale_ranges=scale_ranges,
                    iou_thr=iou_thr,
                    dataset=self.CLASSES,
                    logger=logger)
            eval_results['precious'] = results[0]['final_prec']
            eval_results['recall'] = results[0]['final_recall']
        elif metric == 'recall':
            gt_bboxes = [ann['bboxes'] for ann in annotations]
            recalls = eval_recalls(
                gt_bboxes, results, proposal_nums, iou_thr, logger=logger)
            for i, num in enumerate(proposal_nums):
                for j, iou in enumerate(iou_thrs):
                    eval_results[f'recall@{num}@{iou}'] = recalls[i, j]
            if recalls.shape[1] > 1:
                ar = recalls.mean(axis=1)
                for i, num in enumerate(proposal_nums):
                    eval_results[f'AR@{num}'] = ar[i]
        return eval_results
