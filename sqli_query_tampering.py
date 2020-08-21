
from burp import (IBurpExtender, IIntruderPayloadGeneratorFactory, ITab,
                  IIntruderPayloadGenerator, IIntruderPayloadProcessor)
from tamper import SQLiTamper
from UI import PluginUI

try:
    from exceptions_fix import FixBurpExceptions
    import sys
except ImportError:
    pass

class BurpExtender(IBurpExtender, IIntruderPayloadGeneratorFactory, IIntruderPayloadProcessor, ITab):
  def __init__(self):
    self.tamperedPayloads = []
    self.PayloadList = []
    self.tamper = SQLiTamper()

  def registerExtenderCallbacks(self, callbacks):
    self.callbacks = callbacks
    self.helper = callbacks.getHelpers()
    sys.stdout = callbacks.getStdout()
    
    callbacks.setExtensionName('SQLi Query Tampering')
    callbacks.registerIntruderPayloadGeneratorFactory(self)
    callbacks.registerIntruderPayloadProcessor(self)

    callbacks.addSuiteTab(self)
    print('SQLi Query Tampering v 1.3\nCreated by Xer0Days')
    print('Based on Sqlmap\'s Tampering Functions\n')
    print('---------------------------------------------')
    print('Github:\t\thttps://github.com/xer0days\nTwitter:\thttps://twitter.com/Xer0Days')
    print('---------------------------------------------\n')

  def getGeneratorName(self):
    return 'SQLi Query Tampering'

  def getProcessorName(self):
    return 'SQLi Query Tampering'

  def createNewInstance(self, attack):
    return IntruderPayloadGenerator(self)

  def getTabCaption(self):
      return 'SQLi Tampering'

  def getUiComponent(self):
      self.ui = PluginUI(self)
      return self.ui.mainPanel

  def processPayload(self, currentPayload, originalPayload, baseValue):
    tamperFuncName = self.ui.getProcessorTechName()
    currPayload = self.helper.bytesToString(currentPayload)
    result = getattr(self.tamper, tamperFuncName)(currPayload)
    return self.helper.stringToBytes(result)

  def getTamperFuncsName(self):
    result = []
    for func in self.tamper.techniques['All']:
      result.append(func.__name__)
    return sorted(result)

  def tamperSinglePayload(self, tamperFuncName=None, payload=''):
    if tamperFuncName is None: return
    result = getattr(self.tamper, tamperFuncName)(payload)
    return result

  def generatePayloads(self):
    self.tamperedPayloads[:] = []
    self.tamperedPayloads = self.tamperedPayloads + self.PayloadList

    techs = self.ui.getGeneratorTechsName()
    if not len(techs): return

    for tech in techs:
      for func in self.tamper.techniques[tech]:
        for payload in self.PayloadList:
          tampered = func(payload)
          self.tamperedPayloads.append(tampered)
    # Remove duplicate payloads
    self.tamperedPayloads = list(dict.fromkeys(self.tamperedPayloads))

class IntruderPayloadGenerator(IIntruderPayloadGenerator):
  def __init__(self, extender):
    self.extender = extender
    self.payloadIndex = 0
    self.extender.generatePayloads()
  
  def hasMorePayloads(self):
    return self.payloadIndex < len(self.extender.tamperedPayloads)

  def getNextPayload(self, baseValue):
    payload = self.extender.helper.stringToBytes(self.extender.tamperedPayloads[self.payloadIndex])
    self.payloadIndex += 1
    return payload

  def reset(self):
    self.payloadIndex = 0

try:
    FixBurpExceptions()
except NameError:
    pass
