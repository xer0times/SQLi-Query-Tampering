from javax.swing import (JTabbedPane, JScrollPane, JPanel, JLabel, JList, JButton,
                         JTextField, JSeparator, JCheckBox, GroupLayout, LayoutStyle,
                         JOptionPane, JFileChooser, JComboBox, JTextArea)

from java.awt import Color, Font, Toolkit
from java.lang import Short
from java.io import File
from java.awt.datatransfer  import DataFlavor, StringSelection

class PluginUI():
    def __init__(self, extender):
        self.extender = extender
        self.initComponents()
    
    def showMessage(self, msg):
        JOptionPane.showMessageDialog(self.mainPanel, msg)

    def getProcessorTechName(self):
        return self.comboProcessorTech.getSelectedItem()

    def getGeneratorTechsName(self):
        techList = []
        if self.chkGeneral.isSelected(): techList.append('General')
        if self.chkMAXDB.isSelected(): techList.append('SAP_MaxDB')
        if self.chkMSSQL.isSelected(): techList.append('MSSQL')
        if self.chkMSAccess.isSelected(): techList.append('MSAccess')
        if self.chkPostgres.isSelected(): techList.append('PostgreSQL')
        if self.chkOracle.isSelected(): techList.append('Oracle')
        if self.chkSqlite.isSelected(): techList.append('SQLite')
        if self.chkMysql.isSelected(): techList.append('MySQL')
        return techList

    def pastePayloadButtonAction(self, event):
        clpbrd = Toolkit.getDefaultToolkit().getSystemClipboard()
        content = clpbrd.getContents(None)
        if content and content.isDataFlavorSupported(DataFlavor.stringFlavor):
            items = content.getTransferData(DataFlavor.stringFlavor)
            items = items.splitlines()
            for item in items:
                self.extender.PayloadList.append(item)
            self.listPayloads.setListData(self.extender.PayloadList)
        self.writePayloadsListFile()

    def loadPayloadButtonAction(self, event):
        fileChooser = JFileChooser()       
        fileChooser.dialogTitle = 'Choose Payload List'
        fileChooser.fileSelectionMode = JFileChooser.FILES_ONLY
        if (fileChooser.showOpenDialog(self.mainPanel) == JFileChooser.APPROVE_OPTION):
            file = fileChooser.getSelectedFile()
            with open(file.getAbsolutePath(),'r') as reader:
                    for line in reader.readlines():
                        self.extender.PayloadList.append(line.strip('\n'))
            self.listPayloads.setListData(self.extender.PayloadList)
            self.showMessage('{} payloads loaded'.format(len(self.extender.PayloadList)))
            self.writePayloadsListFile()

    def removePayloadButtonAction(self, event):
        for item in self.listPayloads.getSelectedValuesList():
            self.extender.PayloadList.remove(item)
        self.listPayloads.setListData(self.extender.PayloadList)
        self.writePayloadsListFile()

    def clearPayloadButtonAction(self, event):
        self.extender.PayloadList[:] = []
        self.listPayloads.setListData(self.extender.PayloadList)
        self.writePayloadsListFile()

    def addPayloadButtonAction(self, event):
        if str(self.textNewPayload.text).strip():
            self.extender.PayloadList.append(self.textNewPayload.text)
            self.textNewPayload.text = ''
            self.listPayloads.setListData(self.extender.PayloadList)
        self.writePayloadsListFile()

    def toClipboardButtonAction(self, event):
        self.extender.generatePayloads()
        result = '\n'.join(self.extender.tamperedPayloads)
        result = StringSelection(result)
        clpbrd = Toolkit.getDefaultToolkit().getSystemClipboard()
        clpbrd.setContents (result, None)
        self.showMessage('{} url encoded payload copied to clipboard'.format(len(self.extender.tamperedPayloads)))

    def toFileButtonAction(self, event):
        fileChooser = JFileChooser()       
        fileChooser.dialogTitle = 'Save Payloads'
        fileChooser.fileSelectionMode = JFileChooser.FILES_ONLY
        if (fileChooser.showSaveDialog(self.mainPanel) == JFileChooser.APPROVE_OPTION):
            file = fileChooser.getSelectedFile()
            self.extender.generatePayloads()
            result = '\n'
            result = result.join(self.extender.tamperedPayloads)
            with open(file.getAbsolutePath(),'w') as writer:
                writer.writelines(result)
            self.showMessage('{} url encoded payload written to file'.format(len(self.extender.tamperedPayloads)))

    def tamperPayloadButtonAction(self, event):
        tamperedPayloads = []
        tamperFunction = self.comboProcessorTech.getSelectedItem()
        payloads = self.textPlainPayload.text
        payloads = payloads.splitlines()
        for payload in payloads:
            tamperedPayloads.append(self.extender.tamperSinglePayload(tamperFunction, payload))

        result = '\n'.join(tamperedPayloads)
        self.textTamperedPayload.text = result

    def comboProcessorTechAction(self, event):
        varName = 'SQLiQueryTampering_comboProcessorTech'
        state = str(self.comboProcessorTech.getSelectedIndex())
        self.extender.callbacks.saveExtensionSetting(varName, state)

    def OnCheck(self, event):
        chk = event.getSource()
        varName = 'SQLiQueryTampering_{}'.format(chk.text)
        state =str(1 if chk.isSelected() else 0)
        self.extender.callbacks.saveExtensionSetting(varName, state)

    def writePayloadsListFile(self):
        payloads = '\n'.join(self.extender.PayloadList)
        payloads = payloads.encode('utf-8')
        with open('payloads.lst','w') as writer:
                writer.write(payloads)

    def readPayloadsListFile(self):
        result = []
        with open('payloads.lst','r') as reader:
                for line in reader.readlines():
                    result.append(line.strip('\n'))
        return result

    def initComponents(self):
        TabbedPane1 = JTabbedPane()
        GeneratorScrollPane = JScrollPane()
        GeneratorPanel = JPanel()
        jlbl1 = JLabel()
        jlbl2 = JLabel()
        spanePayloadList = JScrollPane()
        self.listPayloads = JList()
        pastePayloadButton = JButton(actionPerformed=self.pastePayloadButtonAction)
        loadPayloadButton = JButton(actionPerformed=self.loadPayloadButtonAction)
        removePayloadButton = JButton(actionPerformed=self.removePayloadButtonAction)
        clearPayloadButton = JButton(actionPerformed=self.clearPayloadButtonAction)
        self.textNewPayload = JTextField()
        addPayloadButton = JButton(actionPerformed=self.addPayloadButtonAction)
        jSeparator1 = JSeparator()
        jlbl3 = JLabel()
        jlbl4 = JLabel()
        self.chkGeneral = JCheckBox(actionPerformed = self.OnCheck)
        self.chkMAXDB = JCheckBox(actionPerformed = self.OnCheck)
        self.chkMSSQL = JCheckBox(actionPerformed = self.OnCheck)
        self.chkMSAccess = JCheckBox(actionPerformed = self.OnCheck)
        self.chkPostgres = JCheckBox(actionPerformed = self.OnCheck)
        self.chkOracle = JCheckBox(actionPerformed = self.OnCheck)
        self.chkSqlite = JCheckBox(actionPerformed = self.OnCheck)
        self.chkMysql = JCheckBox(actionPerformed = self.OnCheck)
        jlbl5 = JLabel()
        toClipboardButton = JButton(actionPerformed=self.toClipboardButtonAction)
        toFileButton = JButton(actionPerformed=self.toFileButtonAction)
        ProcessorScrollPane = JScrollPane()
        ProcessorPanel = JPanel()
        jLabel1 = JLabel()
        self.comboProcessorTech = JComboBox(itemStateChanged=self.comboProcessorTechAction)
        jSeparator2 = JSeparator()
        jLabel2 = JLabel()
        jLabel3 = JLabel()
        jScrollPane1 = JScrollPane()
        self.textPlainPayload = JTextArea()
        jLabel4 = JLabel()
        jScrollPane2 = JScrollPane()
        self.textTamperedPayload = JTextArea()
        tamperPayloadButton = JButton(actionPerformed=self.tamperPayloadButtonAction)

        jlbl1.setForeground(Color(255, 102, 51))
        jlbl1.setFont(Font(jlbl1.getFont().toString(), 1, 14))
        jlbl1.setText("User-Defiend Payloads")

        jlbl2.setText("This payload type lets you configure a simple list of strings that are used as payloads.")

        spanePayloadList.setViewportView(self.listPayloads)
        self.extender.PayloadList = self.readPayloadsListFile() 
        self.listPayloads.setListData(self.extender.PayloadList)

        pastePayloadButton.setText("Paste")

        loadPayloadButton.setText("Load")

        removePayloadButton.setText("Remove")

        clearPayloadButton.setText("Clear")

        self.textNewPayload.setToolTipText("")

        addPayloadButton.setText("Add")

        jlbl3.setForeground(Color(255, 102, 51))
        jlbl3.setFont(Font(jlbl3.getFont().toString(), 1, 14))
        jlbl3.setText("Tamper Techniques")

        jlbl4.setText("You can select the techniques that you want to perform processing tasks on each user-defined payload")

        self.chkGeneral.setText("General")
        varName = 'SQLiQueryTampering_{}'.format(self.chkGeneral.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkGeneral.setSelected(int(state))

        self.chkMAXDB.setText("SAP MAX DB")
        varName = 'SQLiQueryTampering_{}'.format(self.chkMAXDB.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkMAXDB.setSelected(int(state))

        self.chkMSSQL.setText("MS SQL Server")
        varName = 'SQLiQueryTampering_{}'.format(self.chkMSSQL.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkMSSQL.setSelected(int(state))

        self.chkMSAccess.setText("MS Access")
        varName = 'SQLiQueryTampering_{}'.format(self.chkMSAccess.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkMSAccess.setSelected(int(state))

        self.chkPostgres.setText("Postgres SQL")
        varName = 'SQLiQueryTampering_{}'.format(self.chkPostgres.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkPostgres.setSelected(int(state))

        self.chkOracle.setText("Oracle")
        varName = 'SQLiQueryTampering_{}'.format(self.chkOracle.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkOracle.setSelected(int(state))

        self.chkSqlite.setText("Sqlite")
        varName = 'SQLiQueryTampering_{}'.format(self.chkSqlite.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkSqlite.setSelected(int(state))

        self.chkMysql.setText("MySql")
        varName = 'SQLiQueryTampering_{}'.format(self.chkMysql.text)
        state = self.extender.callbacks.loadExtensionSetting(varName)
        if state : self.chkMysql.setSelected(int(state))

        jlbl5.setText("[?] Save the Generated/Tampered Payloads to :")

        toClipboardButton.setText("Clipboard")

        toFileButton.setText("File")

        GeneratorPanelLayout = GroupLayout(GeneratorPanel)
        GeneratorPanel.setLayout(GeneratorPanelLayout)
        GeneratorPanelLayout.setHorizontalGroup(
            GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GeneratorPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.TRAILING)
                    .addComponent(jlbl2, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jlbl4, GroupLayout.Alignment.LEADING, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                    .addComponent(jSeparator1, GroupLayout.Alignment.LEADING)
                    .addGroup(GeneratorPanelLayout.createSequentialGroup()
                        .addGap(6, 6, 6)
                        .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addGroup(GeneratorPanelLayout.createSequentialGroup()
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING, False)
                                    .addComponent(removePayloadButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(clearPayloadButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(loadPayloadButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(pastePayloadButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                                    .addComponent(addPayloadButton, GroupLayout.DEFAULT_SIZE, GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
                                .addGap(21, 21, 21)
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(self.textNewPayload)
                                    .addComponent(spanePayloadList)))
                            .addComponent(jlbl1)
                            .addComponent(jlbl3)
                            .addGroup(GeneratorPanelLayout.createSequentialGroup()
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(self.chkGeneral)
                                    .addComponent(self.chkMSSQL))
                                .addGap(18, 18, 18)
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(self.chkPostgres)
                                    .addComponent(self.chkMAXDB))
                                .addGap(18, 18, 18)
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(self.chkMSAccess)
                                    .addComponent(self.chkOracle))
                                .addGap(18, 18, 18)
                                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                                    .addComponent(self.chkSqlite)
                                    .addComponent(self.chkMysql)))
                            .addGroup(GeneratorPanelLayout.createSequentialGroup()
                                .addComponent(jlbl5)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(toClipboardButton)
                                .addGap(18, 18, 18)
                                .addComponent(toFileButton, GroupLayout.PREFERRED_SIZE, 97, GroupLayout.PREFERRED_SIZE)))))
                .addContainerGap())
        )
        GeneratorPanelLayout.setVerticalGroup(
            GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GeneratorPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addComponent(jlbl1)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jlbl2, GroupLayout.PREFERRED_SIZE, 21, GroupLayout.PREFERRED_SIZE)
                .addGap(18, 18, 18)
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(spanePayloadList, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addGroup(GeneratorPanelLayout.createSequentialGroup()
                        .addComponent(pastePayloadButton)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(loadPayloadButton)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(removePayloadButton)
                        .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                        .addComponent(clearPayloadButton)))
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(self.textNewPayload, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                    .addComponent(addPayloadButton))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jSeparator1, GroupLayout.PREFERRED_SIZE, 10, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.RELATED)
                .addComponent(jlbl3)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jlbl4)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(self.chkGeneral)
                    .addComponent(self.chkMAXDB)
                    .addComponent(self.chkOracle)
                    .addComponent(self.chkSqlite))
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(self.chkMSSQL)
                    .addComponent(self.chkPostgres)
                    .addComponent(self.chkMSAccess)
                    .addComponent(self.chkMysql))
                .addGap(18, 18, 18)
                .addGroup(GeneratorPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jlbl5)
                    .addComponent(toClipboardButton)
                    .addComponent(toFileButton))
                .addGap(20, 20, 20))
        )

        GeneratorScrollPane.setViewportView(GeneratorPanel)

        TabbedPane1.addTab("Generator", GeneratorScrollPane)

        varName = 'SQLiQueryTampering_comboProcessorTech'
        state = self.extender.callbacks.loadExtensionSetting(varName)
        
        for item in self.extender.getTamperFuncsName():
            self.comboProcessorTech.addItem(item)
        
        if state : self.comboProcessorTech.setSelectedIndex(int(state))

        jLabel1.setText("Processor Technique :")

        jLabel2.setText("Modify Plain Payloads based on the selected Processor Technique. Write one payload per line.")

        jLabel3.setText("Plain Payloads:")

        self.textPlainPayload.setColumns(20)
        self.textPlainPayload.setRows(5)
        jScrollPane1.setViewportView(self.textPlainPayload)

        jLabel4.setText("Tampered Payloads:")

        self.textTamperedPayload.setColumns(20)
        self.textTamperedPayload.setRows(5)
        jScrollPane2.setViewportView(self.textTamperedPayload)

        tamperPayloadButton.setText("Tamper Payloads")

        ProcessorPanelLayout = GroupLayout(ProcessorPanel)
        ProcessorPanel.setLayout(ProcessorPanelLayout)
        ProcessorPanelLayout.setHorizontalGroup(
            ProcessorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(GroupLayout.Alignment.TRAILING, ProcessorPanelLayout.createSequentialGroup()
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE)
                .addComponent(tamperPayloadButton)
                .addContainerGap(GroupLayout.DEFAULT_SIZE, Short.MAX_VALUE))
            .addGroup(ProcessorPanelLayout.createSequentialGroup()
                .addContainerGap()
                .addGroup(ProcessorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                    .addComponent(jSeparator2)
                    .addComponent(jScrollPane1)
                    .addComponent(jScrollPane2)
                    .addGroup(ProcessorPanelLayout.createSequentialGroup()
                        .addGroup(ProcessorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
                            .addComponent(jLabel3)
                            .addComponent(jLabel4)
                            .addGroup(ProcessorPanelLayout.createSequentialGroup()
                                .addComponent(jLabel1)
                                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                                .addComponent(self.comboProcessorTech, GroupLayout.PREFERRED_SIZE, 286, GroupLayout.PREFERRED_SIZE))
                            .addComponent(jLabel2))
                        .addGap(0, 78, Short.MAX_VALUE)))
                .addContainerGap())
        )
        ProcessorPanelLayout.setVerticalGroup(
            ProcessorPanelLayout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addGroup(ProcessorPanelLayout.createSequentialGroup()
                .addGap(33, 33, 33)
                .addGroup(ProcessorPanelLayout.createParallelGroup(GroupLayout.Alignment.BASELINE)
                    .addComponent(jLabel1)
                    .addComponent(self.comboProcessorTech, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE))
                .addGap(18, 18, 18)
                .addComponent(jSeparator2, GroupLayout.PREFERRED_SIZE, 10, GroupLayout.PREFERRED_SIZE)
                .addGap(12, 12, 12)
                .addComponent(jLabel2)
                .addGap(18, 18, 18)
                .addComponent(jLabel3)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane1, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jLabel4)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(jScrollPane2, GroupLayout.PREFERRED_SIZE, GroupLayout.DEFAULT_SIZE, GroupLayout.PREFERRED_SIZE)
                .addPreferredGap(LayoutStyle.ComponentPlacement.UNRELATED)
                .addComponent(tamperPayloadButton)
                .addGap(36, 36, 36))
        )

        ProcessorScrollPane.setViewportView(ProcessorPanel)

        TabbedPane1.addTab("Processor", ProcessorScrollPane)

        self.mainPanel = JPanel()
        layout = GroupLayout(self.mainPanel)
        self.mainPanel.setLayout(layout)
        layout.setHorizontalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(TabbedPane1, GroupLayout.DEFAULT_SIZE, 701, Short.MAX_VALUE)
        )
        layout.setVerticalGroup(
            layout.createParallelGroup(GroupLayout.Alignment.LEADING)
            .addComponent(TabbedPane1)
        )

        TabbedPane1.getAccessibleContext().setAccessibleName("Generator")
    # </editor-fold>   