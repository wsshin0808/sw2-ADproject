from sys import *
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import *

import sys
import time
from word import Word

sys._excepthook = sys.excepthook

def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook

#60초 카운트다운, 카운트다운 종료시 time over!값 발산
class External2(QThread):
    countChanged = pyqtSignal(str)

    def run(self):
        count = 60
        while count > 0:
            count -= 1
            time.sleep(1)
            self.countChanged.emit(str(count))
            if count == 0:
                self.countChanged.emit('Time Over!')

#3초간 카운트다운(스타트버튼 눌린후의 준비시간)
class External1(QThread):
    countChanged = pyqtSignal(str)

    def run(self):
        count = 4
        while count > 0:
            count -= 1
            time.sleep(1)
            self.countChanged.emit(str(count) + "'s later Start!")
            if count == 0:
                self.countChanged.emit('Now Started!')


class TypePractice(QDialog, QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.correct = 0
        self.wrong = 0
        self.totalletters = 0
        self.correctletters = 0
        self.correctrate = 0
        self.totalinput = 0
        self.curlen = 0
        self.initUI()
        self.word = Word('words.txt')

    #UI 초기화
    def initUI(self):
        self.typepracticeLayout = QGridLayout()

        self.nextWordlabel = QLabel('Next Word')
        self.nextWord = QLineEdit()
        self.nextWord.setReadOnly(True)
        self.nextWord.setAlignment(Qt.AlignCenter)
        self.nextWord.setText('')
        self.nextWord.setCursorPosition(0)
        self.typepracticeLayout.addWidget(self.nextWordlabel, 0, 0)
        self.typepracticeLayout.addWidget(self.nextWord, 1, 0, 1, 25)

        label1 = QLabel('')
        label2 = QLabel('')
        self.typepracticeLayout.addWidget(label1, 2, 0)
        self.typepracticeLayout.addWidget(label2, 3, 0)

        self.currentWordlabel = QLabel('Current Word')
        self.currentWord = QLineEdit('')
        self.currentWord.setReadOnly(True)
        self.currentWord.setAlignment(Qt.AlignLeft)
        self.currentWord.setCursorPosition(0)
        font = self.currentWord.font()
        font.setPointSize(font.pointSize() + 8)
        self.currentWord.setFont(font)
        self.typepracticeLayout.addWidget(self.currentWordlabel, 4, 0)
        self.typepracticeLayout.addWidget(self.currentWord, 5, 0, 5, 30)

        self.wordInput = QLineEdit()
        self.wordInput.setMaxLength(0)
        font = self.wordInput.font()
        font.setPointSize(font.pointSize() + 8)
        self.wordInput.setFont(font)
        self.typepracticeLayout.addWidget(self.wordInput, 11, 0, 11, 30)
        self.typepracticeLabel = QLabel('You Input')
        self.typepracticeLayout.addWidget(self.typepracticeLabel,10,0)

        self.statusLayout = QGridLayout()

        self.remainingTime = QLineEdit()
        self.remainingTime.setReadOnly(True)
        self.remainingTime.setAlignment(Qt.AlignCenter)
        font = self.remainingTime.font()
        font.setPointSize(font.pointSize() + 20)
        self.remainingTime.setFont(font)
        self.remainingTime.setText('60')
        self.remainingTimeLabel = QLabel('Left Time : ')
        self.statusLayout.addWidget(self.remainingTimeLabel, 0, 0)
        self.statusLayout.addWidget(self.remainingTime, 0, 1)

        self.correctLabel = QLabel('Correct : ')
        self.correctLb = QLabel(str(self.correct))
        self.wrongLabel = QLabel('Wrong : ')
        self.wrongLb = QLabel(str(self.wrong))
        self.correctrateLabel = QLabel('Correct Rate : ')
        self.correctrateLb = QLabel('')
        self.statusLayout.addWidget(self.correctLabel, 3, 0)
        self.statusLayout.addWidget(self.correctLb, 3, 1)
        self.statusLayout.addWidget(self.wrongLabel, 4, 0)
        self.statusLayout.addWidget(self.wrongLb, 4, 1)
        self.statusLayout.addWidget(self.correctrateLabel, 5, 0)
        self.statusLayout.addWidget(self.correctrateLb, 5, 1)

        self.tpstartLayout = QGridLayout()
        self.msg = QLineEdit('')
        self.msg.setReadOnly(True)
        self.startButton = QToolButton()
        self.startButton.setText('START!')
        self.startButton.clicked.connect(self.startClicked)
        self.tpstartLayout.addWidget(self.msg, 0, 0, 0, 10)
        self.tpstartLayout.addWidget(self.startButton, 1, 2)

        centerLayout1 = QGridLayout()
        for i in range(10):
            centerLayout1.addWidget(QLabel(' || '), i, 0)

        centerLayout2 = QGridLayout()
        for i in range(10):
            centerLayout2.addWidget(QLabel(' || '), i, 0)

        self.setWindowTitle('Type Practice')

        mainLayout = QGridLayout()
        mainLayout.addLayout(self.typepracticeLayout, 0, 0)
        mainLayout.addLayout(centerLayout1, 0, 1)
        mainLayout.addLayout(self.statusLayout, 0, 2)
        mainLayout.addLayout(centerLayout2, 0, 3)
        mainLayout.addLayout(self.tpstartLayout, 0, 4)

        self.setLayout(mainLayout)

    #start 버튼이 클릭되었을때의 콜백 함수
    def startClicked(self):
        self.totalletters = 0
        self.totalinput = 0
        self.correctletters = 0
        self.correct = 0
        self.wrong = 0
        self.correctrate = 0
        self.correctLb.setText(str(self.correct))
        self.wrongLb.setText(str(self.wrong))
        self.correctrateLb.setText(str(self.correctrate))
        self.remainingTime.setText('60')
        self.currentWord.setText(self.word.randFromDB())
        self.nextWord.setText(self.word.randFromDB())
        self.timer = External1()
        self.timer.countChanged.connect(self.msgChange)
        self.timer.start()

    #3초 타이머의 값이 바뀔때마다 호출되는 콜백 함수
    def msgChange(self, value):
        self.msg.setText(value)
        if self.msg.text() == 'Now Started!':
            self.inTimeLimit()

    #3초 타이머의 값이 0이 되었을때 호출되는 함수, 60초 타이머 시작
    def inTimeLimit(self):
        self.timer2 = External2()
        self.timer2.countChanged.connect(self.remainingtimeChange)
        self.timer2.start()
        self.changemaxLen()
        self.remainingTime.textChanged.connect(self.timeCheck)
        self.currentWord.textChanged.connect(self.changemaxLen)
        self.wordInput.returnPressed.connect(self.comparing2)
        self.wordInput.textChanged.connect(self.instantcompare)

    #입력 하는 단어의 최대 글자수를 currentword의 길이에 맞춰줌
    def changemaxLen(self):
        self.wordInput.setMaxLength(len(self.currentWord.text()))

    def timeCheck(self):
        if self.remainingTime.text() == 'Time Over!':
            self.wordInput.setText('')
            self.msg.setText('')
            self.wordInput.setMaxLength(0)
            self.currentWord.setStyleSheet('color: black;')

    def remainingtimeChange(self, value):
        self.remainingTime.setText(str(value))
        if value == 'Time Over!':
            QMessageBox.about(self,'result',"Correct : {}\nWrong : {}\nAccuracy : {}\nTyping Speed : {}".format
            (self.correct, self.wrong, self.correctrate, self.totalinput))



    def instantcompare(self):
        wi = self.wordInput.text()
        cw = self.currentWord.text()
        if len(wi) == 0:
            self.currentWord.setStyleSheet('color: black;')
        else:
            for i in range(len(wi)):
                if wi[i] == cw[i]:
                    self.currentWord.setStyleSheet('color: blue;')
                elif wi[i] != cw[i]:
                    self.currentWord.setStyleSheet('color: red;')
                    break

        if self.curlen < len(self.wordInput.text()) :
            self.totalinput += 1
            self.curlen = len(self.wordInput.text())
        else:
            self.curlen = len(self.wordInput.text())

    def comparing2(self):
        if self.currentWord.text() == self.wordInput.text() :
            self.totalletters += len(self.currentWord.text())
            self.correctletters += len(self.currentWord.text())
            self.correctrate = self.correctletters * 100 / self.totalletters
            self.correctrate = round(self.correctrate, 2)
            self.currentWord.setText(self.nextWord.text())
            self.currentWord.setStyleSheet('color: black;')
            self.nextWord.setText(self.word.randFromDB())
            self.wordInput.clear()
            self.correct += 1
            self.correctLb.setText(str(self.correct))
            self.correctrateLb.setText(str(self.correctrate))
            self.curlen = 0

        elif self.remainingTime.text() == 'Time Over!':
            self.wordInput.setMaxLength(0)

        else:
            wi = self.wordInput.text()
            cw = self.currentWord.text()
            c = 0
            for i in range(len(wi)):
                if wi[i] == cw[i]:
                    c += 1
            self.correctletters += c
            self.totalletters += len(self.currentWord.text())
            self.currentWord.setText(self.nextWord.text())
            self.currentWord.setStyleSheet('color: black;')
            self.nextWord.setText(self.word.randFromDB())
            self.wordInput.clear()
            self.wrong += 1
            self.wrongLb.setText(str(self.wrong))
            self.correctrate = self.correctletters * 100 / self.totalletters
            self.correctrate = round(self.correctrate, 2)
            self.correctrateLb.setText(str(self.correctrate))
            self.curlen = 0


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    tp = TypePractice()
    tp.show()
    try:
        sys.exit(app.exec_())
    except:
        print('Exiting')

