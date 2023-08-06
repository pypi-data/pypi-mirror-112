import os
import shutil
import sys
import time

import numpy as np
import torch
from deprecated.classic import deprecated
from sklearn import metrics
from torch.nn import Module
from torch.optim.lr_scheduler import MultiStepLR

from featurebox.featurizers.generator import MGEDataLoader


def class_eval(prediction, target):
    """Classification."""
    prediction = np.exp(prediction.numpy())
    target = target.numpy()
    pred_label = np.argmax(prediction, axis=1)
    target_label = np.squeeze(target)
    if not target_label.shape:
        target_label = np.asarray([target_label])
    if prediction.shape[1] == 2:
        precision, recall, fscore, _ = metrics.precision_recall_fscore_support(
            target_label, pred_label, average='binary')
        auc_score = metrics.roc_auc_score(target_label, prediction[:, 1])
        accuracy = metrics.accuracy_score(target_label, pred_label)
    else:
        raise NotImplementedError
    return accuracy, precision, recall, fscore, auc_score


class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum = self.sum + val * n  # (if pytorch not support +=)
        self.count += n
        self.avg = self.sum / self.count


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')


def mae(prediction, target):
    """
    Computes the mean absolute error between prediction and target
    Parameters
    ----------
    prediction: torch.Tensor (N, 1)
    target: torch.Tensor (N, 1)
    """
    return torch.mean(torch.abs(target - prediction))


def for_hook(module, input, output):
    print(module)
    for val in input:
        print("input val:", val)
    for out_val in output:
        print("output val:", out_val)


@deprecated(version='0.1.0')
class BaseLearning:
    def __init__(self, model: Module, train_loader: MGEDataLoader, test_loader: MGEDataLoader, device: str = "cpu",
                 optimizer=None, clf: bool = False, loss_method=None, learning_rate: float = 1e-3, milestones=None,
                 weight_decay: float = 0.01, checkpoint=True,
                 loss_threshold: float = 230.0, print_freq: int = None, print_what="all"):
        """

        Parameters
        ----------
        model: module
        train_loader: MGEDataLoader
        test_loader: MGEDataLoader
        device:str
            such as "cuda:0","cpu"
        optimizer:torch.Optimizer
        clf:bool
            under exploit......
        loss_method:torch._Loss
            see more in torch
        learning_rate:float
            see more in torch
        milestones:list of float
            see more in torch
        weight_decay:float
            see more in torch
        checkpoint:bool
            save checkpoint or not.
        loss_threshold:
            see more in torch
        print_freq:int
            print frequency
        print_what:str
            "all","train","test" log.
        """

        self.train_loader = train_loader
        self.test_loader = test_loader

        device = torch.device(device)
        self.train_loader.to_cuda(device)
        self.train_loader.reset_shuffle(shuffle=True)
        if self.test_loader is not None:
            self.test_loader.to_cuda(device)
        self.device = device
        self.model = model
        self.model.to(device)
        self.clf = clf
        self.loss_method = loss_method
        self.milestones = milestones
        self.optimizer = optimizer
        self.checkpoint = checkpoint

        self.train_batch_number = len(self.train_loader.loader)
        self.test_batch_number = len(self.test_loader.loader) if self.test_loader is not None else 0
        if print_freq == "default":
            self.print_freq = int(self.train_batch_number / 10) + 1
        else:
            self.print_freq = self.train_batch_number if print_freq is None else print_freq

        if self.optimizer is None or self.optimizer == "Adam":
            self.optimizer = torch.optim.Adam(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)
        elif self.optimizer == "SGD":
            self.optimizer = torch.optim.SGD(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay
                                             )
            # L2 regularization
        else:
            self.optimizer = optimizer(self.model.parameters(), lr=learning_rate, weight_decay=weight_decay)

        if self.loss_method is None:
            if self.clf is True:
                self.loss_method = torch.nn.CrossEntropyLoss()
            elif self.clf == "multi_label":
                self.loss_method = torch.nn.L1Loss()
                # 主要是用来判定实际的输出与期望的输出的接近程度 MAE: 1/N |y_pred-y| y 为多列
            else:
                self.loss_method = torch.nn.MSELoss()

        else:
            self.loss_method = loss_method
        if self.milestones is None:
            self.milestones = [30, 50, 80]
        self.scheduler = MultiStepLR(self.optimizer, gamma=0.2, milestones=self.milestones)
        self.best_error = 1000000.0
        self.threshold = loss_threshold
        # *.pth.tar or str
        self.run_train = self.run
        self.fit = self.run_train
        self.print_what = print_what
        self.forward_hook_list = []

    def run(self, epoch=50, warm_start=False):
        """
        run loop.

        Parameters
        ----------
        epoch:int
            epoch.
        warm_start: str, False
            The name of resume file, 'checkpoint.pth.tar' or 'model_best.pth.tar'
            If warm_start, try to resume from local disk.
        """

        resume = warm_start if warm_start is not False else None
        start_epoch = 0
        if resume:
            if os.path.isfile(resume):
                print("=> loading checkpoint '{}'".format(resume))
                checkpoint = torch.load(resume)
                start_epoch = checkpoint['epoch']
                self.threshold = checkpoint['best_mae_error']
                self.model.load_state_dict(checkpoint['state_dict'])
                self.optimizer.load_state_dict(checkpoint['optimizer'])
                print("=> loaded checkpoint '{}' (epoch {})"
                      .format(resume, checkpoint['epoch']))
            else:
                print("=> no checkpoint found at '{}'".format(resume))

        self.model.to(self.device)
        self.model.train()
        train_loader = self.train_loader
        if start_epoch > 0:
            epoch += start_epoch
            print("Try to run start from 'resumed epoch' {} to 'epoch' {}".format(start_epoch, epoch))
        for epochi in range(start_epoch, epoch):

            train_loader.reset()

            self._train(epochi)

            score = self._validate(epochi)

            if score != score:
                print('Exit due to NaN')
                sys.exit(1)

            self.scheduler.step()

            is_best = score < self.best_error
            self.best_error = min(score, self.best_error)

            if self.checkpoint:
                save_checkpoint({
                    'epoch': epochi + 1,
                    'state_dict': self.model.state_dict(),
                    'best_mae_error': self.threshold,
                    'optimizer': self.optimizer.state_dict(),
                }, is_best)

            if score <= self.threshold:
                print("Up to requirements and early termination in epoch ({})".format(epochi))
                break

    def _train(self, epochi):
        self.model.train()
        batch_time = AverageMeter()
        losses = AverageMeter()
        if self.clf is False:
            mae_errors = AverageMeter()
        else:
            accuracies = AverageMeter()
            precisions = AverageMeter()
            recalls = AverageMeter()
            fscores = AverageMeter()
            auc_scores = AverageMeter()

        self.train_loader.reset()
        point = time.time()
        for m, (batch_x, batch_y) in enumerate(self.train_loader):
            batch_time.update(time.time() - point)

            self.optimizer.zero_grad()

            y_pred = self.model(*batch_x)
            try:
                lossi = self.loss_method(y_pred, batch_y)
            except TypeError:
                target = batch_y.sign()
                lossi = self.loss_method(y_pred, batch_y, target)
            losses.update(float(lossi.cpu().item()), batch_y.size(0))

            if self.clf is False:
                mae_error = mae(y_pred.data.cpu(), batch_y.cpu())
                mae_errors.update(mae_error, batch_y.size(0))
            else:

                accuracy, precision, recall, fscore, auc_score = \
                    class_eval(y_pred.data.cpu(), batch_y.cpu())

                accuracies.update(accuracy, batch_y.size(0))
                precisions.update(precision, batch_y.size(0))
                recalls.update(recall, batch_y.size(0))
                fscores.update(fscore, batch_y.size(0))
                auc_scores.update(auc_score, batch_y.size(0))

            lossi.backward()

            self.optimizer.step()
            point = time.time()

            if m % self.print_freq == 0 and self.print_what in ["all", "train"]:
                if self.clf is False:
                    print('Train: [{0}][{1}/{2}]\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'MAE {mae_errors.val:.3f} ({mae_errors.avg:.3f})'
                          'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                        .format(
                        epochi, m, len(self.train_loader), loss=losses,
                        batch_time=batch_time, mae_errors=mae_errors))
                else:
                    print('Train: [{0}][{1}/{2}]\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'Accu {accu.val:.3f} ({accu.avg:.3f})\t'
                          'Precision {prec.val:.3f} ({prec.avg:.3f})\t'
                          'Recall {recall.val:.3f} ({recall.avg:.3f})\t'
                          'F1 {f1.val:.3f} ({f1.avg:.3f})\t'
                          'AUC {auc.val:.3f} ({auc.avg:.3f})'
                          'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'.format(
                        epochi, m, len(self.train_loader), loss=losses,
                        batch_time=batch_time,
                        accu=accuracies,
                        prec=precisions, recall=recalls, f1=fscores,
                        auc=auc_scores))

    def _validate(self, epochi):
        self.model.eval()
        mae_errors = AverageMeter()
        if self.clf is False:

            losses = AverageMeter()
        else:
            accuracies = AverageMeter()
            precisions = AverageMeter()
            recalls = AverageMeter()
            fscores = AverageMeter()
            auc_scores = AverageMeter()

        self.model.eval()

        self.test_loader.reset()

        for m, (batch_x, batch_y) in enumerate(self.test_loader):

            y_pred = self.model(*batch_x)
            try:
                lossi = self.loss_method(y_pred, batch_y)
            except TypeError:
                target = batch_y.sign()
                lossi = self.loss_method(y_pred, batch_y, target)

            losses.update(lossi.cpu().item(), batch_y.size(0))
            if self.clf is False:

                mae_error = mae((y_pred.data.cpu()), batch_y.cpu())
                mae_errors.update(mae_error, batch_y.size(0))
            else:
                accuracy, precision, recall, fscore, auc_score = \
                    class_eval(y_pred.data.cpu(), batch_y.cpu())

                accuracies.update(accuracy, batch_y.size(0))
                precisions.update(precision, batch_y.size(0))
                recalls.update(recall, batch_y.size(0))
                fscores.update(fscore, batch_y.size(0))
                auc_scores.update(auc_score, batch_y.size(0))

            if m % self.print_freq == 0 and self.print_what in ["all", "test"]:
                if self.clf is False:
                    print('Test: [{0}][{1}/{2}]\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'MAE {mae_errors.val:.3f} ({mae_errors.avg:.3f})'.format(
                        epochi, m, len(self.test_loader),
                        loss=losses, mae_errors=mae_errors))
                else:
                    print('Test: [{0}][{1}/{2}]\t'
                          'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
                          'Accu {accu.val:.3f} ({accu.avg:.3f})\t'
                          'Precision {prec.val:.3f} ({prec.avg:.3f})\t'
                          'Recall {recall.val:.3f} ({recall.avg:.3f})\t'
                          'F1 {f1.val:.3f} ({f1.avg:.3f})\t'
                          'AUC {auc.val:.3f} ({auc.avg:.3f})'.format(
                        epochi, m, len(self.test_loader),
                        loss=losses, accu=accuracies,
                        prec=precisions, recall=recalls, f1=fscores,
                        auc=auc_scores))

        if self.clf is False:
            return mae_errors.avg
        else:
            return auc_scores.avg

    def mae_score(self, predict_loader):
        """Return MAE score."""
        y_pre, y_true = self.predict(predict_loader, return_y_true=True, add_hook=False)
        return float(mae(y_pre, y_true))

    def predict(self, predict_loader: MGEDataLoader, return_y_true=False, add_hook=True):
        """
        Just predict by model,and add one forward hook to get put.

        Parameters
        ----------
        predict_loader:MGEDataLoader
            MGEDataLoader, the target_y could be ``None``.
        return_y_true:bool
            if return_y_true, return (y_preds, y_true)
        add_hook:bool
            if add_hook, the model must contain torch native nn.ModuleList named ``fcs``
            such as ``self.fcs = nn.ModuleList(...)`` in module.

        Returns
        -------
        y_pred:tensor
        y_true:tensor
            if return_y_true

        """

        predict_loader.reset()
        predict_loader.reset_shuffle(shuffle=False)  # shuffle False
        predict_loader.to_cuda(self.device)

        self.model.eval()

        ############

        handles = []
        if add_hook:
            try:
                self.forward_hook_list = []

                def for_hook(module, input, output):
                    self.forward_hook_list.append(output.detach().cpu())

                handles.append(self.model.conv_to_fc_softplus.register_forward_hook(for_hook))

                le = len(self.model.softpluses)
                for i in range(le):
                    handles.append(self.model.softpluses[i].register_forward_hook(for_hook))  # hook the fcs[i]
            except BaseException as e:
                print(e)
                raise AttributeError("The model must contain sub (model or layer) named ``conv_to_fc_softplus``and "
                                     "nn.ModuleList named ``softpluses``")
        y_preds = []
        y_true = []
        batch_y = []
        for batch_x, *batch_y in predict_loader:
            y_preds.append(self.model(*batch_x).detach().cpu())
            if batch_y:
                y_true.append(batch_y[0].detach().cpu())

        if add_hook:
            [i.remove() for i in handles]  # del

        if return_y_true and batch_y != []:
            return torch.cat(y_preds), torch.cat(y_true)
        else:
            return torch.cat(y_preds)
