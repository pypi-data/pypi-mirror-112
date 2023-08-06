import logging
import torch.nn as nn

from .dice import DiceLoss
from .dice_spline import DiceSplineLoss
from .focal import FocalLoss
from .jaccard import JaccardLoss
from .binary_jaccard import BCEJaccardLoss
from .spline import SplineLoss
from .tversky import TverskyLoss
from .mse import MSELoss
from .mae import MAELoss
from .nll import NLL_Loss

__all__ = ['DiceLoss', 'DiceSplineLoss', 'FocalLoss',
           'JaccardLoss', 'SplineLoss', 'TverskyLoss',
           'BCEJaccardLoss', 'MSELoss', 'MAELoss', 'NLL_Loss']

loss_map_args = {
    'dice': DiceLoss,
    'focal': FocalLoss,
    'jaccard': JaccardLoss,
    'tversky': TverskyLoss,
    'spline': SplineLoss,
    'dice_spline': DiceSplineLoss,
    'binary_jaccard': BCEJaccardLoss,
    'mse': MSELoss,
    'mae': MAELoss,
    'nll': NLL_Loss
}

loss_map_noargs = {
    'ce': nn.CrossEntropyLoss,
    'mlsml': nn.MultiLabelSoftMarginLoss,
    'mlbce': nn.BCEWithLogitsLoss
}


def get_loss(loss_str, loss_args=None):
    """Get loss function based on passed args.

    Parameters
    ----------
    loss_str : str
        string representing loss.
    loss_args : dict
        dictionary of loss parameters

    Returns
    -------
    phobos.loss
        Selected loss class object.

    """
    logging.debug("Enter get_loss routine")
    if loss_str in loss_map_args:
        loss = loss_map_args[loss_str]
        return loss(**loss_args)

    if loss_str in loss_map_noargs:
        loss = loss_map_noargs[loss_str]
        return loss()

def set_loss(loss_str, loss, noargs=False):
    """Allows: 

    1.Addition of a new loss to loss map
    2.Modification of existing loss definitions in loss map

    Parameters
    ----------
    loss_str : string
        string representing loss
    loss : phobos.loss
        loss class
    noargs : boolean
        flag representing whether loss object accepts any arguments
    """
    logging.debug("Enter set_loss routine")
    if noargs:
        loss_map_noargs[loss_str] = loss
    else:
        loss_map_args[loss_str] = loss
    logging.debug("Exit set_loss routine")