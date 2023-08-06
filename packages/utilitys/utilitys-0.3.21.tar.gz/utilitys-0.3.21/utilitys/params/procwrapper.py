from __future__ import annotations

from functools import singledispatch
from functools import wraps
from typing import List, Sequence, Callable, Union

from pyqtgraph.parametertree import Parameter
from pyqtgraph.parametertree.Parameter import PARAM_TYPES
from pyqtgraph.parametertree.parameterTypes import GroupParameter

from .prjparam import PrjParam
from .. import fns
from ..misc import CompositionMixin
from ..processing import *

__all__ = ['NestedProcWrapper']

def _hookupCondition(parentParam: Parameter, chParam: Parameter):
  condition = chParam.opts.get('condition', None)
  if not condition:
    return
  _locals = {p.name(): p.value() for p in parentParam}
  if isinstance(condition, str):
    def cndtnCallable():
      exec(f'__out__ = bool({condition})', {}, _locals)
      # noinspection PyUnresolvedReferences
      return _locals['__out__']
  else:
    cndtnCallable = condition
  def onChanged(param, val):
    _locals[param.name()] = val
    if cndtnCallable():
      chParam.show()
    else:
      chParam.hide()

  ch = None
  for ch in parentParam: ch.sigValueChanging.connect(onChanged)
  # Triger in case condition is initially false
  if ch:
    onChanged(ch, ch.value())

def _mkProcParam(stage: ProcessStage):
  return {'name': stage.name, 'type': 'procgroup', 'process': stage, 'enabled': not stage.disabled}

def atomicRunWrapper(proc: AtomicProcess, param: Parameter):
  def onChange(p, val):
    proc.input.update(**{param.name(): val})
    proc.result = None
  param.sigValueChanged.connect(onChange)

@singledispatch
def addStageToParam(stage: ProcessStage, parentParam: Parameter, **kwargs):
  pass

@addStageToParam.register
def addAtomicToParam(stage: AtomicProcess, parentParam: Parameter,
                     argNameFormat: Callable[[str], str]=None, nestHyperparams=True, **kwargs):
  docParams = fns.docParser(stage.fnDoc)
  if nestHyperparams:
    parentParam = fns.getParamChild(parentParam, chOpts=_mkProcParam(stage))
  if docParams['top-descr']:
    parentParam.setOpts(tip=docParams['top-descr'])
  for key in stage.input.hyperParamKeys:
    val = stage.input[key]
    curParam = docParams.get(key, None)
    if curParam is None:
      curParam = PrjParam(name=key, value=val)
    else:
      if val is not stage.input.FROM_PREV_IO:
        curParam.value = val
      if curParam.pType is None:
        curParam.pType = type(val).__name__.lower()
    if curParam.opts.get('ignore', False):
      # Disregard this parameter
      continue
    paramDict = curParam.toPgDict()
    if paramDict['type'] not in PARAM_TYPES:
      continue
    if argNameFormat is not None and 'title' not in paramDict:
      paramDict['title'] = argNameFormat(key)
    pgParam = fns.getParamChild(parentParam, chOpts=paramDict)
    atomicRunWrapper(stage, pgParam)
    _hookupCondition(parentParam, pgParam)
  return stage

@addStageToParam.register
def addNestedToParam(stage: NestedProcess, parentParam: Parameter, nestHyperparams=True,
                     argNameFormat: Callable[[str], str]=None, treatAsAtomic=False, **kwargs):
  if nestHyperparams:
    parentParam = fns.getParamChild(parentParam, chOpts=_mkProcParam(stage))
  if treatAsAtomic:
    collapsed = AtomicProcess(stage.run, stage.name)
    collapsed.input = stage.input
    addAtomicToParam(collapsed, parentParam, argNameFormat)
    return
  # Special case of a process comprised of just one atomic function
  # if len(stage.stages) == 1:
  #   # Hide this level of the process tree
  #   addStageToParam(stage.stages[0], parentParam, nestHyperparams=False)
  #   return
  for childStage in stage:
    addStageToParam(childStage, parentParam)

class NestedProcWrapper(CompositionMixin):
  def __init__(self, processor: ProcessStage, parentParam: GroupParameter=None,
               argNameFormat: Callable[[str], str] = None, treatAsAtomic=False, nestHyperparams=True):
    self.processor = self.exposes(processor, 'processor')
    self.algName = processor.name
    self.argNameFormat = argNameFormat
    self.treatAsAtomic = treatAsAtomic
    self.nestHyperparams = nestHyperparams
    # A few special things happen when adding a top-level processor. It has to create a parent if none exists without
    # doubly nesting and return a reference to the created parent param or the normal one if no nesting occurred.
    # The if-branching allows this to occur
    if parentParam is None:
      parentParam = Parameter.create(name=self.algName, type='procgroup', process=processor)
      # Avoid doubly-nested top parameter
      self.nestHyperparams = False
    self.parentParam : GroupParameter = parentParam

    self.addStage(self.processor)
    # Extract nested param if it was created
    if  self.nestHyperparams:
      self.parentParam = parentParam.child(self.algName)

    # Reset once more if no initial parent param
    self.nestHyperparams = nestHyperparams


  def addStage(self, stage: ProcessStage, before: Sequence[str]=()):
    parentParam = fns.getParamChild(self.parentParam, *before, allowCreate=False)
    parentStage: NestedProcess = self.getNestedName(self.processor, *before[:-1])
    # Defensive check to only add extra stages onto existing processor
    if stage is not self.processor:
      if before:
        tmpStage = self.getNestedName(parentStage, before[-1])
        beforeIdx = parentStage.stages.index(tmpStage)
        parentStage.stages = parentStage.stages[:beforeIdx] + [stage] + parentStage.stages[beforeIdx:]
      else:
        parentStage.stages.append(stage)
    addStageToParam(stage, parentParam, argNameFormat=self.argNameFormat,
                    treatAsAtomic=self.treatAsAtomic, nestHyperparams=self.nestHyperparams)

  def removeStage(self, *nestedName: str):
    parent = self.getNestedName(self.processor, *nestedName[:-1])
    stage = self.getNestedName(parent, nestedName[-1])
    parent.stages.remove(stage)
    parentParam = fns.getParamChild(self.parentParam, *nestedName[:-1], allowCreate=False)
    childParam = fns.getParamChild(parentParam, nestedName[-1], allowCreate=False)
    parentParam.removeChild(childParam)

  def clear(self):
    if isinstance(self.processor, AtomicProcess):
      raise AttributeError('Cannot clear a wrapper of an atomic process')
    self.processor: NestedProcess
    for stage in self.processor.stages:
      self.removeStage(stage.name)

  def setStageEnabled(self, stageIdx: Sequence[str], enabled: bool):
    paramForStage = self.parentParam.child(*stageIdx)
    prevEnabled = paramForStage.opts['enabled']
    if prevEnabled != enabled:
      paramForStage.setOpts(enabled=enabled)

  def __repr__(self) -> str:
    selfCls = type(self)
    oldName: str = super().__repr__()
    # Remove module name for brevity
    oldName = oldName.replace(f'{selfCls.__module__}.{selfCls.__name__}',
                              f'{selfCls.__name__} \'{self.algName}\'')
    return oldName

  @classmethod
  def getNestedName(cls, curProc: ProcessStage, *nestedName: str):
    if not nestedName or isinstance(curProc, AtomicProcess):
      return curProc
    # noinspection PyUnresolvedReferences
    for stage in curProc:
      if stage.name == nestedName[0]:
        if len(nestedName) == 1:
          return stage
        else:
          return cls.getNestedName(stage, *nestedName[1:])
    # Requested stage not found if execution reaches here
    raise ValueError(f'Stage {nestedName} not found in {curProc}')