from PyQt5 import QtWidgets, uic, QtGui,QtCore
import sys, importlib, random,py_compile
from libabr import System, App, Control, Files, Res, Commands

res = Res();files = Files();app = App();control=Control();cmd = Commands()

class MainApp(QtWidgets.QMainWindow):
    def __init__(self,args):
        super(MainApp, self).__init__()

        # ports
        self.Backend = args[0]
        self.Env = args[1]
        self.Widget = args[2]
        self.AppName = args[3]
        self.External = args[4]

        # resize
        self.Widget.Resize (self,700,500)
        self.Widget.SetWindowTitle(res.get('@string/app_name'))
        self.Widget.SetWindowIcon (QtGui.QIcon(res.get(res.etc(self.AppName,'logo'))))

        self.Widget.SetWindowTitle(res.get('@string/untitled'))

        # text box
        self.teEdit = QtWidgets.QTextEdit()
        self.setCentralWidget(self.teEdit)

        # menubar
        self.menubar = self.menuBar()
        self.file = self.menubar.addMenu(res.get('@string/file'))

        # file menu #
        self.new = self.file.addAction(res.get('@string/new'))
        self.new.triggered.connect (self.new_act)
        self.new.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'text'))))
        self.new_page = self.file.addAction(res.get('@string/new_page'))
        self.new_page.triggered.connect (self.new_page_act)
        self.new_page.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName, 'text'))))
        self.open = self.file.addAction(res.get('@string/open'))
        self.open.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'open'))))
        self.open.triggered.connect (self.open_act)
        self.save = self.file.addAction(res.get('@string/save'))
        self.save.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'save'))))
        self.save.triggered.connect (self.save_)
        self.saveas = self.file.addAction(res.get('@string/save_as'))
        self.saveas.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'save-as'))))
        self.saveas.triggered.connect (self.save_as)
        self.exit = self.file.addAction(res.get('@string/exit'))
        self.exit.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'exit'))))
        self.exit.triggered.connect (self.Widget.Close)

        # code menu
        self.code = self.menubar.addMenu('Code')
        self.run = self.code.addAction('Run')
        self.run.triggered.connect (self.run_)

        self.insert_c = self.code.addMenu('Insert Code')

        # Codes #
        self.lang_c = self.insert_c.addAction(res.get('@string/c'))
        self.lang_c.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c'))))
        self.lang_c.triggered.connect (self.langc)
        self.lang_cpp = self.insert_c.addAction(res.get('@string/c++'))
        self.lang_cpp.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c++'))))
        self.lang_cpp.triggered.connect(self.langcpp)
        self.lang_cs = self.insert_c.addAction(res.get('@string/csharp'))
        self.lang_cs.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'c#'))))
        self.lang_cs.triggered.connect(self.langcs)
        self.lang_java = self.insert_c.addAction(res.get('@string/java'))
        self.lang_java.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'java'))))
        self.lang_java.triggered.connect(self.langjava)
        self.lang_python = self.insert_c.addAction(res.get('@string/python'))
        self.lang_python.triggered.connect(self.langpython)
        self.lang_python.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'py'))))
        self.lang_pythongui = self.insert_c.addAction(res.get('@string/pythongui'))
        self.lang_pythongui.triggered.connect(self.langpythonx)
        self.lang_pythongui.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'py'))))
        self.lang_pythonweb = self.insert_c.addAction('Python WebView')
        self.lang_pythonweb.triggered.connect(self.langpythonweb)
        self.lang_pythonweb.setIcon(QtGui.QIcon(res.get('@icon/web-browser')))
        self.lang_saye = self.insert_c.addAction(res.get('@string/saye'))
        self.lang_saye.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'sa'))))
        self.lang_saye.triggered.connect(self.langsaye)
        self.lang_html = self.insert_c.addAction(res.get('@string/html'))
        self.lang_html.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'html'))))
        self.lang_html.triggered.connect(self.langhtml)
        self.lang_php = self.insert_c.addAction(res.get('@string/php'))
        self.lang_php.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'php'))))
        self.lang_php.triggered.connect(self.langphp)
        self.lang_js = self.insert_c.addAction(res.get('@string/javascript'))
        self.lang_js.setIcon(QtGui.QIcon(res.get(res.etc(self.AppName,'js'))))
        self.lang_js.triggered.connect(self.langjs)

        # set font size
        f = QtGui.QFont()
        f.setFamily('DejaVu Sans Mono')
        f.setPointSize(12)
        self.teEdit.setFont(f)

    def run_(self):
        control = Control()
        if not self.Widget.WindowTitle()==res.get('@string/untitled'):
            self.save_('')
        else:
            self.save_as()

        ## Run it ##
        if self.Widget.WindowTitle().endswith (".c") or self.Widget.WindowTitle().endswith('.cpp') or self.Widget.WindowTitle().endswith('.cxx') or self.Widget.WindowTitle().endswith('.c++'):
            try:
                cmd.cc([self.Widget.WindowTitle()])
            except:
                self.Env.RunApp('text', ['Compile error', 'There is some problem with C/++ Compiler.'])

            self.Env.RunApp('commento',[self.Widget.WindowTitle().replace('.cpp','').replace('.cxx','').replace('.c++','').replace('.c',''),'Barge Console'])
            files.remove(self.Widget.WindowTitle())

        elif self.Widget.WindowTitle().endswith ('.py'):
            # check graphical PyQt5 #
            if files.readall(self.Widget.WindowTitle()).__contains__('from PyQt5') and files.readall(self.Widget.WindowTitle()).__contains__('MainApp'):
                rand = str (random.randint(1000,9999))
                files.create(f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[en]','Debug App',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('name[fa]','برنامه تستی',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('logo','@icon/app',f'/usr/share/applications/debug_{rand}.desk')
                control.write_record('exec',f"debug_{rand}",f'/usr/share/applications/debug_{rand}.desk')
                py_compile.compile(files.input(self.Widget.WindowTitle()),files.input(f'/usr/app/debug_{rand}.pyc'))
                self.Env.RunApp(f'debug_{rand}',[None])
                files.remove(f'/usr/share/applications/debug_{rand}.desk')
                files.remove(f'/usr/app/debug_{rand}.pyc')
            else:
                self.Env.RunApp('commento', [self.Widget.WindowTitle().replace('.py',''),'Barge Console'])
        elif self.Widget.WindowTitle().endswith ('.sa'):
            self.Env.RunApp('commento', [self.Widget.WindowTitle().replace('.sa', ''), 'Barge Console'])
        else:
            if not self.Widget.WindowTitle()==res.get('@string/untitled'):
                self.Env.RunApp('text', ['Cannot support', 'Barge cannot support this syntax or language.'])


    def new_page_act (self):
        self.Env.RunApp ('barge',None)

    def new_act (self):
        self.Widget.SetWindowTitle (res.get('@string/untitled'))
        self.teEdit.clear()

    def gettext (self,filename):
        self.teEdit.setPlainText(files.readall(filename))
        self.Widget.SetWindowTitle(files.output(filename))

        if self.Widget.WindowTitle()=='': self.Widget.SetWindowTitle (res.get('@string/untitled'))

    def saveas_ (self,filename):
        files.write(filename,self.teEdit.toPlainText())
        self.Widget.SetWindowTitle(files.output(filename))

    def save_ (self,filename):
        if not self.Widget.WindowTitle()==res.get('@string/untitled'):
            files.write(files.output(self.Widget.WindowTitle()),self.teEdit.toPlainText())
        else:
            self.Env.RunApp('select', [res.get('@string/saveafile'), 'save', self.saveas_])

    def open_act (self):
        self.Env.RunApp('select',[res.get('@string/chooseafile'),'open',self.gettext])

    def save_as (self):
        self.Env.RunApp('select', [res.get('@string/saveasfile'), 'save-as', self.saveas_])

    def langc (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.c')))

    def langcpp (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.cpp')))

    def langjava (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.java')))

    def langpython (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.py')))

    def langpythonx (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled-gui.py')))

    def langpythonweb (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled-web.py')))

    def langcs (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.cs')))

    def langsaye (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.sa')))

    def langhtml (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.html')))

    def langphp (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.php')))

    def langjs (self):
        self.teEdit.setPlainText(files.readall(res.get('@temp/untitled.js')))